# WorkOS AuthKit Logout Implementation

This implementation provides a secure logout flow that integrates WorkOS AuthKit with Django backend and React frontend.

## How It Works

### Backend (Django)

- `LogoutView` in `backend/app/views.py` handles logout requests
- Loads WorkOS sealed session from `wos_session` cookie
- Gets WorkOS logout URL using `session.get_logout_url()`
- Clears the `wos_session` cookie
- Returns JSON response with logout URL for frontend to handle

### Frontend (React)

- `LogoutButton` component in `frontend/src/components/LogoutButton.jsx`
- Clears local JWT tokens from localStorage
- Calls Django `/api/logout/` endpoint with credentials
- Redirects to WorkOS logout URL returned in response
- Handles error cases gracefully with fallback to login page

## Testing the Logout Flow

### 1. Start the Backend

```bash
cd backend
source .venv/bin/activate  # if using virtual environment
python manage.py runserver 8000
```

### 2. Start the Frontend

```bash
cd frontend
npm start
```

### 3. Test the Flow

1. Navigate to `http://localhost:3000`
2. Login using WorkOS AuthKit
3. You'll be redirected to the Dashboard
4. Click the "Logout" button
5. You should be redirected to WorkOS logout page, then back to login

### 4. Test Backend Endpoint Directly

```bash
# From project root
python test_logout.py
```

## Key Features

### Secure Session Management

- Uses WorkOS sealed sessions stored in secure cookies
- Properly clears both local JWT tokens and WorkOS session
- Handles WorkOS logout URL redirect automatically

### Error Handling

- Graceful fallback if WorkOS session is not found
- Error handling for network failures or API issues
- Always redirects to login page as final fallback

### CORS Configuration

- `CORS_ALLOW_CREDENTIALS = True` enables cookie sharing
- Proper credential handling in frontend fetch requests

## Environment Variables Required

### Backend (.env)

```
WORKOS_API_KEY=workos_sk_...
WORKOS_CLIENT_ID=client_...
WORKOS_COOKIE_PASSWORD=your_cookie_password
```

### Frontend (.env)

```
REACT_APP_WORKOS_CLIENT_ID=client_...
REACT_APP_API_BASE=http://localhost:8000/api
```

## Implementation Details

### LogoutButton Component

- Customizable with `onLogout` callback, custom styles, and children
- Shows loading state during logout process
- Uses `credentials: "include"` for cookie-based authentication
- Handles both successful logout and error scenarios

### Django LogoutView

- CSRF exempt for API usage
- Supports WorkOS `user_management.load_sealed_session()`
- Returns structured JSON response instead of direct redirect
- Properly configured cookie deletion with path and domain settings

### Security Considerations

- Clears local storage before making logout request
- Ensures WorkOS session is properly terminated
- Cookie deletion uses same path/domain as when set
- No sensitive data logged in error cases

## Troubleshooting

### Common Issues

1. **"No active session found"**: User wasn't properly logged in via WorkOS
2. **CORS errors**: Check `CORS_ALLOW_CREDENTIALS` and frontend credential settings
3. **Cookie not clearing**: Verify cookie path and domain configuration
4. **Logout URL not working**: Check WorkOS API key and client configuration

### Debug Steps

1. Check browser Network tab for logout request details
2. Verify `wos_session` cookie exists before logout
3. Check Django logs for any error messages
4. Test logout endpoint directly with `test_logout.py`
