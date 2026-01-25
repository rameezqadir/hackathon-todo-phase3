#!/bin/bash
echo "🏗️  Building Docker images..."
eval $(minikube docker-env)

cd backend
docker build -t todo-backend:v1.0 .

cd ../frontend
docker build -t todo-frontend:v1.0 .

echo "📦 Deploying with Helm..."
cd ..
helm upgrade --install todo-app ./todo-chart --namespace todo-app --create-namespace

echo "⏳ Waiting for pods to be ready..."
kubectl wait --for=condition=ready pod -l app=todo-backend -n todo-app --timeout=300s
kubectl wait --for=condition=ready pod -l app=todo-frontend -n todo-app --timeout=300s

echo "✅ Deployment complete!"
kubectl get pods -n todo-app
