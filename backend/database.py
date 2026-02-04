import mysql.connector

# --- CONFIGURATION ---
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',  # Usually 'root'
    'password': 'Scjjanke7#',  # <--- CHANGE THIS TO YOUR REAL PASSWORD
    'database': 'hackathon_db'
}


# ---------------------

def get_connection():
    """Connects to the MySQL database."""
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Exception as e:
        print(f"❌ DATABASE ERROR: {e}")
        return None


def save_progress(user_id, skill_id):
    """Saves a completed skill to the database."""
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        # 'INSERT IGNORE' means: if it's already saved, don't crash, just ignore it.
        sql = "INSERT IGNORE INTO progress (user_id, skill_id) VALUES (%s, %s)"
        cursor.execute(sql, (user_id, skill_id))
        conn.commit()
        conn.close()
        print(f"✅ Saved: {skill_id} for {user_id}")


def get_user_skills(user_id):
    """Fetches all skills the user has finished."""
    conn = get_connection()
    if not conn:
        return []

    cursor = conn.cursor()
    sql = "SELECT skill_id FROM progress WHERE user_id = %s"
    cursor.execute(sql, (user_id,))
    rows = cursor.fetchall()
    conn.close()

    # Convert from [('html',), ('css',)] to ['html', 'css']
    return [row[0] for row in rows]