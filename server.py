"""Server for youtube_hours app."""

# increased flask

from flask import Flask, render_template

from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import func, Date, cast

import datetime


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

    month_end_at=db.session.query(Hour.month_end_at).count()

    months=[q[0] for q in db.session.query(db.func.to_char(Hour.month_end_at,'Month')).all()]

    from_month=[q[0] for q in db.session.query(db.func.min(Hour.month_end_at))]

    to_month=[q[0] for q in db.session.query(db.func.max(Hour.month_end_at))]

    quarter1=[q[0] for q in db.session.query(db.func.sum(Hour.hours_watched)).filter(Hour.month_end_at.between('2020-01-01','2020-03-31')).all()]

    quarter2=[q[0] for q in db.session.query(db.func.sum(Hour.hours_watched)).filter(Hour.month_end_at.between('2020-04-01','2020-06-30')).all()]
     
    quarter3=[q[0] for q in db.session.query(db.func.sum(Hour.hours_watched)).filter(Hour.month_end_at.between('2020-07-01','2020-09-30')).all()]
    
    quarter4=[q[0] for q in db.session.query(db.func.sum(Hour.hours_watched)).filter(Hour.month_end_at.between('2020-10-01','2020-12-31')).all()]

    hours_watched=[q[0] for q in db.session.query(Hour.hours_watched).all()]

    notes=[q[0] for q in db.session.query(Hour.notes).all()]
      
    last_updated=[q[0] for q in db.session.query(Hour.last_updated).all()]

    total_hours_watched=db.session.query(db.func.sum(Hour.hours_watched)).group_by(Hour.hours_watched)
    
    return render_template('hours.html', channel_name=channel_name, from_month=from_month, to_month=to_month, months=months, month_end_at=month_end_at, quarter1=quarter1, quarter2=quarter2, quarter3=quarter3, quarter4=quarter4, hours_watched=hours_watched, total_hours_watched=total_hours_watched,notes=notes, last_updated=last_updated)

if __name__ == '__main__':
# useful for creating reporting intervals
# https://stackoverflow.com/questions/45684292/postgresql-subtract-exactly-a-year-from-a-date-field-psql
# https://www.postgresql.org/docs/9.1/functions-datetime.html

# added connection to database

    connect_to_db(app)

# during development

    app.run(host='0.0.0.0', debug=True)

# in production

    #app.run()