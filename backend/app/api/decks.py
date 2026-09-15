from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import current_user
from app.schemas.decks import DeckCreate, DeckResponse, DeckUpdate
from app.services import decks as decks_service

router = APIRouter(prefix="/decks", tags=["Decks"])


@router.get("", response_model=list[DeckResponse])
async def list_decks(user: dict = Depends(current_user)) -> list[DeckResponse]:
    decks = await decks_service.list_decks(user["id"])
    return [DeckResponse(**deck) for deck in decks]


@router.post("", response_model=DeckResponse, status_code=status.HTTP_201_CREATED)
async def create_deck(payload: DeckCreate, user: dict = Depends(current_user)) -> DeckResponse:
    deck = await decks_service.create_deck(user["id"], payload.model_dump())
    return DeckResponse(**deck)


@router.get("/{deck_id}", response_model=DeckResponse)
async def get_deck(deck_id: str, user: dict = Depends(current_user)) -> DeckResponse:
    deck = await decks_service.get_deck(user["id"], deck_id)
    if not deck:
        raise HTTPException(status_code=404, detail="Deck not found")
    return DeckResponse(**deck)


@router.put("/{deck_id}", response_model=DeckResponse)
async def update_deck(deck_id: str, payload: DeckUpdate, user: dict = Depends(current_user)) -> DeckResponse:
    deck = await decks_service.update_deck(user["id"], deck_id, payload.model_dump())
    if not deck:
        raise HTTPException(status_code=404, detail="Deck not found")
    return DeckResponse(**deck)


@router.delete("/{deck_id}", response_model=dict[str, str])
async def remove_deck(deck_id: str, user: dict = Depends(current_user)) -> dict[str, str]:
    removed = await decks_service.delete_deck(user["id"], deck_id)
    if not removed:
        raise HTTPException(status_code=404, detail="Deck not found")
    return {"message": "Deck deleted", "id": deck_id}