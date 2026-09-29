import json
import urllib.parse
import urllib.request
from urllib.error import HTTPError, URLError

from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from backend.app.models.card_model import Card
from backend.app.schemas.card_schema import CardCreate, CardUpdate


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
    card_dict = card_data.model_dump()

    # Enriquecimiento automático en backend al persistir la carta
    if not card_dict.get("oracle_text"):
        try:
            scryfall_info = fetch_scryfall_card(card_data.name)
            card_dict["oracle_text"] = scryfall_info.get("oracle_text")
        except Exception:
            # Si no hay conexión o no existe en Scryfall, se guarda igualmente sin romper la API
            card_dict["oracle_text"] = None

    db_card = Card(**card_dict)
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


# SCRYFALL
def fetch_scryfall_card(card_name: str) -> dict:
    cleaned_name = card_name.strip()
    if not cleaned_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debes proporcionar un nombre de carta válido"
        )

    encoded_name = urllib.parse.quote(cleaned_name)
    url = f"https://api.scryfall.com/cards/named?fuzzy={encoded_name}"
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "MTGCollectionVault/1.0",
            "Accept": "application/json"
        }
    )

    try:
        with urllib.request.urlopen(req, timeout=6) as response:
            data = json.loads(response.read().decode("utf-8"))
    except HTTPError as e:
        if e.code == 404:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontró ninguna carta con el nombre '{cleaned_name}' en Scryfall"
            )
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Error al comunicar con Scryfall (código HTTP {e.code})"
        )
    except URLError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="No se pudo conectar con el servicio externo de Scryfall"
        )

    raw_rarity = data.get("rarity", "")
    rarity_formatted = raw_rarity.capitalize() if raw_rarity else "Common"

    mana_cost = data.get("mana_cost")
    type_line = data.get("type_line", "")
    power = data.get("power")
    toughness = data.get("toughness")
    oracle_text = data.get("oracle_text")
    image_url = None

    if "image_uris" in data:
        image_url = data["image_uris"].get("normal") or data["image_uris"].get("art_crop")
    elif "card_faces" in data and len(data["card_faces"]) > 0:
        face = data["card_faces"][0]
        mana_cost = mana_cost or face.get("mana_cost")
        type_line = type_line or face.get("type_line", "")
        power = power or face.get("power")
        toughness = toughness or face.get("toughness")
        oracle_text = oracle_text or face.get("oracle_text")
        if "image_uris" in face:
            image_url = face["image_uris"].get("normal")

    return {
        "name": data.get("name", cleaned_name),
        "mana_cost": mana_cost,
        "type_line": type_line,
        "rarity": rarity_formatted,
        "power": power,
        "toughness": toughness,
        "oracle_text": oracle_text,
        "image_url": image_url
    }