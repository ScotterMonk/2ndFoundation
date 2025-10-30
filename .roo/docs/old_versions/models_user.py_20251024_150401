"""
User management models - streamlined structure reference.
Contains: Notification, User, UserAction, UserDevice, UserFaveDirector, UserFavePerformer, 
         UserFaveGenre, UserMediaAffinity, UserRating, UserSession, UserType
"""
from datetime import datetime, timezone
from flask_login import UserMixin
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer
from flask import current_app
from utils.database import db

class Notification(db.Model):
    """User notification system."""
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String(255))
    message = db.Column(db.Text)
    notification_type = db.Column(db.String(50))
    is_read = db.Column(db.Boolean)
    priority = db.Column(db.String(20))
    action_url = db.Column(db.String(500))
    action_data = db.Column(db.JSON)
    created_at = db.Column(db.DateTime)
    read_at = db.Column(db.DateTime)
    user = db.relationship('User', back_populates='notifications')

class User(UserMixin, db.Model):
    """Central user model with hierarchical reseller structure."""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(255))
    pw_hashed = db.Column(db.String(255))
    users_type_id = db.Column(db.Integer, db.ForeignKey('users_types.id'))
    parent_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    referred_by_users_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    payee_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name_first = db.Column(db.String(100))
    name_last = db.Column(db.String(100))
    name_display = db.Column(db.String(150))
    phone = db.Column(db.String(20))
    address_1 = db.Column(db.String(255))
    address_2 = db.Column(db.String(255))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    postal_zip = db.Column(db.String(20))
    country = db.Column(db.String(100))
    about_users = db.Column(db.Text)
    avatar_url = db.Column(db.String(500))
    user_score_limit = db.Column(db.String(10))
    credit_balance = db.Column(db.Integer)
    total_storage_used_mb = db.Column(db.Integer)
    is_active = db.Column(db.Boolean)
    is_verified = db.Column(db.Boolean)
    is_verified_email = db.Column(db.Boolean)
    is_verified_phone = db.Column(db.Boolean)
    preferences = db.Column(db.JSON)
    new_episode_notification = db.Column(db.Boolean)
    notification_settings = db.Column(db.JSON)
    timezone = db.Column(db.String(50))
    language_preference = db.Column(db.String(10))
    last_login_at = db.Column(db.DateTime)
    failed_login_attempts = db.Column(db.Integer)
    is_locked_out = db.Column(db.Boolean)
    lockout_until = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    password_reset_token = db.Column(db.String(255))
    password_reset_expiration = db.Column(db.DateTime)
    user_type = db.relationship('UserType', foreign_keys=[users_type_id], back_populates='users')
    parent = db.relationship('User', foreign_keys=[parent_id], remote_side=[id], backref='children')
    sessions = db.relationship('UserSession', back_populates='user', cascade='all, delete-orphan', lazy='dynamic')
    devices = db.relationship('UserDevice', back_populates='user', cascade='all, delete-orphan', lazy='dynamic')
    notifications = db.relationship('Notification', back_populates='user', cascade='all, delete-orphan', lazy='dynamic')
    actions = db.relationship('UserAction', back_populates='user', cascade='all, delete-orphan', lazy='dynamic')
    
    def get_hierarchy_level(self):
        """Calculate user's level in hierarchy."""
        level = 0
        current_user = self
        while current_user.parent_id is not None:
            level += 1
            current_user = current_user.parent
            if level > 10:
                break
        return level
    
    def get_all_descendants(self):
        """Get all users below this user in hierarchy."""
        descendants = []
        def collect_children(user):
            for child in user.children:
                descendants.append(child)
                collect_children(child)
        collect_children(self)
        return descendants
    
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id})
    
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token, max_age=1800)['user_id']
        except:
            return None
        return db.session.get(User, user_id)
    
    def can_manage_user(self, target_user):
        """Check if this user can manage target user."""
        if self.user_type.code == 'admin':
            return True
        if target_user.parent_id == self.id:
            return True
        if self.user_type.code == 'reseller':
            return target_user in self.get_all_descendants()
        return False
    
    @property
    def is_admin(self):
        """Check if user is an admin."""
        # Created by Roo | 2025-10-17
        return self.user_type and self.user_type.code == 'admin'

class UserAction(db.Model):
    """User action audit trail."""
    __tablename__ = 'users_actions'
    id = db.Column(db.Integer, primary_key=True)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    action_type = db.Column(db.String(100))
    action_category = db.Column(db.String(50))
    action_data = db.Column(db.JSON)
    ip_address = db.Column(db.String(45))
    users_agent = db.Column(db.Text)
    target_type = db.Column(db.String(50))
    target_id = db.Column(db.Integer)
    created_at = db.Column(db.DateTime)
    user = db.relationship('User', foreign_keys=[users_id], back_populates='actions')
    
    @classmethod
    def log_action(cls, user_id, action_type, action_category='general', details=None,
            ip_address=None, user_agent=None, target_type=None, target_id=None):
        """Log user action."""
        action = cls(
            users_id=user_id,
            action_type=action_type,
            action_category=action_category,
            action_data=details or {},
            ip_address=ip_address,
            users_agent=user_agent,
            target_type=target_type,
            target_id=target_id
        )
        db.session.add(action)
        return action

class UserDevice(db.Model):
    """User device tracking for security and analytics."""
    __tablename__ = 'users_devices'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    device_name = db.Column(db.String(100))
    device_type = db.Column(db.String(50))
    device_fingerprint = db.Column(db.String(255))
    last_active = db.Column(db.DateTime)
    login_count = db.Column(db.Integer)
    is_trusted = db.Column(db.Boolean)
    is_blocked = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime)
    user = db.relationship('User', back_populates='devices')

class UserFaveDirector(db.Model):
    """User favorite directors tracking."""
    __tablename__ = 'users_faves_directors'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    director_id = db.Column(db.Integer, db.ForeignKey('directors.id'))
    weight = db.Column(db.Integer)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', foreign_keys=[user_id], backref='fave_directors')

class UserFavePerformer(db.Model):
    """User favorite performers tracking."""
    __tablename__ = 'users_faves_performers'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    performer_id = db.Column(db.Integer, db.ForeignKey('performers.id'))
    weight = db.Column(db.Integer)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', foreign_keys=[user_id], backref='fave_performers')

class UserFaveGenre(db.Model):
    """User favorite genres tracking."""
    __tablename__ = 'users_faves_genres'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.id'))
    weight = db.Column(db.Integer)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', foreign_keys=[user_id], backref='fave_genres')

class UserSession(db.Model):
    """User authentication session management."""
    __tablename__ = 'users_sessions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    session_token = db.Column(db.String(255))
    expires_at = db.Column(db.DateTime)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    created_at = db.Column(db.DateTime)
    last_activity = db.Column(db.DateTime)
    user = db.relationship('User', back_populates='sessions')
    
    def is_expired(self):
        return datetime.now(timezone.utc) > self.expires_at
    
    def update_activity(self):
        self.last_activity = datetime.now(timezone.utc)

class UserType(db.Model):
    """User type definitions with permissions."""
    __tablename__ = 'users_types'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50))
    name = db.Column(db.String(255))
    description = db.Column(db.Text)
    max_uploads = db.Column(db.Integer)
    max_storage_mb = db.Column(db.Integer)
    can_resell = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    users = db.relationship('User', foreign_keys='User.users_type_id', back_populates='user_type', lazy='dynamic')