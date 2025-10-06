# WorkOS Full-Stack Application

This is a full-stack application with:

- **Frontend**: React (Create React App) with WorkOS AuthKit
- **Backend**: Django + DRF + SimpleJWT + WorkOS integration
- **Authentication Flow**: WorkOS AuthKit → Django JWT minting

## Project Structure

- `backend/` - Django API with WorkOS integration
- `frontend/` - React app with AuthKit

## Setup Instructions

1. Set up backend: `cd backend && python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
2. Configure environment variables in backend/.env
3. Run migrations: `python manage.py migrate`
4. Start backend: `python manage.py runserver 8000`
5. Set up frontend: `cd frontend && npm install`
6. Configure environment variables in frontend/.env
7. Start frontend: `npm start`

## Progress Tracking

- [x] Project structure created
- [x] Backend Django setup
- [x] Frontend React setup
- [x] WorkOS AuthKit integration
- [x] JWT authentication flow
- [x] CORS configuration
- [x] Environment setup
- [x] Docker containerization
- [x] WorkOS AuthKit logout implementation
- [x] Secure session management with sealed cookies

## Key Features

- **Complete Authentication Flow**: Login, callback handling, JWT minting, and secure logout
- **WorkOS Integration**: Sealed session management and proper logout URL handling
- **Docker Support**: Multi-service containerization with PostgreSQL
- **Security**: CORS credentials support, CSRF protection, and proper token management
