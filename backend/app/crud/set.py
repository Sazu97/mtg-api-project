from typing import List, Optional
from sqlalchemy.orm import Session
from backend.app.models.set import Set
from backend.app.schemas.set import SetCreate, SetUpdate

# 1. Leer por ID
def get_set_by_id(db: Session, set_id: int):
    return db.query(Set).filter(Set.id == set_id).first()

# 2. Leer por código oficial
def get_set_by_code(db: Session, code: str):
    return db.query(Set).filter(Set.code == code.upper()).first()

# 3. Leer lista paginada
def get_sets(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Set).offset(skip).limit(limit).all()

# 4. Crear Set
def create_set(db: Session, set_data: SetCreate) -> Set:
    db_set = Set(
        code=set_data.code.upper(),  # Aseguramos código en mayúsculas
        name=set_data.name,
        release_date=set_data.release_date,
    )
    db.add(db_set)
    db.commit()
    db.refresh(db_set)
    return db_set

# 5. Actualizar un Set existente
def update_set(db: Session, db_set: Set, set_data: SetUpdate) -> Set:
    update_dict = set_data.model_dump(exclude_unset=True)

    if "code" in update_dict:
        update_dict["code"] = update_dict["code"].upper()

    for key, value in update_dict.items():
        setattr(db_set, key, value)

    db.commit()
    db.refresh(db_set)
    return db_set

# 6. Eliminar un Set
def delete_set(db: Session, db_set: Set) -> None:
    db.delete(db_set)
    db.commit()