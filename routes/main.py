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
import os
import openai
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user

main_bp = Blueprint('main', __name__)

openai.api_key = os.environ.get('OPENAI_API_KEY')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@main_bp.route('/generate-study-guide', methods=['POST'])
@login_required
def generate_study_guide():
    if current_user.tokens <= 0:
        return jsonify({'error': 'Insufficient tokens. Please upgrade your plan.'}), 402

    input_text = request.form.get('input_text')
    format = request.form.get('format')

    prompt = f"Convert the following text into a {format} format for studying:\n\n{input_text}"
    
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )

    study_guide = response.choices[0].text.strip()
    current_user.tokens -= 1
    db.session.commit()

    return jsonify({'study_guide': study_guide})

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
