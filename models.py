from app import db
import datetime


class Trail(db.Model):
    __tablename__ = 'trails'

    trail_id = db.Column(db.Integer, primary_key=True)
    trail_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(1024))
    country_id = db.Column(db.Integer)
    state_id = db.Column(db.Integer)
    city_id = db.Column(db.Integer)
    distance = db.Column(db.Float)
    elevation_gain = db.Column(db.Integer)
    estimated_time = db.Column(db.Integer)
    route_type = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    created_on = db.Column(db.DateTime, default=datetime.datetime.utcnow)


class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    trails = db.relationship('Trail', backref='author', lazy=True)
