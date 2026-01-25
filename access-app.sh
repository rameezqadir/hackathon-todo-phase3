#!/bin/bash
MINIKUBE_IP=$(minikube ip)
FRONTEND_PORT=$(kubectl get svc todo-frontend-service -n todo-app -o jsonpath='{.spec.ports[0].nodePort}')

echo "🌐 Application Access URLs:"
echo "   Frontend: http://$MINIKUBE_IP:$FRONTEND_PORT"
echo "   Chat: http://$MINIKUBE_IP:$FRONTEND_PORT/chat"
echo ""
echo "📊 Or use port-forward:"
echo "   kubectl port-forward svc/todo-frontend-service 3000:3000 -n todo-app"
