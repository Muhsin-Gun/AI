# Run this to start the FastAPI server
$env:MLAI_BACKEND = "ollama"
$env:MLAI_MODEL = "deepseek-coder-7b"
python -m uvicorn app:app --host 127.0.0.1 --port 5000
