from datetime import datetime, timedelta
from models.study_progress import StudySession, StudyMaterial, UserProgress
from extensions import db

class StudyToolsService:
    @staticmethod
    def start_pomodoro_session(user_id, duration=25):
        session = StudySession(
            user_id=user_id,
            session_type='pomodoro',
            start_time=datetime.utcnow(),
            end_time=datetime.utcnow() + timedelta(minutes=duration)
        )
        db.session.add(session)
        db.session.commit()
        return session

    @staticmethod
    def complete_session(session_id, focus_score):
        session = StudySession.query.get(session_id)
        if session:
            session.end_time = datetime.utcnow()
            session.focus_score = focus_score
            db.session.commit()
            
            # Update user progress
            progress = UserProgress.query.filter_by(user_id=session.user_id).first()
            if progress:
                duration = int((session.end_time - session.start_time).total_seconds() / 60)
                progress.daily_focus_time += duration
                db.session.commit()

    @staticmethod
    def get_user_analytics(user_id):
        sessions = StudySession.query.filter_by(user_id=user_id).all()
        progress = UserProgress.query.filter_by(user_id=user_id).first()
        
        return {
            'total_sessions': len(sessions),
            'average_focus_score': sum(s.focus_score or 0 for s in sessions) / len(sessions) if sessions else 0,
            'daily_focus_time': progress.daily_focus_time if progress else 0,
            'streak_days': progress.streak_days if progress else 0
        }
