

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



load all existing IDs once:

def get_existing_papers(database):
    with database.snapshot() as snapshot:
        results = snapshot.execute_sql("SELECT paper_id FROM Papers")
        return set(row[0] for row in results)


Fix the authentication (1 minute)

Run this in Cloud Shell:

gcloud auth application-default login

Then confirm:

gcloud config set project search4cure-diabetes

Then verify:

gcloud auth application-default print-access-token

If it prints a token → authentication works.

how many papers finished in the graph:

SELECT COUNT(*) FROM Papers;

in **Google Cloud Spanner.





ower the batch size so data is written more often.

Change:

BATCH_SIZE = 5000

to:

BATCH_SIZE = 200

This means:

every ~3 papers → insert into Spanner

so crashes will not lose progress.


✅ batch insertion
✅ crash-safe logging
✅ deduplication with existing_papers
✅ entity extraction fallback
✅ image + caption embeddings
✅ table extraction
✅ page graph nodes

For 300 papers, this is production-level ingestion.


Add Parallel Paper Processing

Instead of:

for paper in loader.stream_pdfs():

Use ThreadPoolExecutor.

Add this import:

from concurrent.futures import ThreadPoolExecutor, as_completed

sequential loop:

for paper in tqdm(loader.stream_pdfs(), desc="Papers", unit="paper"):

That means:

paper1 → paper2 → paper3 → paper4

You want:

paper1
paper2
paper3
paper4  (parallel)

Old pipeline:

300 papers
× 2–3 minutes each
= ~12 hours

Parallel pipeline:

4 workers
300 / 4 = 75 batches
≈ 2–4 hours