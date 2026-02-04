import json
import os


class RoadmapEngine:
    def __init__(self):
        # We try to load the JSON file. If it doesn't exist, we fallback to empty.
        self.data = self.load_data()

    def load_data(self):
        # This is the "Mock Data" that powers the graph
        # You can expand this JSON list later!
        return {
            "frontend": {
                "nodes": [
                    {"id": "html", "label": "HTML", "level": "beginner"},
                    {"id": "css", "label": "CSS", "level": "beginner"},
                    {"id": "js", "label": "JavaScript", "level": "intermediate"},
                    {"id": "react", "label": "React", "level": "advanced"}
                ],
                "edges": [
                    {"from": "html", "to": "css"},
                    {"from": "css", "to": "js"},
                    {"from": "js", "to": "react"}
                ]
            }
        }

    def get_full_roadmap(self, role):
        # Returns the raw graph for Vis.js
        return self.data.get(role, {})

    def calculate_progress(self, role, completed_skills):
        """
        The "Smart" Checklist Logic:
        1. Mark known skills as completed.
        2. Unlock new skills if prerequisites are met.
        """
        roadmap = self.data.get(role)
        if not roadmap:
            return {"error": "Role not found"}

        nodes = roadmap['nodes']
        edges = roadmap['edges']

        # 1. Identify what is done
        completed_set = set(completed_skills)

        # 2. Build the status response
        annotated_nodes = []
        for node in nodes:
            node_id = node['id']
            status = "locked"

            if node_id in completed_set:
                status = "completed"
            else:
                # Find prerequisites (parents)
                prereqs = [e['from'] for e in edges if e['to'] == node_id]

                # If no prereqs OR all prereqs are done -> It's the Next Step!
                if not prereqs or all(p in completed_set for p in prereqs):
                    status = "next_step"
                else:
                    status = "locked"

            annotated_nodes.append({
                "id": node['id'],
                "status": status,
                "label": node['label']
            })

        return {
            "role": role,
            "progress_graph": annotated_nodes
        }