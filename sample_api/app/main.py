from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Sample API", description="A simple API for testing purposes", version="1.0.0")


class Item(BaseModel):
    name: str
    description: Optional[str] = None


class ItemResponse(BaseModel):
    item_id: str
    name: str
    description: Optional[str] = None
    message: str


@app.get("/health")
async def health_check():
    """
    Health check endpoint for testing purposes.
    Returns the status of the API.
    """
    return {"status": "healthy"}


@app.get("/items/{item_id}")
async def get_item(
    item_id: str,
    skip: Optional[int] = Query(0, ge=0, description="Number of items to skip"),
    limit: Optional[int] = Query(10, ge=1, le=100, description="Maximum number of items to return")
):
    """
    GET endpoint that accepts path parameter item_id and optional query parameters.
    Returns the received parameters for testing purposes.
    """
    return {
        "item_id": item_id,
        "skip": skip,
        "limit": limit,
        "message": "GET request processed successfully"
    }


@app.post("/items", response_model=ItemResponse)
async def create_item(item: Item):
    """
    POST endpoint that accepts JSON payload with item data.
    Returns the received payload for testing purposes.
    """
    return {
        "item_id": "new_item",
        "name": item.name,
        "description": item.description,
        "message": "POST request processed successfully"
    }


@app.put("/items/{item_id}", response_model=ItemResponse)
async def update_item(item_id: str, item: Item):
    """
    PUT endpoint that accepts path parameter item_id and JSON payload for updates.
    Returns the received parameters and payload for testing purposes.
    """
    return {
        "item_id": item_id,
        "name": item.name,
        "description": item.description,
        "message": "PUT request processed successfully"
    }

