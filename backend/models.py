"""SQLAlchemy models for the Smart Request Board."""

from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import DeclarativeBase, Session


DATABASE_URL = "sqlite:///requests.db"
engine = create_engine(DATABASE_URL, echo=False)


class Base(DeclarativeBase):
    pass


class Request(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, autoincrement=True)
    raw_input = Column(String, nullable=False)
    item = Column(String, nullable=False)
    category = Column(String, nullable=False)
    budget_chf = Column(Float, nullable=True)
    priority = Column(String, nullable=False, default="normal")
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "raw_input": self.raw_input,
            "item": self.item,
            "category": self.category,
            "budget_chf": self.budget_chf,
            "priority": self.priority,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


def init_db():
    """Create all tables."""
    Base.metadata.create_all(engine)


def get_session() -> Session:
    return Session(engine)
