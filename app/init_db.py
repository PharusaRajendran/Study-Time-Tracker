# app/init_db.py
from app.database import engine, Base, SessionLocal
from app.models import User, Module, StudyEntry

def init_db():
    Base.metadata.create_all(engine)

    with SessionLocal() as session:
        # check if user exists (verhindert doppelte inserts)
        existing_user = session.query(User).first()
        if existing_user:
            return

        user = User(username="Max", password_hash="test123")
        session.add(user)
        session.commit()

        module = Module(user_id=user.id, name="Applied Mathematics 2", color="#A78BFA")
        session.add(module)
        session.commit()

        entry = StudyEntry(module_id=module.id, duration_minutes=60)
        session.add(entry)
        session.commit()

    print("DB initialized")