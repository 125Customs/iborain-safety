#!/usr/bin/env bash
# Deploy the broker to Cloud Run. Run from the monorepo root.
# ASSUMPTION: region us-central1; edit below. Requires: gcloud auth login + a project set.
set -euo pipefail

PROJECT="${GCP_PROJECT:?set GCP_PROJECT}"
REGION="${GCP_REGION:-us-central1}"
SERVICE="pixel-bot-broker"

gcloud builds submit --project "$PROJECT" --tag "gcr.io/$PROJECT/$SERVICE" .

# WebSockets on Cloud Run: session affinity ON, long request timeout,
# min-instances=1 so the in-process session Map + cold-start latency
# never bites during a demo.
gcloud run deploy "$SERVICE" \
  --project "$PROJECT" \
  --region "$REGION" \
  --image "gcr.io/$PROJECT/$SERVICE" \
  --min-instances=1 \
  --max-instances=2 \
  --session-affinity \
  --timeout=3600 \
  --memory=512Mi \
  --allow-unauthenticated \
  --set-env-vars "MODE=${MODE:-echo},GEMINI_MODEL=${GEMINI_MODEL:-gemini-2.5-flash-native-audio-preview-12-2025}" \
  --set-secrets "GEMINI_API_KEY=pixel-gemini-api-key:latest,DEVICE_TOKENS=pixel-device-tokens:latest"

# SCALE-SEAM: multi-region deploys + global LB when latency-sensitive users
# exist outside one region.
echo "Deployed. wss URL: $(gcloud run services describe "$SERVICE" --project "$PROJECT" --region "$REGION" --format 'value(status.url)' | sed 's/^https/wss/')"
