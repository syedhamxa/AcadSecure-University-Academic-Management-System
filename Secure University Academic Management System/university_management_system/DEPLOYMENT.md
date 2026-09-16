# DEPLOYMENT.md - Ready for Production

## ✅ Deployment Status

**Status: PRODUCTION READY**

This document guides the deployment of the University Academic Management System in production environments.

---

## 🚀 Pre-Deployment Checklist

### Code & Configuration
- [ ] Review all Python files for hardcoded credentials (none should exist)
- [ ] Change `app.secret_key` in app.py to a random 32+ character string:
  ```python
  app.secret_key = 'your-random-32-character-secret-key-here-change-this'
  ```
- [ ] Set `debug=False` in app.py:
  ```python
  if __name__ == '__main__':
      app.run(debug=False)  # NEVER use debug=True in production
  ```
- [ ] Verify no test credentials in production data
- [ ] Review all input validation

### Security
- [ ] Enable HTTPS/SSL certificate
- [ ] Configure firewall to allow only necessary ports
- [ ] Disable file directory listing
- [ ] Set proper file permissions on `/data/`:
  ```bash
  chmod 700 data/
  ```
- [ ] Review and implement rate limiting
- [ ] Set up WAF (Web Application Firewall) if needed

### Data & Backup
- [ ] Set up automated daily backups of `/data/`
- [ ] Test backup restore procedure
- [ ] Store backups off-site
- [ ] Document disaster recovery plan
- [ ] Verify backup encryption

### Monitoring
- [ ] Set up error logging (e.g., Sentry)
- [ ] Configure performance monitoring
- [ ] Set up audit log analysis
- [ ] Create alert rules for suspicious activity
- [ ] Monitor disk usage and growth rate

### Documentation
- [ ] Document deployment procedure
- [ ] Document admin user management
- [ ] Document backup/restore procedure
- [ ] Document incident response plan
- [ ] Create runbook for common operations

---

## 🐋 Docker Deployment (Optional)

### Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]
```

### Docker Compose
```yaml
version: '3.8'
services:
  ams:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
    environment:
      - FLASK_ENV=production
    restart: unless-stopped
```

### Deploy
```bash
docker-compose up -d
```

---

## 🖥️ Traditional Server Deployment

### 1. Install System Dependencies
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3 python3-pip nginx
```

### 2. Create Application User
```bash
sudo useradd -m -s /bin/bash ams-user
sudo su - ams-user
```

### 3. Clone/Upload Application
```bash
git clone <repo> university_management_system
cd university_management_system
```

### 4. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 5. Install Python Dependencies
```bash
pip install -r requirements.txt
pip install gunicorn
```

### 6. Initialize Data (if first time)
```bash
python setup.py
```

### 7. Set Permissions
```bash
chmod 700 data/
chmod 600 data/*.json
```

### 8. Create Systemd Service

Create `/etc/systemd/system/ams.service`:
```ini
[Unit]
Description=University Academic Management System
After=network.target

[Service]
User=ams-user
WorkingDirectory=/home/ams-user/university_management_system
Environment="PATH=/home/ams-user/university_management_system/venv/bin"
ExecStart=/home/ams-user/university_management_system/venv/bin/gunicorn \
    -w 4 \
    -b 0.0.0.0:8000 \
    --access-logfile - \
    --error-logfile - \
    app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl daemon-reload
sudo systemctl enable ams
sudo systemctl start ams
```

### 9. Configure Nginx (Reverse Proxy)

Create `/etc/nginx/sites-available/ams`:
```nginx
upstream ams_app {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name yourdomain.com;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name yourdomain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "SAMEORIGIN" always;

    location / {
        proxy_pass http://ams_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /home/ams-user/university_management_system/static;
    }

    location /data {
        deny all;  # Prevent direct access to data files
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/ams /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 10. SSL Certificate (Let's Encrypt)
```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot certonly --nginx -d yourdomain.com
```

---

## 🔍 Post-Deployment Verification

### Test Application
```bash
# Test home page
curl -k https://your-domain.com

# Test login endpoint
curl -k -X POST https://your-domain.com/login \
  -d "email=admin@uni.edu&password=test" 

# Check audit logs accessible only as admin
curl -k https://your-domain.com/audit_logs
```

### Verify Security
- [ ] HTTPS is working (no browser warnings)
- [ ] HTTP redirects to HTTPS
- [ ] Security headers present
- [ ] No debug mode enabled
- [ ] No test credentials in production data

### Monitor Logs
```bash
# Application logs
journalctl -u ams -f

# Nginx logs
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log

