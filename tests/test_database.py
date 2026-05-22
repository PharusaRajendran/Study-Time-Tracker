from app.database import SessionLocal
from app.models import User, Module, StudyEntry
import uuid


def test_database_saves_user():
    with SessionLocal() as session:
        user = User(
            username=f"db_test_user_{uuid.uuid4()}",
            password_hash="test_password"
        )

        session.add(user)
        session.commit()

        saved_user = session.query(User).filter_by(id=user.id).first()

        assert saved_user is not None
        assert saved_user.username == user.username


def test_database_saves_module():
    with SessionLocal() as session:
        module = Module(
            user_id=1,
            name="DB Test Module",
            color="#5898ff"
        )

        session.add(module)
        session.commit()
        session.refresh(module)

        saved_module = session.query(Module).filter_by(name="DB Test Module").first()

        assert saved_module is not None
        assert saved_module.name == "DB Test Module"
        assert saved_module.color == "#5898ff"


def test_database_saves_study_entry():
    with SessionLocal() as session:
        entry = StudyEntry(
            module_id=1,
            duration_minutes=25
        )

        session.add(entry)
        session.commit()
        session.refresh(entry)

        saved_entry = session.query(StudyEntry).filter_by(id=entry.id).first()

        assert saved_entry is not None
        assert saved_entry.duration_minutes == 25