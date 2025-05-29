import os
import httpx
from fastapi import APIRouter, Depends, HTTPException,Path, Body
from sqlalchemy.orm import Session
from typing import Optional
from app.crud import create_item, update_item, delete_item
from app.models import TodoItemCreate, TodoItemUpdate, PromptRequest, ClaudeResponse
from app.database import get_db

router = APIRouter()

@router.get("/manifest.json")
def get_manifest():
    return {
        "tools": [
            {
                "name": "create_todo_item",
                "description": "Crea un nuevo ítem en una lista específica",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "description": {"type": "string"},
                        "list_id": {"type": "integer"},
                        "completed": {"type": "boolean", "default": False}
                    },
                    "required": ["description", "list_id"]
                }
            },
            {
                "name": "update_todo_item",
                "description": "Actualiza un ítem existente (descripción, estado o lista)",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "item_id": {"type": "integer"},
                        "description": {"type": "string"},
                        "completed": {"type": "boolean"},
                        "list_id": {"type": "integer"}
                    },
                    "required": ["item_id"]
                }
            },
            {
                "name": "delete_todo_item",
                "description": "Elimina un ítem dado su ID",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "item_id": {"type": "integer"}
                    },
                    "required": ["item_id"]
                }
            }
        ]
    }
    
@router.post("/claude/prompt", response_model=ClaudeResponse)
async def claude_prompt(data: PromptRequest):
    api_key = os.getenv("CLAUDE_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="API key for Claude not configured")

    url = "https://api.anthropic.com/v1/complete"

    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "claude-v1",
        "prompt": data.prompt,
        "max_tokens_to_sample": 1000,
        "stop_sequences": ["\n\nHuman:"]
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        completion = response.json()
    
    text_response = completion.get("completion", "")
    
    return ClaudeResponse(response=text_response)

@router.post("/create_todo_item")
def create_todo_item(data: TodoItemCreate, db: Session = Depends(get_db)):
    return create_item(db, data)

@router.put("/update_todo_item/{item_id}")
def update_todo_item(
    item_id: int = Path(..., description="ID del ítem a actualizar"),
    item_update: TodoItemUpdate = Body(...),
    db: Session = Depends(get_db)):
    if not any([item_update.description, item_update.completed, item_update.list_id]):
        raise HTTPException(status_code=400, detail="No data to update")

    updated = update_item(db, item_id, item_update)
    if not updated:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated


@router.post("/delete_todo_item/{item_id}")
def delete_todo_item(
    item_id: int = Path(..., description="ID del ítem a eliminar"),
    db: Session = Depends(get_db)
):
    deleted = delete_item(db, item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted"}



