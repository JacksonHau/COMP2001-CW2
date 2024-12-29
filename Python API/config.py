import pathlib
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import urllib.parse

basedir = pathlib.Path(__file__).parent.resolve()

# Set up Connexion
connex_app = connexion.App(__name__, specification_dir=basedir)

# Determine environment (local or production)
LOCAL = False

# Database configuration
server = "DIST-6-505.uopnet.plymouth.ac.uk"
database = 'COMP2001_JHau'
username = "JHau"
driver = "ODBC+Driver+17+for+SQL+Server"
password = "FxuM888+"

# Create the Flask instance from Connexion
app = connex_app.app
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mssql+pyodbc://{username}:{urllib.parse.quote_plus(password)}@{server}/{database}"
    f"?driver={driver}"
    "&Encrypt=yes"
    "&TrustServerCertificate=yes"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)
