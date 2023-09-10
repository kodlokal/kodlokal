import pytest
from unittest.mock import Mock, patch
from app.kodlokal_app import app
from app.inference.model import Model
from ctransformers import AutoModelForCausalLM

@pytest.fixture
def text_model():
  return Model("TEXT")

def test_model_init_exist(text_model):
  assert text_model.category == "TEXT"

def test_model_init_not_exist(text_model):
  model = Model("NON_EXISTING_CATEGORY")

  assert model.category == "NON_EXISTING_CATEGORY"
  assert model.model is None

def test_model_config(text_model):
  app.config["TEXT_MODEL_TYPE"] = "gpt2"
  app.config["TEXT_GPU_LAYERS"] = 2

  assert text_model.config("MODEL_TYPE") == "gpt2"
  assert text_model.config("GPU_LAYERS") == 2

def test_model_name(text_model):
  app.config["MODELS_FOLDER"] = "/path/to/models/"
  app.config["TEXT_MODEL"] = "my_model"
  assert text_model.name() == "/path/to/models/my_model"

def test_model_load_existing(text_model):
  with patch("os.path.exists", return_value=True):
    with patch.object(AutoModelForCausalLM, 'from_pretrained', return_value="FOO"):
      text_model.load()
      assert text_model.model is 'FOO'

def test_model_load_not_existing(text_model):
  with patch("os.path.exists", return_value=False):
    text_model.load()
    assert text_model.model is None

def test_model_suggest(text_model):
  text_model.model = Mock(return_value="Generated text")
  result = text_model.suggest("Input prompt")
  assert result == "Generated text"

def test_model_suggest_no_model(text_model):
  text_model.model = None
  result = text_model.suggest("Input prompt")
  assert result is None

def test_model_prompt_ok(text_model):
  assert text_model.prompt_ok("ABC") is True
  assert text_model.prompt_ok("12") is False
  assert text_model.prompt_ok("") is False
  assert text_model.prompt_ok("A") is False

def test_model_present(text_model):
  app.config["MODELS_FOLDER"] = "/path/to/models/"
  app.config["TEXT_MODEL"] = "my_model"

  result = "Generated text"
  prompt = "Input prompt"

  response_data = text_model.present(result, prompt)

  assert response_data['choices'] == [
      {
        "finish_reason": "length",
        "index": 0,
        "text": result
      }
    ]
  assert response_data['usage'] == {
    "completion_tokens": len(result),
    "prompt_tokens": len(prompt),
    "total_tokens": len(result) + len(prompt)
  }
  assert response_data["object"] == "text_completion"
  assert response_data["model"] == "/path/to/models/my_model"
