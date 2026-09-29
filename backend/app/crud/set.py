from sqlalchemy.orm import Session
from backend.app.models.set import Set
from backend.app.schemas.set import SetCreate, SetUpdate


def get_set_by_id(db: Session, set_id: int) -> Set | None:
    return db.query(Set).filter(Set.id == set_id).first()


def get_set_by_code(db: Session, code: str) -> Set | None:
    return db.query(Set).filter(Set.code == code.strip().upper()).first()


def get_sets(db: Session, skip: int = 0, limit: int = 100) -> list[Set]:
    return db.query(Set).order_by(Set.name.asc()).offset(skip).limit(limit).all()


def create_set(db: Session, set_data: SetCreate) -> Set:
    db_set = Set(**set_data.model_dump())
    db.add(db_set)
    db.commit()
    db.refresh(db_set)
    return db_set


def update_set(db: Session, db_set: Set, set_data: SetUpdate) -> Set:
    update_dict = set_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(db_set, key, value)

    db.commit()
    db.refresh(db_set)
    return db_set


def delete_set(db: Session, db_set: Set) -> None:
    db.delete(db_set)
    db.commit()