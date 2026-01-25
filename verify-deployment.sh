#!/bin/bash

echo "🔍 Phase IV Deployment Verification"
echo "===================================="

echo ""
echo "1️⃣  Checking Minikube status..."
minikube status

echo ""
echo "2️⃣  Checking namespace..."
kubectl get namespace todo-app

echo ""
echo "3️⃣  Checking deployments..."
kubectl get deployments -n todo-app

echo ""
echo "4️⃣  Checking pods..."
kubectl get pods -n todo-app

echo ""
echo "5️⃣  Checking services..."
kubectl get svc -n todo-app

echo ""
echo "6️⃣  Checking ingress..."
kubectl get ingress -n todo-app

echo ""
echo "7️⃣  Checking Helm release..."
helm list -n todo-app

echo ""
echo "8️⃣  Testing backend health..."
BACKEND_POD=$(kubectl get pods -n todo-app -l app=todo-backend -o jsonpath='{.items[0].metadata.name}')
kubectl exec -it $BACKEND_POD -n todo-app -- curl -s http://localhost:8000/health

echo ""
echo "9️⃣  Application URLs:"
MINIKUBE_IP=$(minikube ip)
FRONTEND_PORT=$(kubectl get svc todo-frontend-service -n todo-app -o jsonpath='{.spec.ports[0].nodePort}')
echo "   Frontend: http://$MINIKUBE_IP:$FRONTEND_PORT"
echo "   Chat: http://$MINIKUBE_IP:$FRONTEND_PORT/chat"

echo ""
echo "✅ Verification complete!"
