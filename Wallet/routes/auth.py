from flask import Blueprint, render_template,url_for , redirect, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from ..models.user import User
from ..extensions import db
from werkzeug.security import generate_password_hash, check_password_hash



auth = Blueprint('auth', __name__)




@auth.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('wallet.home'))
    return redirect(url_for('auth.login'))


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
                return redirect(url_for('wallet.home'))
            else:
                flash('Incorrect password, try again.', category='error')    
        else:
            flash('Email does not exist.', category='error')             
    
    print(data)
    return render_template('auth/Login.html')


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    # Redirect if already logged in
    if current_user.is_authenticated:
            return redirect(url_for('wallet.home'))


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
            # Check if email already exists 
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash('Email already exists.', category='error')
                return redirect(url_for('auth.sign_up'))
            
            # Check if username already exists
            existing_username = User.query.filter_by(username=username).first()
            if existing_username:
                flash('Username already taken.', category='error')
                return redirect(url_for('auth.sign_up'))
            
            try:
                # Create new user
                new_user = User(
                    email=email,
                    fullname=fullname,
                    username=username,
                    password=generate_password_hash(password1, method='pbkdf2:sha256')
                )
                db.session.add(new_user)
                db.session.commit()
                
                # Log in the new user
                login_user(new_user, remember=True)
                flash('Account created successfully!', category='success')
                return redirect(url_for('wallet.home'))  # ✅ Fixed redirect
                
            except Exception as e:
                db.session.rollback()
                flash('An error occurred while creating your account.', category='error')
                print(f"Sign-up error: {e}")  # For debugging



    return render_template('auth/Signup.html')



@auth.route('/profile')
@login_required
def profile():
    return render_template('auth/Profile.html')




@auth.route('/logout')
@login_required
def logout():
    logout_user()  # Log out user (Flask-Login)
    
    # Clear session data completely
    from flask import session
    session.clear()
    
    flash('Logged out successfully!', category='success')
    
    # Create response with no-cache headers
    response = redirect(url_for('auth.login'))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    
    return response

