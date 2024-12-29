from db import get_db_connection, close_db_connection

# List of Trails
def list_trails():
    conn = get_db_connection()
    if conn is None:
        return {"message": "Database connection failed"}, 500

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM CW2.Trail")
    trails = cursor.fetchall()
    trails_list = [{'trail_id': trail[0], 'trail_name': trail[1], 'description': trail[2]} for trail in trails]
    close_db_connection(conn)
    return trails_list, 200

# Create Trails
def create_trail(trail_data):
    conn = get_db_connection()
    if conn is None:
        return {"message": "Database connection failed"}, 500

    cursor = conn.cursor()
    sql = """INSERT INTO CW2.Trail (trail_name, description) VALUES (?, ?)"""
    cursor.execute(sql, (trail_data['trail_name'], trail_data['description']))
    conn.commit()
    close_db_connection(conn)
    return {"message": "Trail created successfully"}, 201

# Get trail by ID
def get_trail_by_id(trail_id):
    conn = get_db_connection()
    if conn is None:
        return {"message": "Database connection failed"}, 500

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM CW2.Trail WHERE trail_id = ?", trail_id)
    trail = cursor.fetchone()
    if not trail:
        close_db_connection(conn)
        return {"message": "Trail not found"}, 404

    trail_data = {
        'trail_id': trail[0],
        'trail_name': trail[1],
        'description': trail[2],
        'country_id': trail[3],
        'state_id': trail[4],
        'city_id': trail[5],
        'distance': trail[6],
        'elevation_gain': trail[7],
        'estimated_time': trail[8],
        'route_type': trail[9],
        'user_id': trail[10],
        'created_on': trail[11].strftime('%Y-%m-%d') if trail[11] else None
    }
    close_db_connection(conn)
    return trail_data, 200

# Update Trail
def update_trail(trail_id):
    conn = get_db_connection()
    if conn is None:
        return {"message": "Database connection failed"}, 500

    data = request.get_json()
    cursor = conn.cursor()
    update_parts = [f"{key} = ?" for key in data.keys()]
    update_query = f"UPDATE CW2.Trail SET {', '.join(update_parts)} WHERE trail_id = ?"
    update_values = list(data.values()) + [trail_id]

    cursor.execute(update_query, update_values)
    conn.commit()
    if cursor.rowcount == 0:
        close_db_connection(conn)
        return {"message": "Trail not found"}, 404

    close_db_connection(conn)
    return {"message": "Trail updated successfully"}, 200

# Delete Trail
def delete_trail(trail_id):
    conn = get_db_connection()
    if conn is None:
        return {"message": "Database connection failed"}, 500

    cursor = conn.cursor()
    cursor.execute("DELETE FROM CW2.Trail WHERE trail_id = ?", trail_id)
    conn.commit()
    if cursor.rowcount == 0:
        close_db_connection(conn)
        return {"message": "Trail not found"}, 404

    close_db_connection(conn)
    return {"message": "Trail deleted successfully"}, 204