from flask import Flask, request, jsonify
from flask_cors import CORS
from graph_engine import RoadmapEngine
import database  # <--- IMPORT YOUR NEW FILE

app = Flask(__name__)
CORS(app)
engine = RoadmapEngine()


@app.route('/')
def home():
    return "<h1>Backend Connected to MySQL 🐬</h1>"


# Endpoint 1: Get Roadmap (Now loads SAVED progress!)
@app.route('/roadmap/<role>', methods=['GET'])
def get_roadmap(role):
    user_id = "demo_user"  # Hackathon shortcut: Everyone is "demo_user"

    # 1. Get the graph structure
    full_graph = engine.get_full_roadmap(role)

    # 2. Get completed skills from MySQL
    completed_skills = database.get_user_skills(user_id)

    # 3. Calculate what is next
    result = engine.calculate_progress(role, completed_skills)

    return jsonify(result)


# Endpoint 2: Update Progress (Now SAVES to MySQL!)
@app.route('/update-progress', methods=['POST'])
def update_progress():
    data = request.json
    role = data.get('role')
    new_skill = data.get('skill_id')
    user_id = "demo_user"

    # 1. Save the new skill to MySQL
    if new_skill:
        database.save_progress(user_id, new_skill)

    # 2. Re-calculate the path
    completed_skills = database.get_user_skills(user_id)
    result = engine.calculate_progress(role, completed_skills)

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)