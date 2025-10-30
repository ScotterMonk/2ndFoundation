# -*- coding: utf-8 -*-
"""
Admin authorization utilities.

Provides admin_required decorator used by admin routes to restrict access.
Gracefully handles unauthenticated users (redirect to login) and non-admins (403).

# Created by Roo | 2025-10-16
"""

from functools import wraps
from flask import redirect, url_for, flash, request, abort
from flask_login import current_user


def admin_required(func):
    """Decorator to require admin privileges for a route."""
    # Created by Roo | 2025-10-16
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            # Require login first
            if not current_user.is_authenticated:
                # Mirror app.py login_manager settings where possible
                flash('Please log in to access this page.', 'warning')
                return redirect(url_for('auth.login', next=request.url))

            # Primary attribute check
            if getattr(current_user, 'is_admin', False):
                return func(*args, **kwargs)

            # Fallback: check user_type.code == 'admin' if present
            user_type = getattr(current_user, 'user_type', None)
            code = getattr(user_type, 'code', None)
            if isinstance(code, str) and code.lower() == 'admin':
                return func(*args, **kwargs)

            # Not an admin
            abort(403)
        except Exception:
            # On any unexpected error, fail closed
            abort(403)

    return wrapper