from datetime import datetime
from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))

    modules: Mapped[list["Module"]] = relationship(back_populates="user")


class Module(Base):
    __tablename__ = "modules"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    name: Mapped[str] = mapped_column(String(100))
    color: Mapped[str] = mapped_column(String(7))  # hex color e.g. "#A78BFA"
    is_archived: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="modules")
    entries: Mapped[list["StudyEntry"]] = relationship(back_populates="module")


class StudyEntry(Base):
    __tablename__ = "study_entries"

    id: Mapped[int] = mapped_column(primary_key=True)
    module_id: Mapped[int] = mapped_column(ForeignKey("modules.id"))
    duration_minutes: Mapped[int] = mapped_column(Integer)
    studied_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    module: Mapped["Module"] = relationship(back_populates="entries")