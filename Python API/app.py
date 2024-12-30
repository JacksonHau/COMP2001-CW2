from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flasgger import Swagger
import logging

from CRUD import create_trail, read_trail, update_trail, delete_trail

app = Flask(__name__)
api = Api(app)
swagger = Swagger(app)

logging.basicConfig(level=logging.DEBUG)

class TrailResource(Resource):
    def create(self, trail_id):
        """Retrieve a trail by its ID."""
        trail, status = read_trail(trail_id)
        return jsonify(trail), status

    def read(self):
        """Create a new trail."""
        trail_data = request.get_json()
        result, status = create_trail(trail_data)
        return jsonify(result), status

    def update(self, trail_id):
        """Update an existing trail."""
        trail_data = request.get_json()
        result, status = update_trail(trail_id, trail_data)
        return jsonify(result), status

    def delete(self, trail_id):
        """Delete a trail by its ID."""
        result, status = delete_trail(trail_id)
        return jsonify(result), status

api.add_resource(TrailResource, '/trails/<int:trail_id>')

if __name__ == '__main__':
    app.run(debug=True)