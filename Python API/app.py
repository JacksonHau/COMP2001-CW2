import connexion
from flask_sqlalchemy import SQLAlchemy

connex_app = connexion.App(__name__, specification_dir='.')
connex_app.add_api('swagger.yml')  # Add Swagger file to the app

# Get the underlying Flask app instance
app = connex_app.app

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

if __name__ == '__main__':
    app.run(debug=True)