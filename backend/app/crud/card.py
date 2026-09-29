from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from backend.app.models.card import Card
from backend.app.schemas.card import CardCreate, CardUpdate


def get_card_by_id(db: Session, card_id: int) -> Card | None:
    try:
        return db.query(Card).filter(Card.id == card_id).first()
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error fetching card: {str(error)}"
        )


def get_cards(
    db: Session, 
    skip: int = 0, 
    limit: int = 100, 
    set_id: int | None = None,
    name: str | None = None
) -> list[Card]:
    try:
        query = db.query(Card)
        if set_id is not None:
            query = query.filter(Card.set_id == set_id)
        if name:
            query = query.filter(Card.name.ilike(f"%{name.strip()}%"))
            
        return query.order_by(Card.id.asc()).offset(skip).limit(limit).all()
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error listing cards: {str(error)}"
        )


def create_card(db: Session, card_data: CardCreate) -> Card:
    db_card = Card(**card_data.model_dump())
    try:
        db.add(db_card)
        db.commit()
        db.refresh(db_card)
        return db_card
    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error creating card: {str(error)}"
        )


def update_card(db: Session, db_card: Card, card_data: CardUpdate) -> Card:
    update_dict = card_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(db_card, key, value)

    try:
        db.commit()
        db.refresh(db_card)
        return db_card
    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error updating card: {str(error)}"
        )


def delete_card(db: Session, db_card: Card) -> None:
    try:
        db.delete(db_card)
        db.commit()
    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error deleting card: {str(error)}"
        )