# Google Cloud Project Setup for Search4Cure Diabetes

## Project
- Project ID: `search4cure-diabetes`
- Environment tag: `Development`

## Commands Run

### 1. Set the project
```bash
gcloud config set project search4cure-diabetes --quiet 
```

### 2. Add environment tag
```bash
gcloud resource-manager tags bindings create \
    --parent=projects/search4cure-diabetes \
    --tag-key=environment \
    --tag-value=Development

```

### 3. Enable required services
```bash
gcloud services enable \
  compute.googleapis.com \
  aiplatform.googleapis.com \
  run.googleapis.com \
  cloudbuild.googleapis.com \
  artifactregistry.googleapis.com \
  spanner.googleapis.com \
  storage.googleapis.com
```

## Purpose of Services

- compute.googleapis.com → Compute resources for Cloud Run/Vertex AI

- aiplatform.googleapis.com → Vertex AI (Gemini & embeddings)

- run.googleapis.com → Deploy backend on Cloud Run

- cloudbuild.googleapis.com → Build Docker images

- artifactregistry.googleapis.com → Store Docker images

- spanner.googleapis.com → Graph database for Graph RAG

- storage.googleapis.com → Store files (images, CSVs, etc.)


## Cloud Setup (Automated with `init.sh`)

Instead of manually running all commands, you can use the included `init.sh` script to fully set up your project on Google Cloud Shell.

### Steps:

1. **Pull the latest repo**
```bash
git clone git@github.com:tubakadriye/search4cure-live.git
cd search4cure-live
```
2. **Make init.sh executable**
```
chmod +x init.sh
```
3. **Run init.sh**
```
./init.sh
```

This script automatically:

- Sets your Google Cloud project (gcloud config set project …)

- Adds the environment tag (Development)

- Enables required services (compute.googleapis.com, aiplatform.googleapis.com, etc.)

- Links your billing account

- Installs Python dependencies