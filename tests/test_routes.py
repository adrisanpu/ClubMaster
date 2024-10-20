from flask import Blueprint, request, render_template
from app.models import Event
import pandas as pd


# Define a Blueprint (optional but recommended for larger apps)
test = Blueprint('test', __name__)


@test.route('/view-events', methods=['GET'])
def view_events():
    # Get filtering options from the request arguments
    year = request.args.get('year')
    month = request.args.get('month')

    # Retrieve all events from the database
    events = Event.query.all()

    # Prepare data for a DataFrame
    events_data = [
        {
            "event_id": event.id,
            "event_name": event.event_name,
            "start_datetime": event.start_datetime,
            "end_datetime": event.end_datetime,
            "location": event.location,
            "release_1_name": event.release_1_name,
            "release_1_price": event.release_1_price,
            "release_1_quantity": event.release_1_quantity,
            "release_1_max_date": event.release_1_max_date,
            "release_2_name": event.release_2_name,
            "release_2_price": event.release_2_price,
            "release_2_quantity": event.release_2_quantity,
            "release_2_max_date": event.release_2_max_date,
            "release_3_name": event.release_3_name,
            "release_3_price": event.release_3_price,
            "release_3_quantity": event.release_3_quantity,
            "release_3_max_date": event.release_3_max_date,
            "release_4_name": event.release_4_name,
            "release_4_price": event.release_4_price,
            "release_4_quantity": event.release_4_quantity,
            "release_4_max_date": event.release_4_max_date,
            "release_5_name": event.release_5_name,
            "release_5_price": event.release_5_price,
            "release_5_quantity": event.release_5_quantity,
            "release_5_max_date": event.release_5_max_date,
            "created_at": event.created_at,
            "updated_at": event.updated_at
        }
        for event in events
    ]

    # Create a DataFrame for filtering
    df = pd.DataFrame(events_data)

    # Apply filters if year and month are provided
    if year:
        df = df[df['start_datetime'].dt.year == int(year)]
    if month:
        df = df[df['start_datetime'].dt.month == pd.to_datetime(month, format='%B').month]

    # Convert filtered DataFrame back to json and replace NaN dates with a dummy date
    df = df.fillna('N/A')
    filtered_events = df.to_dict(orient='records')

    # Render the HTML page with filtered events
    return render_template('events.html', events=filtered_events)
