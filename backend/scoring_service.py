from datetime import datetime, timezone
from typing import Optional

def calc_importance_score(importance: int, category_coefficient: float) -> float:
    if not (1 <= importance <= 5):
        raise ValueError("Importance must be between 1 and 5")

    normalize_importance = (importance - 1) / 4
    combined_score = normalize_importance * 0.7 + category_coefficient
    
    importance_score = 1 + (combined_score * 4)
    return importance_score

def calc_urgency_score(
    due_date: Optional[datetime], 
    effort_hours: float, 
    days_when_urgent: float = 2.0
) -> float:
    if not due_date:
        return 0.0
    
    # Use timezone-aware datetime if due_date is timezone-aware
    now = datetime.now(timezone.utc) if due_date.tzinfo else datetime.now()
    delta = due_date - now
    delta_days = delta.total_seconds() / 86400.0
    
    # Overdue tasks are maximally urgent
    if delta_days <= 0:
        return 1.0
    
    # Exponential time coefficient: accelerates as deadline approaches
    # Example: due in 2 days → 0.0, due in 1 day → 0.75, due in 0.5 days → 0.94
    time_ratio = delta_days / days_when_urgent
    time_coeff = max(0.0, min(1.0, 1.0 - (time_ratio ** 2)))
    
    # Effort coefficient: normalize to 8-hour workday
    effort_coeff = min(1.0, effort_hours / 8.0)
    
    # Weighted combination (70% time, 30% effort)
    urgency_score = (0.7 * time_coeff) + (0.3 * effort_coeff)
    
    return urgency_score


def assign_quadrant(urgency_score: float, importance_score: float) -> int:
        if urgency_score >= 0.5 and importance_score >= 2.6: #important + urgent
            return 1
        elif urgency_score < 0.5 and importance_score >= 2.6:  #important 
            return 2
        elif urgency_score >= 0.5 and importance_score >= 0.6: #urgent
            return 3
        else: #not important and not urgent
            return 4
