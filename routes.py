from flask import request, jsonify
from app import app, db
from models import Trail, TrailSchema, User, UserSchema

@app.route('/trails', methods=['GET', 'POST'])
def handle_trails():
    if request.method == 'GET':
        trails = Trail.query.all()
        trail_schema = TrailSchema(many=True)
        return jsonify(trail_schema.dump(trails))
    elif request.method == 'POST':
        new_trail = TrailSchema().load(request.json, session=db.session)
        db.session.add(new_trail)
        db.session.commit()
        return jsonify(TrailSchema().dump(new_trail)), 201

# Additional routes can be added similarly
