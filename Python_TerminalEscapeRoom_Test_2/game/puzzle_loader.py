import json

def load_puzzle(puzzle_id):
    with open("puzzles.json", "r", encoding="utf-8") as f:
        puzzles = json.load(f)
    return puzzles.get(puzzle_id, {})
