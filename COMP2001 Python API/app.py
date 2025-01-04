from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_swagger_ui import get_swaggerui_blueprint
from sqlalchemy import text
from marshmallow import Schema, fields, pre_load, ValidationError
from datetime import timedelta
import logging

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

# Models
class User(db.Model):
    __tablename__ = 'Users'
    __table_args__ = {'schema': 'CW2'}
    User_ID = db.Column(db.Integer, primary_key=True)
    Email = db.Column(db.String(255), unique=True, nullable=False)
    Password = db.Column(db.String(255), nullable=False)
    Name = db.Column(db.String(100))
    Created_On = db.Column(db.Date, nullable=False)

# Marshmallow Schema for Validation
class TrailSchema(Schema):
    Trail_Name = fields.String(required=True)
    Description = fields.String()
    Country_ID = fields.Integer(required=True)
    State_ID = fields.Integer(required=True)
    City_ID = fields.Integer(required=True)
    Distance = fields.Float(required=True)
    Elevation_Gain = fields.Integer(required=True)
    Estimated_Time = fields.Integer(required=True)
    Route_Type = fields.String(required=True)
    User_ID = fields.Integer(required=True)

    @pre_load
    def process_data(self, data, **kwargs):
        # Ensure description is a string or null
        data["Description"] = str(data.get("Description", "")) if data.get("Description") else None
        return data

# Routes
@app.route("/", methods=["GET"])
def home():
    return "Welcome to the Trail API (CW2). Use /swagger to access API documentation."

@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        email = data.get("Email")
        password = data.get("Password")

        if not email or not password:
            return jsonify({"message": "Email and Password are required"}), 400

        user = db.session.query(User).filter(User.Email == email).first()

        if not user or user.Password != password:
            return jsonify({"message": "Invalid email or password"}), 401

        access_token = create_access_token(identity={"User_ID": user.User_ID, "Email": user.Email})
        return jsonify({"access_token": access_token}), 200

    except Exception as e:
        logging.error(f"Error during login: {e}")
        return jsonify({"message": "An error occurred during login"}), 500

@app.route("/trails", methods=["POST"])
@jwt_required()
def insert_trail():
    try:
        data = request.get_json()
        logging.debug(f"Received data: {data}")
        trail_data = TrailSchema().load(data)
    except ValidationError as err:
        logging.error(f"Validation error: {err.messages}")
        return jsonify({"errors": err.messages}), 422

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
        return jsonify({"message": "Trail inserted successfully"}), 201
    except Exception as e:
        logging.error(f"Database error: {e}")
        return jsonify({"message": "An error occurred while inserting the trail"}), 500

@app.route("/trails/read", methods=["GET"])
@jwt_required()
def read_trail():
    try:
        trail_id = request.args.get("Trail_ID")
        trail_name = request.args.get("Trail_Name")
        user_id = request.args.get("User_ID")

        stmt = text("""
            EXEC CW2.ReadTrail 
                @Trail_ID = :Trail_ID,
                @Trail_Name = :Trail_Name,
                @User_ID = :User_ID
        """)
        results = db.session.execute(stmt, {
            "Trail_ID": trail_id,
            "Trail_Name": trail_name,
            "User_ID": user_id
        }).fetchall()

        trails = [dict(row) for row in results]
        return jsonify(trails), 200

    except Exception as e:
        logging.error(f"Error reading trails: {e}")
        return jsonify({"message": "An error occurred while fetching trails"}), 500

@app.route("/trails/delete", methods=["DELETE"])
@jwt_required()
def delete_trail():
    try:
        trail_id = request.args.get("Trail_ID")
        if not trail_id:
            return jsonify({"message": "Trail_ID is required"}), 400

        stmt = text("""
            EXEC CW2.DeleteTrail 
                @Trail_ID = :Trail_ID
        """)
        db.session.execute(stmt, {"Trail_ID": trail_id})
        db.session.commit()
        return jsonify({"message": "Trail deleted successfully"}), 200

    except Exception as e:
        logging.error(f"Error deleting trail: {e}")
        return jsonify({"message": "An error occurred while deleting the trail"}), 500

if __name__ == '__main__':
    print("Starting the application...")
    print("Swagger documentation available at: http://127.0.0.1:5000/swagger")
    print("Login endpoint available at: http://127.0.0.1:5000/login")
    app.run(host="127.0.0.1", port=5000, debug=True)