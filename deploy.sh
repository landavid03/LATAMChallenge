#!/bin/bash

set -e

# Variables
PROJECT_ID="${PROJECT_ID:yy}"
IMAGE_NAME="user-management-api"
REGION="us-central1"
COMMIT_SHA="${COMMIT_SHA:-$(git rev-parse --short HEAD)}"
IMAGE_URI="gcr.io/$PROJECT_ID/$IMAGE_NAME:$COMMIT_SHA"
PORT=8000

# Construir la imagen
echo "🔨 Building Docker image..."
docker build -t "$IMAGE_URI" .

# Subir imagen a Container Registry
echo " Pushing image to Container Registry..."
docker push "$IMAGE_URI"

# Ejecutar tests
echo " Running tests..."
docker run --rm -e DATABASE_URL="$DATABASE_URL" -e LOG_LEVEL="DEBUG" "$IMAGE_URI" python -m pytest -v

# Desplegar en Cloud Run
echo " Deploying to Cloud Run..."
gcloud run deploy "$IMAGE_NAME" \
  --image="$IMAGE_URI" \
  --region="$REGION" \
  --platform=managed \
  --allow-unauthenticated \
  --memory=512Mi \
  --cpu=1 \
  --min-instances=0 \
  --max-instances=10 \
  --port=$PORT \
  --set-env-vars="DATABASE_URL=$DATABASE_URL,LOG_LEVEL=INFO"

echo " Deployment complete."
