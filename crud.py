"""CRUD operations."""

from model import db, View, connect_to_db

import datetime


def create_view(channel_name, month_end_at, views, notes, last_updated):
   

    view = View(channel_name=channel_name,
                month_end_at=month_end_at,
                views=views,
                notes=notes,
                last_updated=last_updated)

    db.session.add(view)

    db.session.commit()

    return View

def get_views():
    """Return all rows of view data."""

    return View.query.all()
 
if __name__ == '__main__':
    from server import app
    connect_to_db(app)
