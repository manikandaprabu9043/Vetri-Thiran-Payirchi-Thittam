import google.generativeai as genai
import os

genai.configure(api_key=os.environ.get("GOOGLE_API_KEY", "YOUR_API_KEY_HERE"))
model = genai.GenerativeModel("gemini-3.5-flash-lite")

def generate_nutrition_tip_with_flash(goal: str) -> str:
    """
    Generate a nutrition or recovery tip using Gemini Flash based on the user's fitness goal.

    Args:
      goal (str): User's fitness goal - "weight loss", "muscle gain", or "general fitness".
    
    Returns:
      str: Generated tip.
    """
    prompt = (
        f"Give one clear, helpful nutrition or recovery tip for someone focused on '{goal}'. "
        "The tip should be practical, friendly, and easy to understand."
    )
    
    try:
        response = model.generate_content(prompt, request_options={"timeout": 60})
        return response.text.strip()
        
    except Exception as e:
        return f"Error generating tip: {str(e)}"