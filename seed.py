from datetime import datetime
from gym_tracker.models import User, Workout, Exercise
from gym_tracker.database import session

def seed_data():
    session.query(Exercise).delete()
    session.query(Workout).delete()
    session.query(User).delete()

    alice = User(name="Alice")
    bob = User(name="Bob")
    charlie = User(name="Charlie")
    session.add_all([
        alice,
        bob,
        charlie
    ])
    session.commit()

    workout1 = Workout(date="2025-04-01", user_id=alice.id)
    workout2 = Workout(date="2025-04-03", user_id=alice.id)
    workout3 = Workout(date="2025-04-02", user_id=bob.id)
    workout4 = Workout(date="2025-04-05", user_id=charlie.id)
    session.add_all([workout1, workout2, workout3, workout4])
    session.commit()

    session.add_all([
        Exercise(name="Push-ups", sets=3, reps=10, workout_id=workout1.id),
        Exercise(name="Squats", sets=4, reps=12, workout_id=workout1.id),
        Exercise(name="Pull-ups", sets=3, reps=8, workout_id=workout2.id),
        Exercise(name="Bench Press", sets=4, reps=8, workout_id=workout3.id),
        Exercise(name="Deadlift", sets=3, reps=6, workout_id=workout3.id),
        Exercise(name="Plank", sets=3, reps=30, workout_id=workout4.id),
        Exercise(name="Sit-ups", sets=3, reps=20, workout_id=workout4.id),
    ])
    session.commit()
    print("✅ Mock data added successfully!")

if __name__ == "__main__":
    seed_data()