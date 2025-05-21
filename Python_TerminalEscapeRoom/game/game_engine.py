from .room import Room
from .player import Player

def load_ascii_art():
    try:
        with open("assets/ascii_art.txt", "r", encoding="utf-8") as f:
            print(f.read())
    except FileNotFoundError:
        print("Welcome to the Escape Room!")

def start_game():
    load_ascii_art()
    player = Player()
    room = Room("rooms/study.json")
    print("Type 'help' for a list of commands.\n")
    print(room.describe())
    while True:
        command = input("> ").strip().lower()
        if command == "quit":
            print("Goodbye!")
            break
        elif command == "help":
            print("Commands: look [object], use [item], enter [code], inventory, quit")
        elif command == "look":
            print(room.describe())
        elif command.startswith("look "):
            print(room.look(command[5:]))
        elif command.startswith("use "):
            print(room.use(command[4:], player))
            if room.is_unlocked:
                print("🎉 You escaped the study room! Well done.")
                break
        elif command.startswith("enter "):
            code = command[6:]
            response = room.enter_code(code)
            print(response)
            if "key" in response.lower():
                player.add_item("key")
        elif command == "inventory":
            print(player.show_inventory())
        else:
            print("❓ Unknown command. Type 'help' for options.")
