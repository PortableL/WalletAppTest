from flask import Blueprint, render_template, request,url_for , redirect, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash



wallet_balance = {"balance": 0.00}


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():

    
    data = request.form
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Log in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('auth.home'))
            else:
                flash('Incorrect password, try again.', category='error')    
        else:
            flash('Email does not exist.', category='error')             
    
    print(data)
    return render_template('Login.html')


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == "POST":
        email = request.form.get('email')
        fullname = request.form.get('fullname', '')
        username = request.form.get('username', '')
        password1 = request.form.get('password1', '')
        password2 = request.form.get('confirm_password', '')

        # check if email already exist in the database
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists', category='error')
            return redirect(url_for('auth.sign_up')) #redirect to the same page to show error


        # Validation
        if not email or len(email) < 4:
            flash('Email must be greater than 4 characters.', category='error')
        elif len(fullname) < 2:
            flash('First name must be greater than 2 characters.', category='error')
        elif password1 != password2:
            flash('Passwords do not match.', category='error')
        elif not password1 or not password2:
            flash('Password fields cannot be empty.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            # Check if user already exists (very basic check)
            user = User.query.filter_by(email=email).first()
            if user:
                flash('Email already exists.', category='error')
            else:
                # Create a new user (Make sure you have a User model that accepts these parameters)
                new_user = User(email=email, fullname =fullname, username=username, password=generate_password_hash(password1, method='pbkdf2:sha256'))
                  # You'll need to hash the password first
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user, remember=True)
                flash('Account created!', category='success')
                return redirect(url_for('auth.home'))  # Redirect to the login page after successful sign up



    return render_template('Signup.html')


@auth.route('/home')
@login_required
def home():
    return render_template('Home.html', balance=wallet_balance["balance"])

# cash in options
@auth.route('/cashin-options')
@login_required
def cashin_options():
    return render_template('CashInOptions.html')

@auth.route('/profile')
@login_required
def profile():
    return render_template('Profile.html')

# to add cash in value
@auth.route('/cashin', methods=['GET', 'POST'])
@login_required
def cashin():
    if request.method == 'POST':
        try:
            amount = float(request.form['amount'])
            if amount <= 0:
                raise ValueError("Invalid amount")
            wallet_balance['balance'] += amount
            return redirect(url_for('auth.home'))
        except:
            return "Invalid input", 400
    return render_template('Cashin.html')

# Savenow button
@auth.route('/save-now')
@login_required
def save_now():
    return render_template('Savenow.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user #log out user(Flask-Login)

    #Clear session data completely
    from flask import session
    session.clear()

    wallet_balance["balance"] = 0.00

    flash('Logged out successfully!', category='success')

    return redirect(url_for('auth.login'))

