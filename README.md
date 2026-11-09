# LangChain e OpenAI

DR3 - TP2. Python 3.11 ou 3.12. Execute os comandos dentro desta pasta.

## Instalação

```bash
python -m venv .venv
# Linux/macOS:
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Execução

```bash
uvicorn main:app --host 127.0.0.1 --port 8000
```

Abra http://127.0.0.1:8000/docs para testar pelo Swagger. Pare uma aplicação antes de iniciar outra na mesma porta. O endpoint `/health` confirma que o startup terminou.

```bash
curl -X POST http://127.0.0.1:8000/translate -H "Content-Type: application/json" -d '{"text":"The weather is beautiful today."}'
```

No PowerShell, use o Swagger ou `curl.exe`. Entrada inválida retorna 422. Falhas de serviço são documentadas no código. Não há autenticação pública: executar como protótipo local.

## Testes

```bash
python -m pytest -q
```

Os testes de contrato substituem a inferência para validar HTTP sem download nem cobrança. Eles não medem qualidade do modelo. Consulte `VALIDACAO.md` na raiz da entrega para as verificações realmente executadas.

## Configuração OpenAI

Defina `OPENAI_API_KEY` no ambiente ou em `.env.local` nesta pasta antes de iniciar. `.env.example` lista as variáveis sem segredos. A chave não acompanha a entrega. `OPENAI_MODEL` permite selecionar outro modelo disponível na conta; padrão: `gpt-4.1-mini`. A conta precisa de acesso e saldo/cota de API; assinatura ChatGPT é separada.

A chamada usa `ainvoke` para não bloquear o loop HTTP. Há timeout de 30 segundos por tentativa e no máximo uma repetição automática; o tempo total pode superar 30 segundos. Isso não garante baixa latência. Erros 429, 502, 503 e 504 têm respostas controladas. Em produção, acrescentar limite de concorrência, orçamento, autenticação e métricas.

Para repetir as versões diretas usadas na validação, instale `requirements-testadas.txt` no lugar de `requirements.txt`. Os pacotes transitivos ainda são resolvidos pelo pip.

## Formato de saída

Exemplo ilustrativo; gerações reais podem variar.

```json
{
  "translation": "Le temps est magnifique aujourd’hui.",
  "source_language": "en",
  "target_language": "fr"
}
```
