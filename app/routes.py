from flask import render_template, redirect, url_for, request, session, flash
from flask import Blueprint
from .auth import login_user, register_user, confirm_register
import datetime as dt
from .models import Event, db


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
            return redirect(url_for('main.create_event'))
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
            return redirect(url_for('auth.confirm'))
        else:
            flash('An error occurred during registration. Please try again.', 'danger')

    return render_template('register.html')

@auth.route('/confirm', methods=['GET', 'POST'])
def confirm():
    if request.method == 'POST':
        # Extract data from the form
        username = request.form['username']
        confirmation_code = request.form['confirmation_code']

        response = confirm_register(username, confirmation_code)
        # Call the confirm_sign_up function to confirm the user
        if response:
            flash('Account confirmed successfully! You can now log in.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash(f'An error occurred during confirmation. Please try again.', 'danger')

    return render_template('confirm.html')

@auth.route('/logout')
def logout():
    session.pop('id_token', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))

@main.route('/events', methods=['GET', 'POST'])
def create_event():
    if request.method == 'POST':
        # Collect Event Details
        event_name = request.form.get('event_name')
        start_datetime = request.form.get('event_start')
        end_datetime = request.form.get('event_end')
        location = request.form.get('location')

        # Convert dates from string to datetime if provided
        start_datetime = dt.datetime.strptime(start_datetime, '%Y-%m-%dT%H:%M')
        end_datetime = dt.datetime.strptime(end_datetime, '%Y-%m-%dT%H:%M')

        # Set up a dictionary to hold release data
        releases_data = {}
        for i in range(1, 6):
            releases_data.update({f"release_{i}_name": None,
                                   f"release_{i}_price": None, 
                                   f"release_{i}_quantity": None, 
                                   f"release_{i}_max_date": None})

        # Iterate over the available releases in the form submission
        for i in range(1, 6):
            release_name = request.form.get(f'release_name_{i}')
            release_price = request.form.get(f'release_price_{i}')
            release_quantity = request.form.get(f'release_quantity_{i}')
            release_max_date = request.form.get(f'release_max_date_{i}')

            # Set release values if they exist in the form
            if release_name:
                releases_data[f'release_{i}_name'] = release_name
            if release_price:
                releases_data[f'release_{i}_price'] = float(release_price)
            if release_quantity:
                releases_data[f'release_{i}_quantity'] = int(release_quantity)
            if release_max_date:
                releases_data[f'release_{i}_max_date'] = dt.datetime.strptime(release_max_date, '%Y-%m-%dT%H:%M')

        # Create new Event object with dynamic release data
        event = Event(
            event_name=event_name,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            location=location,
            **releases_data  # Unpack the dictionary to fill release fields
        )

        # Add and commit the event to the database
        db.session.add(event)
        db.session.commit()

        flash('Event created successfully!', 'success')
        return redirect(url_for('main.create_event'))

    # On GET request, render the page
    return render_template('events.html')