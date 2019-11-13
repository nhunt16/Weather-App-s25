import functools
import json
import os
import datetime
from datetime import datetime
from flask import Flask, request, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_oauth import OAuth
from flask_bootstrap import Bootstrap

from authlib.client import OAuth2Session
import google.oauth2.credentials
import googleapiclient.discovery

import google_auth
import generate as g

SECRET_KEY = 'development key'
DEBUG = True

app = Flask(__name__)
app.debug = DEBUG
app.secret_key = SECRET_KEY
app.register_blueprint(google_auth.app)
oauth = OAuth()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///s25.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# must import models after initializing db
import models


@app.route('/')
def index():
    gen_db()

    if google_auth.is_logged_in():
        user_info = google_auth.get_user_info()
        print("given name:", user_info['given_name'])
        print("email:", user_info['email'])
        global CUSER
        CUSER = user_info['email']
        global CNAME
        CNAME = user_info['given_name']
        users = get_users()
        print("CUSER:{} users:{}".format(CUSER, users))
        if CUSER not in users:
            add_user(CUSER)

        u_id = get_users(CUSER) # get user id

        old = models.UserLocations.query.filter_by(uid=u_id, current=True).first()
        if old is not None:
            temp24 = get_24_temp(old.l_id)
            humid24 = get_24_humid(old.l_id)
            row = models.Temperature.query.filter_by(l_id=old.l_id).first()
            date = row.time
            date24 = get_24_hours(date)
            loc_entry = models.Locations.query.filter_by(l_id=old.l_id).first()
            location = loc_entry.location
            return render_template('dataviz.html', message=CNAME,
            user_location = location, time = date24,
            temp_values = temp24, hum_val =  humid24)
        else:
            return render_template("index.html", message=CNAME)
    else:
        return render_template("notloggedin.html")


@app.route('/manage', methods=['GET', 'POST']) #allow both GET and POST requests
def manage():
    u_id = get_users(CUSER) # get user id
    user_locations = get_user_locations(u_id) # get user's locations

    if request.method == 'POST':  #this block is only entered when the form is submitted
        location = request.form.get('location')
        add_location(u_id, location)
        return redirect('/manage')

    else:
        return render_template('manage.html', result=user_locations)

# TODO: time for data visualizations
@app.route('/dataviz/<location>')
def dataviz(location):
    lid = get_lid(location)
    time2 = ['20:00:00', '19:00:00', '18:00:00', '17:00:00', '16:00:00', '15:00:00', '14:00:00', '13:00:00', '12:00:00', '11:00:00', '10:00:00', '9:00:00', '8:00:00', '7:00:00', '6:00:00', '5:00:00', '4:00:00', '3:00:00', '2:00:00', '1:00:00', '0:00:00', '23:00:00', '22:00:00', '21:00:00', '20:00:00']
    time = [23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0.5, 0]
    temp_values = get_24_temp(lid)
    hum_val = get_24_humid(lid)

    return render_template('dataviz.html', message=CNAME,
    user_location = location, time = time,
    temp_values = temp_values, hum_val =  hum_val)

@app.route('/del-loc/<location>', methods=['POST'])
def del_location(location):
    u_id = get_users(CUSER) # get user id
    user_locations = get_user_locations(u_id) # get user's locations

    lid = get_lid(location)
    print("uid:{} location: {} lid:{}\n".format(u_id, location, lid))
    entry = models.UserLocations.query.filter_by(uid=u_id, l_id=lid).first()

    db.session.delete(entry)
    db.session.commit()

    return redirect('/manage')

@app.route('/testing')
def test():
    set_current_loc("montreal")
    return("tested")

@app.route('/current-loc/<location>', methods=['POST'])
def set_current_loc(location):
    u_id = get_users(CUSER) # get user id
    user_locations = get_user_locations(u_id) # get user's locations

    lid = get_lid(location)
    print("uid:{} location: {} lid:{}\n".format(u_id, location, lid))

    old = models.UserLocations.query.filter_by(uid=u_id, current=True).first()
    if old is not None:
        old.current=False

    entry = models.UserLocations.query.filter_by(uid=u_id, l_id=lid).first()

    entry.current=True
    # db.Session.update(entry)
    db.session.commit()

    return redirect('/manage')

def get_lid(loc):
    print("get_lid: {}\n".format(loc))
    exist_loc = models.Locations.query.filter_by(location=loc).first()
    l_id = exist_loc.l_id

    return l_id

def add_user(username):
    db.create_all()
    new_user = models.User(username=CUSER)

    db.session.add(new_user)
    db.session.commit()

    return("added new user: {}".format(CUSER))

