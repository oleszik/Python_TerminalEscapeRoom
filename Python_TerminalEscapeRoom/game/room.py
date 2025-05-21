from .room_loader import load_room

class Room:
    def __init__(self, json_path):
        data = load_room(json_path)
        self.name = data["name"]
        self.description_text = data["description"]
        self.objects = data["objects"]
        self.books = data.get("books", {})
        self.required_code = data["required_code"]
        self.gives_key = data.get("gives_key", False)
        self.is_unlocked = False
        self.key_revealed = False

    def describe(self):
        return self.description_text

    def look(self, target):
        target = target.lower()
        if target in self.objects:
            return self.objects[target]
        elif target in self.books:
            return f"{target.title()}: \"{self.books[target]}\""
        return "You don't see anything like that."

    def use(self, item, player):
        item = item.lower()
        if item == "note":
            return self.objects["note"]
        elif item == "painting":
            return "You peel the painting back further… nothing but cold wall."
        elif item == "box":
            return "You turn the dials on the box — ready to enter the code?"
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
