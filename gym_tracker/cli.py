from gym_tracker.models import User, Workout, Exercise
from gym_tracker.database import session
from tabulate import tabulate
import csv


def list_users():
    """List all users in the database."""
    session.expire_all()  
    users = session.query(User).all()
    if not users:
        print("No users found.")
        return

    print("\n--- Users ---")
    for user in users:
        print(f"{user.id}: {user.name}")


def add_user():
    """Add a new user to the database."""
    name = input("Enter user name: ").strip()
    if not name:
        print("User name cannot be empty.")
        return

    new_user = User(name=name)
    session.add(new_user)
    try:
        session.commit()
        print(f"User '{name}' added.")
    except Exception as e:
        session.rollback()
        print(f"Failed to add user. Error: {e}")


def log_workout():
    """Log a new workout for an existing user."""
    list_users()
    try:
        user_id = int(input("Select user ID: "))
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        return

    user = session.query(User).get(user_id)
    if not user:
        print("User not found.")
        return

    date = input("Enter workout date (YYYY-MM-DD): ").strip()
    workout = Workout(date=date, user_id=user_id)
    session.add(workout)
    try:
        session.commit()
        print(f"Workout logged for {user.name} on {date}.")
    except Exception as e:
        session.rollback()
        print(f"Failed to log workout. Error: {e}")


def log_exercise():
    """Log a new exercise under an existing workout."""
    try:
        workout_id = int(input("Enter workout ID: "))
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        return

    workout = session.query(Workout).get(workout_id)
    if not workout:
        print("Workout not found.")
        return

    name = input("Exercise name: ").strip()
    try:
        sets = int(input("Number of sets: "))
        reps = int(input("Reps per set: "))
    except ValueError:
        print("Sets and reps must be numbers.")
        return

    exercise = Exercise(name=name, sets=sets, reps=reps, workout_id=workout_id)
    session.add(exercise)

    try:
        session.commit()
        print(f"Logged '{name}', {sets}x{reps} for workout ID {workout_id}.")
    except Exception as e:
        session.rollback()
        print(f"Failed to save exercise. Error: {e}")
        print("Tip: Make sure the workout ID exists.")


def view_workouts():
    """View all workouts and their exercises for a given user."""
    try:
        user_id = int(input("Enter user ID to view workouts: "))
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        return

    session.expire_all() 
    user = session.query(User).get(user_id)

    if not user:
        print("User not found.")
        return

    if not user.workouts:
        print(f"\n--- Workouts for {user.name} ---\nNo workouts found.")
        return

    print(f"\n--- Workouts for {user.name} ---")
    for workout in user.workouts:
        print(f"\nDate: {workout.date}")
        if workout.exercises:
            for ex in workout.exercises:
                print(f" - {ex.name}, {ex.sets}x{ex.reps}")
        else:
            print("  No exercises logged.")


def menu():
    """Main menu loop for the CLI app."""
    while True:
        print("\n--- Gym Tracker ---")
        print("1. List Users")
        print("2. Add User")
        print("3. Log Workout")
        print("4. Log Exercise")
        print("5. View Workouts")
        print("6. Clear All Users")
        print("7. Search Workouts")
        print("8. Export Workouts to CSV")
        print("9. View Summary Stats")
        print("10. Delete Exercise")
        print("11. Calendar View")
        print("12. Exit")
        choice = input("Choose an option: ").strip()

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
            clear_all_users()
        elif choice == '7':
            search_workouts()
        elif choice == '8':
            export_workouts_to_csv()
        elif choice == '9':
            view_summary()
        elif choice == '10':
            delete_exercise()
        elif choice == '11':
            calendar_view()
        elif choice == '12':
            print("Exiting Gym Tracker. Goodbye!")
            break
        else:
            print("Invalid option. Please choose from the menu.")


