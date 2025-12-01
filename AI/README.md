# MyLocalAI Enhanced - Starter Repo

This repository is a starter scaffold for a local AI assistant that runs on your machine and integrates with VS Code.

Structure:
- backend/: FastAPI server + model client (Ollama)
- vscode-extension/: VS Code extension to interact with the server
- scripts/: helper PowerShell scripts (pull models, setup venv)
- docs/: sample prompts and docs

Important:
- Ollama is strongly recommended for a powerful model. Install it from https://ollama.com/download
- After installing Ollama, pull a recommended model such as `deepseek-coder-7b` or `qwen2-7b`.
- If you cannot run heavy models locally, you can test server with dummy responses.

Quick start (PowerShell):
1) cd backend
2) .\install_env.ps1
3) .\.venv\Scripts\Activate.ps1
4) cd ..\scripts
5) .\pull_models.ps1
6) cd ..\backend
7) .\run_server.ps1

Test chat:
curl -X POST http://127.0.0.1:5000/chat -H "Content-Type: application/json" -d '{ "text": "Hello" }'
