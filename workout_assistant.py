import random
from datetime import datetime, timedelta

# Exercise Database
exercises_db = {
    "legs": {
        "hamstrings": [
            {"name": "Deadlifts", "equipment": "barbell"},
            {"name": "Lunges", "equipment": "dumbbell"}
        ],
        "quads": [
            {"name": "Squats", "equipment": "barbell"},
            {"name": "Step-ups", "equipment": "bodyweight"}
        ]
    },
    "arms": {
        "biceps": [
            {"name": "Curls", "equipment": "dumbbell"},
            {"name": "Chin-ups", "equipment": "bodyweight"}
        ],
        "triceps": [
            {"name": "Dips", "equipment": "bodyweight"},
            {"name": "Pushdowns", "equipment": "cable"}
        ]
    },
    "chest": {
        "upper": [
            {"name": "Incline Press", "equipment": "barbell"},
            {"name": "Push-ups", "equipment": "bodyweight"}
        ],
        "lower": [
            {"name": "Decline Press", "equipment": "barbell"},
            {"name": "Dips", "equipment": "bodyweight"}
        ]
    },
    "back": {
        "upper": [
            {"name": "Pull-ups", "equipment": "bodyweight"},
            {"name": "Rows", "equipment": "dumbbell"}
        ],
        "lower": [
            {"name": "Deadlifts", "equipment": "barbell"},
            {"name": "Extensions", "equipment": "bodyweight"}
        ]
    },
    "abs": {
        "core": [
            {"name": "Planks", "equipment": "bodyweight"},
            {"name": "Leg Raises", "equipment": "bodyweight"}
        ]
    }
}

default_sub_parts = {"legs": "hamstrings", "arms": "biceps", "chest": "upper", "back": "upper", "abs": "core"}

def get_user_input():
    while True:
        try:
            print("\n1. Generate a workout plan\n2. Get exercise advice\n3. View progress\n4. General fitness advice")
            choice = int(input("Enter choice: "))
            if choice in [1, 2, 3, 4]:
                break
            print("Invalid input, try again.")
        except ValueError:
            print("Please enter a valid number.")
    
    exercise = None if choice != 2 else input("Enter exercise name: ")
    level = input("Enter your fitness level (beginner/intermediate/advanced): ").strip().lower()
    equipment = input("Enter available equipment (comma-separated): ").strip().split(",")
    duration = int(input("Enter workout duration (30, 45, 60 mins): "))
    return {"level": level, "equipment": equipment, "duration": duration}, exercise, choice

def get_recent_exercises(past_workouts, days=7):
    cutoff_date = datetime.now() - timedelta(days=days)
    return {ex["exercise"] for workout in past_workouts if workout["date"] >= cutoff_date for ex in workout["main"]}

def select_exercise(body_part, sub_part, equipment_list, recent_exercises):
    exercises = exercises_db.get(body_part, {}).get(sub_part, [])
    available = [ex for ex in exercises if ex["equipment"] in equipment_list and ex["name"] not in recent_exercises]
    return random.choice(available or exercises)["name"] if exercises else None

def generate_workout(user_profile, past_workouts):
    duration = user_profile["duration"]
    level = user_profile["level"]
    equipment = user_profile["equipment"]
    recent_exercises = get_recent_exercises(past_workouts)
    main_sets = 2 if level == "beginner" else 3 if level == "intermediate" else 4
    base_reps = 8 if level == "beginner" else 10
    
    workout_plan = {"warmup": ["Jump Rope", "Dynamic Stretching"], "main": [], "stretch": ["Cool-down Stretch"]}
    for body_part, sub_part in default_sub_parts.items():
        exercise = select_exercise(body_part, sub_part, equipment, recent_exercises)
        if exercise:
            workout_plan["main"].append({"exercise": exercise, "sets": main_sets, "reps": base_reps})
    return workout_plan

def display_workout(workout):
    print("\nWarmup:")
    for warmup in workout["warmup"]:
        print(f"  * {warmup}")
    print("\nMain Workout:")
    for ex in workout["main"]:
        print(f"  * {ex['exercise']} - {ex['sets']} sets of {ex['reps']} reps")
    print("\nStretching:")
    for stretch in workout["stretch"]:
        print(f"  * {stretch}")

def collect_feedback(workout):
    feedback = {}
    for ex in workout["main"]:
        while True:
            try:
                rating = int(input(f"Rate {ex['exercise']} (1-10): "))
                if 1 <= rating <= 10:
                    feedback[ex['exercise']] = rating
                    break
                print("Invalid rating. Enter between 1-10.")
            except ValueError:
                print("Please enter a number.")
    return feedback

def adjust_exercise_feedback(exercise, rating):
    return "Consider increasing reps." if rating > 7 else "Maintain current level." if rating > 4 else "Reduce reps."

def main():
    user_profile, exercise, choice = get_user_input()
    past_workouts = []
    if choice == 2:
        advice = {"Squats": "Keep your knees behind your toes.", "Deadlifts": "Keep your back straight."}
        print(advice.get(exercise, "No specific advice available."))
    elif choice == 3:
        print("Progress tracking coming soon!")
    elif choice == 4:
        print("Stay hydrated and get enough sleep!")
    else:
        workout_plan = generate_workout(user_profile, past_workouts)
        display_workout(workout_plan)
        feedback = collect_feedback(workout_plan)
        for ex, rating in feedback.items():
            print(f"Feedback for {ex}: {adjust_exercise_feedback(ex, rating)}")

if __name__ == "__main__":
    main()
