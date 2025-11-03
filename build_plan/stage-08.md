# Application: "2nd Foundation" + RL Task

## Application Core Concept
A **RAG (Retrieval Augmented Generation) system**
Application features outline, stack, and user perspective summary in `build_plan/app-summary.md`.

The following is one stage in a multi-stage "application creation project". Do not stray into doing more than is set out here. If you have ideas that might involve additions:
1) Look at the other stages (`build_plan/stage-**.md`) to be sure they do not already cover the functionality.
2) If they do not, consult user.

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
