"""
Database models for the Learning Risk Assessment Application
Using SQLAlchemy for database operations
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    grade_level = Column(String(10))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    predictions = relationship("Prediction", back_populates="student")
    observations = relationship("ParentObservation", back_populates="student")

class Prediction(Base):
    __tablename__ = 'predictions'
    
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    
    # Academic scores
    math_score = Column(Float)
    reading_score = Column(Float) 
    writing_score = Column(Float)
    attendance = Column(Float)
    behavior = Column(Integer)
    literacy = Column(Integer)
    
    # Prediction results
    prediction = Column(Integer)  # 0 or 1
    probability = Column(Float)
    risk_level = Column(String(20))
    
    # Additional information
    notes = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    student = relationship("Student", back_populates="predictions")

class ParentObservation(Base):
    __tablename__ = 'parent_observations'
    
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    child_name = Column(String(100))
    date = Column(DateTime)
    
    # Academic observations
    homework_completion = Column(Float)
    reading_time = Column(Float)
    focus_level = Column(String(20))
    subjects_struggled = Column(Text)  # JSON string
    
    # Behavioral observations
    behavior_rating = Column(Integer)
    mood_rating = Column(Integer)
    sleep_hours = Column(Float)
    energy_level = Column(String(20))
    
    # Additional observations
    social_interactions = Column(Text)
    learning_wins = Column(Text)
    challenges_faced = Column(Text)
    strategies_used = Column(Text)
    
    # Environmental factors
    screen_time = Column(Float)
    physical_activity = Column(Float)
    medication_taken = Column(Boolean)
    special_events = Column(Text)
    
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    student = relationship("Student", back_populates="observations")

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    password = Column(String(100))  # In production, this should be hashed
    user_type = Column(String(20))  # 'teacher' or 'parent'
    full_name = Column(String(100))
    email = Column(String(100))
    created_date = Column(DateTime, default=datetime.utcnow)

class InterventionRecord(Base):
    __tablename__ = 'intervention_records'
    
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    intervention_type = Column(String(50))
    baseline_score = Column(Float)
    current_score = Column(Float)
    weeks_elapsed = Column(Integer)
    progress_notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    student = relationship("Student")

def get_database_engine():
    """Create database engine from environment variables"""
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        raise ValueError("DATABASE_URL environment variable not set")
    
    engine = create_engine(database_url)
    return engine

def create_tables():
    """Create all database tables"""
    engine = get_database_engine()
    Base.metadata.create_all(engine)
    return engine

def get_session():
    """Get database session"""
    engine = get_database_engine()
    Session = sessionmaker(bind=engine)
    return Session()