from flask import Flask, request, jsonify
from graph_engine import RoadmapEngine
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
engine = RoadmapEngine()


@app.route('/')
def home():
    return "<h1>Roadmap Backend Running 🚦</h1>"


# Endpoint 1: Get the visual graph (for the teammate doing the Frontend graph)
@app.route('/roadmap/<role>', methods=['GET'])
def get_roadmap(role):
    data = engine.get_full_roadmap(role)
    return jsonify(data)


# Endpoint 2: The Checklist Logic (The 'Brain' of your feature)
@app.route('/update-progress', methods=['POST'])
def update_progress():
    # Frontend sends: { "role": "frontend", "completed": ["html", "css"] }
    data = request.json
    role = data.get('role')
    completed_skills = data.get('completed', [])

    # Calculate what to learn next
    result = engine.calculate_progress(role, completed_skills)

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)