from ctransformers import AutoModelForCausalLM
from flask import Flask, request, jsonify
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
log = logging.getLogger(__name__)

model = 'TheBloke/stablecode-completion-alpha-3b-4k-GGML'
llm = AutoModelForCausalLM.from_pretrained(model)

app = Flask(__name__)

@app.route("/")
def main():
  return "Kodlokal server"

@app.route("/code/completions", methods=["POST"])
def code_completions():
  data = request.json
  query = data.get("q")
  log.info(f"Starting Query={query}")
  if query is None or len(query) <= 3:
    return nil #jsonify({'error': 'Missing query_param in request'}), 400
  else:
    result = llm(query, temperature=0.17, max_new_tokens=50)
    log.info(f"/Finished Result={result}")
    if result is not None:
      return result
    else:
      return jsonify({'error': 'No results'}), 404

if __name__ == "__main__":
  app.run(host="127.0.0.1", port=3737)
