# Deployment Checklist

Use this checklist before deploying to production.

## 🔒 Security

### Backend Security

- [ ] Change `DJANGO_SECRET_KEY` to a secure random string
- [ ] Set `DJANGO_DEBUG=False`
- [ ] Configure proper `ALLOWED_HOSTS` for your domain
- [ ] Update `CORS_ALLOWED_ORIGINS` to production frontend URL
- [ ] Change `SIMPLEJWT_SIGNING_KEY` to a secure random string
- [ ] Use environment variables for all sensitive data
- [ ] Set up HTTPS/SSL certificates
- [ ] Configure proper database (PostgreSQL/MySQL instead of SQLite)
- [ ] Set up proper logging configuration
- [ ] Enable Django security middleware

### Frontend Security

- [ ] Update `REACT_APP_WORKOS_CLIENT_ID` to production client ID
- [ ] Update `REACT_APP_WORKOS_REDIRECT_URI` to production domain
- [ ] Update `REACT_APP_API_BASE` to production API URL
- [ ] Remove any development/debugging code
- [ ] Ensure no sensitive data in localStorage
- [ ] Set up Content Security Policy headers

## 🔧 WorkOS Configuration

### Production Setup

- [ ] Create production WorkOS application
- [ ] Configure production redirect URIs
- [ ] Update production API keys and client IDs
- [ ] Test authentication flow in production environment
- [ ] Verify user management settings
- [ ] Set up proper webhook endpoints if needed

## 🗄️ Database

### Production Database

- [ ] Set up PostgreSQL/MySQL database
- [ ] Configure database connection settings
- [ ] Run migrations on production database
- [ ] Set up database backups
- [ ] Configure connection pooling if needed
- [ ] Test database connectivity

## 🌐 Infrastructure

### Server Configuration

- [ ] Set up production server (AWS, DigitalOcean, etc.)
- [ ] Configure web server (Nginx/Apache)
- [ ] Set up application server (Gunicorn for Django)
- [ ] Configure static file serving
- [ ] Set up SSL/TLS certificates
- [ ] Configure firewall rules
- [ ] Set up monitoring and logging

### Domain & DNS

- [ ] Purchase and configure domain
- [ ] Set up DNS records
- [ ] Configure subdomain for API if needed
- [ ] Set up CDN for static assets (optional)

## 📊 Monitoring & Logging

### Application Monitoring

- [ ] Set up error tracking (Sentry, Rollbar)
- [ ] Configure application performance monitoring
- [ ] Set up uptime monitoring
- [ ] Configure log aggregation
- [ ] Set up alerts for critical errors

### Analytics

- [ ] Set up user analytics if needed
- [ ] Configure API usage monitoring
- [ ] Set up business metrics tracking

## 🧪 Testing

### Pre-deployment Testing

- [ ] Run full test suite for backend
- [ ] Run frontend tests
- [ ] Test authentication flow end-to-end
- [ ] Test all API endpoints
- [ ] Verify error handling
- [ ] Test with production-like data
- [ ] Performance testing under load

### Staging Environment

- [ ] Deploy to staging environment first
- [ ] Test with production configuration
- [ ] Verify all integrations work
- [ ] Get stakeholder approval

## 🚀 Deployment

### Backend Deployment

- [ ] Create production requirements.txt
- [ ] Set up production WSGI server
- [ ] Configure process management (systemd, supervisor)
- [ ] Set up reverse proxy configuration
- [ ] Deploy code to production server
- [ ] Run database migrations
- [ ] Collect static files
- [ ] Test API endpoints

### Frontend Deployment

- [ ] Build production bundle (`npm run build`)
- [ ] Upload build files to web server/CDN
- [ ] Configure proper caching headers
- [ ] Test frontend in production environment
- [ ] Verify API connectivity

### Final Checks

- [ ] Test complete user flow in production
- [ ] Verify all links and redirects work
- [ ] Check mobile responsiveness
- [ ] Test error pages (404, 500)
- [ ] Monitor logs for any errors
- [ ] Set up backup procedures

## 📋 Environment Variables Checklist

### Backend Production Environment

```bash
# Required
DJANGO_SECRET_KEY=production-secret-key
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
WORKOS_API_KEY=sk_live_your_production_key
WORKOS_CLIENT_ID=client_production_id
WORKOS_REDIRECT_URI=https://yourdomain.com/auth/callback
SIMPLEJWT_SIGNING_KEY=production-jwt-signing-key
CORS_ALLOWED_ORIGINS=https://yourdomain.com

# Database
DATABASE_URL=postgresql://user:password@host:port/dbname

# Optional
SENTRY_DSN=your_sentry_dsn
LOG_LEVEL=INFO
```

### Frontend Production Environment

```bash
REACT_APP_WORKOS_CLIENT_ID=client_production_id
REACT_APP_WORKOS_REDIRECT_URI=https://yourdomain.com/auth/callback
REACT_APP_API_BASE=https://api.yourdomain.com/api
```

## 🆘 Rollback Plan

### If Deployment Fails

- [ ] Document rollback procedure
- [ ] Keep previous version available
- [ ] Test rollback procedure
- [ ] Have database backup/migration rollback plan
- [ ] Communicate with users about maintenance

## 📞 Post-Deployment

### Immediate Actions

- [ ] Monitor application logs
- [ ] Check error rates and performance
- [ ] Verify user registration/login works
- [ ] Test critical user journeys
- [ ] Monitor resource usage

### Follow-up

- [ ] Document any deployment issues
- [ ] Update deployment procedures
- [ ] Plan next release cycle
- [ ] Set up regular monitoring cadence
