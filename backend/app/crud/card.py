from sqlalchemy.orm import Session
from backend.app.models.card import Card
from backend.app.schemas.card import CardCreate, CardUpdate


def get_card_by_id(db: Session, card_id: int) -> Card | None:
    return db.query(Card).filter(Card.id == card_id).first()


def get_cards(
    db: Session, 
    skip: int = 0, 
    limit: int = 100, 
    set_id: int | None = None,
    name: str | None = None
) -> list[Card]:
    query = db.query(Card)
    if set_id is not None:
        query = query.filter(Card.set_id == set_id)
    if name:
        query = query.filter(Card.name.ilike(f"%{name.strip()}%"))
        
    return query.order_by(Card.id.asc()).offset(skip).limit(limit).all()


def create_card(db: Session, card_data: CardCreate) -> Card:
    db_card = Card(**card_data.model_dump())
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card


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