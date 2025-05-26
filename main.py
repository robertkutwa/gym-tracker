from gym_tracker.database import init_db
from gym_tracker.cli import menu

if __name__ == "__main__":
    init_db()
    menu()