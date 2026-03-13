

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




Advantages:

10× faster

no Ghostscript

works better with research PDFs

fewer dependencies


1️⃣ Set your project

Replace with your project ID if different.

gcloud config set project search4cure-diabetes

2️⃣ Authenticate your user
gcloud auth application-default login


This will open a browser → approve.


5️⃣ Test Vertex AI quickly

Run this test:

python - <<EOF
from vertexai.language_models import TextEmbeddingModel
import vertexai

vertexai.init(project="search4cure-diabetes", location="us-central1")
model = TextEmbeddingModel.from_pretrained("text-embedding-004")
print("Vertex AI works")
EOF


If you see:

Vertex AI works


then your ingestion pipeline will run.

Then run your pipeline again
uv run python -m backend.pipeline.run_full_ingestion