import pytest
from unittest.mock import patch, MagicMock, PropertyMock


@pytest.mark.django_db
class TestPromptGenerationService:
    def test_quota_exceeded_raises(self, user_factory):
        from apps.prompts.services import PromptGenerationService, QuotaExceededError
        from apps.accounts.services import AccountService
        user = user_factory(monthly_quota=0)

        service = PromptGenerationService.__new__(PromptGenerationService)
        service._client = MagicMock()
        service._system_prompt = "system"

        with patch.object(AccountService, "has_quota", return_value=False):
            gen = service.generate_stream(user=user, idea="test")
            with pytest.raises(QuotaExceededError):
                list(gen)

    def test_generate_stream_yields_chunks(self, user_factory):
        from apps.prompts.services import PromptGenerationService

        user = user_factory()
        service = PromptGenerationService.__new__(PromptGenerationService)
        service._system_prompt = "system"

        mock_stream = MagicMock()
        mock_stream.__enter__ = MagicMock(return_value=mock_stream)
        mock_stream.__exit__ = MagicMock(return_value=False)
        mock_stream.text_stream = iter(["SEÇÃO 1 chunk", " more text"])
        mock_final = MagicMock()
        mock_final.usage.input_tokens = 100
        mock_final.usage.output_tokens = 200
        mock_stream.get_final_message.return_value = mock_final

        mock_client = MagicMock()
        mock_client.messages.stream.return_value = mock_stream
        service._client = mock_client

        chunks = list(service.generate_stream(user=user, idea="CRM app"))
        assert len(chunks) == 2
        assert chunks[0] == "SEÇÃO 1 chunk"

    def test_export_to_markdown(self, prompt_factory):
        from apps.prompts.services import ExportService
        prompt = prompt_factory(generated_content="# Test\n\nContent here.")
        result = ExportService.to_markdown(prompt)
        assert "# Test" in result

    def test_export_to_txt_strips_markdown(self, prompt_factory):
        from apps.prompts.services import ExportService
        prompt = prompt_factory(generated_content="# Test\n\n**bold** `code`")
        result = ExportService.to_txt(prompt)
        assert "#" not in result
        assert "**" not in result
