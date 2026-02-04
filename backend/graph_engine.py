import json

class RoadmapEngine:
    def __init__(self):
        # Load hierarchical roadmap
        with open("final_roadmaps.json", encoding="utf-8") as f:
            self.data = json.load(f)

    # ------------------------------------------
    # SEARCH SUGGESTIONS
    # ------------------------------------------
    def get_suggestions(self, query):
        results = []

        def search(node):
            for key, val in node.items():
                if query.lower() in key.lower():
                    results.append(key)
                if isinstance(val, dict):
                    search(val)

        search(self.data)
        return results[:5]

    # ------------------------------------------
    # FIND SUBTREE OF SELECTED SKILL
    # ------------------------------------------
    def find_subtree(self, target):
        def dfs(node):
            for key, val in node.items():
                if key == target:
                    return val
                if isinstance(val, dict):
                    found = dfs(val)
                    if found is not None:
                        return found
            return None
        return dfs(self.data)

    # ------------------------------------------
    # FLATTEN TREE WITH DEPTH CONTROL
    # ------------------------------------------
    def flatten_tree(self, tree, depth_limit=None, current_depth=1):
        result = []

        for key, val in tree.items():
            result.append(key)

            if isinstance(val, dict) and val:
                if depth_limit is None or current_depth < depth_limit:
                    result.extend(
                        self.flatten_tree(val, depth_limit, current_depth + 1)
                    )
        return result

    # ------------------------------------------
    # PREVIEW CHECKLIST (for “Do you know this?”)
    # ------------------------------------------
    def preview_topics(self, skill, level):
        subtree = self.find_subtree(skill)
        if subtree is None:
            return []

        if level == "beginner":
            return self.flatten_tree(subtree, depth_limit=2)
        elif level == "intermediate":
            return self.flatten_tree(subtree, depth_limit=3)
        else:
            return self.flatten_tree(subtree)

    # ------------------------------------------
    # FINAL ROADMAP GENERATOR
    # ------------------------------------------
    def generate(self, skill, level, known_skills):
        subtree = self.find_subtree(skill)
        if subtree is None:
            return []

        if level == "beginner":
            roadmap = self.flatten_tree(subtree, depth_limit=2)
        elif level == "intermediate":
            roadmap = self.flatten_tree(subtree, depth_limit=3)
        else:
            roadmap = self.flatten_tree(subtree)

        # Remove topics user already knows
        roadmap = [topic for topic in roadmap if topic not in known_skills]

        return roadmap