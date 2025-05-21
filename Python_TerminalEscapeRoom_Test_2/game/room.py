from .room_loader import load_room
from .puzzle_engine import PuzzleEngine

class Room:
    def __init__(self, json_path):
        data = load_room(json_path)
        puzzle_engine = PuzzleEngine()
        puzzle = puzzle_engine.get(data["puzzle_id"])

        self.name = data["name"]
        self.puzzle_id = data["puzzle_id"]
        self.description_text = puzzle["description"]

        self.objects = data["objects"]
        self.books = puzzle.get("books", {})
        self.required_code = puzzle.get("required_code", "")
        self.note_text = puzzle.get("note", "")
        self.gives_key = data.get("gives_key", False)

        self.is_unlocked = False
        self.key_revealed = False

        # Setup alias map
        self.alias_map = {}
        for canonical, words in data.get("aliases", {}).items():
            for alias in words:
                self.alias_map[alias.lower()] = canonical
                self.alias_map[alias.lower().replace(" ", "")] = canonical  # support 'metalbox'

    def describe(self):
        return self.description_text

    def look(self, target):
        target = target.lower().strip()
        if target in self.alias_map:
            target = self.alias_map[target]

        if target in self.objects:
            return self.objects[target]

        elif target in self.books:
            return f"{target.title()}: \"{self.books[target]}\""

        elif target == "books":
            book_list = "\n".join(
                f"- {author.title()}: \"{title}\"" for author, title in self.books.items()
            )
            return (
                "You scan the bookshelf and find these titles:\n" +
                book_list +
                "\nTry 'look [author]' to examine one."
            )

        return "You don't see anything like that."

    def use(self, item, player):
        item = item.lower().strip()
        if item in self.alias_map:
            item = self.alias_map[item]

        if item == "note":
            return self.note_text
        elif item == "painting":
            return "You peel the painting back further… nothing but cold wall."
        elif item == "box":
            return (
                "You examine the mechanical box closely. The dials are responsive.\n"
                "You can try entering a code with: 'enter [code]'"
            )
        elif item == "key":
            if "key" in player.inventory:
                self.is_unlocked = True
                return "🔓 You insert the key into a small hidden slot. The iron door unlocks with a deep click!"
            else:
                return "You don’t have a key."

        return "You can't use that here."

    def enter_code(self, code):
        if code.upper() == self.required_code:
            if self.gives_key and not self.key_revealed:
                self.key_revealed = True
                return (
                    "✅ The box clicks open with a mechanical whir.\n"
                    "Inside lies a small iron key — you take it and add it to your inventory."
                )
            elif self.gives_key and self.key_revealed:
                return "The box is already open. You already took the key."
            else:
                self.is_unlocked = True
                return "✅ The code was correct! The door unlocks immediately."
        else:
            return "❌ Nothing happens. Maybe that’s the wrong code."