def search_workouts():
    """Search workouts by date or exercise name."""
    print("\nSearch Options:")
    print("1. By Date")
    print("2. By Exercise Name")
    choice = input("Choose an option: ").strip()

    if choice == '1':
        date = input("Enter date (YYYY-MM-DD): ").strip()
        workouts = session.query(Workout).filter_by(date=date).all()
    elif choice == '2':
        name = input("Enter exercise name: ").strip()
        workouts = session.query(Workout).join(Exercise).filter(Exercise.name.ilike(f"%{name}%")).all()
    else:
        print("Invalid choice.")
        return

    if not workouts:
        print("No matching workouts found.")
        return

    print("\n--- Search Results ---")
    for workout in workouts:
        print(f"\nDate: {workout.date} (User: {workout.user.name})")
        for ex in workout.exercises:
            print(f" - {ex.name}, {ex.sets}x{ex.reps}")


def export_workouts_to_csv():
    """Export a user's workouts and exercises to CSV."""
    try:
        user_id = int(input("Enter user ID to export workouts: "))
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        return

    session.expire_all()
    user = session.query(User).get(user_id)
    if not user:
        print("User not found.")
        return

    filename = f"{user.name}_workouts.csv"
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Workout Date", "Exercise", "Sets", "Reps"])

        for workout in user.workouts:
            for ex in workout.exercises:
                writer.writerow([workout.date, ex.name, ex.sets, ex.reps])

    print(f"Workouts exported to {filename}")


def view_summary():
    """View summary stats for a user (total workouts, sets, reps)."""
    try:
        user_id = int(input("Enter user ID to view summary: "))
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        return

    session.expire_all()
    user = session.query(User).get(user_id)
    if not user:
        print("User not found.")
        return

    total_workouts = len(user.workouts)
    total_exercises = sum(len(w.exercises) for w in user.workouts)
    total_sets = sum(ex.sets for w in user.workouts for ex in w.exercises)
    total_reps = sum(ex.reps * ex.sets for w in user.workouts for ex in w.exercises)

    print(f"\n--- Summary for {user.name} ---")
    print(f"Total Workouts: {total_workouts}")
    print(f"Total Exercises: {total_exercises}")
    print(f"Total Sets: {total_sets}")
    print(f"Total Reps: {total_reps}")


def delete_exercise():
    """Delete an exercise by its ID."""
    try:
        exercise_id = int(input("Enter exercise ID to delete: "))
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        return

    exercise = session.query(Exercise).get(exercise_id)
    if not exercise:
        print("Exercise not found.")
        return

    session.delete(exercise)
    try:
        session.commit()
        print("Exercise deleted successfully.")
    except Exception as e:
        session.rollback()
        print(f"Error deleting exercise: {e}")


def calendar_view():
    """Display workout history in a table format by date."""
    try:
        user_id = int(input("Enter user ID: "))
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        return

    session.expire_all()
    user = session.query(User).get(user_id)
    if not user:
        print("User not found.")
        return

    workouts = session.query(Workout).filter_by(user_id=user_id).all()
    table = []
    for w in workouts:
        table.append([w.date, len(w.exercises)])

    print(tabulate(table, headers=["Date", "# of Exercises"], tablefmt="grid"))


def clear_all_users():
    """Delete all users (and associated workouts and exercises)."""
    confirm = input("Are you sure you want to delete ALL users? This cannot be undone. (y/n): ").strip().lower()
    if confirm != 'y':
        print("Operation canceled.")
        return

    session.query(User).delete()
    try:
        session.commit()
        print("All users have been deleted.")
    except Exception as e:
        session.rollback()
        print(f"Failed to clear users. Error: {e}")


def debug_list_exercises():
    """Debug function to list all exercises directly from the DB."""
    session.expire_all()
    exercises = session.query(Exercise).all()
    print("\n--- All Exercises (Debug) ---")
    for ex in exercises:
        print(f"ID: {ex.id}, Name: {ex.name}, Workout ID: {ex.workout_id}, Sets: {ex.sets}, Reps: {ex.reps}")