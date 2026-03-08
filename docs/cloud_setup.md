# Google Cloud Project Setup for Search4Cure Diabetes

## Project
- Project ID: `search4cure-diabetes`
- Environment tag: `Development`

## Commands Run

### 1. Set the project
```bash
gcloud config set project search4cure-diabetes --quiet 
```


### 2. Enable required services
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


### 3. Clone the Repository
```
bash
git clone https://github.com/tubakadriye/search4cure-live.git
cd search4cure-live
```

If the repo already exists:

```
bash
cd search4cure-live
git pull
```

### 4. Automated Cloud Setup Script

Instead of manually configuring everything, run the included setup script.

**Make the script executable**

```
bash
chmod +x scripts/setup.sh
```

**Run the setup script**
```
bash
./scripts/setup.sh
```

### 5. Example Output

Running the script should produce something similar to this:

```
--- Setting Google Cloud Environment Variables ---
Checking gcloud authentication status...
gcloud is authenticated.

Setting gcloud project to: search4cure-diabetes
Updated property [core/project].

PROJECT_ID=search4cure-diabetes
PROJECT_NUMBER=941266239729
SERVICE_ACCOUNT_NAME=941266239729-compute@developer.gserviceaccount.com

Vertex AI enabled

--- Configuring Storage Bucket ---
Creating bucket...
Creating gs://search4cure-diabetes-search4cure-data/...

Storage bucket ready

--- Configuring Spanner Graph ---
INSTANCE_ID=diabetes-research-network
DATABASE_ID=research-graph-db
GRAPH_NAME=DiabetesResearchGraph

--- Creating .env file ---
.env file created

```

### 6. Resources Created by the Script

The setup script automatically creates and configures the following resources.

### Environment Variables

- `PROJECT_ID`
- `PROJECT_NUMBER`
- `SERVICE_ACCOUNT_NAME`
- `REGION`
- `GOOGLE_CLOUD_LOCATION`

### Storage

**Google Cloud Storage Bucket**
    gs://search4cure-diabetes-search4cure-data


### Spanner Graph Configuration

```
INSTANCE_ID=diabetes-research-network
DATABASE_ID=research-graph-db
GRAPH_NAME=DiabetesResearchGraph
```

### `.env` File

The script automatically generates a `.env` file containing all required configuration variables for the project.

---

### 7. Next Step: Initialize the Graph Database

After the setup completes, initialize the **Diabetes Research Graph**.

```bash
python backend/setup_graph.py --project=$PROJECT_ID --force
```

This command will:

- Create the Cloud Spanner instance

- Create the database

- Build the property graph schema

- Insert sample research data

### 8. Final Architecture After Setup

After initialization, the Search4Cure system architecture will look like this:

User
 │
 ▼
Streamlit UI
 │
 ▼
Cloud Run API
 │
 ▼
Agent Orchestrator (ADK)
 │
 ▼
Graph RAG
 ├ Spanner Graph (research relationships)
 └ Vector embeddings
 │
 ▼
Gemini (Vertex AI)




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