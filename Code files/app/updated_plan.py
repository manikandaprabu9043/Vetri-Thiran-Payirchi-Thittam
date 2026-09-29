import google.generativeai as genai
import os

genai.configure(api_key=os.environ.get("GOOGLE_API_KEY", "YOUR API_KEY_HERE"))
model = genai.GenerativeModel("gemini-3.5-flash-lite")

def update_workout_plan(original_plan: str, user_feedback: str) -> str:
    """
    Use Gemini 1.5 Pro to update the workout plan based on user feedback.
    """
    prompt = f"""
    You are a professional fitness trainer assistant.
    
    Here's the original 7-day workout plan:
    {original_plan}
    
    User Feedback:
    "{user_feedback}"
    
    Based on the feedback, revise the relevant parts of the workout plan. Keep the format and rest of the plan unchanged if not needed.
    """
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error updating plan: {e}"