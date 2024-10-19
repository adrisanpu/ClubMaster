from flask import render_template, redirect, url_for, request, session, flash
from flask import Blueprint
from .auth import login_user, register_user, confirm_register

# Define a Blueprint (optional but recommended for larger apps)
main = Blueprint('main', __name__)
auth = Blueprint('auth', __name__)
events = Blueprint('events', __name__)

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
            return redirect(url_for('events.create_event'))
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


@events.route('/events', methods=['GET', 'POST'])
def create_event():
    if 'releases' not in session:
        session['releases'] = [{}]  # Start with one empty release

    if request.method == 'POST':
        # Save event data in session (or persist in a database as per your requirement)
        session['event_name'] = request.form.get('event_name')
        session['event_start'] = request.form.get('event_start')
        session['event_end'] = request.form.get('event_end')
        session['location'] = request.form.get('location')

        # Save releases data
        releases = []
        for i in range(len(session['releases'])):
            release = {
                'name': request.form.get(f'release_name_{i+1}'),
                'price': request.form.get(f'release_price_{i+1}'),
                'quantity': request.form.get(f'release_quantity_{i+1}'),
                'max_date': request.form.get(f'release_max_date_{i+1}')
            }
            releases.append(release)
        session['releases'] = releases

        flash('Event data saved!', 'success')
        return redirect(url_for('events.create_event'))

    return render_template('events.html', event=session)

@events.route('/add_release', methods=['POST'])
def add_release():
    if 'releases' not in session:
        session['releases'] = [{}]

    if len(session['releases']) < 5:
        session['releases'].append({})  # Add an empty release

    return redirect(url_for('events.create_event'))

@events.route('/remove_release/<int:index>', methods=['POST'])
def remove_release(index):
    if 'releases' in session and len(session['releases']) > 1:
        releases = session['releases']
        if 0 <= index < len(releases):
            del releases[index]
        session['releases'] = releases

    return redirect(url_for('events.create_event'))