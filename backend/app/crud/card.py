from typing import List, Optional
from sqlalchemy.orm import Session
from backend.app.models.card import Card
from backend.app.schemas.card import CardCreate, CardUpdate

# 1. Obtener una carta específica por ID
def get_card_by_id(db: Session, card_id: int) -> Optional[Card]:
    return db.query(Card).filter(Card.id == card_id).first()

# 2. Listado con paginación, filtro por Set y búsqueda por texto
def get_cards(
    db: Session, 
    skip: int = 0, 
    limit: int = 100, 
    set_id: Optional[int] = None,
    name: Optional[str] = None
) -> List[Card]:
    query = db.query(Card)
    if set_id is not None:
        query = query.filter(Card.set_id == set_id)
    if name:
        query = query.filter(Card.name.ilike(f"%{name}%"))
        
    return query.offset(skip).limit(limit).all()

# 3. Crear una carta
def create_card(db: Session, card_data: CardCreate) -> Card:
    db_card = Card(
        name=card_data.name,
        mana_cost=card_data.mana_cost,
        type_line=card_data.type_line,
        rarity=card_data.rarity,
        power=card_data.power,
        toughness=card_data.toughness,
        set_id=card_data.set_id,
    )
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card

#4. Actualizar y eliminar una carta
def update_card(db: Session, db_card: Card, card_data: CardUpdate) -> Card:
    update_dict = card_data.model_dump(exclude_unset=True)

    for key, value in update_dict.items():
        setattr(db_card, key, value)

    db.commit()
    db.refresh(db_card)
    return db_card


def delete_card(db: Session, db_card: Card) -> None:
    db.delete(db_card)
    db.commit()