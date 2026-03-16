

### 1. Set the project
```bash
gcloud config set project search4cure-diabetes --quiet 
```
export GCS_BUCKET=diabetes-rag-assets

Run it from the project root (search4cure-live), 
Go one level up
cd ~/search4cure-live

git pull or 
git pull origin  main

Remove old environment & cache:

rm -rf .venv
rm -rf ~/.cache/uv


Create and sync your environment:

uv sync --active


Force install missing LangChain package:

uv add langchain-community

Create the bucket (if missing)

gcloud storage buckets create gs://diabetes-rag-assets \
--location=us-central1

Run ingestion:

uv run python -m backend.pipeline.run_full_ingestion
or 

source .venv/bin/activate

python -m backend.pipeline.run_full_ingestion

run long pipelines on cloudshell:

nohup uv run python -m backend.pipeline.run_full_ingestion > pipeline.log 2>&1 &

- nohup → keeps the process alive

- > pipeline.log → saves output to a log file

- & → runs it in the background

check logs:
tail -f pipeline.log

To check the process:

ps aux | grep run_full_ingestion

Monitor progress
watch -n 5 'grep -c "Completed paper:" pipeline.log'


grep -c "Completed paper:" pipeline.log


Expected runtime

From your earlier run:

~34 seconds per paper

For 300 papers:

300 × 34s ≈ 2.8 hours

So the run will likely finish in 2.5–3 hours.






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

Save your local changes.

git add pyproject.toml
git commit -m "fix dependency config"
git pull


Gemini Flash pricing (important for your project)
Example: Gemini Flash models


| Model            | Input cost               | Output cost              |
| ---------------- | ------------------------ | ------------------------ |
| Gemini 2.5 Flash | ~$0.30 per **1M tokens** | ~$2.50 per **1M tokens** |
| Gemini 2.0 Flash | ~$0.15 per **1M tokens** | ~$0.60 per **1M tokens** |



This is extremely cheap compared to most models.

Example:

1 paper ≈ 3k–10k tokens

300 papers ≈ 1–3M tokens

Cost estimate:

| Papers     | Estimated cost |
| ---------- | -------------- |
| 10 papers  | ~$0.01         |
| 100 papers | ~$0.05         |
| 300 papers | ~$0.10 – $0.30 |








