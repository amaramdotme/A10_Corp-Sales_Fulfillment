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

# Apply manifests
echo "Applying manifests..."
kubectl apply -f infra/k8s/namespace.yaml
kubectl apply -f infra/k8s/backend/k8s-manifests.yaml
kubectl apply -f infra/k8s/frontend/k8s-manifests.yaml

echo "Waiting for deployments..."
kubectl rollout status deployment/backend -n sales-fulfillment
kubectl rollout status deployment/frontend -n sales-fulfillment

echo "Done! You can access the app by port-forwarding:"
echo "kubectl port-forward svc/frontend 5003:80 -n sales-fulfillment"
