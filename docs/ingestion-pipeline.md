Run it from the project root (search4cure-live), not from backend.

Go one level up
cd ~/search4cure-live

git pull

Remove old environment & cache:

rm -rf .venv
rm -rf ~/.cache/uv


Create and sync your environment:

uv sync --active


Force install missing LangChain package:

uv add langchain-community


Run ingestion:

python -m backend.pipeline.run_full_ingestion

or with uv (your comment suggests you use it):

uv run python backend/pipeline/run_full_ingestion.py

