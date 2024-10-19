from flask import render_template, redirect, url_for, request, session, flash
from flask import Blueprint
from .auth import login_user, register_user

# Define a Blueprint (optional but recommended for larger apps)
main = Blueprint('main', __name__)
auth = Blueprint('auth', __name__)

@main.route('/')
def home():
    return redirect(url_for('auth.login'))

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Call the login function from auth.py
        token = login_user(username, password)

        if token:
            # Store token in session or wherever you need it
            session['id_token'] = token
            flash('Login successful!', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Login failed. Please check your credentials.', 'danger')

    return render_template('login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Extract data from the form
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
        family_name = request.form['family_name']
        birthdate = request.form['birthdate']
        gender = request.form['gender']
        phone_number = request.form['phone_number']
        address = request.form['address']

        # Call the signup_user function to register the user with Cognito
        response = register_user(username=email, password=password, email=email, name=name, family_name=family_name, birthdate=birthdate, gender=gender, phone_number=phone_number, address=address)

        if response:
            flash('Registration successful! Please check your email to confirm your account.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('An error occurred during registration. Please try again.', 'danger')

    return render_template('register.html')