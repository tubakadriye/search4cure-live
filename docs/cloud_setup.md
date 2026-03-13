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
One time only.
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

| Service                         | Purpose                         |
| ------------------------------- | ------------------------------- |
| compute.googleapis.com          | Compute resources               |
| aiplatform.googleapis.com       | Vertex AI (Gemini + embeddings) |
| run.googleapis.com              | Cloud Run deployment            |
| cloudbuild.googleapis.com       | Container builds                |
| artifactregistry.googleapis.com | Docker storage                  |
| spanner.googleapis.com          | Graph database                  |
| storage.googleapis.com          | File storage                    |



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

## Initialize the Graph Database

After the setup completes, initialize the **Diabetes Research Graph**.

```bash
python backend/setup_data.py --project=$PROJECT_ID --force
```

This command will:

- Create the Cloud Spanner instance

- Create the database

- Build the property graph schema

- Insert sample research data

## Backend Virtual Environment Setup

**Option 1 — Activate .venv manually:**

```
bash
cd ~/search4cure-live/backend
source .venv/bin/activate   # Linux / Cloud Shell
python ../scripts/setup_data.py --force
```




**Option 2 — Use uv run (auto-uses .venv):**

```
cd ~/search4cure-live/backend
uv run python ../scripts/setup_data.py
```

The output will be:

![Output](../data/images/graph_created_output.png)

**Tip:** Always run from inside .venv or using uv run to ensure dependencies (like python-dotenv) are correctly loaded.



[def]: ../data/images/graph_created_output.png