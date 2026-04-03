from database import SessionLocal
from models import StudyEntry

def save_study_entry(module_id: int, duration_minutes: int):
    with SessionLocal() as session:
        entry = StudyEntry(
            module_id=module_id,
            duration_minutes=duration_minutes
        )
        session.add(entry)
        session.commit() 

def get_all_entries():
    with SessionLocal() as session:
        entries = session.query(StudyEntry).all()
        return entries       