# to add location, check Locations file if exists, if not add to both Locations and UserLocations,
# if it does then get l_id and add to UserLocations
def add_location(u_id, new_location):
    locations = str(get_locations()) # get all locations
    user_loc = str(get_user_locations(u_id)) # get all user locations
    print(user_loc)

    if new_location.lower() not in locations.lower():
        # add to Locations
        new = models.Locations(location=new_location)
        db.session.add(new)
        db.session.commit()

        # add to UserLocations(user)
        exist_loc = models.Locations.query.filter_by(location=new_location).first()
        l_id = exist_loc.l_id
        new = models.UserLocations(uid=u_id, l_id=l_id, current=False)
        db.session.add(new)
        db.session.commit()

        # call gen_data to generate 24 hours of temp data, then commit to db
        data = g.Generate().gen_data()
        date = str(datetime.now().replace(second=0, microsecond=0, minute=0, hour=datetime.now().hour))[11:]

        day_t = models.Temperature(l_id=l_id, t0=data[0][0], t1=data[1][0], t2=data[2][0], t3=data[3][0], t4=data[4][0], t5=data[5][0], t6=data[6][0], t7=data[7][0], t8=data[8][0], t9=data[9][0], t10=data[10][0], t11=data[11][0], t12=data[12][0], t13=data[13][0], t14=data[14][0], t15=data[15][0], t16=data[16][0], t17=data[17][0], t18=data[18][0], t19=data[19][0], t20=data[20][0], t21=data[21][0], t22=data[22][0], t23=data[23][0], time=date)
        db.session.add(day_t)
        db.session.commit()

        day_h = models.Humidity(l_id=l_id, h0=data[0][1], h1=data[1][1], h2=data[2][1], h3=data[3][1], h4=data[4][1], h5=data[5][1], h6=data[6][1], h7=data[7][1], h8=data[8][1], h9=data[9][1], h10=data[10][1], h11=data[11][1], h12=data[12][1], h13=data[13][1], h14=data[14][1], h15=data[15][1], h16=data[16][1], h17=data[17][1], h18=data[18][1], h19=data[19][1], h20=data[20][1], h21=data[21][1], h22=data[22][1], h23=data[23][1], time=date)
        db.session.add(day_h)
        db.session.commit()

        print("NEW LOCATION= {}".format(new_location))
        return 1

    elif new_location.lower() in locations.lower() and new_location.lower() not in user_loc.lower():
        # add to just UserLocations(user)
        exist_loc = models.Locations.query.filter_by(location=new_location).first()
        l_id = exist_loc.l_id

        new = models.UserLocations(uid=u_id, l_id=l_id, current=False)
        db.session.add(new)
        db.session.commit()
        print("ADD EXISTING LOCATION TO LIST OF USER LOCATIONS")
        return 1

    else:
            print("NOT A NEW LOCATION")
            return 0

def get_users(name=""):
    # if user provided, return user information
    if name:
        exist_user = models.User.query.filter_by(username=name).first()
        u_uid = exist_user.uid
        return u_uid


    users = models.User.query.all()
    u_out = []
    for u in users:
        u_out.append(u.username)
    return u_out

def get_locations():
    return db.session.query(models.Locations.location).all()

def get_user_locations(id):
    exist_user = models.UserLocations.query.filter_by(uid=id).all()
    lids = set()
    if exist_user == None:
        print("*****USER HAS NO LOCATIONS*****".format(id))
        return lids
    else:
        # print("*****USER HAS LOCATIONS******\n")
        l_out = []
        for row in exist_user:
            lids.add(row.l_id)
        for lid in lids:
            exist_loc = models.Locations.query.filter_by(l_id=lid).first()
            x = exist_loc.location
            l_out.append(x)
        return l_out

def gen_db():
    try:
        users = models.User.query.all()
    except:
        print("tables not found\ngenerating...")
        db.create_all()

def get_24_hours(date):
    times = []
    hour1 = int(date[0:2])
    new_hr = hour1
    for i in range(25):
        if new_hr < 0:
            new_hr = 23
        times.append(str(new_hr)+":00:00")
        new_hr = new_hr-1
    return times

def get_24_temp(lid):
    # temps = []
    row = models.Temperature.query.filter_by(l_id=lid).first()
    t_data = []
    for column in row.__table__.columns:
        t_data.append(getattr(row, column.name))

    t_data = t_data[1:len(t_data)-1] # exclude first/last column (l_id/time-stamp)
    print(t_data)
    return t_data

def get_24_humid(lid):
    # temps = []
    row = models.Humidity.query.filter_by(l_id=lid).first()
    h_data = []
    for column in row.__table__.columns:
        h_data.append(getattr(row, column.name))

    h_data = h_data[1:len(h_data)-1] # exclude first/last column (l_id/time-stamp)

    return h_data
