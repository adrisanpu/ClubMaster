from flask import render_template, redirect, url_for, request, session, flash
from flask import Blueprint
from .auth import login_user

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