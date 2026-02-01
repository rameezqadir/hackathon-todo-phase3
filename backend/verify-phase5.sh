#!/bin/bash

echo "🔍 Phase V Verification"
echo "======================="

# Check Minikube
echo "☸️  Checking Minikube..."
if minikube status | grep -q "Running"; then
    echo "✅ Minikube is running"
else
    echo "❌ Minikube is not running"
fi

# Check Kafka in Minikube
echo "📦 Checking Kafka in Minikube..."
if kubectl get pods -n kafka 2>/dev/null | grep -q "todo-kafka.*Running"; then
    echo "✅ Kafka is running in Minikube"
    
    # Check topics
    echo "📊 Checking Kafka Topics..."
    TOPICS=$(kubectl exec -n kafka -it todo-kafka -- /opt/kafka/bin/kafka-topics.sh \
      --bootstrap-server localhost:9092 \
      --list 2>/dev/null)
    
    if [ $? -eq 0 ]; then
        echo "✅ Kafka topics:"
        echo "$TOPICS"
    else
        echo "❌ Cannot list Kafka topics"
    fi
else
    echo "❌ Kafka is not running in Minikube"
fi

# Check Dapr
echo "🔷 Checking Dapr..."
if kubectl get pods -n dapr-system 2>/dev/null | grep -q "Running"; then
    echo "✅ Dapr is installed"
else
    echo "❌ Dapr is not installed"
fi

# Check Application
echo "🚀 Checking Application..."
if kubectl get pods -n todo-app 2>/dev/null | grep -q "Running"; then
    echo "✅ Application is deployed"
    kubectl get pods -n todo-app
else
    echo "❌ Application is not deployed"
fi

# Check port-forward
echo "🔗 Checking Kafka port-forward..."
if netstat -tuln 2>/dev/null | grep -q ":9092"; then
    echo "✅ Kafka port-forward active (localhost:9092)"
else
    echo "⚠️  Kafka not port-forwarded to localhost:9092"
fi

echo ""
echo "🎯 Summary:"
echo "- Kafka: localhost:9092 (from Minikube)"
echo "- Minikube Dashboard: minikube dashboard"
echo "- Application: kubectl get svc -n todo-app"
echo "- Dapr: kubectl get pods -n dapr-system"
echo ""
echo "🔧 Quick fixes:"
echo "  If Kafka not port-forwarded: kubectl port-forward svc/todo-kafka -n kafka 9092:9092"
echo "  If app not deployed: kubectl apply -f k8s/ -n todo-app"
