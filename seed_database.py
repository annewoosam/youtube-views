"""Script to seed database."""

import os

import json

from datetime import datetime

import crud

import model

import server


os.system('dropdb youtube_views')

os.system('createdb youtube_views')

model.connect_to_db(server.app)

model.db.create_all()


# Create view table's initial data.

with open('data/view.json') as f:

    view_data = json.loads(f.read())

view_in_db = []

for view in view_data:
    channel_name, month_end_at, views, notes, last_updated= (
                                   view['channel_name'],
                                   view['month_end_at'],
                                   view['views'],
                                   view['notes'],
                                   view['last_updated'])
    db_view = crud.create_view(
                                 channel_name,
                                 month_end_at,
                                 views,
                                 notes,
                                 last_updated)

    view_in_db.append(db_view)
