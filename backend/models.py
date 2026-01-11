from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional, List, Dict

class newTask(BaseModel):
    description: str = Field(..., min_length=1)
    is_done: bool = False
    due_date: Optional[datetime] = None
    estimated_effort_hours: float = Field(..., gt=0)
    importance: int = Field(..., ge=1, le=5)
    category_id: int


class newCategory(BaseModel):
    name: str = Field(..., min_length=1)
    coefficient: float = Field(..., ge=0.0, le=1.0)


class updatedTask(BaseModel):
    id: int
    description: str
    is_done: bool = False
    due_date: Optional[datetime]
    estimated_effort_hours: float
    importance: int
    category_id: int
    urgency_score: Optional[float]
    imp_score: Optional[float]
    quadrant: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    model_config = {"from_attributes": True}


class updatedCategory(BaseModel):
    id: int
    name: str
    coefficient: float
    
    model_config = {"from_attributes": True}


class CategorySetupRequest(BaseModel):
    categories: List[newCategory] = Field(..., min_length=1, max_length=6)
    
    @field_validator('categories')
    @classmethod
    def validate_coefficients_sum(cls, v):
        total = sum(cat.coefficient for cat in v)
        if abs(total - 1.0) > 0.01:
            raise ValueError(f"Coefficients must sum to 1.0, got {total}")
        return v

class ScoringPolicyResponse(BaseModel):
    id: int
    version: int
    category_weights: Dict[int, float]
    urgency_threshold: float
    importance_threshold: float
    urgent_boundary_days: float
    created_at: datetime
    
    model_config = {"from_attributes": True}

class SetupStatusResponse(BaseModel):
    setup_complete: bool
    category_count: int = 0


class TasksByQuadrant(BaseModel):
    quadrants: Dict[str, List[updatedTask]]