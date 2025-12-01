import os
import requests
import json
from typing import Optional

# Remote Ollama base URL and optional API key
OLLAMA_API = os.environ.get("OLLAMA_API", "http://127.0.0.1:11434")
OLLAMA_API_KEY = os.environ.get("OLLAMA_API_KEY", "")


class ModelClient:
    def __init__(self, backend='ollama', model_name='deepseek-coder-7b'):
        self.backend = backend
        self.model_name = model_name

    def chat(self, prompt: str, context: Optional[str] = None, max_tokens: int = 512) -> str:
        if self.backend == 'ollama':
            return self._ollama_chat(prompt, max_tokens)
        else:
            return "Local transformers mode not implemented in this starter. Install Ollama or set MLAI_BACKEND=ollama."

    def _ollama_chat(self, prompt: str, max_tokens: int):
        """
        Call a remote Ollama HTTP API. The environment variable `OLLAMA_API`
        can point to a remote Ollama server (e.g. a Replit proxy). If
        `OLLAMA_API_KEY` is set, it will be sent as a Bearer token.
        This function tries common Ollama endpoints and attempts to
        extract a usable string from the response.
        """
        base = OLLAMA_API.rstrip('/')
        endpoints = [
            '/v1/complete',
            '/v1/completions',
            '/v1/responses',
        ]

        headers = {}
        if OLLAMA_API_KEY:
            headers['Authorization'] = f"Bearer {OLLAMA_API_KEY}"

        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "max_tokens": max_tokens,
        }

        last_err = None
        for ep in endpoints:
            url = f"{base}{ep}"
            try:
                r = requests.post(url, json=payload, headers=headers or None, timeout=60)
                r.raise_for_status()
                data = r.json()

                # Try common fields returned by Ollama-like APIs
                if isinstance(data, dict):
                    if 'completion' in data and isinstance(data['completion'], str):
                        return data['completion']
                    if 'output' in data:
                        out = data['output']
                        if isinstance(out, list):
                            return '\n'.join(map(str, out))
                        return str(out)
                    if 'choices' in data and len(data['choices']) > 0:
                        choice = data['choices'][0]
                        # choice may contain 'text' or 'message'
                        if isinstance(choice, dict):
                            if 'message' in choice:
                                return choice['message']
                            if 'text' in choice:
                                return choice['text']
                # Fallback: return raw text body
                text = r.text
                if text:
                    return text
                return json.dumps(data)
            except Exception as e:
                last_err = e
                continue

        return f"Error calling Ollama API: {last_err}\nTried URL base: {base} (endpoints: {endpoints})"

