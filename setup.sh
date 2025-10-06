#!/bin/bash

# WorkOS Full-Stack Application Setup Script

echo "🚀 Setting up WorkOS Full-Stack Application..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed. Please install Python 3.8+ first.${NC}"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js is not installed. Please install Node.js 16+ first.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Prerequisites check passed${NC}"

# Setup backend
echo -e "${YELLOW}📦 Setting up backend...${NC}"
cd backend

# Create virtual environment
python3 -m venv .venv
echo -e "${GREEN}✅ Virtual environment created${NC}"

# Activate virtual environment
source .venv/bin/activate
echo -e "${GREEN}✅ Virtual environment activated${NC}"

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt
echo -e "${GREEN}✅ Python dependencies installed${NC}"

# Copy environment template
if [ ! -f .env ]; then
    cp .env.example .env
    echo -e "${YELLOW}⚠️  Please edit backend/.env with your WorkOS credentials${NC}"
else
    echo -e "${GREEN}✅ Environment file already exists${NC}"
fi

# Run Django migrations
python manage.py migrate
echo -e "${GREEN}✅ Database migrations completed${NC}"

cd ..

# Setup frontend
echo -e "${YELLOW}📦 Setting up frontend...${NC}"
cd frontend

# Install Node.js dependencies
npm install
echo -e "${GREEN}✅ Node.js dependencies installed${NC}"

# Copy environment template
if [ ! -f .env ]; then
    cp .env.example .env
    echo -e "${YELLOW}⚠️  Please edit frontend/.env with your WorkOS client ID${NC}"
else
    echo -e "${GREEN}✅ Environment file already exists${NC}"
fi

cd ..

echo -e "${GREEN}🎉 Setup completed!${NC}"
echo ""
echo -e "${YELLOW}📝 Next steps:${NC}"
echo "1. Update backend/.env with your WorkOS API key and client ID"
echo "2. Update frontend/.env with your WorkOS client ID"
echo "3. Start the backend: cd backend && source .venv/bin/activate && python manage.py runserver 8000"
echo "4. Start the frontend: cd frontend && npm start"
echo "5. Open http://localhost:3000 in your browser"
echo ""
echo -e "${GREEN}🔗 Useful links:${NC}"
echo "• WorkOS Dashboard: https://dashboard.workos.com/"
echo "• Documentation: See README.md"