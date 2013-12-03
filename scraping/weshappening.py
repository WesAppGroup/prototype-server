from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from pygeocoder import Geocoder
import simplejson
import os
import time
import urllib

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'
db = SQLAlchemy(app)

cats = {0: "Auditions",  1: "Theater", 2: "Sports", 
        3: "Admissions", 4: "Concert", 5:"Other"}

class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    location = db.relationship('Location') 
    time = db.Column(db.DateTime)
    link = db.Column(db.String(200))
    description = db.Column(db.Text)
    category = db.Column(db.Integer)
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)

    def __init__(self, name, location, time, link, description, category, lat=0.0, lon=0.0):
        self.name = name
        self.location = location
        self.time = time
        self.link = link
        self.description = description
        self.category = category
        self.lat = lat
        self.lon = lon

    def __repr__(self):
        return '<Event %s>' % self.name


class Location(db.Model):
    __tablename__ = 'location'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    short_name = db.Column(db.String(50))
    addr = db.Column(db.String(100))

    def __init__(self, name, short_name, addr):
        self.name = name
        self.short_name = short_name
        self.addr = addr

    def __repr__(self):
        return '<Location %s>' % self.name


def serialize(locs):
    locations = []
    for loc in locs:
       l = {'name': loc.name}
       locations.append(l)
    return simplejson.dumps(locations)

        
def serialize_events(events):
    evs = []
    for event in events:
        time = '%s,%s,%s,%s,%s' % (event.time.year, event.time.month, event.time.day, event.time.hour, event.time.minute)

        ev = {'name': event.name, 'location': event.location.name,
              'time': time, 'link': event.link,
              'description': event.description,
              'lat': event.lat, 'lon': event.lon,
              'category': cats[event.category]}
        evs.append(ev)
    return simplejson.dumps(evs)


def query_name(pattern, d):
    patterns = pattern.split(" ")
    if d == "location":
        locs = Location.query.all()
        for p in patterns:
            match = []
            for loc in locs:
                if not (loc.name.find(p) == -1):
                    match.append(loc)
            if len(match) > 0:
                locs = match
        return locs[0]
    elif d == "event":
        evs = Event.query.all()
        for p in patterns:
            match = []
            for ev in evs:
                if not (ev.name.find(p) == -1):
                    match.append(ev)
            if len(match) > 0:
                evs = match
        return evs[0]
    return None

@app.route('/')
def index():
#  locations = simplejson.dumps(Location.query.all())
  locations = serialize(Location.query.all())
  #events = ['option_1','option_2','option_3','option_4']
  events = serialize_events(Event.query.all())
  events2 = Event.query.all()
  ite = 0
  for i in events2:
    events2[ite].time = i.time.strftime("%b %e at %I:%M %p") 
    ite += 1 
  categories = ['cat 1','cat 2','cat 3']
  return render_template("index.html", locations = locations, events = events, events2=events2,categories = categories)

# @app.route("/#<regex('.*'):param>")
# def to_pin(param):
    

def add_event(event):
    name = event["name"]
    loc = event["location"]
    if len(loc) == 0: loc = "TBA"
    lat, lon = (0.0, 0.0)
    try:
        lat, lon = Geocoder.geocode(loc + ", Middletown, CT, 06457").coordinates
    except:
        lat, lon = (41.5555, -72.6575)
    tm = str(int(time.mktime(event["time"].timetuple())))
    link = event["link"]
    if len(link) == 0: link = "N/A"
    desc = event["description"]
    cat = event["category"]
    try:
        os.system('curl http://localhost/events?name=' + urllib.quote(str(name)) + '\&location=' + urllib.quote(str(loc)) + '\&time=' + str(tm) + '\&link=' + urllib.quote(str(link)) + '\&description=' + urllib.quote(str(desc)) + '\&category=' + urllib.quote(str(cat)) + '\&latitude=' + str(lat) + '\&longitude=' + str(lon))
    except:
        a=2+2
    # else:
    #     print "EXISTS",name,loc
       # delete_event(exists.name)
       # add_event(event)

def delete_event(event):
    ev = Event.query.filter_by(name=event).first()
    if ev:
        db.session.delete(ev)
        db.session.commit()

if __name__ == "__main__":
  app.debug = True
  app.run()
