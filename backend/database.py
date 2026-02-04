import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Random@777",
    database="roadmap_db"
)

def get_user_skills(user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT skill_id FROM user_progress WHERE user_id = %s", (user_id,))
    skills = [row[0] for row in cursor.fetchall()]
    cursor.close()
    return skills


def save_progress(user_id, skill_id):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO user_progress (user_id, skill_id) VALUES (%s, %s)",
        (user_id, skill_id)
    )
    conn.commit()
    cursor.close()