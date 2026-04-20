from sqlalchemy import func
from database import SessionLocal
from models import StudyEntry, Module


def create_entry(module_id: int, duration_minutes: int):
    with SessionLocal() as session:
        entry = StudyEntry(
            module_id=module_id,
            duration_minutes=duration_minutes
        )
        session.add(entry)
        session.commit()
        session.refresh(entry)
        return entry


def get_entries(module_id: int):
    with SessionLocal() as session:
        return (
            session.query(StudyEntry)
            .filter_by(module_id=module_id)
            .all()
        )


def get_all_entries(user_id: int):
    with SessionLocal() as session:
        return (
            session.query(StudyEntry)
            .join(Module)
            .filter(Module.user_id == user_id)
            .all()
        )


def get_total_minutes(user_id: int):
    with SessionLocal() as session:
        total = (
            session.query(func.sum(StudyEntry.duration_minutes))
            .join(Module)
            .filter(Module.user_id == user_id)
            .scalar()
        )
        return total or 0