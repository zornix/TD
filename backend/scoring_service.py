from datetime import datetime, timezone
from typing import Optional

def check_in_range(value: float, min_value: float, max_value: float) -> float:
    return max(min_value, min(max_value, value))

def calc_importance_score(importance: int, category_coefficient: float, num_categories_created: int) -> float:
    weight_importance = 0.7
    if not (1 <= importance <= 5):
        raise ValueError("Importance must be between 1 and 5")
    if not (1 <= num_categories_created <= 6):
        raise ValueError("num_categories_created must be between 1 and 6")
    if not (0.0 < category_coefficient <= 1.0):
        raise ValueError("category_coefficient must be in (0, 1]")
    
    normalize_importance = (importance - 1) / 4 #0...1
    m = num_categories_created

    if m == 1: 
        k = 1.0
    else: 
        avg = 1.0 / m
        #normalize relative to the average category coefficient
        k = check_in_range((category_coefficient - avg) / (1 - avg), 0.0, 1.0)
    combined_score = weight_importance * normalize_importance + (1 - weight_importance) * k

    importance_score = 1 + (combined_score * 4)
    return importance_score

def calc_urgency_score(
    due_date: Optional[datetime], 
    effort_hours: float, 
    days_when_urgent: float = 2.0
) -> float:
    if not due_date:
        return 0.0
    if effort_hours <= 0:
        raise ValueError("Effort hours must be > 0")
    if days_when_urgent <= 0:
        raise ValueError("days_when_urgent must be > 0")
    
    # Timezone aware handling
    now = datetime.now(timezone.utc) if due_date.tzinfo else datetime.now()
    delta_days = (due_date - now).total_seconds() / 86400.0
    
    # Overdue tasks are maximally urgent
    if delta_days <= 0:
        return 1.0
    
    # Exponential time coefficient: accelerates as deadline approaches
    # Example: due in 2 days → 0.0, due in 1 day → 0.75, due in 0.5 days → 0.94
    time_ratio = delta_days / days_when_urgent
    time_coeff = check_in_range(1-(time_ratio ** 2), 0.0,1.0)
    
    # Effort coefficient: normalize to 8-hour workday
    effort_coeff = check_in_range((effort_hours / 8.0), 0.0, 1.0)
    
    # Weighted combination (70% time, 30% effort)
    urgency_score = (0.7 * time_coeff) + (0.3 * effort_coeff)
    
    return urgency_score


def assign_quadrant(urgency_score: float, importance_score: float) -> int:
        u_thresh = 0.5
        i_thresh = 3
        if urgency_score >= u_thresh and importance_score >= i_thresh: #important + urgent
            return 1
        elif urgency_score < u_thresh and importance_score >= i_thresh:  #important 
            return 2
        elif urgency_score >= u_thresh and importance_score < i_thresh: #urgent
            return 3
        else: #not important and not urgent
            return 4
