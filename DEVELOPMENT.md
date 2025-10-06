# Development Guide

This guide covers development workflows, troubleshooting, and best practices for the WorkOS Full-Stack application.

## 🛠️ Development Workflow

### Quick Start

1. **One-time setup**:

   ```bash
   ./setup.sh
   ```

2. **Daily development**:

   ```bash
   # Terminal 1 - Backend
   cd backend
   source .venv/bin/activate
   python manage.py runserver 8000

   # Terminal 2 - Frontend
   cd frontend
   npm start
   ```

### Environment Management

#### Backend Environment

- **Activate virtual environment**: `source backend/.venv/bin/activate`
- **Deactivate**: `deactivate`
- **Install new package**: `pip install package_name && pip freeze > requirements.txt`

#### Frontend Environment

- **Install new package**: `npm install package_name`
- **Update packages**: `npm update`

## 🐛 Troubleshooting

### Common Issues

#### Backend Issues

**Django Import Errors**

```bash
# Solution: Ensure virtual environment is activated
cd backend
source .venv/bin/activate
pip install -r requirements.txt
```

**Database Issues**

```bash
# Reset database
rm db.sqlite3
python manage.py migrate
```

**CORS Errors**

- Check `CORS_ALLOWED_ORIGINS` in settings.py
- Ensure frontend URL matches (http://localhost:3000)

#### Frontend Issues

**Module Not Found**

```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

**Environment Variables Not Loading**

- Ensure `.env` file exists in frontend/
- Restart development server after changing .env
- Variables must start with `REACT_APP_`

#### Authentication Issues

**WorkOS Callback Fails**

1. Check WorkOS dashboard redirect URI matches exactly
2. Verify API key and client ID in environment files
3. Check browser network tab for error details

**JWT Token Issues**

```bash
# Check if tokens are stored
localStorage.getItem('access')
localStorage.getItem('refresh')
```

### Debugging Tips

1. **Enable Django Debug Mode**: Set `DJANGO_DEBUG=True` in backend/.env
2. **Check Browser Console**: F12 → Console tab for frontend errors
3. **Django Logs**: Check terminal running Django server
4. **Network Tab**: Monitor API requests and responses

## 🔧 Development Tools

### Backend Tools

```bash
# Django shell
python manage.py shell

# Create superuser
python manage.py createsuperuser

# Run tests
python manage.py test

# Check for issues
python manage.py check
```

### Frontend Tools

```bash
# Build for production
npm run build

# Run tests
npm test

# Lint code (if ESLint configured)
npm run lint
```

## 📝 Code Style & Standards

### Backend (Python/Django)

- Follow PEP 8 style guide
- Use descriptive variable and function names
- Add docstrings to functions and classes
- Keep views focused and single-purpose

### Frontend (React/JavaScript)

- Use functional components with hooks
- Follow React best practices
- Use meaningful component and variable names
- Keep components small and reusable

## 🔄 Adding New Features

### Backend API Endpoint

1. **Add URL pattern** in `app/urls.py`:

   ```python
   path("new-endpoint/", NewView.as_view(), name="new-endpoint"),
   ```

2. **Create view** in `app/views.py`:

   ```python
   class NewView(APIView):
       permission_classes = (permissions.IsAuthenticated,)

       def get(self, request):
           return Response({"data": "example"})
   ```

3. **Add serializer** if needed in `app/serializers.py`

### Frontend Component

1. **Create component** in `src/components/`:

   ```jsx
   import React from "react";

   export default function NewComponent() {
     return <div>New Component</div>;
   }
   ```

2. **Add route** in `src/App.js`:
   ```jsx
   <Route path="/new" element={<NewComponent />} />
   ```

## 🚀 Deployment Preparation

### Backend

1. **Security checklist**:

   - [ ] Change `DJANGO_SECRET_KEY`
   - [ ] Set `DJANGO_DEBUG=False`
   - [ ] Configure proper `ALLOWED_HOSTS`
   - [ ] Set up proper database (PostgreSQL)
   - [ ] Configure static file serving

2. **Environment variables for production**:
   ```bash
   DJANGO_SECRET_KEY=secure-random-key
   DJANGO_DEBUG=False
   DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
   DATABASE_URL=postgresql://...
   ```

### Frontend

1. **Build optimization**:

   ```bash
   npm run build
   ```

2. **Environment variables for production**:
   ```bash
   REACT_APP_WORKOS_CLIENT_ID=client_production_id
   REACT_APP_WORKOS_REDIRECT_URI=https://yourdomain.com/auth/callback
   REACT_APP_API_BASE=https://api.yourdomain.com/api
   ```

## 🧪 Testing

### Backend Tests

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test app

# Run with coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

### Frontend Tests

```bash
# Run tests
npm test

# Run tests with coverage
npm test -- --coverage
```

## 📚 Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [React Documentation](https://react.dev/)
- [WorkOS Documentation](https://workos.com/docs)
- [Django REST Framework](https://www.django-rest-framework.org/)

## 🤝 Contributing

1. Create feature branch from `main`
2. Make changes following code style guidelines
3. Add tests for new functionality
4. Update documentation if needed
5. Submit pull request with clear description
