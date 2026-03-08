#!/bin/bash

# --- Error handler ---
handle_error() {
    echo -e "\nError: $1"
    exit 1
}

PROJECT_FILE="$HOME/project_id.txt"

# 1. Use existing project if available
if [ -s "$PROJECT_FILE" ]; then
    FINAL_PROJECT_ID=$(cat "$PROJECT_FILE" | tr -d '[:space:]')
    echo "Using saved project: $FINAL_PROJECT_ID"
    gcloud config set project "$FINAL_PROJECT_ID" || handle_error "Cannot set project"
else
    FINAL_PROJECT_ID="search4cure-diabetes"
    echo "Setting project to: $FINAL_PROJECT_ID"
    gcloud config set project "$FINAL_PROJECT_ID" || handle_error "Cannot set project"
    echo "$FINAL_PROJECT_ID" > "$PROJECT_FILE"
fi

# 2. Set environment tag
gcloud resource-manager tags bindings create \
    --parent=projects/$FINAL_PROJECT_ID \
    --tag-key=environment \
    --tag-value=Development || echo "Environment tag may already exist"

# 3. Link billing account
gcloud beta billing projects link $FINAL_PROJECT_ID --billing-account=YOUR_BILLING_ACCOUNT_ID || handle_error "Billing not linked"

# 4. Enable services
gcloud services enable \
    compute.googleapis.com \
    aiplatform.googleapis.com \
    run.googleapis.com \
    cloudbuild.googleapis.com \
    artifactregistry.googleapis.com \
    spanner.googleapis.com \
    storage.googleapis.com || handle_error "Failed to enable services"

# 5. Install Python dependencies
pip install --upgrade -r requirements.txt || handle_error "Failed to install dependencies"

echo "✅ Search4Cure Diabetes project initialized!"
exit 0
