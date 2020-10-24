"""Script to seed database."""

import os

import json

from datetime import datetime

import crud

import model

import server


os.system('dropdb youtube_hours')

os.system('createdb youtube_hours')

model.connect_to_db(server.app)

model.db.create_all()


# Create hour table's initial data.

with open('data/hour.json') as f:

    hour_data = json.loads(f.read())

hour_in_db = []

for hour in hour_data:
    channel_name, month_end_at, hours_watched, notes, last_updated= (
                                   hour['channel_name'],
                                   hour['month_end_at'],
                                   hour['hours_watched'],
                                   hour['notes'],
                                   hour['last_updated'])
    db_hour = crud.create_hour(
                                 channel_name,
                                 month_end_at,
                                 hours_watched,
                                 notes,
                                 last_updated)

    hour_in_db.append(db_hour)
