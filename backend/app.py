from flask import Flask, render_template, request, jsonify
from graph_engine import RoadmapEngine

app = Flask(__name__)
engine = RoadmapEngine()

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/suggest')
def suggest():
    query = request.args.get('q', '')
    return jsonify(engine.get_suggestions(query))

@app.route('/preview')
def preview():
    skill = request.args.get("skill")
    level = request.args.get("level")
    return jsonify(engine.preview_topics(skill, level))

@app.route('/generate', methods=['POST'])
def generate():
    skill = request.form.get("skill_input")
    level = request.form.get("level")
    known = request.form.getlist("known_skills")
    roadmap = engine.generate(skill, level, known)
    return render_template("roadmap.html", roadmap=roadmap)

if __name__ == '__main__':
    app.run(debug=True)
