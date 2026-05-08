
from app.database import SessionLocal
from app.models import StudyEntry, Module, User
import hashlib
from sqlalchemy import func


def create_entry(module_id: int, duration_minutes: int):
    with SessionLocal() as session:
        entry = StudyEntry(
            module_id=module_id,
            duration_minutes=duration_minutes
        )
        session.add(entry)
        session.commit()


def get_entries(module_id: int):
    with SessionLocal() as session:
        return session.query(StudyEntry).filter_by(module_id=module_id).all()


def get_total_minutes(user_id: int):
    with SessionLocal() as session:
        total = (
            session.query(func.sum(StudyEntry.duration_minutes))
            .join(Module)
            .filter(Module.user_id == user_id)
            .scalar()
        )
        return total or 0       

def create_user(username: str, password_hash: str):
    with SessionLocal() as session:
        user = User(
            username=username,
            password_hash=password_hash
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
 
def create_module(user_id: int, name: str, color: str):
    with SessionLocal() as session:
        module = Module(
            user_id=user_id,
            name=name,
            color=color
        )
        session.add(module)
        session.commit()
        session.refresh(module)
        return module
        
def get_active_modules(user_id: int):
    """Return non-archived modules for the given user_id, each with its entries.

    Returns a list of dicts with module fields and an `entries` list so callers
    can display the module and its entries without needing an open DB session.
    """
    with SessionLocal() as session:
        modules = (
            session.query(Module)
            .filter(Module.user_id == user_id)
            .filter(Module.is_archived == False)
            .all()
        )

        result = []
        for m in modules:
            entries = (
                session.query(StudyEntry)
                .filter(StudyEntry.module_id == m.id)
                .order_by(StudyEntry.studied_at.desc())
                .all()
            )

            entries_list = [
                {
                    "id": e.id,
                    "module_id": e.module_id,
                    "duration_minutes": e.duration_minutes,
                    "studied_at": e.studied_at,
                }
                for e in entries
            ]

            result.append(
                {
                    "id": m.id,
                    "user_id": m.user_id,
                    "name": m.name,
                    "color": m.color,
                    "is_archived": m.is_archived,
                    "created_at": m.created_at,
                    "entries": entries_list,
                }
            )

        return result
        
def get_archived_modules(user_id: int):
    """Return archived modules for the given user_id, each with its entries."""
    with SessionLocal() as session:
        modules = (
            session.query(Module)
            .filter(Module.user_id == user_id)
            .filter(Module.is_archived == True)
            .all()
        )

        result = []
        for m in modules:
            entries = (
                session.query(StudyEntry)
                .filter(StudyEntry.module_id == m.id)
                .order_by(StudyEntry.studied_at.desc())
                .all()
            )

            entries_list = [
                {
                    "id": e.id,
                    "module_id": e.module_id,
                    "duration_minutes": e.duration_minutes,
                    "studied_at": e.studied_at,
                }
                for e in entries
            ]

            result.append(
                {
                    "id": m.id,
                    "user_id": m.user_id,
                    "name": m.name,
                    "color": m.color,
                    "is_archived": m.is_archived,
                    "created_at": m.created_at,
                    "entries": entries_list,
                }
            )

        return result

def archive_module(module_id: int):
    """Archive the module identified by `module_id` and return it.

    If the module does not exist, returns None.
    """
    with SessionLocal() as session:
        module = session.query(Module).filter(Module.id == module_id).first()
        if not module:
            return None

        if not module.is_archived:
            module.is_archived = True
            session.add(module)
            session.commit()
            session.refresh(module)

        return module

def delete_module(module_id: int):
    """Delete the module and all its study entries.

    Returns True on successful deletion, or None if the module wasn't found.
    """
    with SessionLocal() as session:
        module = session.query(Module).filter(Module.id == module_id).first()
        if not module:
            return None

        # delete related study entries first
        session.query(StudyEntry).filter(StudyEntry.module_id == module_id).delete(synchronize_session=False)
        session.delete(module)
        session.commit()
        return True
        
def get_user(username: str, password: str):
    """Authenticate and return the User for given username and password.

    Authentication order:
    - Fallback to direct equality (covers plaintext test data).
    - Also accept stored SHA256 hex of the password.
    Returns the `User` on success, or `None` on failure.
    """
    with SessionLocal() as session:
        user = session.query(User).filter(User.username == username).first()
        if not user:
            return None

        stored = user.password_hash or ""

        if stored == password:
            return user

        if stored == hashlib.sha256(password.encode()).hexdigest():
            return user

        return None