from .room import Room
from .player import Player
from .room_loader import load_room


def load_ascii_art():
    try:
        with open("assets/ascii_art.txt", "r", encoding="utf-8") as f:
            print(f.read())
    except FileNotFoundError:
        print("Welcome to the Escape Room!")

def start_game():
    load_ascii_art()
    player = Player()
    current_room_path = "rooms/study.json"
    room = Room(current_room_path)

    print("Type 'help' for a list of commands.\n")
    print(room.describe())

    while True:
        command = input("> ").strip().lower()

        if command == "quit":
            print("Goodbye!")
            break

        elif command == "help":
            print("Commands: look [object], use [item], enter [code], go [room], inventory, quit")

        elif command == "look":
            print(room.describe())

        elif command.startswith("look "):
            print(room.look(command[5:]))

        elif command.startswith("use "):
            print(room.use(command[4:], player))
            if room.is_unlocked:
                print("🎉 The door swings open with a groan...")
                print("📚 You step into the musty, dimly lit library. Shadows stretch across endless shelves.")
                # Automatically move to next room if available
                next_rooms = getattr(room, "next_rooms", {})
                if "library" in next_rooms:
                    requirement = next_rooms["library"].get("unlocked_by")
                    if requirement in player.inventory:
                        current_room_path = "rooms/library.json"
                        room = Room(current_room_path)
                        print("\nYou move into the library...\n")
                        print(room.describe())

        elif command.startswith("enter "):
            code = command[6:]
            response = room.enter_code(code)
            print(response)
            if "key" in response.lower():
                player.add_item("key")

        elif command.startswith("go "):
            destination = command[3:]
            next_rooms = getattr(room, "next_rooms", {})
            if destination in next_rooms:
                requirement = next_rooms[destination].get("unlocked_by")
                if requirement in player.inventory:
                    current_room_path = f"rooms/{destination}.json"
                    room = Room(current_room_path)
                    print(f"\nYou move into the {destination}...\n")
                    print(room.describe())
                else:
                    print(f"You can't go to {destination} yet. You need: {requirement}")
            else:
                print("You can't go there from here.")

        elif command == "inventory":
            print(player.show_inventory())

        else:
            print("❓ Unknown command. Type 'help' for options.")
