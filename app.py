import os
import stripe
from flask import Flask

stripe.api_key = os.environ.get('sk_test_51QNhYHKkNhYowr218u21VXIVZsyU46k2uL6hLlWdd8zK13uRk5uLLCIjqvpFvLhtldshmQlHHfeULPeMPcT21Xix00UiN2sFZZ')
import os
from extensions import db, login_manager
from models.user import User

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.urandom(24)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///adhd_study.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.signup'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from routes.main import main_bp
    from routes.auth import auth_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    return app

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
