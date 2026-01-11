from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from database import get_db, init_db, Category, Task
from models import (
    newTask, 
    newCategory, 
    updatedTask, 
    updatedCategory,
    CategorySetupRequest,
)
from scoring_service import calc_importance_score, calc_urgency_score, assign_quadrant


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_db()
    yield

app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Hello, World! DB connected."}


# Category Endpoints
@app.get("/api/categories", response_model=List[updatedCategory])
def get_categories(db: Session = Depends(get_db)):
    """Retrieve all categories."""
    categories = db.query(Category).all()
    return categories


@app.post("/api/categories", response_model=updatedCategory)
def create_category(category: newCategory, db: Session = Depends(get_db)):
    """Create a new category."""
    # Check if category with same name already exists
    existing = db.query(Category).filter(Category.name == category.name).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Category '{category.name}' already exists")
    
    db_category = Category(
        name=category.name,
        coefficient=category.coefficient
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    
    return db_category

@app.post("/api/categories/bulk", response_model=List[updatedCategory])
def create_bulk_categories(request: CategorySetupRequest, db: Session = Depends(get_db)):
    """
    Create multiple categories from a request.
    Automatically assigns category_id to each category (handled by SQLAlchemy primary key).
    Validates that coefficients sum to 1.0 (handled by Pydantic validator).
    """
    created_categories = []
    
    for category in request.categories:
        # Check if category with same name already exists
        existing = db.query(Category).filter(Category.name == category.name).first()
        if existing:
            raise HTTPException(
                status_code=400, 
                detail=f"Category '{category.name}' already exists"
            )
        
        db_category = Category(
            name=category.name,
            coefficient=category.coefficient
        )
        db.add(db_category)
        created_categories.append(db_category)
    
    db.commit()
    
    # Refresh all categories to get their assigned IDs
    for category in created_categories:
        db.refresh(category)

    return created_categories

# Task Endpoints
@app.post("/api/tasks", response_model=updatedTask)
def create_task(task: newTask, db: Session = Depends(get_db)):
    """
    Create a new task.
    Calculates urgency_score, imp_score, and assigns quadrant automatically.
    """
    # Fetch category to get coefficient
    category = db.query(Category).filter(Category.id == task.category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail=f"Category with id {task.category_id} not found")
    
    num_categories_created = db.query(Category).count()

    # Calculate scores
    imp_score = calc_importance_score(task.importance, category.coefficient, num_categories_created)
    urgency_score = calc_urgency_score(task.due_date, task.estimated_effort_hours)
    quadrant = assign_quadrant(urgency_score, imp_score)
    
    # Create task in database
    db_task = Task(
        description=task.description,
        is_done=task.is_done,
        due_date=task.due_date,
        estimated_effort_hours=task.estimated_effort_hours,
        importance=task.importance,
        category_id=task.category_id,
        urgency_score=urgency_score,
        imp_score=imp_score,
        quadrant=quadrant
    )
    
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    
    # Convert quadrant to string for response (matching updatedTask model)
    task_dict = {
        "id": db_task.id,
        "description": db_task.description,
        "is_done": db_task.is_done,
        "due_date": db_task.due_date,
        "estimated_effort_hours": db_task.estimated_effort_hours,
        "importance": db_task.importance,
        "category_id": db_task.category_id,
        "urgency_score": db_task.urgency_score,
        "imp_score": db_task.imp_score,
        "quadrant": str(db_task.quadrant) if db_task.quadrant else None,
        "created_at": db_task.created_at,
        "updated_at": db_task.updated_at
    }
    
    return updatedTask(**task_dict)


@app.get("/api/tasks", response_model=List[updatedTask])
def get_tasks(db: Session = Depends(get_db)):
    """Retrieve all tasks."""
    tasks = db.query(Task).all()
    
    # Convert to updatedTask format
    result = []
    for task in tasks:
        task_dict = {
            "id": task.id,
            "description": task.description,
            "is_done": task.is_done,
            "due_date": task.due_date,
            "estimated_effort_hours": task.estimated_effort_hours,
            "importance": task.importance,
            "category_id": task.category_id,
            "urgency_score": task.urgency_score,
            "imp_score": task.imp_score,
            "quadrant": str(task.quadrant) if task.quadrant else None,
            "created_at": task.created_at,
            "updated_at": task.updated_at
        }
        result.append(updatedTask(**task_dict))
    
    return result


@app.patch("/api/tasks/{task_id}/done", response_model=updatedTask)
def toggle_task_done(task_id: int, db: Session = Depends(get_db)):
    """Toggle the is_done status of a task."""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
    
    task.is_done = not task.is_done
    task.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(task)
    
    task_dict = {
        "id": task.id,
        "description": task.description,
        "is_done": task.is_done,
        "due_date": task.due_date,
        "estimated_effort_hours": task.estimated_effort_hours,
        "importance": task.importance,
        "category_id": task.category_id,
        "urgency_score": task.urgency_score,
        "imp_score": task.imp_score,
        "quadrant": str(task.quadrant) if task.quadrant else None,
        "created_at": task.created_at,
        "updated_at": task.updated_at
    }
    
    return updatedTask(**task_dict)


@app.delete("/api/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """Delete a task from the database."""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
    
    db.delete(task)
    db.commit()
    
    return {"message": f"Task {task_id} deleted successfully"}
