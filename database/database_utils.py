"""
Database utility functions for the Learning Risk Assessment Application
Provides high-level database operations and data management
"""

from database.models import (
    Student, Prediction, ParentObservation, User, InterventionRecord,
    get_session, create_tables, get_database_engine
)
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, date
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def initialize_database():
    """Initialize database and create tables if they don't exist"""
    try:
        engine = create_tables()
        logger.info("Database initialized successfully")
        
        # Create default users if they don't exist
        session = get_session()
        try:
            existing_users = session.query(User).count()
            if existing_users == 0:
                default_users = [
                    User(
                        username="admin",
                        password="admin123",  # In production, hash this
                        user_type="teacher",
                        full_name="Administrator",
                        email="admin@school.edu"
                    ),
                    User(
                        username="teacher1",
                        password="teacher123",
                        user_type="teacher",
                        full_name="Demo Teacher",
                        email="teacher@school.edu"
                    ),
                    User(
                        username="parent1",
                        password="parent123",
                        user_type="parent",
                        full_name="Demo Parent",
                        email="parent@email.com"
                    )
                ]
                
                for user in default_users:
                    session.add(user)
                session.commit()
                logger.info("Default users created")
                
        except Exception as e:
            session.rollback()
            logger.error(f"Error creating default users: {e}")
        finally:
            session.close()
            
        return True
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        return False

def save_prediction_to_db(prediction_data):
    """Save prediction data to database"""
    session = get_session()
    try:
        # Get or create student
        student_name = prediction_data.get('student_name', 'Unknown Student')
        grade_level = prediction_data.get('grade_level', 'Unknown')
        
        student = session.query(Student).filter_by(name=student_name).first()
        if not student:
            student = Student(name=student_name, grade_level=grade_level)
            session.add(student)
            session.flush()  # Get the student ID
        
        # Create prediction record
        prediction = Prediction(
            student_id=student.id,
            math_score=prediction_data.get('math_score'),
            reading_score=prediction_data.get('reading_score'),
            writing_score=prediction_data.get('writing_score'),
            attendance=prediction_data.get('attendance'),
            behavior=prediction_data.get('behavior'),
            literacy=prediction_data.get('literacy'),
            prediction=prediction_data.get('prediction'),
            probability=prediction_data.get('probability'),
            risk_level=prediction_data.get('risk_level'),
            notes=prediction_data.get('notes', ''),
            timestamp=datetime.fromisoformat(prediction_data.get('timestamp', datetime.now().isoformat()))
        )
        
        session.add(prediction)
        session.commit()
        logger.info(f"Prediction saved for student: {student_name}")
        return True
        
    except Exception as e:
        session.rollback()
        logger.error(f"Error saving prediction: {e}")
        return False
    finally:
        session.close()

def save_parent_observation_to_db(observation_data):
    """Save parent observation to database"""
    session = get_session()
    try:
        # Get or create student
        child_name = observation_data.get('child_name', 'Unknown Child')
        
        student = session.query(Student).filter_by(name=child_name).first()
        if not student:
            student = Student(name=child_name, grade_level='Unknown')
            session.add(student)
            session.flush()
        
        # Convert subjects_struggled list to JSON string
        subjects_struggled = observation_data.get('subjects_struggled', [])
        if isinstance(subjects_struggled, list):
            subjects_struggled = json.dumps(subjects_struggled)
        
        # Create observation record
        observation = ParentObservation(
            student_id=student.id,
            child_name=child_name,
            date=datetime.fromisoformat(observation_data.get('date', date.today().isoformat())),
            homework_completion=observation_data.get('homework_completion'),
            reading_time=observation_data.get('reading_time'),
            focus_level=observation_data.get('focus_level'),
            subjects_struggled=subjects_struggled,
            behavior_rating=observation_data.get('behavior_rating'),
            mood_rating=observation_data.get('mood_rating'),
            sleep_hours=observation_data.get('sleep_hours'),
            energy_level=observation_data.get('energy_level'),
            social_interactions=observation_data.get('social_interactions', ''),
            learning_wins=observation_data.get('learning_wins', ''),
            challenges_faced=observation_data.get('challenges_faced', ''),
            strategies_used=observation_data.get('strategies_used', ''),
            screen_time=observation_data.get('screen_time'),
            physical_activity=observation_data.get('physical_activity'),
            medication_taken=observation_data.get('medication_taken', False),
            special_events=observation_data.get('special_events', ''),
            timestamp=datetime.fromisoformat(observation_data.get('timestamp', datetime.now().isoformat()))
        )
        
        session.add(observation)
        session.commit()
        logger.info(f"Parent observation saved for: {child_name}")
        return True
        
    except Exception as e:
        session.rollback()
        logger.error(f"Error saving parent observation: {e}")
        return False
    finally:
        session.close()

