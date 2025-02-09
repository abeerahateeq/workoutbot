import random
from datetime import datetime, timedelta


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


default_sub_parts = {
    "legs": "hamstrings",
    "arms": "biceps",
    "chest": "upper",
    "back": "upper",
    "abs": "core"
}

def get_user_input():
    print("Welcome to the Workout Assistant!")
    print("What would you like to do?")
    print("1. Generate a workout plan")
    print("2. Get advice on a specific exercise")
    print("3. View progress and suggest improvements")
    print("4. Get general fitness advice")
    choice = input("Enter the number of your choice: ")

    if choice == "1":
        exercise = None
        advice_type = None
    elif choice == "2":
        exercise = input("Enter the name of the exercise you want advice on (e.g., Squats, Deadlifts): ")
        advice_type = None
    elif choice == "3":
        exercise = None
        advice_type = "progress"
    elif choice == "4":
        exercise = None
        advice_type = "fitness_advice"
    else:
        print("Invalid option, try again.")
        return get_user_input()

    
    level = input("Enter your fitness level (beginner, intermediate, advanced): ").strip().lower()
    equipment = input("Enter your available equipment (comma-separated): ").strip().split(",")
    equipment = [item.strip() for item in equipment]
    duration = int(input("Enter your desired workout duration in minutes (30, 45, 60): ").strip())

    user_profile = {
        "level": level,
        "equipment": equipment,
        "duration": duration
    }

    return user_profile, exercise, advice_type

def get_recent_exercises(past_workouts, days=7):
    recent_exercises = set()
    cutoff_date = datetime.now() - timedelta(days=days)
    for workout in past_workouts:
        if workout.get("date") and workout["date"] >= cutoff_date:
            for ex in workout.get("main", []):
                recent_exercises.add(ex["exercise"])
    return recent_exercises

def select_exercise(body_part, sub_body_part, equipment_list, recent_exercises):
    available = []
    for ex in exercises_db.get(body_part, {}).get(sub_body_part, []):
        if ex["equipment"] not in equipment_list:
            continue
        if ex["name"] in recent_exercises:
            continue
        available.append(ex)
    
    if not available:
        for ex in exercises_db.get(body_part, {}).get(sub_body_part, []):
            if ex["equipment"] in equipment_list:
                available.append(ex)
    
    if available:
        return random.choice(available)["name"]
    else:
        all_options = exercises_db.get(body_part, {}).get(sub_body_part, [])
        if all_options:
            return random.choice(all_options)["name"]
        return None

def adjust_sets_reps(base_sets, base_reps, exercise, past_workouts, feedback):
    for workout in sorted(past_workouts, key=lambda w: w.get("date", datetime.min), reverse=True):
        for ex in workout.get("main", []):
            if ex["exercise"] == exercise:
                fb = feedback.get(exercise, "")
                if fb.lower() == "too easy":
                    return base_sets, base_reps + 1
                elif fb.lower() == "too hard":
                    return base_sets, max(1, base_reps - 1)
    return base_sets, base_reps

def generate_workout(user_profile, past_workouts, feedback):
    workout_plan = {"warmup": [], "main": [], "stretch": []}
    
    duration = user_profile.get("duration", 45)
    if duration == 30:
        warmup_count = 2
        main_sets = 2
        stretch_count = random.randint(2, 3)
    elif duration == 45:
        warmup_count = 2
        main_sets = 3
        stretch_count = random.randint(2, 3)
    else:
        warmup_count = 3
        main_sets = 4
        stretch_count = random.randint(4, 5)
    
    level = user_profile.get("level", "beginner").lower()
    if level == "beginner":
        main_sets = max(2, main_sets - 1)
        base_reps = 8
    elif level == "intermediate":
        base_reps = 10
    else:
        base_reps = 10
    
    recent_exercises = get_recent_exercises(past_workouts, days=7)
    
    for body_part in ["legs", "arms", "chest", "back", "abs"]:
        sub_part = default_sub_parts.get(body_part, None)
        if not sub_part:
            continue
        exercise_name = select_exercise(body_part, sub_part, user_profile.get("equipment", []), recent_exercises)
        if exercise_name:
            sets, reps = adjust_sets_reps(main_sets, base_reps, exercise_name, past_workouts, feedback)
            workout_plan["main"].append({
                "exercise": exercise_name,
                "sets": sets,
                "reps": reps
            })
    
    for i in range(warmup_count):
        workout_plan["warmup"].append(f"Dynamic Warmup {i+1}")
    
    for i in range(stretch_count):
        workout_plan["stretch"].append(f"Stretch {i+1} focusing on muscles worked")
    
    return workout_plan

