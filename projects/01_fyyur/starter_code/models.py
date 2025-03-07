from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

migrate = Migrate(app, db)

class Venue(db.Model):
    __tablename__ = 'Venue'

    #add nullable to several columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable = False)
    genres = db.Column(db.ARRAY(db.String)) #addeed field
    city = db.Column(db.String(120), nullable = False)
    state = db.Column(db.String(120), nullable = False)
    address = db.Column(db.String(120), nullable = False)
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500), nullable = False)
    website = db.Column(db.String()) #added field
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean) #added field
    seeking_description = db.Column(db.String()) #added field;
    shows = db.relationship('Show', backref = 'venue', lazy = True)

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable = False)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String))
    image_link = db.Column(db.String(500), nullable = False)
    website = db.Column(db.String()) #added field
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, nullable = False) #added field
    seeking_description = db.Column(db.String()) #added field
    shows = db.relationship('Show', backref = 'artist', lazy = True)

class Show(db.Model):
    __tablename__ = 'Show'
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable =False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable =False)
