from fastapi import FastAPI
from pydantic import BaseModel
from model_client import ModelClient
from utils import apply_patch_to_file, run_shell_command
import os
import uvicorn

app = FastAPI(title="MyLocalAI Enhanced")

# Choose backend: 'ollama' (recommended) or 'local' (transformers)
MODEL_BACKEND = os.environ.get("MLAI_BACKEND", "ollama")
MODEL_NAME = os.environ.get("MLAI_MODEL", "deepseek-coder-7b")

client = ModelClient(backend=MODEL_BACKEND, model_name=MODEL_NAME)

class Prompt(BaseModel):
    text: str
    context: str | None = None
    max_tokens: int = 512

class FileRequest(BaseModel):
    path: str

class PatchRequest(BaseModel):
    patch: str  # unified diff

class CommandRequest(BaseModel):
    command: str

@app.post("/chat")
def chat(prompt: Prompt):
    resp = client.chat(prompt.text, context=prompt.context, max_tokens=prompt.max_tokens)
    return {"response": resp}

@app.post("/analyze_file")
def analyze_file(req: FileRequest):
    if not os.path.isfile(req.path):
        return {"error": "file not found", "path": req.path}
    with open(req.path, "r", encoding="utf-8") as f:
        content = f.read()
    prompt = f"Analyze this file and list issues, improvements and possible fixes. File path: {req.path}\n\n{content}"
    resp = client.chat(prompt, max_tokens=1024)
    return {"analysis": resp}

@app.post("/apply_patch")
def apply_patch(req: PatchRequest):
    result = apply_patch_to_file(req.patch)
    return {"result": result}

@app.post("/run_command")
def run_command(req: CommandRequest):
    out = run_shell_command(req.command)
    return {"output": out}


if __name__ == "__main__":
    # When running directly (e.g., on Replit), bind to all interfaces
    # and use port 3000 so the Replit web server can expose the app.
    uvicorn.run("app:app", host="0.0.0.0", port=3000, reload=True)
