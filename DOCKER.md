# Docker Setup Guide

This guide explains how to run the WorkOS Full-Stack application using Docker and Docker Compose.

## 📋 Prerequisites

- [Docker](https://docs.docker.com/get-docker/) (20.10.0 or later)
- [Docker Compose](https://docs.docker.com/compose/install/) (2.0.0 or later)
- WorkOS account with API credentials

## 🚀 Quick Start

### 1. Environment Setup

Create your environment file:

```bash
cp .env.docker .env
```

Edit `.env` with your WorkOS credentials:

```bash
WORKOS_API_KEY=sk_your_actual_api_key
WORKOS_CLIENT_ID=client_your_actual_client_id
WORKOS_REDIRECT_URI=http://localhost:3000/auth/callback
WORKOS_COOKIE_PASSWORD=32-character-minimum-secret-key-replace-this
SIMPLEJWT_SIGNING_KEY=your-jwt-signing-key-change-in-production
```

### 2. Start the Application

```bash
# Build and start all services
docker-compose up --build

# Or run in background
docker-compose up -d --build
```

### 3. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/api
- **Database**: localhost:5432 (postgres/postgres)

## 🏗️ Architecture

The Docker setup includes:

- **PostgreSQL**: Database server (port 5432)
- **Django Backend**: API server (port 8000)
- **React Frontend**: Web application (port 3000)
- **Nginx**: Reverse proxy (port 80, optional)

## 📦 Services

### Database (PostgreSQL)

```yaml
# Access database directly
docker-compose exec db psql -U postgres -d workos_fullstack
```

### Backend (Django)

```bash
# Run Django commands
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
docker-compose exec backend python manage.py collectstatic

# View logs
docker-compose logs backend

# Access shell
docker-compose exec backend python manage.py shell
```

### Frontend (React)

```bash
# Install new package
docker-compose exec frontend npm install package-name

# View logs
docker-compose logs frontend

# Access shell
docker-compose exec frontend sh
```

## 🔧 Development Workflow

### Hot Reloading

Both frontend and backend support hot reloading:

- **Backend**: Django's auto-reload detects Python file changes
- **Frontend**: React development server detects changes and hot-reloads

### Making Changes

1. **Code changes**: Edit files normally - they're mounted as volumes
2. **New dependencies**:
   - Backend: Add to `requirements.txt` → restart backend service
   - Frontend: Use `docker-compose exec frontend npm install package`
3. **Database changes**: Run migrations with `docker-compose exec backend python manage.py migrate`

### Debugging

```bash
# View all logs
docker-compose logs

# View specific service logs
docker-compose logs backend
docker-compose logs frontend
docker-compose logs db

# Follow logs in real-time
docker-compose logs -f backend
```

## 🛠️ Useful Commands

### Container Management

```bash
# Start services
docker-compose up

# Start services in background
docker-compose up -d

# Stop services
docker-compose down

# Rebuild and start
docker-compose up --build

# Stop and remove volumes
docker-compose down -v
```

### Database Operations

```bash
# Reset database
docker-compose down -v
docker-compose up -d db
docker-compose exec backend python manage.py migrate

# Backup database
docker-compose exec db pg_dump -U postgres workos_fullstack > backup.sql

# Restore database
docker-compose exec -T db psql -U postgres workos_fullstack < backup.sql
```

### Service Management

```bash
# Restart specific service
docker-compose restart backend

# Scale services (if needed)
docker-compose up -d --scale backend=2

# View service status
docker-compose ps

# View resource usage
docker-compose top
```

## 🔄 Production Deployment

### 1. Production Docker Compose

Create `docker-compose.prod.yml`:

```yaml
version: "3.8"
services:
  backend:
    environment:
      - DJANGO_DEBUG=False
      - DJANGO_ALLOWED_HOSTS=yourdomain.com
      - CORS_ALLOWED_ORIGINS=https://yourdomain.com
    command: >
      sh -c "python manage.py collectstatic --noinput &&
             python manage.py migrate &&
             gunicorn config.wsgi:application --bind 0.0.0.0:8000"

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.prod
    environment:
      - REACT_APP_API_BASE=https://api.yourdomain.com/api
```

### 2. Use Production Configuration

```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### 3. With Nginx

```bash
# Start with Nginx reverse proxy
docker-compose --profile production up -d
```

## 🐛 Troubleshooting

### Common Issues

**Database Connection Issues**

```bash
# Check if database is running
docker-compose ps db

# Check database logs
docker-compose logs db

# Wait for database to be ready
docker-compose exec backend python manage.py migrate --check
```

**Port Conflicts**

```bash
# Check what's using the port
lsof -i :3000
lsof -i :8000
lsof -i :5432

# Use different ports
docker-compose up -d -p 3001:3000 frontend
```

**Build Issues**

```bash
# Clean build
docker-compose down
docker-compose build --no-cache

# Remove all containers and images
docker system prune -a
```

### Performance Issues

**Slow File Watching (macOS)**
Add to `docker-compose.yml`:

```yaml
volumes:
  - ./frontend:/app:delegated # Add :delegated for better performance
```

**Memory Issues**

```bash
# Check Docker resource usage
docker system df

# Clean up unused resources
docker system prune
```

## 📊 Monitoring

### Health Checks

Services include health checks:

```bash
# Check service health
docker-compose ps

# View health check logs
docker inspect $(docker-compose ps -q backend) | grep -A 10 Health
```

### Logs

```bash
# Structured logging for production
docker-compose logs --timestamps --follow

# Export logs
docker-compose logs > app.log
```

## 🔐 Security Considerations

### Development

- Default credentials are fine for development
- Database is accessible on localhost:5432

### Production

- [ ] Change all default passwords
- [ ] Use Docker secrets for sensitive data
- [ ] Limit database access
- [ ] Use HTTPS with proper certificates
- [ ] Set up proper firewall rules

## 📚 Additional Resources

- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Django in Docker Best Practices](https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/)
- [React in Docker](https://mherman.org/blog/dockerizing-a-react-app/)
- [PostgreSQL Docker Image](https://hub.docker.com/_/postgres)
