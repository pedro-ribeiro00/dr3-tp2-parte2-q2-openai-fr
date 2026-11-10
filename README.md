# Parte 2 - Questão 2: OpenAI

## Como executar

Use Python 3.11 ou 3.12. Dentro desta pasta, crie um ambiente e instale as dependências:

```bash
python -m venv .venv
```

Ative o ambiente:

```bash
# Linux ou macOS
source .venv/bin/activate
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

```bash
python -m pip install -r requirements.txt
uvicorn main:app --port 8000
```

Abra http://127.0.0.1:8000/docs, selecione POST /translate, clique em “Try it out” e envie:

```json
{"text": "The weather is beautiful today."}
```

Também é possível enviar pelo terminal (no Windows, use curl.exe):

```bash
curl -X POST http://127.0.0.1:8000/translate -H "Content-Type: application/json" -d '{"text":"The weather is beautiful today."}'
```

Execute uma aplicação por vez na porta 8000. Textos vazios são recusados com erro 422.

## Chave OpenAI

Antes de executar, crie `.env.local` nesta pasta e defina `OPENAI_API_KEY` com sua chave, ou use essa variável no ambiente. A chave não acompanha o trabalho. A API precisa de acesso ao modelo gpt-4.1-mini e saldo ou cota disponível.

A chamada ao modelo é assíncrona, com uma tentativa e timeout de 30 segundos. Limite de uso retorna 429; indisponibilidade retorna 503. A resposta tem o campo `translation`.