def collect_feedback(workout):
    feedback = {}
    overall_rating = 0
    for ex in workout["main"]:
        rating = int(input(f"Rate your experience with {ex['exercise']} (1-10): "))
        feedback[ex['exercise']] = rating
        overall_rating += rating
    overall_rating = overall_rating / len(workout["main"]) if workout["main"] else 0
    return feedback, overall_rating

def adjust_exercise_feedback(exercise, rating):
    if rating <= 3:
        return "Consider reducing the weight or reps."
    elif rating <= 6:
        return "Maintain the current level."
    else:
        return "Consider increasing the weight or reps."


def main():
    user_profile, exercise, advice_type = get_user_input()

    if exercise:
        print("\nAdvice on " + exercise + ":")
        # Assuming you have a fitness_advice dictionary, display relevant advice.
        fitness_advice = {
            "Squats": ["Keep your knees behind your toes", "Use proper form to avoid injury"],
            "Deadlifts": ["Lift with your legs, not your back", "Keep your back straight during the movement"],
            "Lunges": ["Step forward with a controlled movement", "Keep your torso upright", "Ensure your knee doesn't extend past your toes."],
    "Step-ups": ["Step onto a bench with your entire foot", "Keep your chest upright", "Engage your glutes and quads."],
    "Curls": ["Keep your elbows close to your torso", "Control the movement throughout", "Don't swing the dumbbell."],
    "Chin-ups": ["Pull yourself up by engaging your lats", "Keep your body straight", "Don't use momentum to complete the lift."],
    "Dips": ["Keep your elbows at a 90-degree angle", "Don't let your shoulders roll forward", "Engage your chest and triceps."],
    "Pushdowns": ["Maintain a slight bend in your elbows", "Don't use your back to push the weight down", "Engage your triceps fully."],
    "Incline Press": ["Keep your feet flat on the ground", "Don't arch your back", "Control the barbell during the descent."],
    "Push-ups": ["Engage your core", "Keep your body in a straight line", "Don't let your elbows flare out too much."],
    "Decline Press": ["Ensure a controlled movement throughout", "Keep your feet firmly planted", "Focus on engaging your lower chest."],
    "Pull-ups": ["Pull your chest up to the bar", "Keep your body still", "Avoid swinging during the movement."],
    "Rows": ["Pull with your back, not your arms", "Keep your shoulders back and down", "Squeeze your shoulder blades together at the top."],
    "Extensions": ["Maintain a neutral spine", "Don't arch your back", "Ensure your glutes are engaged during the lift."],
    "Planks": ["Keep your body in a straight line", "Engage your core", "Avoid letting your hips sag."],
    "Leg Raises": ["Lift your legs using your core", "Don't let your lower back come off the ground", "Control the movement both up and down."],
            "Yoga": ["Start with a single pose and progressively increase the duration", "Keep your body relaxed and centered"],
            "Stretching": ["Start with a full stretch and progressively increase the duration", "Keep your body relaxed and centered"],
            "Swimming": ["Start with a full swim and progressively increase the duration", "Keep your body relaxed and centered"],
            "Cycling": ["Start with a full cycle and progressively increase the duration", "Keep your body relaxed and centered"],
            "Running": ["Start with a full run and progressively increase the duration", "Keep your body relaxed and centered"],
        }
    if exercise in fitness_advice:
        for tip in fitness_advice.get(exercise, []):
            print(f"  * {tip}")

    elif advice_type == "progress":
        print("\nHere are your progress suggestions based on feedback and past workouts.")
        

    elif advice_type == "fitness_advice":
        print("\nHere are some general fitness tips:")
        print("  * Ensure proper hydration and nutrition.")
        print("  * Sleep well to aid recovery.")

    else:
        print("\nGenerating workout plan...")
        past_workouts = []  
        feedback = {}  
        workout_plan = generate_workout(user_profile, past_workouts, feedback)
        
        print("\nWarmup:")
        for warmup in workout_plan["warmup"]:
            print(f"  * {warmup}")
        
        print("\nMain Workout:")
        for ex in workout_plan["main"]:
            print(f"  * {ex['exercise']} - {ex['sets']} sets of {ex['reps']} reps")
        
        print("\nStretching:")
        for stretch in workout_plan["stretch"]:
            print(f"  * {stretch}")

        
        feedback, overall_rating = collect_feedback(workout_plan)
        print(f"\nOverall rating: {overall_rating}")
        for ex, rating in feedback.items():
            feedback_message = adjust_exercise_feedback(ex, rating)
            print(f"Feedback for {ex}: {feedback_message}")

if __name__ == "__main__":
    main()
