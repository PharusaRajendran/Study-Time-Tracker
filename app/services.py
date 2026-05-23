from app.database import SessionLocal
from app.models import StudyEntry, Module, User
from sqlalchemy import func
import hashlib

class ServiceError(Exception):
    pass

class UserService:

    def create_user(self, username: str, password_hash: str):
        with SessionLocal() as session:
            user = User(
                username=username,
                password_hash=password_hash
            )
            session.add(user)
            session.commit()
            session.refresh(user)
            return user
    
    def get_user(self, username: str, password: str):
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
    

class ModuleService:

    def create_module(self, user_id: int, name: str, color: str):
        try:
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
        except Exception as error:
            raise ServiceError(f"Module could not be created: {error}")
        
    def get_active_modules(self, user_id: int):
        with SessionLocal() as session:
            modules = (
                session.query(Module)
                .filter(Module.user_id == user_id)
                .filter(Module.is_archived.is_(False))
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
        

    def get_archived_modules(self, user_id: int):
        with SessionLocal() as session:
            modules = (
                session.query(Module)
                .filter(Module.user_id == user_id)
                .filter(Module.is_archived.is_(True))
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

    def archive_module(self, module_id: int):
        with SessionLocal() as session:
            module = session.query(Module).filter(Module.id == module_id).first()
            if not module:
                raise ServiceError("Module not found.")

            if not module.is_archived:
                module.is_archived = True
                session.add(module)
                session.commit()
                session.refresh(module)

        return module
    
    def unarchive_module(self, module_id: int):
        with SessionLocal() as session:
            module = session.query(Module).filter(Module.id == module_id).first()

            if not module:
                raise ServiceError("Module not found.")

            if module.is_archived:
                module.is_archived = False
                session.commit()
                session.refresh(module)

            return module
    

    def delete_module(self, module_id: int):
        with SessionLocal() as session:
            module = session.query(Module).filter(Module.id == module_id).first()
            if not module:
                raise ServiceError("Module not found.")

            session.query(StudyEntry).filter(StudyEntry.module_id == module_id).delete(synchronize_session=False)
            session.delete(module)
            session.commit()
            return True
            
            
class StudyEntryService:

    def create_entry(self, module_id: int, duration_minutes: int):
        if duration_minutes <= 0:
            raise ServiceError("Duration must be greater than 0.")
        
        try:
            with SessionLocal() as session:
                entry = StudyEntry(
                    module_id=module_id,
                    duration_minutes=duration_minutes
                )
                session.add(entry)
                session.commit()
        except Exception as error:
            raise ServiceError(f"Study entry could not be created: {error}")


    def get_entries(self, module_id: int):
        with SessionLocal() as session:
            return session.query(StudyEntry).filter_by(module_id=module_id).all()


    def get_total_minutes(self, user_id: int):
        with SessionLocal() as session:
            total = (
                session.query(func.sum(StudyEntry.duration_minutes))
                .join(Module)
                .filter(Module.user_id == user_id)
                .scalar()
            )
            return total or 0       


user_service = UserService()
module_service = ModuleService()
study_entry_service = StudyEntryService()

        

        

        
