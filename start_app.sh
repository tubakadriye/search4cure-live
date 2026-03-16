#!/bin/bash

echo "Starting backend..."

cd backend

uvicorn api.main:app --reload --port 8000