from ctransformers import AutoModelForCausalLM
from flask import Flask, request, jsonify
import logging

import os

app = Flask(__name__)
app.config['models_folder'] = os.environ.get('KODLOKAL_MODELS') or './models/'
app.config['use_model'] = os.environ.get('KODLOKAL_SIZE') or 'xs'

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
log = logging.getLogger(__name__)

if app.config['use_model'] == 'm':
  print("Using M model")
  code_model_name = f"{app.config['models_folder']}WizardCoder-15B-1.0.ggmlv3.q5_1.bin"
  code_model_type="starcoder"
else:
  print("Using XS model")
  code_model_name = f"{app.config['models_folder']}stablecode-completion-alpha-3b-4k.ggmlv1.q5_1.bin"
  code_model_type = "gpt-neox"
  text_model_name = f"{app.config['models_folder']}orca_mini_v3_7b.ggmlv3.q5_0.bin"
  text_model_type = "llama"

code_model = AutoModelForCausalLM.from_pretrained(code_model_name, model_type=code_model_type)
text_model = AutoModelForCausalLM.from_pretrained(text_model_name, model_type=text_model_type)

def code_suggest(query):
  return code_model(query, temperature=0.2, max_new_tokens=42)

def text_suggest(query):
  return text_model(query, temperature=0.2, max_new_tokens=42)

@app.route("/")
def main():
  return "Kodlokal server"

@app.route("/code/completions", methods=["POST"])
def code_completions():
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
  app.run(host="127.0.0.1", port=3737)
