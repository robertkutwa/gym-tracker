# gym_tracker/cli.py

from gym_tracker.models import User, Workout, Exercise
from gym_tracker.database import session


def list_users():
    users = session.query(User).all()
    for user in users:
        print(f"{user.id}: {user.name}")


def add_user():
    name = input("Enter user name: ")
    new_user = User(name=name)
    session.add(new_user)
    session.commit()
    print("User added.")


def log_workout():
    list_users()
    try:
        user_id = int(input("Select user ID: "))
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    date = input("Enter workout date (YYYY-MM-DD): ")
    workout = Workout(date=date, user_id=user_id)
    session.add(workout)
    session.commit()
    print("Workout logged.")


def log_exercise():
    try:
        workout_id = int(input("Enter workout ID: "))
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    name = input("Exercise name: ")
    try:
        sets = int(input("Number of sets: "))
        reps = int(input("Reps per set: "))
    except ValueError:
        print("Invalid input. Sets and reps must be numbers.")
        return

    exercise = Exercise(name=name, sets=sets, reps=reps, workout_id=workout_id)
    session.add(exercise)
    session.commit()
    print("Exercise logged.")


def view_workouts():
    try:
        user_id = int(input("Enter user ID to view workouts: "))
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    user = session.query(User).get(user_id)
    if not user:
        print("User not found.")
        return

    print(f"\n--- Workouts for {user.name} ---")
    for workout in user.workouts:
        print(f"\nDate: {workout.date}")
        for ex in workout.exercises:
            print(f" - {ex.name}, {ex.sets}x{ex.reps}")


def menu():
    while True:
        print("\n--- Gym Tracker ---")
        print("1. List Users")
        print("2. Add User")
        print("3. Log Workout")
        print("4. Log Exercise")
        print("5. View Workouts")
        print("6. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            list_users()
        elif choice == '2':
            add_user()
        elif choice == '3':
            log_workout()
        elif choice == '4':
            log_exercise()
        elif choice == '5':
            view_workouts()
        elif choice == '6':
            break
        else:
            print("Invalid option.")