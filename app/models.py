from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Event(db.Model):
    __tablename__ = 'events'
    
    # General Event Details
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(100), nullable=False)
    start_datetime = db.Column(db.DateTime, nullable=False)
    end_datetime = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(255), nullable=False)

    # Ticket Releases (up to 5 releases, each release can be null)
    release_1_name = db.Column(db.String(100), nullable=True)
    release_1_price = db.Column(db.Float, nullable=True)
    release_1_quantity = db.Column(db.Integer, nullable=True)
    release_1_max_date = db.Column(db.DateTime, nullable=True)

    release_2_name = db.Column(db.String(100), nullable=True)
    release_2_price = db.Column(db.Float, nullable=True)
    release_2_quantity = db.Column(db.Integer, nullable=True)
    release_2_max_date = db.Column(db.DateTime, nullable=True)

    release_3_name = db.Column(db.String(100), nullable=True)
    release_3_price = db.Column(db.Float, nullable=True)
    release_3_quantity = db.Column(db.Integer, nullable=True)
    release_3_max_date = db.Column(db.DateTime, nullable=True)

    release_4_name = db.Column(db.String(100), nullable=True)
    release_4_price = db.Column(db.Float, nullable=True)
    release_4_quantity = db.Column(db.Integer, nullable=True)
    release_4_max_date = db.Column(db.DateTime, nullable=True)

    release_5_name = db.Column(db.String(100), nullable=True)
    release_5_price = db.Column(db.Float, nullable=True)
    release_5_quantity = db.Column(db.Integer, nullable=True)
    release_5_max_date = db.Column(db.DateTime, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Event {self.event_name}>"
