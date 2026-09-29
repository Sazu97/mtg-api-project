from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.schemas.set_schema import SetCreate, SetResponse, SetUpdate
from backend.app.crud import set_crud as crud_set

router = APIRouter()

@router.get(
    "/",
    response_model=list[SetResponse],
    summary="Listar colecciones",
    description="Devuelve el listado completo de colecciones con paginación."
)
def read_sets(
    skip: int = Query(default=0, ge=0, description="Registros a omitir"),
    limit: int = Query(default=100, ge=1, le=100, description="Límite máximo por página"),
    db: Session = Depends(get_db)
):
    return crud_set.get_sets(db, skip=skip, limit=limit)


@router.get(
    "/{set_id}",
    response_model=SetResponse,
    summary="Obtener una colección por ID"
)
def read_set(set_id: int, db: Session = Depends(get_db)):
    db_set = crud_set.get_set_by_id(db, set_id=set_id)
    if not db_set:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Set con ID {set_id} no encontrado"
        )
    return db_set


@router.post(
    "/",
    response_model=SetResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear una nueva colección"
)
def create_set(set_data: SetCreate, db: Session = Depends(get_db)):
    existing_set = crud_set.get_set_by_code(db, code=set_data.code)
    if existing_set:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ya existe un set registrado con el código '{set_data.code}'"
        )
    return crud_set.create_set(db, set_data=set_data)


@router.put(
    "/{set_id}",
    response_model=SetResponse,
    summary="Actualizar una colección existente"
)
def update_set(set_id: int, set_data: SetUpdate, db: Session = Depends(get_db)):
    db_set = crud_set.get_set_by_id(db, set_id=set_id)
    if not db_set:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Set con ID {set_id} no encontrado"
        )
    
    if set_data.code:
        existing_set = crud_set.get_set_by_code(db, code=set_data.code)
        if existing_set and existing_set.id != set_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe otra colección registrada con el código '{set_data.code}'"
            )
            
    return crud_set.update_set(db, db_set=db_set, set_data=set_data)


@router.delete(
    "/{set_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar una colección"
)
def delete_set(set_id: int, db: Session = Depends(get_db)):
    db_set = crud_set.get_set_by_id(db, set_id=set_id)
    if not db_set:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Set con ID {set_id} no encontrado"
        )
    crud_set.delete_set(db, db_set=db_set)
    return None