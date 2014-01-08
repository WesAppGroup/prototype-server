from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from pygeocoder import Geocoder
import simplejson
import os
import time
import operator
import urllib

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'
db = SQLAlchemy(app)

locations = {
    "Fauver Apartments": "19 Foss Hill Drive",
    "Foss Hill 5": "57 Foss Hill Drive",
    "Wasch Center for Retired Faculty": "51 Lawn Avenue",
    "Rehearsal Hall": "283 Washington Terrace",
    "North College": "237 High Street",
    "Romance Languages and Literatures": "300 High Street",
    "Human Resources": "212 College Street",
    "WesWings at 156 High": "156 High Street",
    "Softball Field": "Softball Field",
    "Art Studio South": "283  Washington Terrace",
    "CFA Film Studies": "301  Washington Terrace",
    "Memorial Chapel": "221 High Street",
    "Art Workshops": "283  Washington Terrace",
    "Public Affairs Center": "238 Church Street",
    "PAC": "228 Church Street",
    "Harriman Hall": "238 Church Street",
    "Center for the Americas ": "255 High Street",
    "Fisk Hall": "262 High Street",
    "Senior Townhouses": "20 A/B/C Fountain Ave",
    "Weshop/ Foss Hill 1-Westco": "18 Foss Hill Drive",
    "Investment Office": "74 Wyllys Avenue",
    "CFA Music Studios": "283  Washington Terrace",
    "Smith Field": "Smith Field",
    "Russell House": "350 High Street",
    "Cady Building &#8211; Facilities Office": "170 Long Lane",
    "CFA Cinema": "283  Washington Terrace",
    "President&#8217;s House": "269 High Street",
    "Davison Art Library": "301 High Street",
    "Hall - Atwater": "Hall - Atwater",
    "Fauver Frosh": "35 Foss Hill Drive",
    "Exley Science Center": "265 Church Street",
    "ESC": "265 Church Street",
    "Art Studio North": "283  Washington Terrace",
    "Graduate Liberal Studies Program": "184 High Street",
    "Fayerweather": "45 Wyllys Avenue",
    "Beckam Hall": "45 Wyllys Avenue",
    "Davidson Health Center": "327 High Street",
    "The Bayit": "157 Church Street",
    "CFA Theater": "271  Washington Terrace",
    "Zilkha Gallery": "283  Washington Terrace",
    "Mansfield Freeman Center for East Asian Studies": "343  Washington Terrace",
    "Judd Hall": "207 High Street",
    "Public Safety": "208 High Street",
    "Clark Hall": "268 Church Street",
    "Usdan University Center": "43 Wyllys Avenue",
    "Center for Humanities": "95 Pearl Street",
    "Butterfield Colleges": "Butterfield Colleges",
    "Shanklin Laboratory": "237 Church Street",
    "Freeman Athletic Center": "161 Cross Street",
    "Van Vleck Observatory": "96 Foss Hill",
    "Upward Bound": "41 Lawn Avenue",
    "South College": "229 High Street",
    "Crowell Concert Hall": "283  Washington Terrace",
    "Alpha Delta Phi": "185 Church Street",
    "Broad Street Books": "45 Broad Street",
    "World Music Hall": "283  Washington Terrace",
    "Davidson Art Center": "301 High Street",
    "Center for African American Studies (Malcolm X House)": "343 High Street",
    "Dance Studio": "247 Pine Street",
    "University Relations/The Wesleyan Fund": "164 Mount Vernon Street",
    "Patricelli 92 Theater": "213 High Street",
    "English Department": "285 Court Street",
    "Alumni Office": "330 High Street",
    "Olin Library": "252 Church Street",
    "Office of Admission": "70 Wyllys Avenue",
    "Steward M. Reid House": "70 Wyllys Avenue",
    "Center for Community Partnerships/Chaplains Offices": "167/169 High Street",
    "Downey House": "294 High Street",
    "John Woods Memorial Tennis Courts": "Vine Street",
    "Unknown": "Foss Hill",
    "Home": "Foss Hill",
    "Away": "Foss Hill",
    "Neutral": "Foss Hill",
    "Multi-Use": "Usdan",
    "Wasch Center": "wasch center middletown ct",
    "Astronomy": "Van Vleck Observatory",
    "Malcom X House":"345 High Street"
}



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

        
# def serialize_events(events):
#     evs = []
#     for event in events:
#         time = '%s,%s,%s,%s,%s' % (event.time.year, event.time.month, event.time.day, event.time.hour, event.time.minute)

#         ev = {'name': event.name, 'location': event.location.name,
#               'time': time, 'link': event.link,
#               'description': event.description,
#               'lat': event.lat, 'lon': event.lon,
#               'category': cats[event.category]}
#         evs.append(ev)
#     return simplejson.dumps(evs)


def query_name(pattern, d, locations):
    patterns = pattern.split(" ")
    if d == "location":
        if pattern in locations:
            return locations[pattern]
        elif pattern == "":
            return pattern
        locs = locations
        best = ""
        bestMatches = {}
        for p in patterns:
            match = []
            for loc in locs:
                if not (loc.lower().find(p.lower()) == -1):
                    if loc not in bestMatches:
                        bestMatches[loc] = 0
                    else:
                        bestMatches[loc] += 1
            if bestMatches:
                best = max(bestMatches.iteritems(), key=operator.itemgetter(1))[0]
                # print "BEST = ",best
                return best
            else:
                # print "no good match"
                return pattern


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
    locRaw = event["location"]
    loc = query_name(locRaw,'location',locations)
    if len(loc) == 0: 
        loc = "TBA"
        print "No location data, defaulting to foss"
        lat, lon = (41.5555971, -72.65834300000002)
    else:
        try:
            lat, lon = Geocoder.geocode(loc + ", Middletown, CT, 06457").coordinates
        except:
            print "defaulting to foss"
            lat, lon = (41.5555971, -72.65834300000002)
    tm = str(int(time.mktime(event["time"].timetuple())))
    link = event["link"]
    if len(link) == 0: 
        link = "N/A"
    desc = event["description"]
    cat = event["category"]
    try:
        os.system('curl http://localhost/events?name=' + urllib.quote(str(name)) + '\&location=' + urllib.quote(str(loc)) + '\&time=' + str(tm) + '\&link=' + urllib.quote(str(link)) + '\&description=' + urllib.quote(str(desc)) + '\&category=' + urllib.quote(str(cat)) + '\&latitude=' + str(lat) + '\&longitude=' + str(lon))
    except:
        pass
    print lat,lon


def delete_event(event):
    ev = Event.query.filter_by(name=event).first()
    if ev:
        db.session.delete(ev)
        db.session.commit()

if __name__ == "__main__":
  app.debug = True
  app.run()
