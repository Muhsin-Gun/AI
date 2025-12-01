# MyLocalAI Enhanced - Backend

This backend exposes endpoints to chat with a local model (via Ollama by default), analyze files, apply patches, and run shell commands.

Requirements:
- Python 3.10+
- Ollama (recommended) installed and running for best model performance and research capabilities.

Quick start (Windows PowerShell):

```powershell
cd backend
.\install_env.ps1
.\.venv\Scripts\Activate.ps1
# Pull models using Ollama (from scripts folder)
cd ..
cd scripts
.\pull_models.ps1
cd ../backend
# Start server (example uses deepseek-coder-7b)
.\run_server.ps1
```

Test with curl:

```powershell
curl -X POST http://127.0.0.1:5000/chat -H "Content-Type: application/json" -d '{ "text": "Hello, introduce yourself in one sentence." }'
```

If you do not want Ollama, switch MLAI_BACKEND to 'local' and implement local model code in model_client.py (note: large models require GPU/large RAM).
