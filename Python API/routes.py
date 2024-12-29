from flask import request, jsonify
from db import get_db_connection, close_db_connection

def list_trails():
    conn = get_db_connection()
    if not conn:
        return jsonify({'message': 'Database connection failed'}), 500

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM CW2.Trail")
    trails = cursor.fetchall()
    trail_list = [{'trail_id': trail[0], 'trail_name': trail[1], 'description': trail[2], 'country_id': trail[3],
                   'state_id': trail[4], 'city_id': trail[5], 'distance': trail[6], 'elevation_gain': trail[7],
                   'estimated_time': trail[8], 'route_type': trail[9], 'user_id': trail[10], 'created_on': trail[11]}
                  for trail in trails]
    close_db_connection(conn)
    return jsonify(trail_list), 200

def create_trail():
    data = request.get_json()
    conn = get_db_connection()
    if not conn:
        return jsonify({'message': 'Database connection failed'}), 500

    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO CW2.Trail (trail_name, description, country_id, state_id, city_id, distance, elevation_gain, 
            estimated_time, route_type, user_id, created_on) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, GETDATE())
        """, (data['trail_name'], data['description'], data['country_id'], data['state_id'], data['city_id'],
              data['distance'], data['elevation_gain'], data['estimated_time'], data['route_type'], data['user_id']))
        conn.commit()
    except Exception as e:
        close_db_connection(conn)
        return jsonify({'message': 'Failed to create trail', 'error': str(e)}), 400

    close_db_connection(conn)
    return jsonify({'message': 'Trail created successfully'}), 201

def get_trail_by_id(trail_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({'message': 'Database connection failed'}), 500

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM CW2.Trail WHERE trail_id = ?", (trail_id,))
    trail = cursor.fetchone()
    if trail is None:
        close_db_connection(conn)
        return jsonify({'message': 'Trail not found'}), 404

    trail_data = {col[0]: trail[idx] for idx, col in enumerate(cursor.description)}
    close_db_connection(conn)
    return jsonify(trail_data), 200

def update_trail(trail_id):
    data = request.get_json()
    conn = get_db_connection()
    if not conn:
        return jsonify({'message': 'Database connection failed'}), 500

    cursor = conn.cursor()
    update_parts = ', '.join([f"{key} = ?" for key in data.keys()])
    values = list(data.values())
    values.append(trail_id)
    cursor.execute(f"UPDATE CW2.Trail SET {update_parts} WHERE trail_id = ?", values)
    if cursor.rowcount == 0:
        close_db_connection(conn)
        return jsonify({'message': 'Trail not found'}), 404

    conn.commit()
    close_db_connection(conn)
    return jsonify({'message': 'Trail updated successfully'}), 200

def delete_trail(trail_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({'message': 'Database connection failed'}), 500

    cursor = conn.cursor()
    cursor.execute("DELETE FROM CW2.Trail WHERE trail_id = ?", (trail_id,))
    if cursor.rowcount == 0:
        close_db_connection(conn)
        return jsonify({'message': 'Trail not found'}), 404

    conn.commit()
    close_db_connection(conn)
    return jsonify({'message': 'Trail deleted successfully'}), 204
