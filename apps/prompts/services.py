import logging
import time
from pathlib import Path
from typing import Generator
from django.conf import settings
import anthropic
from apps.accounts.models import User
from apps.accounts.services import AccountService

logger = logging.getLogger("apps.prompts")

SYSTEM_PROMPT_PATH = Path(__file__).parent / "llm_prompts" / "system_v1.md"


def _load_system_prompt() -> str:
    return SYSTEM_PROMPT_PATH.read_text(encoding="utf-8")


class QuotaExceededError(Exception):
    pass


class LLMError(Exception):
    pass


class QuotaService:
    @staticmethod
    def check_and_reserve(user: User) -> None:
        if not AccountService.has_quota(user):
            raise QuotaExceededError(
                f"Limite mensal de {user.monthly_quota} gerações atingido."
            )


class PromptGenerationService:
    """Orquestra a geração de Super Prompts via Claude API com streaming."""

    def __init__(self):
        self._client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        self._system_prompt = _load_system_prompt()

    def _build_user_message(self, idea: str, stack: str, complexity: str, focus: list) -> str:
        focus_str = ", ".join(focus) if focus else "Nenhum foco adicional"
        return (
            f"## Ideia do Aplicativo\n\n{idea}\n\n"
            f"## Configurações\n\n"
            f"- Stack alvo: {stack}\n"
            f"- Complexidade: {complexity}\n"
            f"- Focos adicionais: {focus_str}\n\n"
            "Gere o Super Prompt completo com as 12 seções."
        )

    def generate_stream(
        self,
        user: User,
        idea: str,
        stack: str = "Django",
        complexity: str = "complete",
        focus: list = None,
    ) -> Generator[str, None, None]:
        """Gera o prompt via streaming. Yields chunks de texto."""
        QuotaService.check_and_reserve(user)

        from apps.prompts.models import Prompt
        draft = Prompt.objects.create(
            user=user,
            idea_input=idea,
            stack_target=stack,
            complexity_level=complexity,
            focus_tags=focus or [],
            status=Prompt.Status.DRAFT,
        )

        user_message = self._build_user_message(idea, stack, complexity, focus or [])
        full_content = []
        total_tokens = 0
        model = settings.ANTHROPIC_MODEL_PRIMARY

        for attempt in range(settings.ANTHROPIC_MAX_RETRIES):
            try:
                with self._client.messages.stream(
                    model=model,
                    max_tokens=8000,
                    system=[
                        {
                            "type": "text",
                            "text": self._system_prompt,
                            "cache_control": {"type": "ephemeral"},
                        }
                    ],
                    messages=[{"role": "user", "content": user_message}],
                ) as stream:
                    for chunk in stream.text_stream:
                        full_content.append(chunk)
                        yield chunk

                    final_msg = stream.get_final_message()
                    total_tokens = (
                        final_msg.usage.input_tokens + final_msg.usage.output_tokens
                    )
                break

            except anthropic.APIStatusError as exc:
                logger.warning("Claude API error (attempt %d): %s", attempt + 1, exc)
                if attempt == settings.ANTHROPIC_MAX_RETRIES - 1:
                    if model == settings.ANTHROPIC_MODEL_PRIMARY:
                        model = settings.ANTHROPIC_MODEL_FALLBACK
                        logger.info("Falling back to %s", model)
                    else:
                        draft.delete()
                        raise LLMError("Falha na geração após múltiplas tentativas.") from exc
                time.sleep(2 ** attempt)

        generated = "".join(full_content)
        title = generated.split("\n")[0].lstrip("#= ").strip()[:100] or idea[:100]

        draft.generated_content = generated
        draft.title = title
        draft.status = Prompt.Status.SAVED
        draft.token_count = total_tokens
        draft.save(update_fields=["generated_content", "title", "status", "token_count", "updated_at"])

        AccountService.increment_usage(user, tokens=total_tokens)


class RefinementService:
    """Gerencia sessões de refinamento iterativo de prompts."""

    def __init__(self):
        self._client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)

    def refine_stream(self, session, user_message: str) -> Generator[str, None, None]:
        messages = list(session.messages)
        messages.append({"role": "user", "content": user_message})

        with self._client.messages.stream(
            model=settings.ANTHROPIC_MODEL_PRIMARY,
            max_tokens=4000,
            system=(
                "Você é o CHRONUS. O usuário quer refinar o Super Prompt gerado. "
                "Aplique as alterações solicitadas mantendo a estrutura de 12 seções."
            ),
            messages=messages,
        ) as stream:
            full_response = []
            for chunk in stream.text_stream:
                full_response.append(chunk)
                yield chunk

            messages.append({"role": "assistant", "content": "".join(full_response)})
            session.messages = messages
            session.save(update_fields=["messages"])


class ExportService:
    """Gera artefatos de exportação a partir de um Prompt."""

    @staticmethod
    def to_markdown(prompt) -> str:
        return prompt.generated_content

    @staticmethod
    def to_txt(prompt) -> str:
        import re
        return re.sub(r"[#*`>~_\-=\[\]()]", "", prompt.generated_content)

    @staticmethod
    def to_pdf(prompt) -> bytes:
        from weasyprint import HTML
        html = ExportService._md_to_html(prompt.generated_content)
        full_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body {{ font-family: sans-serif; margin: 40px; color: #1A1A2E; }}
  h1, h2, h3 {{ color: #1E3A5F; }}
  pre, code {{ background: #F8FAFC; padding: 4px 8px; border-radius: 4px; }}
  .header {{ background: #1E3A5F; color: white; padding: 20px; margin: -40px -40px 30px; }}
</style>
</head>
<body>
<div class="header"><h1>CHRONUS</h1><p>{prompt.title}</p></div>
{html}
</body>
</html>"""
        return HTML(string=full_html).write_pdf()

    @staticmethod
    def _md_to_html(md: str) -> str:
        import re
        html = md
        html = re.sub(r"^### (.+)$", r"<h3>\1</h3>", html, flags=re.MULTILINE)
        html = re.sub(r"^## (.+)$", r"<h2>\1</h2>", html, flags=re.MULTILINE)
        html = re.sub(r"^# (.+)$", r"<h1>\1</h1>", html, flags=re.MULTILINE)
        html = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", html)
        html = re.sub(r"`(.+?)`", r"<code>\1</code>", html)
        html = html.replace("\n\n", "</p><p>")
        return f"<p>{html}</p>"
