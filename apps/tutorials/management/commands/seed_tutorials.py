from django.core.management.base import BaseCommand
from apps.tutorials.models import TutorialCategory, Tutorial


TUTORIALS_DATA = [
    {
        "category": {"name": "Fundamentos de Programação", "slug": "fundamentos", "icon": "💡", "order": 1,
                     "description": "Conceitos essenciais para quem está começando na programação."},
        "tutorials": [
            {
                "title": "O que é Programação?",
                "slug": "o-que-e-programacao",
                "difficulty": "beginner",
                "estimated_minutes": 8,
                "description": "Entenda o que é programação, como computadores executam instruções e por que programar é uma habilidade tão valiosa.",
                "tags": ["introdução", "conceitos"],
                "content": """# O que é Programação?

## Definição simples

Programação é o processo de escrever **instruções** que um computador consegue entender e executar. Assim como uma receita de culinária diz ao cozinheiro exatamente o que fazer, um programa diz ao computador exatamente quais passos seguir.

## Como o computador pensa?

O computador só entende dois estados: **ligado (1)** e **desligado (0)**. Tudo que existe em software — textos, imagens, músicas — é representado como sequências de 0s e 1s, chamadas de **binário**.

```
01001000 01100101 01101100 01101100 01101111
  H         e        l        l        o
```

## Linguagens de Programação

Para não precisarmos escrever 0s e 1s diretamente, usamos **linguagens de programação** — idiomas intermediários que são mais fáceis para humanos lerem e escreverem.

Exemplos populares:

- **Python** — simples, legível, muito usado em IA e ciência de dados
- **JavaScript** — linguagem da web, roda nos navegadores
- **Java** — muito usada em sistemas corporativos
- **Django** — framework Python para criar sistemas web

## Por que aprender programação?

- Automatizar tarefas repetitivas
- Criar sistemas que resolvem problemas reais
- Comunicar melhor com equipes técnicas
- Entender melhor as ferramentas que você usa todo dia

## Conclusão

Todo sistema que você usa — WhatsApp, Instagram, o próprio CHRONUS — foi construído por programadores seguindo esse princípio: **quebrar um problema grande em passos menores** que o computador consegue executar um a um.
"""
            },
            {
                "title": "Lógica de Programação",
                "slug": "logica-de-programacao",
                "difficulty": "beginner",
                "estimated_minutes": 12,
                "description": "Aprenda os blocos fundamentais da lógica: variáveis, condicionais e loops.",
                "tags": ["lógica", "variáveis", "condicionais"],
                "content": """# Lógica de Programação

## O que é lógica de programação?

É a capacidade de **decompor um problema** em passos sequenciais e lógicos que um computador pode executar. Antes de escrever qualquer código, você precisa pensar logicamente sobre o problema.

## Variáveis — guardando informações

Uma variável é como uma **caixa com etiqueta** que guarda um valor.

```python
nome = "João"
idade = 25
salario = 4500.50
ativo = True
```

Os tipos mais comuns são:
- `str` (string) — textos: `"João"`, `"CSHUB"`
- `int` — números inteiros: `25`, `100`
- `float` — números decimais: `4500.50`
- `bool` — verdadeiro ou falso: `True`, `False`

## Condicionais — tomando decisões

O `if/else` permite que o programa tome **decisões diferentes** dependendo de uma condição.

```python
idade = 18

if idade >= 18:
    print("Maior de idade")
else:
    print("Menor de idade")
```

Você também pode encadear condições com `elif`:

```python
nota = 75

if nota >= 90:
    print("Excelente")
elif nota >= 70:
    print("Aprovado")
else:
    print("Reprovado")
```

## Loops — repetindo ações

Loops executam um bloco de código **várias vezes**.

**For** — quando você sabe quantas vezes repetir:

```python
for i in range(5):
    print(f"Iteração {i}")
# Saída: Iteração 0, Iteração 1, ... Iteração 4
```

**While** — enquanto uma condição for verdadeira:

```python
contador = 0
while contador < 3:
    print(f"Contagem: {contador}")
    contador += 1
```

## Funções — reutilizando código

Funções agrupam código que pode ser **reutilizado**:

```python
def saudacao(nome):
    return f"Olá, {nome}! Bem-vindo ao CHRONUS."

mensagem = saudacao("Maria")
print(mensagem)  # Olá, Maria! Bem-vindo ao CHRONUS.
```

## Exercício mental

Pense em como você descreveria ao computador os passos para fazer um café:

1. Verificar se há café em pó → *variável/condição*
2. Enquanto a água não ferver → *loop while*
3. Se o café estiver forte, adicionar água → *condicional if*

Esse raciocínio é o coração da programação!
"""
            },
        ]
    },
    {
        "category": {"name": "Git & Versionamento", "slug": "git", "icon": "🔀", "order": 2,
                     "description": "Controle de versão com Git e GitHub para trabalho em equipe."},
        "tutorials": [
            {
                "title": "Introdução ao Git",
                "slug": "introducao-ao-git",
                "difficulty": "beginner",
                "estimated_minutes": 15,
                "description": "Entenda o que é controle de versão e por que o Git é essencial para qualquer desenvolvedor.",
                "tags": ["git", "versionamento", "controle de versão"],
                "content": """# Introdução ao Git

## O problema que o Git resolve

Imagine que você está desenvolvendo um sistema. Você faz uma mudança, algo quebra, e você não lembra mais como estava antes. Ou dois colegas editam o mesmo arquivo ao mesmo tempo. **Git resolve esses problemas.**

Git é um **sistema de controle de versão** — ele rastreia todas as mudanças no seu código ao longo do tempo, como uma "máquina do tempo" para o seu projeto.

## Conceitos fundamentais

**Repositório (repo)** — a pasta do projeto com todo o histórico de mudanças.

**Commit** — um "snapshot" do seu código em um momento específico. É como tirar uma foto do estado atual.

**Branch** — uma linha paralela de desenvolvimento. Você cria branches para trabalhar em novas funcionalidades sem afetar o código principal.

**Merge** — juntar uma branch de volta à branch principal.

## Comandos essenciais

```bash
# Iniciar um repositório
git init

# Ver o estado atual dos arquivos
git status

# Adicionar arquivos para o próximo commit
git add nome-do-arquivo.py
git add .  # adiciona todos os arquivos modificados

# Criar um commit
git commit -m "Adiciona tela de login"

# Ver o histórico de commits
git log --oneline

# Criar e mudar para uma nova branch
git checkout -b feature/nova-funcionalidade

# Voltar para a branch principal
git checkout main

# Juntar a branch de volta ao main
git merge feature/nova-funcionalidade
```

## Trabalhando com GitHub

```bash
# Conectar seu repositório local ao GitHub
git remote add origin https://github.com/cshub/projeto.git

# Enviar commits para o GitHub
git push origin main

# Baixar atualizações do GitHub
git pull origin main

# Clonar um repositório existente
git clone https://github.com/cshub/projeto.git
```

## Fluxo de trabalho da equipe CSHUB

1. `git pull` — baixar as últimas mudanças
2. `git checkout -b feature/minha-tarefa` — criar sua branch
3. Fazer as mudanças no código
4. `git add . && git commit -m "Descrição clara do que foi feito"`
5. `git push origin feature/minha-tarefa`
6. Abrir um Pull Request no GitHub para revisão

> **Regra de ouro:** nunca faça commit direto na branch `main`. Sempre use branches e Pull Requests.
"""
            },
            {
                "title": "Boas práticas de commits",
                "slug": "boas-praticas-commits",
                "difficulty": "intermediate",
                "estimated_minutes": 10,
                "description": "Como escrever mensagens de commit claras e organizar seu histórico de forma profissional.",
                "tags": ["git", "commits", "boas práticas"],
                "content": """# Boas Práticas de Commits

## Por que mensagens de commit importam?

Um bom histórico de commits é como um **diário do projeto**. Quando algo quebra em produção às 2h da manhã, você vai querer entender exatamente o que mudou e por quê.

## Convenção de commits (Conventional Commits)

O padrão mais adotado na indústria usa o formato:

```
tipo(escopo): descrição curta

corpo opcional com mais detalhes

rodapé opcional
```

### Tipos principais

| Tipo | Quando usar |
|------|------------|
| `feat` | Nova funcionalidade |
| `fix` | Correção de bug |
| `docs` | Apenas documentação |
| `style` | Formatação (sem mudança de lógica) |
| `refactor` | Refatoração sem nova feature ou fix |
| `test` | Adicionando ou corrigindo testes |
| `chore` | Tarefas de manutenção |

### Exemplos bons vs. ruins

```bash
# ❌ Ruim — não diz nada
git commit -m "mudanças"
git commit -m "fix"
git commit -m "wip"

# ✅ Bom — claro e descritivo
git commit -m "feat(auth): adiciona login com Google OAuth"
git commit -m "fix(prompts): corrige erro ao gerar prompt com ideia vazia"
git commit -m "docs: atualiza README com instruções de deploy"
```

## Commits atômicos

Cada commit deve representar **uma única mudança lógica**. Evite commits gigantes com 20 arquivos alterados e sem relação entre si.

```bash
# ❌ Commit gigante — difícil de entender e reverter
git commit -m "várias coisas"

# ✅ Commits separados e claros
git commit -m "feat(dashboard): adiciona cards de estatísticas"
git commit -m "style(dashboard): ajusta espaçamento dos cards"
git commit -m "test(dashboard): adiciona testes dos cards de stats"
```

## .gitignore — nunca comite o que não deve

Crie um `.gitignore` para excluir arquivos sensíveis:

```gitignore
# Nunca suba para o repositório:
.env
*.pem
*.key
db.sqlite3
__pycache__/
venv/
node_modules/
```

> **Segurança crítica:** se você acidentalmente fizer commit de uma senha ou API key, considere-a comprometida e a troque imediatamente.
"""
            },
        ]
    },
    {
        "category": {"name": "Python & Django", "slug": "python-django", "icon": "🐍", "order": 3,
                     "description": "A linguagem Python e o framework Django que usamos no CHRONUS."},
        "tutorials": [
            {
                "title": "Python para Iniciantes",
                "slug": "python-iniciantes",
                "difficulty": "beginner",
                "estimated_minutes": 20,
                "description": "Uma introdução prática ao Python — a linguagem principal usada nos projetos CSHUB.",
                "tags": ["python", "sintaxe", "iniciante"],
                "content": """# Python para Iniciantes

## Por que Python?

Python é a linguagem escolhida pela CSHUB por vários motivos:

- **Legível** — o código se parece quase com inglês
- **Versátil** — web, IA, automação, ciência de dados
- **Ecossistema gigante** — milhares de bibliotecas prontas
- **Django** — o melhor framework web é em Python

## Sintaxe básica

```python
# Isso é um comentário — Python ignora esta linha

# Variáveis (sem precisar declarar o tipo)
nome = "CSHUB"
ano = 2024
pi = 3.14
ativo = True

# Imprimir na tela
print(f"Bem-vindo ao {nome}!")  # f-strings são ótimas para formatar texto

# Entrada do usuário
usuario = input("Qual seu nome? ")
print(f"Olá, {usuario}!")
```

## Listas e Dicionários

```python
# Lista — coleção ordenada
tecnologias = ["Python", "Django", "Tailwind", "Alpine.js"]
tecnologias.append("Docker")       # adicionar
tecnologias.remove("Alpine.js")    # remover
primeira = tecnologias[0]          # acessar pelo índice

# Percorrer uma lista
for tech in tecnologias:
    print(f"- {tech}")

# Dicionário — chave: valor (como JSON)
usuario = {
    "nome": "João",
    "email": "joao@cshub.com",
    "plano": "pro"
}

print(usuario["nome"])          # João
print(usuario.get("plano"))     # pro
usuario["cargo"] = "dev"        # adicionar novo campo
```

## Funções e Classes

```python
# Função simples
def calcular_area(largura, altura):
    return largura * altura

area = calcular_area(5, 3)
print(f"Área: {area}")  # Área: 15

# Classe — objeto com propriedades e métodos
class Projeto:
    def __init__(self, nome, cliente):
        self.nome = nome
        self.cliente = cliente
        self.concluido = False

    def concluir(self):
        self.concluido = True
        return f"Projeto '{self.nome}' concluído!"

meu_projeto = Projeto("ERP Fiscal", "CSHUB")
print(meu_projeto.concluir())
```

## Tratamento de erros

```python
try:
    resultado = 10 / 0
except ZeroDivisionError:
    print("Erro: divisão por zero!")
except Exception as e:
    print(f"Erro inesperado: {e}")
finally:
    print("Isso sempre executa")
```

## Próximos passos

Agora que você conhece o básico do Python, o próximo passo é aprender como o Django usa Python para criar sistemas web completos!
"""
            },
            {
                "title": "Como o Django funciona",
                "slug": "como-django-funciona",
                "difficulty": "intermediate",
                "estimated_minutes": 18,
                "description": "Entenda a arquitetura MVT do Django e como as peças se encaixam.",
                "tags": ["django", "mvt", "arquitetura"],
                "content": """# Como o Django Funciona

## O padrão MVT

O Django segue o padrão **MVT** (Model-View-Template), uma variação do famoso MVC:

```
Navegador → URLs → View → Model (banco de dados)
                 ↓
              Template (HTML renderizado) → Navegador
```

- **Model** — define a estrutura dos dados (tabelas do banco)
- **View** — contém a lógica de negócio (o que fazer com os dados)
- **Template** — o HTML que será enviado ao navegador

## Models — seu banco de dados em Python

Em vez de escrever SQL diretamente, você define classes Python:

```python
from django.db import models

class Prompt(models.Model):
    titulo = models.CharField(max_length=200)
    conteudo = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo
```

O Django converte isso automaticamente em uma tabela SQL:

```sql
CREATE TABLE prompts_prompt (
    id INTEGER PRIMARY KEY,
    titulo VARCHAR(200),
    conteudo TEXT,
    criado_em DATETIME,
    usuario_id INTEGER REFERENCES auth_user(id)
);
```

## Views — a lógica da aplicação

Uma view recebe uma requisição HTTP e retorna uma resposta:

```python
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Prompt

@login_required
def lista_prompts(request):
    # Buscar prompts do usuário logado
    prompts = Prompt.objects.filter(usuario=request.user)

    # Renderizar o template com os dados
    return render(request, 'prompts/lista.html', {
        'prompts': prompts
    })
```

## URLs — roteamento de requisições

```python
# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('prompts/', views.lista_prompts, name='lista-prompts'),
    path('prompts/<int:id>/', views.detalhe_prompt, name='detalhe-prompt'),
]
```

## Templates — o HTML dinâmico

```html
<!-- lista.html -->
<h1>Meus Prompts</h1>

{% for prompt in prompts %}
  <div class="card">
    <h2>{{ prompt.titulo }}</h2>
    <p>Criado em: {{ prompt.criado_em|date:"d/m/Y" }}</p>
    <a href="{% url 'detalhe-prompt' prompt.id %}">Ver detalhes</a>
  </div>
{% empty %}
  <p>Nenhum prompt ainda.</p>
{% endfor %}
```

## O fluxo completo

1. Usuário acessa `/prompts/`
2. Django verifica as URLs e encontra `lista_prompts`
3. A view consulta o banco: `Prompt.objects.filter(usuario=request.user)`
4. Os dados são passados ao template
5. O template gera o HTML final
6. O HTML é enviado de volta ao navegador

## ORM — consultas sem SQL

O Django ORM (Object-Relational Mapper) permite consultas em Python puro:

```python
# Todos os prompts
Prompt.objects.all()

# Filtrar
Prompt.objects.filter(titulo__contains="CRM")

# Ordenar
Prompt.objects.order_by('-criado_em')

# Criar
novo = Prompt.objects.create(titulo="Meu Prompt", conteudo="...")

# Atualizar
prompt.titulo = "Novo Título"
prompt.save()

# Deletar
prompt.delete()
```
"""
            },
        ]
    },
    {
        "category": {"name": "APIs & REST", "slug": "apis-rest", "icon": "🔌", "order": 4,
                     "description": "Como funcionam as APIs, o protocolo HTTP e o padrão REST."},
        "tutorials": [
            {
                "title": "O que é uma API?",
                "slug": "o-que-e-api",
                "difficulty": "beginner",
                "estimated_minutes": 10,
                "description": "Entenda APIs, HTTP e como sistemas se comunicam entre si.",
                "tags": ["api", "http", "rest"],
                "content": """# O que é uma API?

## Definição

**API** (Application Programming Interface) é uma forma padronizada de um sistema se comunicar com outro. É como uma tomada elétrica — você não precisa entender a usina para usar a eletricidade, só precisa encaixar o plugue.

## A analogia do restaurante

Imagine um restaurante:

- **Você** = Frontend (cliente)
- **Garçom** = API
- **Cozinha** = Backend/Banco de dados

Você não entra na cozinha. Você faz o pedido ao garçom (API), que leva até a cozinha (backend) e traz o resultado (resposta).

## HTTP — o protocolo da web

Toda comunicação na web usa o protocolo **HTTP**. Cada requisição tem:

- **Método** — o que você quer fazer
- **URL** — onde você está fazendo
- **Headers** — informações extras (autenticação, tipo de conteúdo)
- **Body** — dados que você envia (opcional)

### Métodos HTTP

| Método | Operação | Exemplo |
|--------|----------|---------|
| `GET` | Ler dados | Listar prompts |
| `POST` | Criar novo | Gerar um prompt |
| `PUT/PATCH` | Atualizar | Editar título |
| `DELETE` | Deletar | Remover prompt |

## Status codes — o que aconteceu?

```
200 OK              → Tudo certo
201 Created         → Criado com sucesso
400 Bad Request     → Você enviou dados errados
401 Unauthorized    → Não autenticado
403 Forbidden       → Sem permissão
404 Not Found       → Não encontrado
500 Server Error    → Erro no servidor
```

## Exemplo real — API do CHRONUS

```http
POST /api/prompts/generate/stream/
Content-Type: application/json
Authorization: Bearer eyJhbGc...

{
  "idea": "Quero um CRM para escritório contábil",
  "stack": "Django",
  "complexity": "complete"
}
```

Resposta (streaming de texto):

```
HTTP/1.1 200 OK
Content-Type: text/event-stream

data: # Seção 1 — Contexto...
data: O sistema será um CRM completo...
event: done
```

## JSON — a língua das APIs

A maioria das APIs modernas usa **JSON** para trocar dados:

```json
{
  "id": "abc-123",
  "title": "CRM Contábil",
  "stack": "Django",
  "created_at": "2024-01-15T10:30:00Z",
  "user": {
    "email": "joao@cshub.com"
  }
}
```

JSON é basicamente um dicionário Python — chave/valor, simples e legível por humanos e máquinas.

## Próximos passos

Agora que você entende o conceito, explore como o Django REST Framework cria APIs em Python e como o CHRONUS usa a API do Claude para gerar os prompts!
"""
            },
        ]
    },
    {
        "category": {"name": "Banco de Dados", "slug": "banco-de-dados", "icon": "🗄️", "order": 5,
                     "description": "SQL, PostgreSQL e modelagem de dados para aplicações web."},
        "tutorials": [
            {
                "title": "Introdução ao SQL",
                "slug": "introducao-sql",
                "difficulty": "beginner",
                "estimated_minutes": 15,
                "description": "Aprenda os comandos SQL fundamentais para consultar e manipular dados.",
                "tags": ["sql", "banco de dados", "postgresql"],
                "content": """# Introdução ao SQL

## O que é um banco de dados relacional?

Um banco de dados relacional organiza dados em **tabelas** (como planilhas), onde cada linha é um registro e cada coluna é um atributo. As tabelas se **relacionam** entre si através de chaves.

## Estrutura básica

```
Tabela: usuarios
+----+-------------+------------------+------------+
| id | nome        | email            | criado_em  |
+----+-------------+------------------+------------+
|  1 | João Silva  | joao@cshub.com   | 2024-01-10 |
|  2 | Maria Costa | maria@cshub.com  | 2024-01-12 |
+----+-------------+------------------+------------+

Tabela: prompts
+----+-----------+------------------+-----------+
| id | titulo    | conteudo         | usuario_id|
+----+-----------+------------------+-----------+
|  1 | CRM 2024  | # Seção 1...     |     1     |
|  2 | ERP Fiscal| # Seção 1...     |     1     |
+----+-----------+------------------+-----------+
```

## Comandos fundamentais

### SELECT — consultar dados

```sql
-- Todos os usuários
SELECT * FROM usuarios;

-- Colunas específicas
SELECT nome, email FROM usuarios;

-- Com filtro
SELECT * FROM prompts WHERE usuario_id = 1;

-- Ordenado
SELECT * FROM prompts ORDER BY criado_em DESC;

-- Limitado
SELECT * FROM prompts LIMIT 10;
```

### INSERT — inserir dados

```sql
INSERT INTO usuarios (nome, email)
VALUES ('Pedro Santos', 'pedro@cshub.com');
```

### UPDATE — atualizar dados

```sql
UPDATE prompts
SET titulo = 'CRM Contábil 2024'
WHERE id = 1;
```

### DELETE — remover dados

```sql
-- CUIDADO: sem WHERE apaga tudo!
DELETE FROM prompts WHERE id = 2;
```

## JOINs — relacionando tabelas

O JOIN combina dados de duas ou mais tabelas:

```sql
-- Listar prompts com o nome do usuário
SELECT
    p.titulo,
    p.criado_em,
    u.nome AS autor
FROM prompts p
JOIN usuarios u ON p.usuario_id = u.id
ORDER BY p.criado_em DESC;
```

## Funções de agregação

```sql
-- Quantos prompts por usuário
SELECT
    u.nome,
    COUNT(p.id) AS total_prompts
FROM usuarios u
LEFT JOIN prompts p ON p.usuario_id = u.id
GROUP BY u.nome
ORDER BY total_prompts DESC;

-- Média, soma, mín, máx
SELECT
    AVG(token_count) AS media_tokens,
    MAX(token_count) AS max_tokens
FROM prompts;
```

## PostgreSQL no CHRONUS

O CHRONUS usa **PostgreSQL** (via Supabase) por recursos avançados:

```sql
-- Full-text search (busca de texto completo)
SELECT * FROM prompts
WHERE search_vector @@ to_tsquery('portuguese', 'CRM & contábil');

-- JSONB (JSON armazenado e consultável)
SELECT * FROM prompts
WHERE focus_tags @> '["Segurança"]'::jsonb;
```

## Dica importante

Sempre que possível, use o **ORM do Django** em vez de SQL direto — é mais seguro (previne SQL Injection) e mais Pythônico. Use SQL raw apenas quando precisar de otimizações específicas.
"""
            },
        ]
    },
    {
        "category": {"name": "Docker & Deploy", "slug": "docker-deploy", "icon": "🐳", "order": 6,
                     "description": "Containerização com Docker e deploy de aplicações em produção."},
        "tutorials": [
            {
                "title": "Docker para Iniciantes",
                "slug": "docker-iniciantes",
                "difficulty": "intermediate",
                "estimated_minutes": 15,
                "description": "Entenda containers, imagens Docker e como o CHRONUS é empacotado para deploy.",
                "tags": ["docker", "containers", "deploy"],
                "content": """# Docker para Iniciantes

## O problema que o Docker resolve

"Funciona na minha máquina!" — essa frase famosa acontece porque cada computador tem configurações diferentes. Docker resolve isso criando **ambientes idênticos** em qualquer máquina.

## Conceitos fundamentais

**Imagem** — o "molde" do container. Contém o sistema operacional base, dependências e o código.

**Container** — uma instância em execução de uma imagem. É isolado do resto do sistema.

**Dockerfile** — arquivo de instruções para construir uma imagem.

**docker-compose** — ferramenta para orquestrar múltiplos containers juntos.

## Dockerfile — construindo uma imagem

```dockerfile
# Imagem base
FROM python:3.12-slim

# Variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Diretório de trabalho
WORKDIR /app

# Instalar dependências primeiro (aproveita cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código
COPY . .

# Porta que o app usa
EXPOSE 8000

# Comando para iniciar
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
```

## Docker Compose — múltiplos serviços

O CHRONUS usa vários serviços juntos:

```yaml
# docker-compose.yml
version: "3.9"

services:
  web:        # Aplicação Django
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - redis

  worker:     # Celery (tarefas em background)
    build: .
    command: celery -A config worker

  redis:      # Cache e fila de tarefas
    image: redis:7-alpine
    ports:
      - "6379:6379"
```

## Comandos essenciais

```bash
# Construir as imagens
docker-compose build

# Iniciar todos os serviços
docker-compose up

# Iniciar em background
docker-compose up -d

# Ver logs
docker-compose logs -f web

# Executar comando em um container
docker-compose exec web python manage.py migrate

# Parar tudo
docker-compose down
```

## Por que usamos Docker no CHRONUS?

1. **Consistência** — dev, staging e produção têm o mesmo ambiente
2. **Isolamento** — cada serviço roda em seu próprio container
3. **Escalabilidade** — fácil de escalar serviços individualmente
4. **Deploy simples** — um `docker-compose up` e o sistema está no ar

## Volumes — persistindo dados

Containers são efêmeros — ao reiniciar, os dados são perdidos. Volumes persistem dados:

```yaml
services:
  web:
    volumes:
      - ./media:/app/media      # arquivos de upload
      - static_volume:/app/staticfiles

volumes:
  static_volume:
```

## Próximos passos

Com Docker dominado, o próximo passo é entender CI/CD — pipelines automáticos que testam e fazem deploy do código toda vez que você faz um push para o GitHub!
"""
            },
        ]
    },
]