def load_student_predictions():
    """Load all student prediction data from database"""
    session = get_session()
    try:
        predictions = session.query(Prediction).join(Student).all()
        
        prediction_list = []
        for pred in predictions:
            prediction_dict = {
                'id': pred.id,
                'student_name': pred.student.name,
                'grade_level': pred.student.grade_level,
                'math_score': pred.math_score,
                'reading_score': pred.reading_score,
                'writing_score': pred.writing_score,
                'attendance': pred.attendance,
                'behavior': pred.behavior,
                'literacy': pred.literacy,
                'prediction': pred.prediction,
                'probability': pred.probability,
                'risk_level': pred.risk_level,
                'notes': pred.notes,
                'timestamp': pred.timestamp.isoformat()
            }
            prediction_list.append(prediction_dict)
        
        return prediction_list
        
    except Exception as e:
        logger.error(f"Error loading predictions: {e}")
        return []
    finally:
        session.close()

def load_parent_observations():
    """Load all parent observation data from database"""
    session = get_session()
    try:
        observations = session.query(ParentObservation).join(Student).all()
        
        observation_list = []
        for obs in observations:
            # Parse subjects_struggled back to list
            subjects_struggled = obs.subjects_struggled or '[]'
            try:
                subjects_struggled = json.loads(subjects_struggled)
            except json.JSONDecodeError:
                subjects_struggled = []
            
            observation_dict = {
                'id': obs.id,
                'child_name': obs.child_name,
                'date': obs.date.isoformat(),
                'homework_completion': obs.homework_completion,
                'reading_time': obs.reading_time,
                'focus_level': obs.focus_level,
                'subjects_struggled': subjects_struggled,
                'behavior_rating': obs.behavior_rating,
                'mood_rating': obs.mood_rating,
                'sleep_hours': obs.sleep_hours,
                'energy_level': obs.energy_level,
                'social_interactions': obs.social_interactions,
                'learning_wins': obs.learning_wins,
                'challenges_faced': obs.challenges_faced,
                'strategies_used': obs.strategies_used,
                'screen_time': obs.screen_time,
                'physical_activity': obs.physical_activity,
                'medication_taken': obs.medication_taken,
                'special_events': obs.special_events,
                'timestamp': obs.timestamp.isoformat()
            }
            observation_list.append(observation_dict)
        
        return observation_list
        
    except Exception as e:
        logger.error(f"Error loading observations: {e}")
        return []
    finally:
        session.close()

def authenticate_user_db(username, password):
    """Authenticate user against database"""
    session = get_session()
    try:
        user = session.query(User).filter_by(username=username, password=password).first()
        if user:
            return {
                'id': user.id,
                'username': user.username,
                'user_type': user.user_type,
                'full_name': user.full_name,
                'email': user.email,
                'created_date': user.created_date.isoformat()
            }
        return None
        
    except Exception as e:
        logger.error(f"Error authenticating user: {e}")
        return None
    finally:
        session.close()

def save_intervention_record(intervention_data):
    """Save intervention tracking record"""
    session = get_session()
    try:
        # Get or create student
        student_name = intervention_data.get('student_name', 'Unknown Student')
        
        student = session.query(Student).filter_by(name=student_name).first()
        if not student:
            student = Student(name=student_name, grade_level='Unknown')
            session.add(student)
            session.flush()
        
        # Create intervention record
        intervention = InterventionRecord(
            student_id=student.id,
            intervention_type=intervention_data.get('intervention_type'),
            baseline_score=intervention_data.get('baseline_score'),
            current_score=intervention_data.get('current_score'),
            weeks_elapsed=intervention_data.get('weeks_elapsed'),
            progress_notes=intervention_data.get('notes', '')
        )
        
        session.add(intervention)
        session.commit()
        logger.info(f"Intervention record saved for: {student_name}")
        return True
        
    except Exception as e:
        session.rollback()
        logger.error(f"Error saving intervention record: {e}")
        return False
    finally:
        session.close()

def get_database_stats():
    """Get database statistics"""
    session = get_session()
    try:
        stats = {
            'total_students': session.query(Student).count(),
            'total_predictions': session.query(Prediction).count(),
            'total_observations': session.query(ParentObservation).count(),
            'total_users': session.query(User).count(),
            'total_interventions': session.query(InterventionRecord).count()
        }
        
        # Get latest records
        latest_prediction = session.query(Prediction).order_by(Prediction.timestamp.desc()).first()
        latest_observation = session.query(ParentObservation).order_by(ParentObservation.timestamp.desc()).first()
        
        stats['last_prediction_date'] = latest_prediction.timestamp.isoformat() if latest_prediction else None
        stats['last_observation_date'] = latest_observation.timestamp.isoformat() if latest_observation else None
        
        return stats
        
    except Exception as e:
        logger.error(f"Error getting database stats: {e}")
        return {
            'total_students': 0,
            'total_predictions': 0,
            'total_observations': 0,
            'total_users': 0,
            'total_interventions': 0,
            'last_prediction_date': None,
            'last_observation_date': None
        }
    finally:
        session.close()