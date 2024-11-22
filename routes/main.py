import os
import stripe
from flask import Blueprint, render_template, url_for, redirect
from flask_login import login_required, current_user

stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

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
