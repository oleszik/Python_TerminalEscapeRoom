import json

class PuzzleEngine:
    def __init__(self, json_path="puzzles.json"):
        self.puzzles = self._load_puzzles(json_path)

    def _load_puzzles(self, path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def get(self, puzzle_id):
        return self.puzzles.get(puzzle_id, {})

    def list_ids(self):
        return list(self.puzzles.keys())

    # (Optional) track puzzle state if needed later
    def is_valid_code(self, puzzle_id, code):
        puzzle = self.get(puzzle_id)
        return puzzle.get("required_code", "").upper() == code.upper()
