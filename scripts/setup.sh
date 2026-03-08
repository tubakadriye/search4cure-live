#!/bin/bash

# -------------------------------
# Search4Cure Live Initialization
# -------------------------------

# --- Configuration ---
PROJECT_FILE="~/project_id.txt"
export REPO_NAME="search4cure-live"
# ---------------------

# --- Spanner Graph Configuration ---
INSTANCE_ID="diabetes-research-network"
DATABASE_ID="research-graph-db"
GRAPH_NAME="DiabetesResearchGraph"
# -----------------------------------

echo "--- Setting Google Cloud Environment Variables ---"

# --- Authentication Check ---
echo "Checking gcloud authentication status..."

if gcloud auth print-access-token > /dev/null 2>&1; then
    echo "gcloud is authenticated."
else
    echo "Error: gcloud is not authenticated."
    echo "Please run: gcloud auth login"
    exit 1
fi

# --- Load Project ID ---
PROJECT_FILE_PATH=$(eval echo $PROJECT_FILE)

if [ ! -f "$PROJECT_FILE_PATH" ]; then
    echo "Error: Project file not found at $PROJECT_FILE_PATH"
    echo "Create it with:"
    echo "echo YOUR_PROJECT_ID > ~/project_id.txt"
    exit 1
fi

PROJECT_ID_FROM_FILE=$(cat "$PROJECT_FILE_PATH")

echo "Setting gcloud project to: $PROJECT_ID_FROM_FILE"
gcloud config set project "$PROJECT_ID_FROM_FILE" --quiet

# --- Export Variables ---

export PROJECT_ID=$(gcloud config get project)
echo "PROJECT_ID=$PROJECT_ID"

export PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format="value(projectNumber)")
echo "PROJECT_NUMBER=$PROJECT_NUMBER"

export SERVICE_ACCOUNT_NAME=$(gcloud compute project-info describe --format="value(defaultServiceAccount)")
echo "SERVICE_ACCOUNT_NAME=$SERVICE_ACCOUNT_NAME"

export GOOGLE_CLOUD_PROJECT="$PROJECT_ID"

# --- Vertex AI ---
export GOOGLE_GENAI_USE_VERTEXAI="TRUE"
export REGION="us-central1"
export GOOGLE_CLOUD_LOCATION="$REGION"

echo "Vertex AI enabled"

# ---------------------------
# Google Cloud Storage Bucket
# ---------------------------

echo "--- Configuring Storage Bucket ---"

export BUCKET_NAME="${PROJECT_ID}-search4cure-data"

if gsutil ls -b "gs://$BUCKET_NAME" > /dev/null 2>&1; then
    echo "Bucket already exists."
else
    echo "Creating bucket..."

    gcloud storage buckets create "gs://$BUCKET_NAME" \
        --project="$PROJECT_ID" \
        --location="$REGION" \
        --uniform-bucket-level-access \
        --quiet
fi

export GOOGLE_CLOUD_BUCKET="gs://$BUCKET_NAME"
export GCS_BUCKET_NAME="$BUCKET_NAME"

echo "Storage bucket ready"

# ---------------------------
# Spanner Graph Configuration
# ---------------------------

echo "--- Configuring Spanner Graph ---"

export INSTANCE_ID="$INSTANCE_ID"
export DATABASE_ID="$DATABASE_ID"
export GRAPH_NAME="$GRAPH_NAME"

echo "INSTANCE_ID=$INSTANCE_ID"
echo "DATABASE_ID=$DATABASE_ID"
echo "GRAPH_NAME=$GRAPH_NAME"

# ---------------------------
# Write Environment File
# ---------------------------

echo "--- Creating .env file ---"

cat <<EOF > .env
PROJECT_ID=$PROJECT_ID
PROJECT_NUMBER=$PROJECT_NUMBER
SERVICE_ACCOUNT_NAME=$SERVICE_ACCOUNT_NAME

GOOGLE_CLOUD_PROJECT=$GOOGLE_CLOUD_PROJECT
GOOGLE_GENAI_USE_VERTEXAI=$GOOGLE_GENAI_USE_VERTEXAI

REGION=$REGION
GOOGLE_CLOUD_LOCATION=$GOOGLE_CLOUD_LOCATION

BUCKET_NAME=$BUCKET_NAME
GOOGLE_CLOUD_BUCKET=$GOOGLE_CLOUD_BUCKET
GCS_BUCKET_NAME=$GCS_BUCKET_NAME

INSTANCE_ID=$INSTANCE_ID
DATABASE_ID=$DATABASE_ID
GRAPH_NAME=$GRAPH_NAME

# Vertex AI Models
EMBEDDING_MODEL=text-embedding-004
GEMINI_MODEL=gemini-1.5-pro

# Optional features
USE_MEMORY_BANK=false
EOF

echo ".env file created"

echo ""
echo "------------------------------------"
echo "Search4Cure environment ready 🚀"
echo "------------------------------------"
