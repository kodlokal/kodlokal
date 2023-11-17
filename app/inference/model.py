"""
The inference model
"""

import time
import uuid
import os
from ctransformers import AutoModelForCausalLM
from app.kodlokal_app import app
from app.log import log


class Model():
    """
  The model class.

  :param category: the category of the model, one of "TEXT", "CODE", "CHAT"
  :category version: str
  """

    def __init__(self, category):
        self.category = category
        self.model = None
        self.system_prompt = None
        if self.exist():
            self.load()
            log.info("Started %s model for %s", self.category, self.name())
        else:
            log.warning("%s model does not exist in config", self.category)

    def __str__(self):
        return f'Model category: {self.category}'

    def config(self, key):
        """
        Configuration parameters for this model
        """
        return app.config[f"{self.category}_{key}"]

    def name(self):
        """
        Full path for the model
        """
        return f"{app.config['MODELS_FOLDER']}{self.config('MODEL')}"

    def exist(self):
        """
        Is this configured?
        """
        return f"{self.category}_MODEL" in app.config

    def load(self):
        """
        Load the machine learning model into the memory
        """
        if os.path.exists(self.name()):
            self.model = AutoModelForCausalLM.from_pretrained(
                self.name(),
                model_type=self.config('MODEL_TYPE'),
                gpu_layers=self.config('GPU_LAYERS'),
                context_length=self.config('CONTEXT_LENGTH'))
            system_template_file_path = f"{self.name()}.system.template"
            if os.path.exists(system_template_file_path):
                with open(system_template_file_path, 'r', encoding='utf-8') as file:
                    self.system_prompt = file.read()
        else:
            self.model = None

    def get_prompt(self, prompt):
        if not self.system_prompt is None:
            return self.system_prompt.replace('{PROMPT}', prompt)

    def suggest(self, prompt):
        """
        Do an inference
        """
        prompt = self.get_prompt(prompt)
        if self.model is not None:
            return self.model(prompt,
                              temperature=self.config('TEMPERATURE'),
                              max_new_tokens=self.config('MAX_NEW_TOKENS'))

        return None

    def prompt_ok(self, prompt):
        """
        Is the prompt valid?
        """
        return prompt is not None and len(prompt) >= 3

    def present(self, result, prompt):
        """
        Convert the suggestions to an object for jsonification
        """
        response_data = {
            "choices": [{
                "finish_reason": "length",
                "index": 0,
                "text": result
            }],
            "created": int(time.time()),
            "id": str(uuid.uuid4()),
            "model": self.name(),
            "object": "text_completion",
            "usage": {
                "completion_tokens": len(result),
                "prompt_tokens": len(prompt),
                "total_tokens": len(result) + len(prompt)
            }
        }
        return response_data
