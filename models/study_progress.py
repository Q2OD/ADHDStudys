from extensions import db
from datetime import datetime

class StudySession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime)
    session_type = db.Column(db.String(50))  # 'pomodoro', 'quiz', 'flashcards', etc.
    focus_score = db.Column(db.Integer)  # 0-100 score based on breaks and completion
    notes = db.Column(db.Text)

class StudyMaterial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200))
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    category = db.Column(db.String(50))
    format_type = db.Column(db.String(50))  # 'flashcard', 'summary', 'quiz'
    
class UserProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    daily_focus_time = db.Column(db.Integer, default=0)  # in minutes
    weekly_goals_completed = db.Column(db.Integer, default=0)
    streak_days = db.Column(db.Integer, default=0)
    last_activity = db.Column(db.DateTime, default=datetime.utcnow)
