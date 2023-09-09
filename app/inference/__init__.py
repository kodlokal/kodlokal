from ctransformers import AutoModelForCausalLM
from app.log import log
from app.kodlokal_app import app
import time

code_model_exist = 'CODE_MODEL' in app.config

print("Using models:")
if code_model_exist:
  code_model_name = f"{app.config['MODELS_FOLDER']}{app.config['CODE_MODEL']}"
  code_model_type = app.config['CODE_MODEL_TYPE']
  print(f"""code: {code_model_name}/{code_model_type}""")

text_model_exist = 'TEXT_MODEL' in app.config
if text_model_exist:
  text_model_name = f"{app.config['MODELS_FOLDER']}{app.config['TEXT_MODEL']}"
  text_model_type = app.config['TEXT_MODEL_TYPE']
  print(f"""text: {text_model_name}/{text_model_type}""")

if code_model_exist:
  code_model = AutoModelForCausalLM.from_pretrained(code_model_name,
                                                  model_type=code_model_type,
                                                  gpu_layers=app.config['CODE_GPU_LAYERS'])

if text_model_exist:
  text_model = AutoModelForCausalLM.from_pretrained(text_model_name,
                                                  model_type=text_model_type,
                                                  gpu_layers=app.config['TEXT_GPU_LAYERS'])
def full_response(result, prompt, model_name):
  response_data = {
    "choices": [
      {
        "finish_reason": "length",
        "index": 0,
        "logprobs": None,
        "text": result
      }
    ],
    "created": int(time.time()),
    "id": "cmpl-7C9Wxi9Du4j1lQjdjhxBlO22M61LD",
    "model": model_name,
    "object": "text_completion",
    "usage": {
      "completion_tokens": len(result),
      "prompt_tokens": len(prompt),
      "total_tokens": len(result) + len(prompt)
    }
  }
  return response_data

def code_suggest(prompt):
  result = code_model(prompt,
                      temperature=app.config['CODE_TEMPERATURE'],
                      max_new_tokens=app.config['CODE_MAX_NEW_TOKENS'])

  return full_response(result, prompt, code_model_name)

def text_suggest(prompt):
  result = text_model(prompt,
                    temperature=app.config['TEXT_TEMPERATURE'],
                    max_new_tokens=app.config['TEXT_MAX_NEW_TOKENS'])

  return full_response(result, prompt, text_model_name)

def instruct_prompt(prompt, input=""):
  return f"""### System:
You are an AI assistant that follows instruction extremely well. Help as much as you can.

### User:
{prompt}

### Input:
{input}

### Response:"""
