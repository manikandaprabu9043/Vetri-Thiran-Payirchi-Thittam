from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os
import os
import time

from app.database import SessionLocal, User, WorkoutPlan
from app.gemini_generator import generate_workout_gemini
from app.gemini_flash_generator import generate_nutrition_tip_with_flash
from app.updated_plan import update_workout_plan

router = APIRouter()

# Setup templates directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(os.path.dirname(BASE_DIR), "templates")
templates = Jinja2Templates(directory=TEMPLATE_DIR)

# 1. Home Page
@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    # Updated syntax for latest FastAPI
    return templates.TemplateResponse(request=request, name="index.html")

# 2. Generate Workout Plan
@router.post("/generate-workout", response_class=HTMLResponse)
def generate_workout(
    request: Request,
    username: str = Form(...),
    user_id: int = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...)
):
    db = SessionLocal()
    
    # Save or update user
    existing_user = db.query(User).filter(User.id == user_id).first()
    if not existing_user:
        new_user = User(id=user_id, name=username, age=age, weight=weight, goal=goal, intensity=intensity)
        db.add(new_user)
    else:
        existing_user.name = username
        existing_user.age = age
        existing_user.weight = weight
        existing_user.goal = goal
        existing_user.intensity = intensity
    db.commit()

    # Generate AI Plans
    user_input = {"goal": goal, "intensity": intensity}
    plan = generate_workout_gemini(user_input)
    
    time.sleep(3)  
    
    nutrition_tip = generate_nutrition_tip_with_flash(goal)

    # Save generated plan
    workout = WorkoutPlan(user_id=user_id, original_plan=plan)
    db.add(workout)
    db.commit()
    db.close()

    return templates.TemplateResponse(request=request, name="result.html", context={
        "username": username,
        "user_id": user_id,
        "age": age,
        "weight": weight,
        "goal": goal,
        "intensity": intensity,
        "workout_plan": plan,
        "nutrition_tip": nutrition_tip
    })

# 3. Submit Feedback and Update Plan
@router.post("/submit-feedback", response_class=HTMLResponse)
def submit_feedback(request: Request, user_id: int = Form(...), feedback: str = Form(...)):
    db = SessionLocal()
    workout = db.query(WorkoutPlan).filter(WorkoutPlan.user_id == user_id).first()
    
    updated_plan_text = ""
    if workout:
        original_plan = workout.original_plan
        updated_plan_text = update_workout_plan(original_plan, feedback)
        workout.updated_plan = updated_plan_text
        db.commit()
    db.close()

    return templates.TemplateResponse(request=request, name="result.html", context={
        "feedback_success": True,
        "updated_plan": updated_plan_text,
        "user_id": user_id
    })

# 4. Admin View All Users
@router.get("/view-all-users", response_class=HTMLResponse)
def view_all_users(request: Request):
    db = SessionLocal()
    users = db.query(User).all()
    user_data = []
    for user in users:
        plan = db.query(WorkoutPlan).filter(WorkoutPlan.user_id == user.id).first()
        user_data.append({
            "id": user.id,
            "name": user.name,
            "age": user.age,
            "weight": user.weight,
            "goal": user.goal,
            "intensity": user.intensity,
            "original_plan": plan.original_plan if plan else "N/A",
            "updated_plan": plan.updated_plan if plan and plan.updated_plan else "Not updated"
        })
    db.close()
    return templates.TemplateResponse(request=request, name="all_users.html", context={
        "users": user_data
    })