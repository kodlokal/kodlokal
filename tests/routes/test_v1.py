import json
import pytest
from app.kodlokal_app import app
from unittest.mock import MagicMock, patch
from app.inference.model import Model


@pytest.fixture
def mock_model():
    obj = MagicMock()
    obj.exist.return_value = True
    obj.prompt_ok.return_value = True
    obj.suggest.return_value = "And it is great"
    return obj


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_v1_completions_valid(client):
    with patch.object(Model, 'suggest') as mock_suggest:
        mock_suggest.return_value = "And it is great"
        data = {"model": "code", "prompt": "This is a test prompt."}
        response = client.post('/v1/completions', json=data)
        assert response.status_code == 200
        result = json.loads(response.data)
        assert "error" not in result
        assert "choices" in result
        assert result["choices"][0]["text"] == "And it is great"


def test_v1_completions_invalid_model(client):

    data = {"model": "invalid_model", "prompt": ""}
    response = client.post('/v1/completions', json=data)
    assert response.status_code == 404
    result = json.loads(response.data)
    assert "error" in result
    assert "Model invalid_model not found" in result["error"]


def test_v1_completions_empty_prompt(client):
    data = {"model": "code", "prompt": ""}
    response = client.post('/v1/completions', json=data)
    assert response.status_code == 404
    result = json.loads(response.data)
    assert "error" in result
    assert "Model code Prompt is empty or less than 3 chars" in result["error"]


def test_v1_completions_empty_suggestion(client):
    with patch.object(Model, 'suggest') as mock_suggest:
        mock_suggest.return_value = None
        data = {"model": "code", "prompt": "This is a test prompt."}
        response = client.post('/v1/completions', json=data)
        assert response.status_code == 404
        result = json.loads(response.data)
        assert "error" in result
        assert "Result not found" in result["error"]
