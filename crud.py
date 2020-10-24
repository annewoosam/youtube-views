"""CRUD operations."""

from model import db, Hour, connect_to_db

import datetime


def create_hour(channel_name, month_end_at, hours_watched, notes, last_updated):
   

    hour = Hour(channel_name=channel_name,
                month_end_at=month_end_at,
                hours_watched=hours_watched,
                notes=notes,
                last_updated=last_updated)

    db.session.add(hour)

    db.session.commit()

    return hour

def get_hours():
    """Return all rows of hour data."""

    return Hour.query.all()
 
if __name__ == '__main__':
    from server import app
    connect_to_db(app)
