#!/bin/bash

# Docker Quick Start Script for WorkOS Full-Stack Application

echo "🐳 Starting WorkOS Full-Stack Application with Docker..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}❌ Docker is not running. Please start Docker first.${NC}"
    exit 1
fi

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ docker-compose is not installed. Please install Docker Compose.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Docker is running${NC}"

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  Creating .env file from template...${NC}"
    cp .env.docker .env
    echo -e "${YELLOW}📝 Please edit .env with your WorkOS credentials before continuing.${NC}"
    echo -e "${BLUE}   Required variables:${NC}"
    echo "   - WORKOS_API_KEY=sk_your_api_key"
    echo "   - WORKOS_CLIENT_ID=client_your_client_id"
    echo ""
    read -p "Press Enter when you've updated the .env file..."
fi

echo -e "${BLUE}🏗️  Building and starting services...${NC}"

# Build and start services
docker-compose up --build -d

# Wait a moment for services to start
sleep 3

echo ""
echo -e "${GREEN}🎉 Application started successfully!${NC}"
echo ""
echo -e "${BLUE}📱 Access your application:${NC}"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000/api"
echo "   Database: localhost:5432 (postgres/postgres)"
echo ""
echo -e "${BLUE}🔧 Useful commands:${NC}"
echo "   View logs: docker-compose logs -f"
echo "   Stop services: docker-compose down"
echo "   Backend shell: docker-compose exec backend python manage.py shell"
echo "   Database shell: docker-compose exec db psql -U postgres workos_fullstack"
echo ""
echo -e "${YELLOW}📖 See DOCKER.md for detailed documentation${NC}"

# Check if services are healthy
echo -e "${BLUE}🔍 Checking service status...${NC}"
sleep 5

if curl -f http://localhost:3000 > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Frontend is running${NC}"
else
    echo -e "${YELLOW}⚠️  Frontend may still be starting...${NC}"
fi

if curl -f http://localhost:8000/api/hello 2>/dev/null | grep -q "Hello"; then
    echo -e "${GREEN}✅ Backend is running${NC}"
else
    echo -e "${YELLOW}⚠️  Backend may still be starting or needs authentication...${NC}"
fi

echo ""
echo -e "${GREEN}🚀 Ready to go! Open http://localhost:3000 in your browser.${NC}"