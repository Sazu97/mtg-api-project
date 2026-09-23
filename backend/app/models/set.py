from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from backend.app.core.database import Base


class Set(Base):
    __tablename__ = "sets"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(10), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    release_date = Column(Date, nullable=True)

    cards = relationship("Card", back_populates="set", cascade="all, delete-orphan")