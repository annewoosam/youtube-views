"""Server for youtube_hours app."""

# increased flask

from flask import Flask, render_template

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# created import allowing connection to database

from model import connect_to_db, Hour, db

app = Flask(__name__)

# imported Jinja secret key settings
from jinja2 import StrictUndefined

app.secret_key = "dev"

app.jinja_env.undefined = StrictUndefined

import crud

@app.route('/')

def all_hours():

    stats=crud.get_hours()
    
    channel_name=[q[0] for q in db.session.query(Hour.channel_name).all()]

    month_end_at=[q[0] for q in db.session.query(Hour.month_end_at).all()]
     
    hours_watched=[q[0] for q in db.session.query(Hour.hours_watched).all()]

    notes=[q[0] for q in db.session.query(Hour.notes).all()]
      
    last_updated=[q[0] for q in db.session.query(Hour.last_updated).all()]
    
    return render_template('hours.html', channel_name=channel_name, month_end_at=month_end_at, hours_watched=hours_watched, notes=notes, last_updated=last_updated)

if __name__ == '__main__':

# added connection to database

    connect_to_db(app)

# during development

    app.run(host='0.0.0.0', debug=True)

# in production

    #app.run()