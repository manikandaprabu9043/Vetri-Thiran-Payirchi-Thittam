from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="FitBuddy - AI Workout Generator", version="1.0")

# Register all routes from routes.py
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)