#!/bin/bash

echo "🚀 Starting Phase V Environment with Minikube"

# Stop Docker Kafka if running (to free port 9092)
echo "📦 Stopping Docker Kafka (if running)..."
docker-compose -f docker-compose.kafka.yml down 2>/dev/null || true

# Start Minikube
echo "☸️  Starting Minikube..."
minikube start --driver=docker --cpus=4 --memory=8192
minikube addons enable ingress

# Setup Kafka in Minikube
echo "📦 Setting up Kafka in Minikube..."
kubectl create namespace kafka 2>/dev/null || true

# Deploy Kafka if not already running
if ! kubectl get pod todo-kafka -n kafka 2>/dev/null | grep -q "Running"; then
    kubectl apply -n kafka -f - <<'KAFKA_YAML'
apiVersion: v1
kind: Pod
metadata:
  name: todo-kafka
  namespace: kafka
spec:
  containers:
  - name: kafka
    image: apache/kafka:3.7.0
    command:
    - /bin/sh
    - -c
    - |
      # Generate cluster ID
      KAFKA_CLUSTER_ID=\$(/opt/kafka/bin/kafka-storage.sh random-uuid)
      
      # Create config
      cat > /tmp/kafka.properties <<EOL
      process.roles=broker,controller
      node.id=1
      controller.quorum.voters=1@localhost:9093
      listeners=PLAINTEXT://:9092,CONTROLLER://:9093
      advertised.listeners=PLAINTEXT://todo-kafka:9092
      controller.listener.names=CONTROLLER
      inter.broker.listener.name=PLAINTEXT
      num.partitions=3
      offsets.topic.replication.factor=1
      transaction.state.log.replication.factor=1
      EOL
      
      # Format and start
      /opt/kafka/bin/kafka-storage.sh format -t \$KAFKA_CLUSTER_ID -c /tmp/kafka.properties
      exec /opt/kafka/bin/kafka-server-start.sh /tmp/kafka.properties
    ports:
    - containerPort: 9092
    - containerPort: 9093
---
apiVersion: v1
kind: Service
metadata:
  name: todo-kafka
  namespace: kafka
spec:
  selector:
    app: todo-kafka
  ports:
  - port: 9092
    targetPort: 9092
  - port: 9093
    targetPort: 9093
KAFKA_YAML

    echo "⏳ Waiting for Kafka to start..."
    sleep 15
    kubectl wait --for=condition=Ready pod/todo-kafka -n kafka --timeout=120s
fi

echo "✅ Kafka ready in Minikube"

# Create Kafka topics for Phase V
echo "📊 Creating Phase V Kafka topics..."
kubectl exec -n kafka -it todo-kafka -- /opt/kafka/bin/kafka-topics.sh \
  --bootstrap-server localhost:9092 \
  --create \
  --topic reminders \
  --partitions 1 \
  --replication-factor 1 2>/dev/null || echo "Reminders topic exists"

kubectl exec -n kafka -it todo-kafka -- /opt/kafka/bin/kafka-topics.sh \
  --bootstrap-server localhost:9092 \
  --create \
  --topic task-events \
  --partitions 3 \
  --replication-factor 1 2>/dev/null || echo "Task events topic exists"

kubectl exec -n kafka -it todo-kafka -- /opt/kafka/bin/kafka-topics.sh \
  --bootstrap-server localhost:9092 \
  --create \
  --todo recurring-tasks \
  --partitions 1 \
  --replication-factor 1 2>/dev/null || echo "Recurring tasks topic exists"

# Install Dapr
echo "🔷 Installing Dapr..."
dapr init --kubernetes --wait

# Deploy application
echo "🚀 Deploying application..."
kubectl create namespace todo-app 2>/dev/null || true

# Check if k8s/ directory exists
if [ -d "k8s" ]; then
    kubectl apply -f k8s/ -n todo-app
else
    echo "⚠️ k8s/ directory not found, deploying sample app..."
    
    # Create sample deployment
    kubectl apply -n todo-app -f - <<'SAMPLE_YAML'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: todo-backend
  labels:
    app: todo-backend
spec:
  replicas: 1
  selector:
    matchLabels:
      app: todo-backend
  template:
    metadata:
      labels:
        app: todo-backend
      annotations:
        dapr.io/enabled: "true"
        dapr.io/app-id: "todo-backend"
        dapr.io/app-port: "8000"
    spec:
      containers:
      - name: backend
        image: python:3.9-slim
        command: ["sh", "-c"]
        args:
        - |
          pip install fastapi uvicorn kafka-python
          cat > app.py <<'EOF'
          from fastapi import FastAPI
          app = FastAPI()
          @app.get("/health")
          def health(): return {"status": "ok", "phase": "V"}
          EOF
          uvicorn app:app --host 0.0.0.0 --port 8000
        ports:
        - containerPort: 8000
---
apiVersion: v1
kind: Service
metadata:
  name: todo-backend-service
spec:
  selector:
    app: todo-backend
  ports:
  - port: 8000
    targetPort: 8000
SAMPLE_YAML
fi

# Port-forward Kafka for local access
echo "🔗 Port-forwarding Kafka to localhost:9092..."
pkill -f "kubectl port-forward.*kafka.*9092" 2>/dev/null || true
kubectl port-forward svc/todo-kafka -n kafka 9092:9092 > /dev/null 2>&1 &
sleep 2

# Start Kafka consumers (if they exist)
echo "👂 Starting Kafka consumers..."
if [ -f "backend/recurring_task_consumer.py" ]; then
    cd backend
    source venv/bin/activate 2>/dev/null || echo "Using system Python"
    python recurring_task_consumer.py &
    CONSUMER1_PID=$!
    echo "✅ Recurring task consumer started (PID: $CONSUMER1_PID)"
    
    if [ -f "reminder_consumer.py" ]; then
        python reminder_consumer.py &
        CONSUMER2_PID=$!
        echo "✅ Reminder consumer started (PID: $CONSUMER2_PID)"
    fi
    cd ..
else
    echo "⚠️ Consumer scripts not found in backend/"
fi

echo ""
echo "✅ Phase V environment ready!"
echo "📊 Kafka: localhost:9092 (from Minikube)"
echo "☸️  Minikube Dashboard: minikube dashboard"
echo "🌐 App Services: kubectl get svc -n todo-app"
echo ""
echo "To test Kafka:"
echo "  kubectl exec -n kafka -it todo-kafka -- /opt/kafka/bin/kafka-topics.sh --list --bootstrap-server localhost:9092"
echo ""
echo "To test API (after deploying):"
echo "  kubectl port-forward svc/todo-backend-service -n todo-app 8000:8000"
echo "  curl http://localhost:8000/health"
