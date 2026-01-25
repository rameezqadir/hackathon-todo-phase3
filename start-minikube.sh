#!/bin/bash
echo "🚀 Starting Minikube cluster..."
minikube start --driver=docker --cpus=4 --memory=8192
echo "✅ Minikube started"

echo "🔧 Enabling addons..."
minikube addons enable ingress
minikube addons enable metrics-server
echo "✅ Addons enabled"

echo "📊 Cluster info:"
kubectl cluster-info
kubectl get nodes
