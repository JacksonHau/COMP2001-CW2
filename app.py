import connexion
from flask_sqlalchemy import SQLAlchemy
from config import Config

# Create the Connexion application instance
connex_app = connexion.App(__name__, specification_dir='.')
connex_app.add_api('swagger.yml')

# Get the underlying Flask app instance
app = connex_app.app

# Configure the SQLAlchemy part
app.config.from_object(Config)
db = SQLAlchemy(app)

if __name__ == "__main__":
    connex_app.run(debug=True)
