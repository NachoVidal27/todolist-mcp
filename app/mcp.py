import os
from fastapi import APIRouter, Depends, HTTPException,Path, Body
from sqlalchemy.orm import Session
from typing import Optional
from app.crud import create_item, update_item, delete_item
from app.models import TodoItemCreate, TodoItemUpdate, PromptRequest, ClaudeResponse
from app.database import get_db
import requests

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
def claude_prompt(data: PromptRequest):
    api_key = os.getenv("CLAUDE_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="API key for Claude not configured")
    
    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "claude-3-5-sonnet-20241022",  # Updated model
        "messages": [
            {
                "role": "user",
                "content": data.prompt  # Use actual prompt from request
            }
        ],
        "max_tokens": 1000
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        completion = response.json()
        
        # Better error handling for response parsing
        if "content" not in completion or not completion["content"]:
            raise HTTPException(status_code=500, detail="Invalid response from Claude API")
        
        text_response = completion["content"][0].get("text", "")
        if not text_response:
            raise HTTPException(status_code=500, detail="Empty response from Claude API")
            
        return ClaudeResponse(response=text_response)
        
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Request to Claude failed: {str(e)}")
    except (KeyError, IndexError) as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse Claude response: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    
@router.post("/claude/test")
def test_claude():
    api_key = os.getenv("CLAUDE_API_KEY")
    if not api_key:
        return {"error": "No API key"}
    
    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    
    # Minimal test payload
    payload = {
        "model": "claude-3-5-sonnet-20241022",
        "max_tokens": 100,
        "messages": [{"role": "user", "content": "Hello"}]
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        return {
            "status_code": response.status_code,
            "response_text": response.text[:500],  # First 500 chars
            "success": response.status_code == 200
        }
    except Exception as e:
        return {"error": str(e)}    
    
    

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



