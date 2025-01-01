from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
)
from flask_swagger_ui import get_swaggerui_blueprint
import logging
from datetime import timedelta

app = Flask(__name__)

# JWT Configuration
app.config["JWT_SECRET_KEY"] = "your-256-bit-secret"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

jwt = JWTManager(app)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://JHau:FxuM888+@dist-6-505.uopnet.plymouth.ac.uk/COMP2001_JHau?driver=ODBC+Driver+17+for+SQL+Server'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Logging Configuration
logging.basicConfig(level=logging.DEBUG)

# Swagger UI setup
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Every Models
class User(db.Model):
    __tablename__ = 'Users'
    __table_args__ = {'schema': 'CW2'}
    User_ID = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(100), unique=True, nullable=False)
    Name = db.Column(db.String(100))
    Created_On = db.Column(db.Date, nullable=False)

class Trail(db.Model):
    __tablename__ = 'Trail'
    __table_args__ = {'schema': 'CW2'}
    Trail_ID = db.Column(db.Integer, primary_key=True)
    Trail_Name = db.Column(db.String(255), nullable=False)
    Description = db.Column(db.Text)
    Country_ID = db.Column(db.Integer)
    State_ID = db.Column(db.Integer)
    City_ID = db.Column(db.Integer)
    Distance = db.Column(db.Float, nullable=False)
    Created_On = db.Column(db.Date, nullable=False)
    Elevation_Gain = db.Column(db.Integer)
    Estimated_Time = db.Column(db.Integer)
    Route_Type = db.Column(db.String(50))
    User_ID = db.Column(db.Integer, db.ForeignKey('CW2.Users.User_ID'), nullable=False)

class TrailPoint(db.Model):
    __tablename__ = 'TrailPoint'
    __table_args__ = {'schema': 'CW2'}
    Point_ID = db.Column(db.Integer, primary_key=True)
    Trail_ID = db.Column(db.Integer, db.ForeignKey('CW2.Trail.Trail_ID'), nullable=False)
    Latitude = db.Column(db.Numeric(9, 6), nullable=False)
    Longitude = db.Column(db.Numeric(9, 6), nullable=False)
    Position = db.Column(db.Integer, nullable=False)

# Routes
@app.route("/", methods=["GET"])
def home():
    return "Welcome to the Trail API. Use /swagger to access API documentation."

# CRUD operations for User
@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([{"User_ID": u.User_ID, "Username": u.Username, "Name": u.Name, "Created_On": str(u.Created_On)} for u in users])

@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    new_user = User(**data)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully."}), 201

if __name__ == '__main__':
    host = '127.0.0.1'
    port = 5000
    swagger_url = f"http://{host}:{port}/swagger"
    
    print(f"Server running at: http://{host}:{port}")
    print(f"Swagger documentation available at: {swagger_url}")
    
    app.run(host=host, port=port, debug=True)