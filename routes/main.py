from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return render_template('home.html')
@main.route('/pricing')
def pricing():
    return render_template('pricing.html')
@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')
