# Application: "2nd Foundation" + RL Task

## Application Core Concept
A **RAG (Retrieval Augmented Generation) system**
Application features outline, stack, and user perspective summary in `build_plan/app-summary.md`.

## STAGE 08: Deployment Considerations
Use `build_plan/ref-environment-config.md` and requirements files for
- Production Setup
  - Non-Docker deployment options:
    - Linux: Gunicorn behind Nginx as a systemd service
    - Windows: Waitress or Gunicorn via NSSM as a Windows service
    - macOS: launchd service for development
    - PaaS: Render, Fly.io, Railway, or Heroku-like platforms
  - PostgreSQL with pgVector installed (managed service or self-hosted)
  - Environment config via .env and system secrets
- Security Checklist
  - Environment variables for secrets
  - CSRF protection
  - Input sanitization
  - Rate limiting
  - HTTPS in production
  - Code execution sandboxing
  - SQL injection monitoring
  - Authentication/authorization
  - Dependency updates
