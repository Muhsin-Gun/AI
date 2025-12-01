# Create and activate venv, then install requirements
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
echo "Virtual environment ready. To start server: .\.venv\Scripts\Activate.ps1; uvicorn app:app --host 127.0.0.1 --port 5000"
