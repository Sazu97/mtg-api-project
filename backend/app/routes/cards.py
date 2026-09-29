from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.schemas.card import CardCreate, CardResponse, CardUpdate
from backend.app.crud import card as crud_card
from backend.app.crud import set as crud_set

router = APIRouter()


@router.get(
    "/",
    response_model=list[CardResponse],
    summary="Listar cartas con filtros",
    description="Permite filtrar cartas por nombre o colección con paginación controlada."
)
def read_cards(
    name: str | None = Query(default=None, description="Filtrar por coincidencia de texto"),
    set_id: int | None = Query(default=None, description="Filtrar por ID de colección"),
    skip: int = Query(default=0, ge=0, description="Registros a omitir"),
    limit: int = Query(default=100, ge=1, le=100, description="Límite máximo por página"),
    db: Session = Depends(get_db)
):
    return crud_card.get_cards(db, name=name, set_id=set_id, skip=skip, limit=limit)


@router.get(
    "/{card_id}",
    response_model=CardResponse,
    summary="Obtener una carta por ID"
)
def read_card(card_id: int, db: Session = Depends(get_db)):
    db_card = crud_card.get_card_by_id(db, card_id=card_id)
    if not db_card:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Carta con ID {card_id} no encontrada"
        )
    return db_card


@router.post(
    "/",
    response_model=CardResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear una nueva carta"
)
def create_card(card_data: CardCreate, db: Session = Depends(get_db)):
    db_set = crud_set.get_set_by_id(db, set_id=card_data.set_id)
    if not db_set:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No se puede crear la carta: el Set con ID {card_data.set_id} no existe"
        )
    return crud_card.create_card(db, card_data=card_data)


@router.put(
    "/{card_id}",
    response_model=CardResponse,
    summary="Actualizar una carta existente"
)
def update_card(card_id: int, card_data: CardUpdate, db: Session = Depends(get_db)):
    db_card = crud_card.get_card_by_id(db, card_id=card_id)
    if not db_card:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Carta con ID {card_id} no encontrada"
        )

    if card_data.set_id is not None:
        db_set = crud_set.get_set_by_id(db, set_id=card_data.set_id)
        if not db_set:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"No se puede actualizar la carta: el Set con ID {card_data.set_id} no existe"
            )

    return crud_card.update_card(db, db_card=db_card, card_data=card_data)


@router.delete(
    "/{card_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar una carta"
)
def delete_card(card_id: int, db: Session = Depends(get_db)):
    db_card = crud_card.get_card_by_id(db, card_id=card_id)
    if not db_card:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Carta con ID {card_id} no encontrada"
        )
    crud_card.delete_card(db, db_card=db_card)
    return None