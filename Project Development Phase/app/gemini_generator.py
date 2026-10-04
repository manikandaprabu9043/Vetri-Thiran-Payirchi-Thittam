import google.generativeai as genai
import os

# Set your API key
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY", "YOUR_API_KEY_HERE"))

# Using gemini-3.5flash for active compatibility
model = genai.GenerativeModel("gemini-3.5-flash-lite")

def generate_workout_gemini(user_input):
    prompt = f"""
    You are a professional fitness trainer.

    Create a personalized, structured 7-day workout plan for someone with the goal of **{user_input['goal']}**, and prefers **{user_input['intensity']}** intensity workouts.

    Each day must include:
    - A warm-up (5-10 mins)
    - Main workout (targeted exercises, sets & reps)
    - Cooldown or recovery tip

    Format:
    Day 1:
    Warm-up: ...
    Main Workout: ...
    Cooldown: ...
    (Repeat for Day 2-7)
    """
    try:
        # 10 seconds timeout set pandrom
        response = model.generate_content(prompt, request_options={"timeout": 60})
        return response.text
    except Exception as e:
        return f"Error: {e}"
