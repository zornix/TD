from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, Session, relationship
from datetime import datetime, timezone

# Database connection string based on docker-compose.yml
DATABASE_URL = "postgresql://app_user:app_password@localhost:5432/app_db"

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Helper function for UTC timestamps
def utc_now():
    return datetime.now(timezone.utc)

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    coefficient = Column(Float, nullable=False)
    created_at = Column(DateTime, default=utc_now, nullable=False)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now, nullable=False)
    
    # Relationship to tasks
    tasks = relationship("Task", back_populates="category")

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    is_done = Column(Boolean, default=False, nullable=False)
    due_date = Column(DateTime, nullable=True)
    estimated_effort_hours = Column(Float, nullable=False)
    importance = Column(Integer, nullable=False)  # 1-5 scale
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    
    # Computed scores
    urgency_score = Column(Float, nullable=True)
    imp_score = Column(Float, nullable=True)
    quadrant = Column(Integer, nullable=True)  # 1-4
    
    # Timestamps
    created_at = Column(DateTime, default=utc_now, nullable=False)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now, nullable=False)
    
    # Relationship to category
    category = relationship("Category", back_populates="tasks")

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize database tables
def init_db():
    Base.metadata.create_all(bind=engine)