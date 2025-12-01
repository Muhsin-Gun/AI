import os
import requests
import json
import subprocess
from typing import Optional

OLLAMA_API = os.environ.get("OLLAMA_API", "http://127.0.0.1:11434")  # default Ollama REST api

class ModelClient:
    def __init__(self, backend='ollama', model_name='deepseek-coder-7b'):
        self.backend = backend
        self.model_name = model_name

    def chat(self, prompt: str, context: Optional[str]=None, max_tokens: int=512) -> str:
        if self.backend == 'ollama':
            return self._ollama_chat(prompt, max_tokens)
        else:
            # placeholder for local transformers support
            return "Local transformers mode not implemented in this starter. Install Ollama and pull a model."

    def _ollama_chat(self, prompt: str, max_tokens: int):
        # This calls Ollama's local API. Ollama must be installed & running.
        url = f"{OLLAMA_API}/v1/complete"
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "max_tokens": max_tokens
        }
        try:
            r = requests.post(url, json=payload, timeout=60)
            r.raise_for_status()
            data = r.json()
            # Ollama's API format may vary; this assumes 'completion' or 'choices'
            if 'completion' in data:
                return data['completion']
            if 'choices' in data and len(data['choices'])>0:
                return data['choices'][0].get('message', '') or data['choices'][0].get('text','')
            return json.dumps(data)
        except Exception as e:
            return f"Error calling Ollama API: {e}\nEnsure Ollama is installed and a model is pulled. URL: {url}"

