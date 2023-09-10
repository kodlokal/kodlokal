import json
from flask import request, jsonify
from app.kodlokal_app import app
from app.log import log
from app.inference.model import Model

code_model = Model('CODE')
text_model = Model('TEXT')

def choose_model(category):
  if category == 'code':
    return code_model
  elif category == 'text':
    return text_model
  else:
    return None

@app.route("/v1/completions", methods=["POST"])
def v1_completions():
  data = request.json
  category = data.get("model") or "code"
  model = choose_model(category)

  if model is None or not model.exist():
    error = f"Model {category} not found in config"
    log.error(error)
    return { "error": error }, 404

  prompt = data.get("prompt")
  if not model.prompt_ok(prompt):
    error = f"Model {category} Prompt is empty or less than 3 chars"
    log.error(error)
    return {"error": error}, 404

  log.info(f"Starting with model={category} prompt={prompt}")
  suggestion = model.suggest(prompt)

  if suggestion is None:
    log.error(f"/Finished with no result")
    return {"error": "Result not found"}, 404

  result = model.present(suggestion, prompt)
  log.info(f"/Finished with completion={json.dumps(result)}")
  return jsonify(result)
