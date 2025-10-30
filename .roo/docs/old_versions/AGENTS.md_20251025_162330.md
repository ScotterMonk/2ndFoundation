# Debug Mode - Non-Obvious Patterns

This file provides guidance to agents when working with code in this repository.

## Database Scripts (CRITICAL)
- Write database scripts to `temp/` folder and run, never paste multi-line scripts in terminal
- When creating a script to "check the database", write a temp .py file in `temp/` folder and run it

## TestingConfig Behavior
- TestingConfig intentionally has `WTF_CSRF_ENABLED = False` - this is by design, not a bug

## Querystring Authentication (Local Testing Only)
- For local testing, use querystring login: `http://localhost:5000/auth/login?email=[creds]&password=[hashed]`
- If any bug arises with existing users, prepare WTS package and delegate to `/debug`