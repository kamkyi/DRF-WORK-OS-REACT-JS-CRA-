# WorkOS Full-Stack Application

A complete full-stack application demonstrating authentication using WorkOS AuthKit with React frontend and Django backend.

## 🏗️ Architecture

- **Frontend**: React (Create React App) with WorkOS AuthKit
- **Backend**: Django + DRF + SimpleJWT + WorkOS integration
- **Authentication Flow**: WorkOS AuthKit → Django JWT minting
- **CORS**: Configured for local development

## 📁 Project Structure

```
workos-fullstack/
├── backend/                    # Django API server
│   ├── config/                # Django project settings
│   │   ├── __init__.py
│   │   ├── settings.py        # Django configuration
│   │   ├── urls.py           # Main URL routing
│   │   ├── wsgi.py           # WSGI application
│   │   └── asgi.py           # ASGI application
│   ├── app/                  # Django application
│   │   ├── __init__.py
│   │   ├── models.py         # Database models
│   │   ├── views.py          # API views
│   │   ├── urls.py           # App URL routing
│   │   ├── serializers.py    # DRF serializers
│   │   └── permissions.py    # Custom permissions
│   ├── manage.py             # Django management script
│   ├── requirements.txt      # Python dependencies
│   └── .env                  # Environment variables
├── frontend/                 # React application
│   ├── public/
│   │   └── index.html        # HTML template
│   ├── src/
│   │   ├── auth/             # Authentication components
│   │   │   ├── AuthKitProviderWrapper.jsx
│   │   │   └── ProtectedRoute.jsx
│   │   ├── pages/            # Page components
│   │   │   ├── Login.jsx
│   │   │   └── Dashboard.jsx
│   │   ├── App.js            # Main app component
│   │   ├── index.js          # React entry point
│   │   └── api.js            # Axios configuration
│   ├── package.json          # Node.js dependencies
│   └── .env                  # Environment variables
└── README.md                 # This file
```

## 🚀 Setup Instructions

Choose one of the following setup methods:

### 🐳 Docker Setup (Recommended)

**Prerequisites:**

- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/)
- WorkOS account and application setup

**Quick Start:**

```bash
# Clone and navigate to project
cd workos-fullstack

# Copy environment template
cp .env.docker .env

# Edit .env with your WorkOS credentials
# WORKOS_API_KEY=sk_your_api_key
# WORKOS_CLIENT_ID=client_your_client_id

# Start all services with Docker
docker-compose up --build

# Access the application
open http://localhost:3000
```

See [DOCKER.md](DOCKER.md) for detailed Docker instructions.

### 💻 Local Development Setup

**Prerequisites:**

- Python 3.8+
- Node.js 16+
- WorkOS account and application setup

### 1. WorkOS Setup

1. Create a WorkOS account at [workos.com](https://workos.com)
2. Create a new application in the WorkOS dashboard
3. Note down your:
   - `WORKOS_API_KEY` (starts with `sk_`)
   - `WORKOS_CLIENT_ID` (starts with `client_`)
4. Set redirect URI to: `http://localhost:3000/auth/callback`

### 2. Backend Setup

```bash
cd backend

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env  # Create from template
# Edit .env with your WorkOS credentials

# Run migrations
python manage.py migrate

# Start the development server
python manage.py runserver 8000
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Configure environment variables
cp .env.example .env  # Create from template
# Edit .env with your WorkOS client ID

# Start the development server
npm start
```

## 🔧 Environment Configuration

### Backend (.env)

```bash
# Django Settings
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost

# WorkOS Configuration
WORKOS_API_KEY=sk_your_api_key_here
WORKOS_CLIENT_ID=client_your_client_id_here
WORKOS_REDIRECT_URI=http://localhost:3000/auth/callback
WORKOS_COOKIE_PASSWORD=32-character-minimum-secret-key

# JWT Configuration
SIMPLEJWT_SIGNING_KEY=your-jwt-signing-key

# CORS Configuration
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

### Frontend (.env)

```bash
REACT_APP_WORKOS_CLIENT_ID=client_your_client_id_here
REACT_APP_WORKOS_REDIRECT_URI=http://localhost:3000/auth/callback
REACT_APP_API_BASE=http://localhost:8000/api
```

## 🔐 Authentication Flow

1. **User Login**: User clicks "Sign in with AuthKit" on `/login`
2. **WorkOS Redirect**: AuthKit redirects to WorkOS hosted login
3. **Authentication**: User completes authentication on WorkOS
4. **Callback**: WorkOS redirects back to `/auth/callback` with auth code
5. **Token Exchange**: Frontend sends code to Django `/api/auth/workos/callback`
6. **Verification**: Django verifies with WorkOS and creates/updates user
7. **JWT Minting**: Django returns JWT access/refresh tokens
8. **Storage**: Frontend stores tokens in localStorage
9. **API Access**: Subsequent API calls use JWT Bearer tokens

## 🛠️ API Endpoints

### Authentication

- `POST /api/auth/workos/callback` - Exchange WorkOS code for JWT tokens
  - Body: `{"code": "workos_auth_code"}` or `{"id_token": "workos_id_token"}`
  - Returns: `{"access": "jwt_token", "refresh": "refresh_token", "user": {...}}`

### Protected Endpoints

- `GET /api/hello` - Protected endpoint example
  - Headers: `Authorization: Bearer <access_token>`
  - Returns: `{"message": "Hello username! Time: timestamp"}`

## 🧪 Testing the Application

1. **Start both servers**:

   - Backend: `http://localhost:8000`
   - Frontend: `http://localhost:3000`

2. **Test the flow**:

   - Open `http://localhost:3000/login`
   - Click "Sign in with AuthKit"
   - Complete WorkOS authentication
   - Verify redirect to dashboard with protected API call

3. **Test protected endpoint**:
   ```bash
   curl -H "Authorization: Bearer <ACCESS_TOKEN>" \
        http://localhost:8000/api/hello
   ```

## 📚 Key Technologies

- **React**: Frontend framework with hooks and routing
- **WorkOS AuthKit**: Hosted authentication UI and management
- **Django**: Python web framework for backend API
- **Django REST Framework**: API building toolkit
- **SimpleJWT**: JWT authentication for Django
- **CORS Headers**: Cross-origin request handling
- **Axios**: HTTP client for API calls

## 🔒 Security Features

- **JWT Authentication**: Secure token-based authentication
- **CORS Protection**: Configured cross-origin policies
- **Environment Variables**: Sensitive data in environment files
- **Token Refresh**: Automatic token renewal capability
- **Server-side Verification**: WorkOS code exchange on backend

## 🚨 Production Considerations

- [ ] Replace demo secret keys with secure random values
- [ ] Configure proper CORS origins for production domains
- [ ] Set up HTTPS for all environments
- [ ] Implement proper error handling and logging
- [ ] Add token refresh logic on frontend
- [ ] Set up proper database (PostgreSQL/MySQL)
- [ ] Configure static file serving
- [ ] Add rate limiting and security middleware
- [ ] Set up monitoring and health checks

## 📖 Additional Resources

- [WorkOS Documentation](https://workos.com/docs)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [SimpleJWT Documentation](https://django-rest-framework-simplejwt.readthedocs.io/)
- [React Router](https://reactrouter.com/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details
# DRF-WORK-OS-REACT-JS-CRA-
