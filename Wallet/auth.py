from flask import Blueprint, render_template, request,url_for , redirect, request, flash

from .models import User
from . import db


wallet_balance = {"balance": 0.00}


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    data = request.form
    print(data)
    return render_template('Login.html')

@auth.route('/logout')
def logout():
    return render_template()


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == "POST":
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # Validation
        if len(email) < 4:
            flash('Email must be greater than 4 characters.', category='error')
        elif len(firstName) < 2:
            flash('First name must be greater than 2 characters.', category='error')
        elif password1 != password2:
            flash('Passwords do not match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            # Check if user already exists (very basic check)
            user = User.query.filter_by(email=email).first()
            if user:
                flash('Email already exists.', category='error')
            else:
                # Create a new user (Make sure you have a User model that accepts these parameters)
                new_user = User(email=email, firstName=firstName, password=password1)  # You'll need to hash the password first
                db.session.add(new_user)
                db.session.commit()

                flash('Account created!', category='success')
                return redirect(url_for('auth.login'))  # Redirect to the login page after successful sign up

    return render_template('Signup.html')

@auth.route('/home')
def home():
    return render_template('Home.html', balance=wallet_balance["balance"])

# cash in options
@auth.route('/cashin-options')
def cashin_options():
    return render_template('CashInOptions.html')

# to add cash in value
@auth.route('/cashin', methods=['GET', 'POST'])
def cashin():
    if request.method == 'POST':
        try:
            amount = float(request.form['amount'])
            if amount <= 0:
                raise ValueError("Invalid amount")
            wallet_balance['balance'] += amount
            return redirect(url_for('home'))
        except:
            return "Invalid input", 400
    return render_template('Cashin.html')

# Savenow button
@auth.route('/save-now')
def save_now():
    return render_template('Savenow.html')