# Data directory
ls -la data/
```

---

## 📊 Performance Tuning

### Gunicorn Workers
```bash
# Recommended: (2 × CPU_cores) + 1
# For 4-core server:
gunicorn -w 9 app:app
```

### Nginx Worker Connections
In `/etc/nginx/nginx.conf`:
```nginx
worker_processes auto;
worker_connections 4096;
```

### Database Caching (Future)
When data grows large, add Redis:
```python
from flask_caching import Cache
cache = Cache(app, config={'CACHE_TYPE': 'redis'})
```

---

## 🚨 Monitoring & Alerts

### Key Metrics to Monitor
1. **Application Health**
   - Response time (should be < 200ms)
   - Error rate (should be < 1%)
   - CPU usage (should be < 50%)
   - Memory usage (should be < 500MB)

2. **Audit Trail**
   - Unusual login attempts
   - Bulk data operations
   - Failed access attempts
   - Grade modifications

3. **Data Integrity**
   - File system errors
   - Permission changes
   - Backup failures
   - Disk space warnings

### Alert Thresholds
- [ ] High error rate (> 5% errors)
- [ ] High response time (> 2 seconds)
- [ ] Disk space low (< 10% free)
- [ ] Failed backup
- [ ] Unauthorized access attempts

---

## 🔄 Maintenance Procedures

### Daily
- [ ] Monitor error logs
- [ ] Verify backup completion
- [ ] Check application health

### Weekly
- [ ] Review audit logs for anomalies
- [ ] Test backup restore
- [ ] Monitor performance metrics

### Monthly
- [ ] Review security logs
- [ ] Analyze user activity
- [ ] Update dependencies (test first)
- [ ] Review and optimize slow queries

### Quarterly
- [ ] Security audit
- [ ] Penetration testing
- [ ] Disaster recovery drill
- [ ] Capacity planning

###Annual
- [ ] Full security assessment
- [ ] Code review
- [ ] Database optimization (if migrated)
- [ ] User training and updates

---

## 🔐 Security Hardening

### Additional Measures for Production

1. **Rate Limiting**
   ```python
   from flask_limiter import Limiter
   limiter = Limiter(app, key_func=lambda: session.get('user', {}).get('id'))
   ```

2. **CORS Configuration**
   ```python
   from flask_cors import CORS
   CORS(app, resources={r"/api/*": {"origins": ["your-domain.com"]}})
   ```

3. **CSP Headers**
   ```python
   @app.after_request
   def set_csp(response):
       response.headers['Content-Security-Policy'] = "default-src 'self'"
       return response
   ```

4. **SQL Injection Prevention**
   - ✅ Already implemented (no database/SQL)

5. **XSS Prevention**
   ```python
   from markupsafe import escape
   # All template variables auto-escaped by Jinja2
   ```

---

## 📞 Incident Response

### Security Incident Procedure
1. **Detect** - Set up alerts for suspicious activity
2. **Assess** - Check audit logs for scope
3. **Contain** - Disable affected user accounts if needed
4. **Investigate** - Review complete audit trail
5. **Recover** - Restore from backup if necessary
6. **Communicate** - Notify stakeholders
7. **Document** - Update incident log

### Common Incidents

**Unauthorized Access**
- Check audit logs for login attempts
- Review IP addresses in logs
- Reset affected user passwords
- Review access logs for data access

**Data Modification**
- Check record_hash values for integrity
- Review audit logs for who modified what
- Restore from backup if necessary
- Document changes

**Performance Degradation**
- Check system resources (CPU, memory, disk)
- Review audit logs for bulk operations
- Monitor database/file size growth
- Optimize slow operations

---

## 🛠️ Troubleshooting Production Issues

### Application Won't Start
```bash
# Check Flask app syntax
python -m py_compile app.py

# Check module imports
python -c "from modules import authentication"

# Check port availability
sudo lsof -i :8000
```

### Slow Response Times
```bash
# Check system resources
free -h
df -h
top

# Check nginx logs
tail -100 /var/log/nginx/error.log

# Check Flask logs
journalctl -u ams -n 100 --no-pager
```

### Data Files Corrupted
```bash
# Validate JSON
python -m json.tool data/students.json

# Check file integrity
sha256sum data/*.json

# Restore from backup
cp backup/data/students.json data/
```

---

## 📈 Scaling Strategy

### Phase 1: < 1000 Students
- **Setup:** Single server (4GB RAM, 50GB disk)
- **Database:** JSON files
- **Cache:** None needed
- **Load Balancer:** Not needed

### Phase 2: 1000-10000 Students
- **Setup:** Single server (8GB RAM, 200GB disk) + backup
- **Database:** JSON files still OK
- **Cache:** Redis for session caching
- **Load Balancer:** Not needed yet

### Phase 3: 10000+ Students
- **Migration:** Move to relational database (PostgreSQL)
- **Setup:** Primary + replica servers
- **Cache:** Redis for sessions and queries
- **Load Balancer:** Nginx or HAProxy
- **CDN:** CloudFlare or similar

---

## 📋 Regulatory Compliance

### Data Protection
- ✅ GDPR-ready (role-based visibility)
- ✅ Audit trail for compliance
- ✅ Hash verification for data integrity
- [ ] Implement data retention policies
- [ ] Data deletion procedures

### Required Policies
- [ ] Data Protection Policy
- [ ] Privacy Policy
- [ ] Terms of Service
- [ ] Incident Response Plan
- [ ] Disaster Recovery Plan

---

## 🎯 Success Criteria

After deployment, verify:

✅ Application responding within 200ms  
✅ No errors in logs  
✅ HTTPS working  
✅ Backups running daily  
✅ Audit logs operational  
✅ All 3 roles functioning  
✅ Data integrity verified  
✅ Monitoring alerts configured  
✅ Documentation complete  
✅ Team trained on operations  

---

## 📞 Support Escalation

### Tier 1: Applications Team
- Login issues
- User account management
- Data entry problems
- Feature function questions

### Tier 2: Infrastructure Team
- Server performance
- Backup/restore
- HTTPS/SSL issues
- Network problems

### Tier 3: Developer Team
- Code bugs
- Database migration
- Security vulnerabilities
- Architecture changes

---

**Deployment Ready!** 🚀

Follow this guide for a smooth, secure production deployment.
