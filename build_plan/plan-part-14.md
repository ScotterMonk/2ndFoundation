## Deployment Considerations

### Production Setup

Choose one of the following deployment options based on your environment.

- Linux (Ubuntu/Debian/RHEL): Gunicorn behind Nginx via systemd
  - App setup
    ```bash
    # app directory
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    # configure .env with DATABASE_URL, SECRET_KEY, etc.
    flask db upgrade
    ```
  - systemd unit file (example at /etc/systemd/system/second-foundation.service)
    ```ini
    [Unit]
    Description=2nd Foundation Flask App
    After=network.target

    [Service]
    User=www-data
    Group=www-data
    WorkingDirectory=/opt/second-foundation
    Environment="FLASK_ENV=production"
    EnvironmentFile=/opt/second-foundation/.env
    ExecStart=/opt/second-foundation/.venv/bin/gunicorn --bind 127.0.0.1:5000 --workers 4 wsgi:app
    Restart=always

    [Install]
    WantedBy=multi-user.target
    ```
  - Nginx reverse proxy (snippet)
    ```nginx
    server {
        listen 80;
        server_name example.com;

        location / {
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_pass http://127.0.0.1:5000;
        }
    }
    ```
  - Enable services
    ```bash
    sudo systemctl daemon-reload
    sudo systemctl enable --now second-foundation
    sudo systemctl restart nginx
    ```

- Windows: Waitress (or Gunicorn) as a Windows service via NSSM
  - App setup (PowerShell)
    ```powershell
    py -m venv .venv
    .\.venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    $env:FLASK_ENV="production"
    # configure .env with DATABASE_URL, SECRET_KEY, etc.
    flask db upgrade
    ```
  - Run with Waitress (manual)
    ```powershell
    pip install waitress
    waitress-serve --port=5000 wsgi:app
    ```
  - Install as a service with NSSM (example)
    ```powershell
    nssm install 2ndFoundation "C:\path\to\project\.venv\Scripts\python.exe" `
      "C:\path\to\project\.venv\Scripts\gunicorn.exe" --bind 127.0.0.1:5000 wsgi:app
    nssm set 2ndFoundation AppDirectory "C:\path\to\project"
    nssm start 2ndFoundation
    ```

- macOS: launchd service (development/staging)
  - Example plist at ~/Library/LaunchAgents/com.secondfoundation.app.plist
    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
     "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
    <plist version="1.0">
      <dict>
        <key>Label</key><string>com.secondfoundation.app</string>
        <key>ProgramArguments</key>
        <array>
          <string>/Users/you/project/.venv/bin/gunicorn</string>
          <string>--bind</string><string>127.0.0.1:5000</string>
          <string>wsgi:app</string>
        </array>
        <key>WorkingDirectory</key><string>/Users/you/project</string>
        <key>EnvironmentVariables</key>
        <dict>
          <key>FLASK_ENV</key><string>production</string>
        </dict>
        <key>RunAtLoad</key><true/>
        <key>KeepAlive</key><true/>
      </dict>
    </plist>
    ```
  - Load
    ```bash
    launchctl load ~/Library/LaunchAgents/com.secondfoundation.app.plist
    ```

- PaaS (containers handled by provider, no local Docker required): Render, Fly.io, Railway, Heroku-like
  - Use a Python build plan, set environment vars, and point to wsgi:app
  - Use a managed PostgreSQL with pgVector support; set DATABASE_URL
  - Ensure a start command like:
    ```txt
    gunicorn --bind 0.0.0.0:8080 --workers 4 wsgi:app
    ```

- PostgreSQL with pgVector
  - Managed Postgres: enable extension in your database
    ```sql
    CREATE EXTENSION IF NOT EXISTS vector;
    ```
  - Self-hosted Postgres:
    - Install PostgreSQL 16+ from your OS packages
    - Install/enable pgVector extension for your distribution
    - In your DB:
      ```sql
      CREATE EXTENSION IF NOT EXISTS vector;
      ```

- Local development
  ```bash
  python run.py
  # or
  flask run
  ```

### Security Checklist

- [ ] Use environment variables for secrets
- [ ] Enable CSRF protection
- [ ] Sanitize all user inputs
- [ ] Rate limit API endpoints
- [ ] Use HTTPS in production
- [ ] Regular security audits of model-generated code
- [ ] Sandbox code execution properly
- [ ] Monitor for SQL injection attempts
- [ ] Implement proper authentication/authorization
- [ ] Regular dependency updates