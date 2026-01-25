# Hackathon Todo - Evolution from CLI to Kubernetes

**Panaversity AI-Native Development Hackathon**

## 🏆 Project Overview

A progressive todo application demonstrating the evolution from a simple console app to a cloud-native, AI-powered chatbot deployed on Kubernetes.

**Developer:** Rameez Qadir  
**GitHub:** [@rameezqadir](https://github.com/rameezqadir)

---

## 🎯 Phases Completed

### ✅ Phase I: Console Application (100 points)
- In-memory Python todo app
- Basic CRUD operations
- Spec-driven development with Claude Code

### ✅ Phase II: Full-Stack Web Application (150 points)
- Next.js frontend + FastAPI backend
- PostgreSQL database (Neon)
- RESTful API
- **Live Demo:** https://hackathon-todo-phase3.vercel.app

### ✅ Phase III: AI-Powered Chatbot (200 points)
- OpenAI integration with Function Calling
- MCP server with 5 tools
- Natural language task management
- Stateless architecture
- **Live Chat:** https://hackathon-todo-phase3.vercel.app/chat

### ✅ Phase IV: Kubernetes Deployment (250 points)
- **Current Phase**
- Docker containerization
- Minikube local deployment
- Helm charts
- High availability (2 replicas)
- Health checks & monitoring

**Total Points:** 700/1000

---

## 🚀 Live Deployments

| Component | URL | Status |
|-----------|-----|--------|
| Frontend | https://hackathon-todo-phase3.vercel.app | ✅ Live |
| Chat Interface | https://hackathon-todo-phase3.vercel.app/chat | ✅ Live |
| Backend API | https://your-backend.railway.app | ✅ Live |
| API Docs | https://your-backend.railway.app/docs | ✅ Live |

---

## 📦 Phase IV: Kubernetes Architecture
┌─────────────────────────────────────────────────────┐
│              Minikube Cluster                       │
│                                                     │
│  ┌───────────────────┐    ┌───────────────────┐   │
│  │  Frontend Pod 1   │    │  Backend Pod 1    │   │
│  │  (Next.js)        │───▶│  (FastAPI+AI)     │   │
│  └───────────────────┘    └───────────────────┘   │
│  ┌───────────────────┐    ┌───────────────────┐   │
│  │  Frontend Pod 2   │    │  Backend Pod 2    │   │
│  │  (Next.js)        │───▶│  (FastAPI+AI)     │   │
│  └───────────────────┘    └───────────────────┘   │
│           │                        │               │
│      NodePort                  ClusterIP           │
│           │                        │               │
│  ┌────────▼────────────────────────▼──────────┐   │
│  │         Ingress Controller                  │   │
│  └─────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
│
▼
External Access

### Components Deployed

- **Frontend:** 2 replicas, NodePort service
- **Backend:** 2 replicas, ClusterIP service
- **ConfigMap:** Environment variables
- **Secrets:** Database URL, OpenAI API key
- **Ingress:** Unified access point
- **Helm Chart:** Deployment management

---

## 🛠️ Technology Stack

### Phase IV Additions

| Category | Technology |
|----------|------------|
| Containerization | Docker |
| Orchestration | Kubernetes (Minikube) |
| Package Manager | Helm 3 |
| Monitoring | Kubernetes Metrics Server |
| Load Balancing | Kubernetes Service |

### Complete Stack

- **Frontend:** Next.js 14, TypeScript, Tailwind CSS
- **Backend:** FastAPI, Python 3.11
- **AI:** OpenAI GPT-4o-mini, MCP Protocol
- **Database:** Neon PostgreSQL
- **Container:** Docker
- **Orchestration:** Kubernetes
- **Deployment:** Vercel, Railway, Minikube

---

## 🚀 Quick Start - Phase IV

### Prerequisites
```bash
# Install required tools
sudo apt update
sudo apt install docker.io -y
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install kubectl /usr/local/bin/
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```

### Deploy to Minikube
```bash
# 1. Start Minikube
./start-minikube.sh

# 2. Deploy application
./deploy-app.sh

# 3. Access application
./access-app.sh

# 4. Verify deployment
./verify-deployment.sh
```

### Manual Deployment
```bash
# Start cluster
minikube start --driver=docker --cpus=4 --memory=8192

# Build images
eval $(minikube docker-env)
docker build -t todo-backend:v1.0 ./backend
docker build -t todo-frontend:v1.0 ./frontend

# Deploy with Helm
helm install todo-app ./todo-chart --namespace todo-app --create-namespace

# Get access URL
minikube service todo-frontend-service -n todo-app
```

---

## 📊 Monitoring & Management

### View Application Status
```bash
# Check all resources
kubectl get all -n todo-app

# View logs
kubectl logs -l app=todo-backend -n todo-app
kubectl logs -l app=todo-frontend -n todo-app

# Resource usage
kubectl top pods -n todo-app
```

### Scaling
```bash
# Scale backend
kubectl scale deployment todo-backend --replicas=3 -n todo-app

# Scale frontend
kubectl scale deployment todo-frontend --replicas=3 -n todo-app
```

---

## 🧪 Testing

### Test Backend Health
```bash
BACKEND_POD=$(kubectl get pods -n todo-app -l app=todo-backend -o jsonpath='{.items[0].metadata.name}')
kubectl exec -it $BACKEND_POD -n todo-app -- curl http://localhost:8000/health
```

### Test Chat Functionality
```bash
kubectl exec -it $BACKEND_POD -n todo-app -- curl -X POST http://localhost:8000/api/demo-user/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Add task: Test Kubernetes deployment"}'
```

---

## 📁 Project Structure
hackathon-todo-phase3/
├── backend/                 # FastAPI backend
│   ├── Dockerfile
│   ├── main.py
│   ├── ai_agent.py
│   ├── mcp_server.py
│   └── models.py
├── frontend/                # Next.js frontend
│   ├── Dockerfile
│   ├── app/
│   │   ├── page.tsx
│   │   └── chat/page.tsx
│   └── package.json
├── k8s/                     # Kubernetes manifests
│   ├── namespace.yaml
│   ├── configmap.yaml
│   ├── backend-deployment.yaml
│   ├── frontend-deployment.yaml
│   └── ingress.yaml
├── todo-chart/              # Helm chart
│   ├── Chart.yaml
│   ├── values.yaml
│   └── templates/
├── specs/                   # Specifications
│   └── phase4-k8s.specify
├── start-minikube.sh        # Helper scripts
├── deploy-app.sh
├── access-app.sh
├── verify-deployment.sh
└── README.md

---

## 🎥 Demo Videos

- **Phase II Demo:** [YouTube Link]
- **Phase III Demo:** [YouTube Link]
- **Phase IV Demo:** [YouTube Link]

---

## 📝 Features

### Phase IV Highlights

✅ **Containerization**
- Multi-stage Docker builds
- Optimized image sizes
- Health checks

✅ **Kubernetes Deployment**
- High availability (2 replicas)
- Auto-scaling ready
- Resource limits
- Liveness & readiness probes

✅ **Helm Integration**
- Parameterized deployments
- Easy upgrades
- Rollback capability

✅ **Monitoring**
- Metrics server enabled
- Resource usage tracking
- Log aggregation

✅ **Security**
- Secrets management
- ConfigMap for non-sensitive data
- Network policies ready

---

## 🔧 Configuration

### Environment Variables

**Backend (.env):**
```env
DATABASE_URL=postgresql://...
OPENAI_API_KEY=sk-...
ALLOWED_ORIGINS=*
```

**Kubernetes Secrets:**
```bash
kubectl create secret generic todo-secrets \
  --from-literal=DATABASE_URL='...' \
  --from-literal=OPENAI_API_KEY='...' \
  -n todo-app
```

---

## 🐛 Troubleshooting

### Pods Not Starting
```bash
kubectl describe pod <pod-name> -n todo-app
kubectl logs <pod-name> -n todo-app
```

### Service Not Accessible
```bash
kubectl get svc -n todo-app
kubectl get ingress -n todo-app
minikube service list
```

### Reset Everything
```bash
helm uninstall todo-app -n todo-app
kubectl delete namespace todo-app
minikube delete
minikube start
```

---

## 📚 Documentation

- [Phase I Documentation](./docs/phase1.md)
- [Phase II Documentation](./docs/phase2.md)
- [Phase III Documentation](./docs/phase3.md)
- [Phase IV Kubernetes Guide](./K8S-README.md)

---

## 🎓 Learning Outcomes

### Skills Demonstrated

- ✅ Spec-driven development
- ✅ Full-stack web development
- ✅ AI/ML integration
- ✅ Microservices architecture
- ✅ Container orchestration
- ✅ Kubernetes deployment
- ✅ Helm chart creation
- ✅ DevOps practices
- ✅ Cloud-native development

---

## 🏅 Hackathon Submission

**Submission Form:** https://forms.gle/KMKEKaFUD6ZX4UtY8

### Required Information

1. **GitHub Repository:** https://github.com/rameezqadir/hackathon-todo-phase3
2. **Live Application:** https://hackathon-todo-phase3.vercel.app
3. **Demo Video:** [Your 90-second video link]
4. **WhatsApp:** +92-xxx-xxxxxxx

---

## 📅 Timeline

| Phase | Due Date | Status |
|-------|----------|--------|
| Phase I | Dec 7, 2025 | ✅ Completed |
| Phase II | Dec 14, 2025 | ✅ Completed |
| Phase III | Dec 21, 2025 | ✅ Completed |
| **Phase IV** | **Jan 4, 2026** | ✅ **Completed** |
| Phase V | Jan 18, 2026 | 🔄 In Progress |

---

## 🚀 Next Steps: Phase V

Phase V will include:
- [ ] Cloud deployment (GKE/AKS/OKE)
- [ ] Kafka integration
- [ ] Dapr implementation
- [ ] Advanced features (Recurring tasks, Reminders)
- [ ] CI/CD pipeline
- [ ] Production monitoring

---

## 📄 License

MIT License

---

## 🙏 Acknowledgments

- **Panaversity** - For organizing the hackathon
- **PIAIC & GIAIC** - Educational support
- **Claude Code** - AI development assistant
- **OpenAI** - AI infrastructure

---

**Built with ❤️ for Panaversity AI-Native Development Hackathon**
