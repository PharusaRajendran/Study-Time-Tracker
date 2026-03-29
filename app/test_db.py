from database import engine, Base, SessionLocal
from models import User, Module, StudyEntry
import models 

# 1. create all tables
Base.metadata.create_all(engine)
print("Tables created:", [t for t in Base.metadata.tables])

# 2. insert test data
with SessionLocal() as session:
    user = User(username="Max", password_hash="test123")
    session.add(user)
    session.commit()

    module = Module(user_id=user.id, name="Applied Mathematics 2", color="#A78BFA")
    session.add(module)
    session.commit()

    entry = StudyEntry(module_id=module.id, duration_minutes=60)
    session.add(entry)
    session.commit()

# 3. show all entires
with SessionLocal() as session:
    entries = session.query(StudyEntry).all()
    for entry in entries:
        print(f"{entry.module.name} - {entry.duration_minutes} min - {entry.studied_at} - {entry.module.user.username}")
 
print("All good!")