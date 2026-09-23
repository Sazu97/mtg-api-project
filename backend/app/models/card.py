from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.core.database import Base


class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), index=True, nullable=False)
    mana_cost = Column(String(30), nullable=True)
    type_line = Column(String(150), nullable=False)
    rarity = Column(String(20), nullable=False)
    power = Column(String(10), nullable=True)
    toughness = Column(String(10), nullable=True)

    set_id = Column(Integer, ForeignKey("sets.id", ondelete="CASCADE"), nullable=False)

    set = relationship("Set", back_populates="cards")