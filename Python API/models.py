from config import db, ma
from datetime import datetime, timezone

class Trail(db.Model):
    __table_name__ = 'trails'
    __table_args__ = {'schema': 'CW2', "extend_existing": True}

    trail_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    trail_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(1024))
    country_id = db.Column(db.Integer)
    state_id = db.Column(db.Integer)
    city_id = db.Column(db.Integer)
    distance = db.Column(db.Float, nullable=False)
    elevation_gain = db.Column(db.Integer)
    estimated_time = db.Column(db.Integer)
    route_type = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey("CW2.users.user_id"))
    created_on = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    author = db.relationship('User', back_populates='trails')

class User(db.Model):
    __table_name__ = 'users'
    __table_args__ = {'schema': 'CW2', "extend_existing": True}

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    role = db.Column(db.String(100), nullable=False)

    trails = db.relationship('Trail', back_populates='author', lazy=True)

class TrailSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Trail
        sqla_session = db.session
        load_instance = True

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        sqla_session = db.session
        load_instance = True