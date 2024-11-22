from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return render_template('home.html')
@main_bp.route('/pricing')
def pricing():
    return render_template('pricing.html')
@main_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')
