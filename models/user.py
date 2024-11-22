from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    subscription_type = db.Column(db.String(20), default='free')
    token_balance = db.Column(db.Integer, default=10)
    last_token_reset = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)
    api_calls_count = db.Column(db.Integer, default=0, nullable=True)
    last_api_call = db.Column(db.DateTime, nullable=True)
    
    # New fields for enhanced features
    display_name = db.Column(db.String(50))
    preferences = db.Column(db.JSON, default={})
    total_study_time = db.Column(db.Integer, default=0)  # in minutes
    achievement_points = db.Column(db.Integer, default=0)
    
    # Relationships
    study_sessions = db.relationship('StudySession', backref='user', lazy=True)
    study_materials = db.relationship('StudyMaterial', backref='user', lazy=True)
    progress = db.relationship('UserProgress', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_token_cost(self):
        costs = {
            'free': 4,
            'standard': 3,
            'premium': 2
        }
        return costs.get(self.subscription_type, 4)
    
    def get_monthly_tokens(self):
        limits = {
            'free': 10,
            'standard': 120,
            'premium': 300
        }
        return limits.get(self.subscription_type, 10)
    
    def can_generate_study_guide(self):
        return self.token_balance >= self.get_token_cost()
