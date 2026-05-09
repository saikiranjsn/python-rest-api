#!/bin/bash

# Flask API Load Testing Setup Script
# This script sets up the complete CNCF monitoring stack for load testing

echo "🚀 Starting Flask API Load Testing Environment..."
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Build and start all services
echo "📦 Building and starting services..."
docker compose up -d --build

# Wait for services to be healthy
echo "⏳ Waiting for services to start..."
sleep 10

# Check if services are running
echo "🔍 Checking service status..."
docker compose ps

echo ""
echo "✅ Services started successfully!"
echo ""
echo "🌐 Access URLs:"
echo "   Flask API:     http://localhost:5000"
echo "   Grafana:       http://localhost:3000 (admin/admin)"
echo "   Prometheus:    http://localhost:9090"
echo "   Locust:        http://localhost:8089"
echo ""
echo "📊 Load Testing Instructions:"
echo "1. Open Locust UI: http://localhost:8089"
echo "2. Set Number of users: 10 (start small)"
echo "3. Set Spawn rate: 1 user/second"
echo "4. Set Host: http://flask-app:5000"
echo "5. Click 'Start swarming'"
echo ""
echo "📈 Monitoring:"
echo "1. Open Grafana: http://localhost:3000"
echo "2. View the 'Flask API Load Testing Dashboard'"
echo "3. Watch CPU, Memory, and Response Times in real-time"
echo ""
echo "🛑 To stop: docker compose down"
echo "🧹 To cleanup: docker compose down -v"