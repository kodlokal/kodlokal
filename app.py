from ctransformers import AutoModelForCausalLM
from flask import Flask, request, jsonify
from waitress import serve
import logging

import os

app = Flask(__name__)
app.config.from_pyfile('config.py')

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
log = logging.getLogger(__name__)

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

def code_suggest(query):
  return code_model(query,
                    temperature=app.config['CODE_TEMPERATURE'],
                    max_new_tokens=app.config['CODE_MAX_NEW_TOKENS'])

def text_suggest(query):
  return text_model(query,
                    temperature=app.config['TEXT_TEMPERATURE'],
                    max_new_tokens=app.config['TEXT_MAX_NEW_TOKENS'])

@app.route("/")
def main():
  return "Kodlokal server"

@app.route("/code/completions", methods=["POST"])
def code_completions():
  if not code_model_exist:
    return nil, 404
  data = request.json
  query = data.get("q")
  log.info(f"Starting Query={query}")
  if query is None or len(query) <= 3:
    return nil
  else:
    result = code_suggest(query)
    log.info(f"/Finished Result={result}")
    if result is not None:
      return result
    else:
      return nil

def text_prompt(query, input=""):
  return f"""### System:
You are an AI assistant that follows instruction extremely well. Help as much as you can.

### User:
{query}

### Input:
{input}

### Response:"""

@app.route("/text/completions", methods=["POST"])
def text_completions():
  if not text_model_exist:
    return nil, 404
  data = request.json
  query = data.get("q")
  prompt = text_prompt(query)
  log.info(f"Starting Query={query}")
  if query is None or len(query) <= 3:
    return nil
  else:
    result = text_suggest(query)
    log.info(f"/Finished Result={result}")
    if result is not None:
      return result
    else:
      return nil

if __name__ == "__main__":
  serve(app,
        host=app.config['HOST'],
        port=app.config['PORT'],
        threads=app.config['THREADS'],
        channel_timeout=app.config['TIMEOUT'])
