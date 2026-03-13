Run it from the project root (search4cure-live), not from backend.

Go one level up
cd ~/search4cure-live

Then run:

python backend/pipeline/run_full_ingestion.py

or with uv (your comment suggests you use it):

uv run python backend/pipeline/run_full_ingestion.py