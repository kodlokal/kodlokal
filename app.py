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
  model_name = f"{app.config['models_folder']}WizardCoder-15B-1.0.ggmlv3.q5_1.bin"
  model_type="starcoder"
else:
  print("Using XS model")
  model_name = f"{app.config['models_folder']}stablecode-completion-alpha-3b-4k.ggmlv1.q5_1.bin"
  model_type = "gpt-neox"

model = AutoModelForCausalLM.from_pretrained(model_name,
                                             model_type=model_type)
def suggest(query):
  return model(query, temperature=0.2, max_new_tokens=42)

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
    result = suggest(query)
    log.info(f"/Finished Result={result}")
    if result is not None:
      return result
    else:
      return nil

if __name__ == "__main__":
  app.run(host="127.0.0.1", port=3737)
