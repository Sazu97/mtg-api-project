from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from backend.app.models.set import Set
from backend.app.schemas.set import SetCreate, SetUpdate


def get_set_by_id(db: Session, set_id: int) -> Set | None:
    try:
        return db.query(Set).filter(Set.id == set_id).first()
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error fetching set: {str(error)}"
        )


def get_set_by_code(db: Session, code: str) -> Set | None:
    try:
        return db.query(Set).filter(Set.code == code.strip().upper()).first()
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error fetching set by code: {str(error)}"
        )


def get_sets(db: Session, skip: int = 0, limit: int = 100) -> list[Set]:
    try:
        return db.query(Set).order_by(Set.name.asc()).offset(skip).limit(limit).all()
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error listing sets: {str(error)}"
        )


def create_set(db: Session, set_data: SetCreate) -> Set:
    db_set = Set(**set_data.model_dump())
    try:
        db.add(db_set)
        db.commit()
        db.refresh(db_set)
        return db_set
    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error creating set: {str(error)}"
        )


def update_set(db: Session, db_set: Set, set_data: SetUpdate) -> Set:
    update_dict = set_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(db_set, key, value)

    try:
        db.commit()
        db.refresh(db_set)
        return db_set
    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error updating set: {str(error)}"
        )


def delete_set(db: Session, db_set: Set) -> None:
    try:
        db.delete(db_set)
        db.commit()
    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error deleting set: {str(error)}"
        )