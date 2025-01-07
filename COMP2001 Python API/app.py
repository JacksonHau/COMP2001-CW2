from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_swagger_ui import get_swaggerui_blueprint
from datetime import timedelta
from marshmallow import Schema, fields, ValidationError, pre_load
from sqlalchemy import text
import logging

# Flask App Initialization
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

# Swagger Configuration
app.config['SWAGGER'] = {
    "title": "Trail API",
    "uiversion": 3
}

# Swagger UI Setup
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Models
class User(db.Model):
    __tablename__ = 'Users'
    __table_args__ = {'schema': 'CW2'}
    User_ID = db.Column(db.Integer, primary_key=True)
    Email = db.Column(db.String(255), unique=True, nullable=False)
    Password = db.Column(db.String(255), nullable=False)
    Name = db.Column(db.String(100))
    Created_On = db.Column(db.Date, nullable=False)

class Trail(db.Model):
    __tablename__ = 'Trail'
    __table_args__ = {'schema': 'CW2'}
    Trail_ID = db.Column(db.Integer, primary_key=True)
    Trail_Name = db.Column(db.String(255), nullable=False)
    Description = db.Column(db.Text, nullable=True)
    Country_ID = db.Column(db.Integer, nullable=False)
    State_ID = db.Column(db.Integer, nullable=False)
    City_ID = db.Column(db.Integer, nullable=False)
    Distance = db.Column(db.Float, nullable=False)
    Elevation_Gain = db.Column(db.Float, nullable=True)
    Estimated_Time = db.Column(db.Integer, nullable=False)
    Route_Type = db.Column(db.String(100), nullable=False)
    User_ID = db.Column(db.Integer, nullable=False)

class TrailSchema(Schema):
    Trail_Name = fields.String(required=True)
    Description = fields.String()
    Country_ID = fields.Integer(required=True)
    State_ID = fields.Integer(required=True)
    City_ID = fields.Integer(required=True)
    Distance = fields.Float(required=True)
    Elevation_Gain = fields.Float(required=False)
    Estimated_Time = fields.Integer(required=True)
    Route_Type = fields.String(required=True)
    User_ID = fields.Integer(required=True)

    @pre_load
    def process_data(self, data, **kwargs):
        # Ensure description is a string or null
        data["Description"] = str(data.get("Description", "")) if data.get("Description") else None
        return data

# Routes
@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([{"User_ID": u.User_ID, "Email": u.Email, "Name": u.Name} for u in users])

# Log in endpoint
@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        logging.debug(f"Received data: {data}")

        email = data.get("Email")  
        password = data.get("Password")  

        if not email or not password:
            logging.warning("Missing email or password in the request")
            return jsonify({"message": "Missing email or password"}), 400

        user = User.query.filter_by(Email=email).first()
        if not user or user.Password != password: 
            return jsonify({"message": "Invalid email or password"}), 401

        access_token = create_access_token(identity={"User_ID": user.User_ID})
        return jsonify({"access_token": access_token}), 200

    except Exception as e:
        logging.error(f"Error during login: {e}")
        return jsonify({"message": "An error occurred during login"}), 500

@app.route("/trails", methods=["GET"])
@jwt_required()
def get_trails():
    trails = Trail.query.all()
    return jsonify([{col.name: getattr(t, col.name) for col in Trail.__table__.columns} for t in trails])

@app.route("/trails", methods=["POST"])
@jwt_required()
def insert_trail():
    try:
        data = request.get_json()
        logging.debug(f"Received data: {data}")
        trail_data = TrailSchema().load(data)  # Validation happens here
    except ValidationError as err:
        logging.error(f"Validation error: {err.messages}")
        return jsonify({"errors": err.messages}), 422
    except Exception as e:
        logging.error(f"Unexpected error during validation: {e}")
        return jsonify({"message": "Invalid request data"}), 400

    try:
        stmt = text("""
            EXEC CW2.InsertTrail 
                @Trail_Name = :Trail_Name,
                @Description = :Description,
                @Country_ID = :Country_ID,
                @State_ID = :State_ID,
                @City_ID = :City_ID,
                @Distance = :Distance,
                @Elevation_Gain = :Elevation_Gain,
                @Estimated_Time = :Estimated_Time,
                @Route_Type = :Route_Type,
                @User_ID = :User_ID
        """)
        db.session.execute(stmt, trail_data)
        db.session.commit()
        logging.info("Trail successfully inserted into the database.")
        return jsonify({"message": "Trail inserted successfully"}), 201
    except Exception as e:
        logging.error(f"Database error: {e}")
        return jsonify({"message": "An error occurred while inserting the trail"}), 500

@app.route("/trails/<int:trail_id>", methods=["GET"])
@jwt_required()
def get_trail_by_id(trail_id):
    trail = Trail.query.get(trail_id)
    if not trail:
        return jsonify({"message": "Trail not found"}), 404
    return jsonify({col.name: getattr(trail, col.name) for col in Trail.__table__.columns})

@app.route("/trails/<int:trail_id>", methods=["PUT"])
@jwt_required()
def update_trail(trail_id):
    trail = Trail.query.get(trail_id)
    if not trail:
        return jsonify({"message": "Trail not found"}), 404

    data = request.get_json()
    for key, value in data.items():
        if hasattr(trail, key):
            setattr(trail, key, value)
    db.session.commit()
    return jsonify({"message": "Trail updated successfully."}), 200

@app.route("/trails/<int:trail_id>", methods=["DELETE"])
@jwt_required()
def delete_trail(trail_id):
    trail = Trail.query.get(trail_id)
    if not trail:
        return jsonify({"message": "Trail not found"}), 404

    try:
        db.session.delete(trail)
        db.session.commit()
        return jsonify({"message": "Trail deleted successfully."}), 200
    except Exception as e:
        logging.error(f"Error deleting trail: {e}")
        return jsonify({"message": "An error occurred while deleting the trail."}), 500

if __name__ == '__main__':
    print("Starting the application...")
    print("Swagger documentation available at: http://127.0.0.1:5000/swagger")
    print("Login endpoint available at: http://127.0.0.1:5000/login")
    app.run(host="127.0.0.1", port=5000, debug=True)