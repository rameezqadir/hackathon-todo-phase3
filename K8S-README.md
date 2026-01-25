# Phase IV: Kubernetes Deployment

## Architecture
┌─────────────────────────────────────────────┐
│         Minikube Cluster                    │
│                                             │
│  ┌──────────────┐    ┌──────────────┐      │
│  │   Frontend   │    │   Backend    │      │
│  │   (2 pods)   │───▶│   (2 pods)   │      │
│  │  NodePort    │    │  ClusterIP   │      │
│  └──────────────┘    └──────────────┘      │
│         │                    │              │
│         │                    │              │
│    ┌────▼────────────────────▼────┐        │
│    │       Ingress Controller     │        │
│    └─────────────────────────────┘        │
└─────────────────────────────────────────────┘
│
▼
External Access

## Quick Start
```bash
# 1. Start cluster
./start-minikube.sh

# 2. Deploy application
./deploy-app.sh

# 3. Access application
./access-app.sh

# 4. Stop cluster
./stop-minikube.sh
```

## Manual Commands

### Start Minikube
```bash
minikube start --driver=docker
```

### Build Images
```bash
eval $(minikube docker-env)
cd backend && docker build -t todo-backend:v1.0 .
cd frontend && docker build -t todo-frontend:v1.0 .
```

### Deploy with Helm
```bash
helm install todo-app ./todo-chart --namespace todo-app --create-namespace
```

### Access Application
```bash
minikube service todo-frontend-service -n todo-app
```

## Monitoring

### View Pods
```bash
kubectl get pods -n todo-app
kubectl logs -f <pod-name> -n todo-app
```

### View Services
```bash
kubectl get svc -n todo-app
```

### Resource Usage
```bash
kubectl top pods -n todo-app
```

## Troubleshooting

### Pods Not Starting
```bash
kubectl describe pod <pod-name> -n todo-app
kubectl logs <pod-name> -n todo-app
```

### Reset Everything
```bash
helm uninstall todo-app -n todo-app
kubectl delete namespace todo-app
minikube delete
minikube start
```

## Scaling

### Scale Backend
```bash
kubectl scale deployment todo-backend --replicas=3 -n todo-app
```

### Scale Frontend
```bash
kubectl scale deployment todo-frontend --replicas=3 -n todo-app
```

## Update Deployment
```bash
# Rebuild images
eval $(minikube docker-env)
docker build -t todo-backend:v1.1 ./backend
docker build -t todo-frontend:v1.1 ./frontend

# Update Helm
helm upgrade todo-app ./todo-chart --namespace todo-app
```
