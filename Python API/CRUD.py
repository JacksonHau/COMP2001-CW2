import pyodbc

# Database connection function
def get_db_connection():
    try:
        conn = pyodbc.connect(
            'DRIVER={SQL Server};SERVER=DIST-6-505;DATABASE=COMP2001_JHau;UID=JHau;PWD=FxuM888+',
            autocommit=True
        )
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

# Close database connection
def close_db_connection(conn):
    if conn:
        conn.close()

# Create new trail
def create_trail(trail_data):
    conn = get_db_connection()
    if not conn:
        return {"error": "Database connection failed"}, 500

    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO CW2.Trail (trail_name, description, country_id, state_id, city_id,
                                    distance, elevation_gain, estimated_time, route_type, user_id, created_on)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, GETDATE())
        """, (
            trail_data['trail_name'], trail_data['description'], trail_data['country_id'],
            trail_data['state_id'], trail_data['city_id'], trail_data['distance'],
            trail_data['elevation_gain'], trail_data['estimated_time'], trail_data['route_type'],
            trail_data['user_id']
        ))
        conn.commit()
        return {"message": "Trail created successfully"}, 201
    except Exception as e:
        print(f"Error: {str(e)}")
        return {"error": str(e)}, 400
    finally:
        close_db_connection(conn)

# Read a single trail by ID
def read_trail(trail_id):
    conn = get_db_connection()
    if not conn:
        return {"error": "Database connection failed"}, 500

    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM CW2.Trail WHERE trail_id = ?", trail_id)
        trail = cursor.fetchone()
        if trail:
            trail_data = {desc[0]: trail[i] for i, desc in enumerate(cursor.description)}
            return trail_data, 200
        else:
            return {"message": "Trail not found"}, 404
    finally:
        close_db_connection(conn)

# Update a trail
def update_trail(trail_id, trail_data):
    conn = get_db_connection()
    if not conn:
        return {"error": "Database connection failed"}, 500

    cursor = conn.cursor()
    try:
        update_parts = ', '.join([f"{k} = ?" for k in trail_data.keys()])
        values = list(trail_data.values())
        values.append(trail_id)
        cursor.execute(f"UPDATE CW2.Trail SET {update_parts} WHERE trail_id = ?", values)
        conn.commit()
        if cursor.rowcount == 0:
            return {"message": "Trail not found"}, 404
        return {"message": "Trail updated successfully"}, 200
    finally:
        close_db_connection(conn)

# Delete trail
def delete_trail(trail_id):
    conn = get_db_connection()
    if not conn:
        return {"error": "Database connection failed"}, 500

    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM CW2.Trail WHERE trail_id = ?", trail_id)
        conn.commit()
        if cursor.rowcount == 0:
            return {"message": "Trail not found"}, 404
        return {"message": "Trail deleted successfully"}, 204
    finally:
        close_db_connection(conn)
