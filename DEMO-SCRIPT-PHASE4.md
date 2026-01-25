# Phase IV Demo Video Script (90 seconds)

## Setup (Before Recording)
- Minikube running with application deployed
- Terminal ready with commands
- Browser open to application URL

---

## Script (90 seconds)

### Introduction (10 seconds)
"Hi, I'm Rameez Qadir. This is my Phase IV submission - deploying the AI-powered todo chatbot to Kubernetes using Minikube and Helm."

### Show Kubernetes Cluster (20 seconds)
```bash
# Show running cluster
kubectl get nodes

# Show deployed applications
kubectl get all -n todo-app

# Show 2 replicas of each service
kubectl get pods -n todo-app
```

**Say:** "I have a Minikube cluster with 2 replicas each of frontend and backend for high availability."

### Show Helm Deployment (15 seconds)
```bash
# Show Helm release
helm list -n todo-app

# Show Helm chart structure
tree todo-chart/
```

**Say:** "The application is deployed using Helm for easy management and updates."

### Access Application (20 seconds)
```bash
# Get URL
minikube service todo-frontend-service -n todo-app --url
```

**Open browser and navigate to the URL**

**Say:** "Here's the application running on Kubernetes. Let me test the chat functionality."

### Demonstrate AI Chat (20 seconds)
**In browser:**
1. Click "AI Assistant"
2. Type: "Add task: Complete Phase IV deployment"
3. Show AI response
4. Type: "What's on my list?"
5. Show tasks displayed

**Say:** "The AI chatbot is fully functional, managing tasks through natural language."

### Show Monitoring (5 seconds)
```bash
kubectl top pods -n todo-app
```

**Say:** "Resource usage is monitored in real-time."

### Conclusion (5 seconds)
**Say:** "Phase IV complete - containerized, orchestrated, and production-ready. Thank you!"

---

## Recording Tips

1. **Practice first** - Do a dry run
2. **Keep it moving** - Don't pause
3. **Show, don't explain too much**
4. **Focus on working features**
5. **End exactly at 90 seconds**

## Tools to Record

- **OBS Studio:** `obs` (in WSL with X server)
- **SimpleScreenRecorder**
- **Loom:** https://www.loom.com (easiest)
- **Windows Game Bar:** Win+G

## After Recording

1. Upload to YouTube (Unlisted)
2. Or upload to Google Drive (Public link)
3. Video should be under 90 seconds
4. Verify link works before submitting
ENDOFFILEcat > DEMO-SCRIPT-PHASE4.md << 'ENDOFFILE'
# Phase IV Demo Video Script (90 seconds)

## Setup (Before Recording)
- Minikube running with application deployed
- Terminal ready with commands
- Browser open to application URL

---

## Script (90 seconds)

### Introduction (10 seconds)
"Hi, I'm Rameez Qadir. This is my Phase IV submission - deploying the AI-powered todo chatbot to Kubernetes using Minikube and Helm."

### Show Kubernetes Cluster (20 seconds)
```bash
# Show running cluster
kubectl get nodes

# Show deployed applications
kubectl get all -n todo-app

# Show 2 replicas of each service
kubectl get pods -n todo-app
```

**Say:** "I have a Minikube cluster with 2 replicas each of frontend and backend for high availability."

### Show Helm Deployment (15 seconds)
```bash
# Show Helm release
helm list -n todo-app

# Show Helm chart structure
tree todo-chart/
```

**Say:** "The application is deployed using Helm for easy management and updates."

### Access Application (20 seconds)
```bash
# Get URL
minikube service todo-frontend-service -n todo-app --url
```

**Open browser and navigate to the URL**

**Say:** "Here's the application running on Kubernetes. Let me test the chat functionality."

### Demonstrate AI Chat (20 seconds)
**In browser:**
1. Click "AI Assistant"
2. Type: "Add task: Complete Phase IV deployment"
3. Show AI response
4. Type: "What's on my list?"
5. Show tasks displayed

**Say:** "The AI chatbot is fully functional, managing tasks through natural language."

### Show Monitoring (5 seconds)
```bash
kubectl top pods -n todo-app
```

**Say:** "Resource usage is monitored in real-time."

### Conclusion (5 seconds)
**Say:** "Phase IV complete - containerized, orchestrated, and production-ready. Thank you!"

---

## Recording Tips

1. **Practice first** - Do a dry run
2. **Keep it moving** - Don't pause
3. **Show, don't explain too much**
4. **Focus on working features**
5. **End exactly at 90 seconds**

## Tools to Record

- **OBS Studio:** `obs` (in WSL with X server)
- **SimpleScreenRecorder**
- **Loom:** https://www.loom.com (easiest)
- **Windows Game Bar:** Win+G

## After Recording

1. Upload to YouTube (Unlisted)
2. Or upload to Google Drive (Public link)
3. Video should be under 90 seconds
4. Verify link works before submitting
