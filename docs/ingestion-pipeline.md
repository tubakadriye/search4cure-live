

### 1. Set the project
```bash
gcloud config set project search4cure-diabetes --quiet 
```

Run it from the project root (search4cure-live), 
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

uv run python -m backend.pipeline.run_full_ingestion
or 

source .venv/bin/activate

python -m backend.pipeline.run_full_ingestion




