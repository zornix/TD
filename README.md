# Task Prioritizer

Task Prioritizer is a full-stack web application that helps you organize tasks by automatically calculating urgency and importance scores, then categorizing them into four quadrants based on the Eisenhower Matrix:

1. **Urgent + Important** 
2. **Important (Not Urgent)** 
3. **Urgent (Not Important)** 
4. **Not Urgent + Not Important** 

## Tech Stack

### Backend
- **Python**
- **FastAPI** & **Pydantic**
- **SQLAlchemy** & **PostgreSQL** 

### Frontend
- **React** & **Vanilla CSS**

### Infrastructure
- **Docker** - to run postgres instance
- **CORS Middleware**

### Architecture

React Fronted (Port 3000) <-HTTP-> Fast API Backend (Port 8000) --> PostgreSQL  

Data Flow 
1. Category Setup
   User --> Frontend --> POST /api/categories/bulk --> Database
   
2. Task Creation
   User Input --> Frontend --> POST /api/tasks --> Scoring Service --> Calculate Urgency & Importance Scores & Assign Quadrant --> Database

3. Task Display
   Frontend --> GET /api/tasks --> Database --> Group by Quadrant --> Display


### Features
1. The User can create up to 6 categories (tags) for their tasks (e.g. Work, School, Health) and assign different coefficient weights to each. Coeffiecients determine the importance multiplier for each task.

2. The importance and urgency scores are used to determine which "quadrant" the task will be placed into.  

    The **importance score** is calculated in the following way:  
        User's importance score (0.7), which gets normalized to a 0-1 range.  
        Category coefficient (0.3) that gets normalized against the average across all categories.  
        The final score gets mapped back to a 1-5 scale.  

    The **urgency score** is calculated using an exponential time decay model.  
        Time pressure (0.7) that increases quadratically as the deadline approaches.  
        Uses a 2-day urgency threshold as the reference point.  
        Overdue tasks get maximum urgency (1).  
        Effort factor (0.3) based on user estimated hours to complete task normalized to an 8 hour workday.   
        Larger time investments increase urgency, regardles of deadline.  


