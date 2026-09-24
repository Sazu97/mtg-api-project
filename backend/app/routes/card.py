from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.schemas.card import CardCreate, CardResponse, CardUpdate
from backend.app.crud import card as crud_card
from backend.app.crud import set as crud_set

router = APIRouter()

# 1. Obtener lista de cartas con filtros
@router.get("/", response_model=List[CardResponse])
def read_cards(
    name: Optional[str] = None,
    set_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return crud_card.get_cards(db, name=name, set_id=set_id, skip=skip, limit=limit)

# 2. Obtener una carta por ID
@router.get("/{card_id}", response_model=CardResponse)
def read_card(card_id: int, db: Session = Depends(get_db)):
    db_card = crud_card.get_card_by_id(db, card_id=card_id)
    if not db_card:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Carta con ID {card_id} no encontrada"
        )
    return db_card

# 3. Crear una nueva carta
@router.post("/", response_model=CardResponse, status_code=status.HTTP_201_CREATED)
def create_card(card_data: CardCreate, db: Session = Depends(get_db)):
    db_set = crud_set.get_set_by_id(db, set_id=card_data.set_id)
    if not db_set:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No se puede crear la carta: el Set con ID {card_data.set_id} no existe"
        )
    return crud_card.create_card(db, card_data=card_data)

# 4. Actualizar una carta existente
@router.put("/{card_id}", response_model=CardResponse)
def update_card(card_id: int, card_data: CardUpdate, db: Session = Depends(get_db)):
    db_card = crud_card.get_card_by_id(db, card_id=card_id)
    if not db_card:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Carta con ID {card_id} no encontrada"
        )

    # Comprobar existencia del Set 
    if card_data.set_id is not None:
        db_set = crud_set.get_set_by_id(db, set_id=card_data.set_id)
        if not db_set:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"No se puede actualizar la carta: el Set con ID {card_data.set_id} no existe"
            )

    return crud_card.update_card(db, db_card=db_card, card_data=card_data)

# 5. Eliminar una carta
@router.delete("/{card_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_card(card_id: int, db: Session = Depends(get_db)):
    db_card = crud_card.get_card_by_id(db, card_id=card_id)
    if not db_card:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Carta con ID {card_id} no encontrada"
        )
    crud_card.delete_card(db, db_card=db_card)
    return None