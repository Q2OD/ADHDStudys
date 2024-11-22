import os
import stripe
from datetime import datetime
from flask import Blueprint, render_template, url_for, redirect, request, jsonify
from flask_login import login_required, current_user
from extensions import db
from services.claude_service import ClaudeService
from functools import wraps
import time

stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')
claude_service = ClaudeService()

main_bp = Blueprint('main', __name__)

def rate_limit(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.last_api_call:
            time_diff = (datetime.utcnow() - current_user.last_api_call).total_seconds()
            if time_diff < 5:  # 5 seconds between calls
                return jsonify({'error': 'Please wait before making another request'}), 429
        return f(*args, **kwargs)
    return decorated_function

@main_bp.route('/')
def home():
    return render_template('index.html')

@main_bp.route('/pricing')
def pricing():
    return render_template('pricing.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@main_bp.route('/generate-study-guide', methods=['POST'])
@login_required
@rate_limit
def generate_study_guide():
    if not current_user.can_generate_study_guide():
        return jsonify({'error': 'Insufficient tokens. Please upgrade your plan.'}), 402

    input_text = request.form.get('input_text')
    format_type = request.form.get('format')

    if not input_text or not format_type:
        return jsonify({'error': 'Missing required parameters'}), 400

    # Update API call tracking
    current_user.last_api_call = datetime.utcnow()
    current_user.api_calls_count += 1
    
    # Generate study guide
    study_guide = claude_service.generate_study_guide(input_text, format_type)
    
    # Deduct tokens
    token_cost = current_user.get_token_cost()
    current_user.token_balance -= token_cost
    
    db.session.commit()

    return jsonify({
        'study_guide': study_guide,
        'tokens_remaining': current_user.token_balance,
        'token_cost': token_cost
    })

@main_bp.route('/create-checkout-session', methods=['POST'])
@login_required
def create_checkout_session():
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': 'price_12345',  # Replace with actual price ID
                    'quantity': 1,
                },
            ],
            mode='subscription',
            success_url=url_for('main.dashboard', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=url_for('main.pricing', _external=True),
            client_reference_id=current_user.id
        )
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        return 'Error creating checkout session: ' + str(e)