class Command(BaseCommand):
    help = "Popula o banco com tutoriais iniciais da CSHUB"

    def handle(self, *args, **options):
        created_total = 0
        for cat_data in TUTORIALS_DATA:
            cat_info = cat_data["category"]
            category, cat_created = TutorialCategory.objects.get_or_create(
                slug=cat_info["slug"],
                defaults={
                    "name": cat_info["name"],
                    "icon": cat_info["icon"],
                    "order": cat_info["order"],
                    "description": cat_info["description"],
                },
            )
            if cat_created:
                self.stdout.write(f"  + Categoria: {category.name}")

            for i, tut_data in enumerate(cat_data["tutorials"]):
                tut, tut_created = Tutorial.objects.get_or_create(
                    slug=tut_data["slug"],
                    defaults={
                        "category": category,
                        "title": tut_data["title"],
                        "description": tut_data["description"],
                        "content": tut_data["content"].strip(),
                        "difficulty": tut_data["difficulty"],
                        "estimated_minutes": tut_data["estimated_minutes"],
                        "tags": tut_data.get("tags", []),
                        "order": i,
                        "is_published": True,
                    },
                )
                if tut_created:
                    self.stdout.write(f"    > Tutorial: {tut.title}")
                    created_total += 1

        self.stdout.write(self.style.SUCCESS(f"\nOK: {created_total} tutoriais criados com sucesso!"))
