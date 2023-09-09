import json
from flask import request, jsonify
from app.kodlokal_app import app
from app.log import log
from app.inference import text_suggest, code_suggest

@app.route("/v1/completions", methods=["POST"])
def v1_completions():
    data = request.json
    model = data.get("model") or "code"

    if model == "code" and not 'CODE_MODEL' in app.config:
        return {"error": "Model not found"}, 404

    if model == "text" and not 'TEXT_MODEL' in app.config:
        return {"error": "Model not found"}, 404

    prompt = data.get("prompt")
    if prompt is None or len(prompt) <= 3:
        return {"error": "Prompt is empty or less than 3 chars"}, 404

    log.info(f"Starting with model={model} prompt={prompt}")
    if model == "code":
        result = code_suggest(prompt)
    elif model == "text":
        result = text_suggest(prompt)
    else:
        return {"error": "Model not found"}, 404

    if result is not None:
        log.info(f"/Finished with completion={json.dumps(result)}")
        return jsonify(result)
    else:
        return {"error": "Result not found"}, 404
