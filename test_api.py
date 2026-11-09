from fastapi.testclient import TestClient
from unittest.mock import Mock, AsyncMock
from main import app

def test_translation_and_validation():
    # Sem lifespan: não baixa pesos nem chama serviços externos.
    app.state.translate = Mock(return_value="Bonjour")
    app.state.translate.invoke = Mock(return_value="Guten Tag")
    app.state.chain = Mock()
    app.state.chain.ainvoke = AsyncMock(return_value="Bonjour")
    client = TestClient(app)
    response = client.post("/translate", json={"text": "Hello"})
    assert response.status_code == 200
    assert response.json()["translation"] == "Bonjour"
    assert response.json()["target_language"] == "fr"
    assert response.json()["source_language"] == "en"
    assert client.post("/translate", json={"text":"   "}).status_code == 422
    assert client.post("/translate", json={}).status_code == 422


def test_timeout_and_rate_limit():
    import httpx
    from openai import APITimeoutError, RateLimitError
    client = TestClient(app)
    request = httpx.Request("POST", "https://api.openai.com/v1/chat/completions")
    app.state.chain.ainvoke = AsyncMock(side_effect=APITimeoutError(request=request))
    assert client.post("/translate", json={"text":"Hello"}).status_code == 504
    response = httpx.Response(429, request=request)
    app.state.chain.ainvoke = AsyncMock(side_effect=RateLimitError("limit", response=response, body=None))
    assert client.post("/translate", json={"text":"Hello"}).status_code == 429
