from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.schemas.set import SetCreate, SetResponse, SetUpdate
from backend.app.crud import set as crud_set

router = APIRouter()

# 1. Listado de Sets
@router.get("/", response_model=List[SetResponse])
def read_sets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_set.get_sets(db, skip=skip, limit=limit)

# 2. Buscar Sets por ID
@router.get("/{set_id}", response_model=SetResponse)
def read_set(set_id: int, db: Session = Depends(get_db)):
    db_set = crud_set.get_set_by_id(db, set_id=set_id)
    if not db_set:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Set con ID {set_id} no encontrado"
        )
    return db_set

# 3. Crear nuevo Set
@router.post("/", response_model=SetResponse, status_code=status.HTTP_201_CREATED)
def create_set(set_data: SetCreate, db: Session = Depends(get_db)):
    existing_set = crud_set.get_set_by_code(db, code=set_data.code)
    if existing_set:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un set con el código '{set_data.code}'"
        )
    return crud_set.create_set(db, set_data=set_data)

# 4. Editar un Set
@router.put("/{set_id}", response_model=SetResponse)
def update_set(set_id: int, set_data: SetUpdate, db: Session = Depends(get_db)):
    db_set = crud_set.get_set_by_id(db, set_id=set_id)
    if not db_set:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Set con ID {set_id} no encontrado"
        )
    
    # Comprobación de ID duplicado
    if set_data.code:
        existing_set = crud_set.get_set_by_code(db, code=set_data.code)
        if existing_set and existing_set.id != set_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe otro set con el código '{set_data.code}'"
            )
            
    return crud_set.update_set(db, db_set=db_set, set_data=set_data)

# 5. Eliminar un Set 
@router.delete("/{set_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_set(set_id: int, db: Session = Depends(get_db)):
    db_set = crud_set.get_set_by_id(db, set_id=set_id)
    if not db_set:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Set con ID {set_id} no encontrado"
        )
    crud_set.delete_set(db, db_set=db_set)
    return None