#!/bin/bash
set -e

CLUSTER_NAME="a10-corp"

# Create cluster
if ! kind get clusters | grep -q "$CLUSTER_NAME"; then
  echo "Creating kind cluster..."
  kind create cluster --name "$CLUSTER_NAME" --config deploy/local/kind-config.yaml
else
  echo "Cluster $CLUSTER_NAME already exists."
fi

# Build images
echo "Building images..."
docker build -t a10-backend:latest src/backend
docker build -t a10-frontend:latest src/frontend

# Load images into kind
echo "Loading images into kind..."
kind load docker-image a10-backend:latest --name "$CLUSTER_NAME"
kind load docker-image a10-frontend:latest --name "$CLUSTER_NAME"

# Install with Helm
echo "Installing application with Helm..."
# Use upgrade --install for idempotency
helm upgrade --install sales-fulfillment-app charts/sales-fulfillment \
  --create-namespace \
  --namespace sales-fulfillment \
  --wait

echo "Done! You can access the app by port-forwarding:"
echo "kubectl port-forward svc/frontend 7004:80 -n sales-fulfillment"
