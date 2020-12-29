"""Server for youtube_views app."""

# increased flask

from flask import Flask, render_template

from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import func, Date, cast

from datetime import date, datetime,timedelta

from dateutil.relativedelta import relativedelta


db = SQLAlchemy()

# created import allowing connection to database

from model import connect_to_db, View, db

app = Flask(__name__)

# imported Jinja secret key settings
from jinja2 import StrictUndefined

app.secret_key = "dev"

app.jinja_env.undefined = StrictUndefined

import crud

@app.route('/')

def all_views():

    stats=crud.get_views()
    
    channel_name=[q[0] for q in db.session.query(View.channel_name).all()]

    month_end_at=db.session.query(View.month_end_at).count()

    months=[q[0] for q in db.session.query(db.func.to_char(View.month_end_at,'Month')).all()]

    from_month=[q[0] for q in db.session.query(db.func.min(View.month_end_at))]

    to_month=[q[0] for q in db.session.query(db.func.max(View.month_end_at))]

    quarter1=[q[0] for q in db.session.query(db.func.sum(View.views)).filter(View.month_end_at.between('2020-01-01','2020-03-31')).all()]

    quarter2=[q[0] for q in db.session.query(db.func.sum(View.views)).filter(View.month_end_at.between('2020-04-01','2020-06-30')).all()]
     
    quarter3=[q[0] for q in db.session.query(db.func.sum(View.views)).filter(View.month_end_at.between('2020-07-01','2020-09-30')).all()]
    
    quarter4=[q[0] for q in db.session.query(db.func.sum(View.views)).filter(View.month_end_at.between('2020-10-01','2020-12-31')).all()]

    views=[q[0] for q in db.session.query(View.views).all()]

    notes=[q[0] for q in db.session.query(View.notes).all()]
      
    last_updated=[q[0] for q in db.session.query(db.func.max(View.last_updated))]

    total_views_watched=db.session.query(db.func.sum(View.views)).group_by(View.views)

    current_time = datetime.utcnow()

    one_month_ago = current_time -  timedelta(1)

    last_month = [q[0] for q in db.session.query(db.func.sum(View.views)).filter(View.month_end_at > one_month_ago).all()]

    three_months_ago = current_time -  relativedelta(months=+2)

    three_months = [q[0] for q in db.session.query(db.func.sum(View.views)).filter(View.month_end_at > three_months_ago).all()]

    six_months_ago = current_time -  relativedelta(months=+5)

    six_months = [q[0] for q in db.session.query(db.func.sum(View.views)).filter(View.month_end_at > six_months_ago).all()]

    nine_months_ago = current_time -  relativedelta(months=+8)

    nine_months = [q[0] for q in db.session.query(db.func.sum(View.views)).filter(View.month_end_at > nine_months_ago).all()]

    eleven_months_ago = current_time -  relativedelta(months=+1)

    eleven_months = [q[0] for q in db.session.query(db.func.sum(View.views)).filter(View.month_end_at > eleven_months_ago).all()]

    eleven_months_ago_for_projection = current_time -  relativedelta(months=+10)

    eleven_months_for_projection = [q[0] for q in db.session.query(db.func.sum(View.views)).filter(View.month_end_at > eleven_months_ago_for_projection).all()]

    twelve_months_ago = current_time -  relativedelta(months=+11)

    twelve_months = [q[0] for q in db.session.query(db.func.sum(View.views)).filter(View.month_end_at > twelve_months_ago).all()]

    s1 = [str(i) for i in last_month]

    result1 = str("".join(s1))

    variance1= round(int(result1)-2500,2)

    variance1g=int(result1)

    s3 = [str(i) for i in last_month]

    result3 = str("".join(s3))

    variance3= round(int(result3)-7500)

    s6 = [str(i) for i in last_month]

    result6 = str("".join(s6))

    variance6= round(int(result1)-15000)

    s9 = [str(i) for i in last_month]

    result9 = str("".join(s9))

    variance9= round(int(result1)-22500)

    s12 = [str(i) for i in twelve_months]

    result12 = str("".join(s12))

    variance12= int(result12)-30000

    s11 = [str(i) for i in eleven_months]

    result11 = str("".join(s11))

    month11=int(result11)

    variance11= int(result11)-int(result1)

    s11p = [str(i) for i in eleven_months_for_projection]

    result11p = str("".join(s11p))

    month11p=int(result11p)

    growthrate=variance1g/variance11

    next_month_projected=round(variance1g*growthrate)

    next_month_projected_total=round(next_month_projected+month11p)

    return render_template('views.html', month11p=month11p, result1=result1, result3=result3, result6=result6, result9=result9, result11=result11, result12=result12, variance1=variance1, variance3=variance3, variance6=variance6, variance9=variance9, variance12=variance12, variance1g=variance1g, variance11=variance11, growthrate=growthrate, channel_name=channel_name, current_time=current_time, last_month=last_month, one_month_ago=one_month_ago, three_months=three_months, three_months_ago=three_months_ago, six_months=six_months, six_months_ago=six_months_ago, nine_months=nine_months, nine_months_ago=nine_months_ago, eleven_months=eleven_months, eleven_months_ago=eleven_months_ago, twelve_months=twelve_months, twelve_months_ago=twelve_months_ago, next_month_projected=next_month_projected, next_month_projected_total=next_month_projected_total,from_month=from_month, to_month=to_month, months=months, month_end_at=month_end_at, quarter1=quarter1, quarter2=quarter2, quarter3=quarter3, quarter4=quarter4, views=views, total_views_watched=total_views_watched, notes=notes, last_updated=last_updated)

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