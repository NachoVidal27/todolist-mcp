import os
import requests
from dotenv import load_dotenv

load_dotenv()

CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
CLAUDE_API_URL = os.getenv("CLAUDE_API_URL")

def get_claude_response(prompt: str) -> str:
    headers = {
        "x-api-key": CLAUDE_API_KEY,
        "Content-Type": "application/json",
    }

    data = {
        "model": "claude-2",
        "messages": [
            {"role": "system", "content": "Eres un asistente útil."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens_to_sample": 300,
        "temperature": 0.7,
    }

    response = requests.post(CLAUDE_API_URL, headers=headers, json=data)
    response.raise_for_status()
    result = response.json()
    # La respuesta con texto suele estar en "completion"
    return result.get("completion", "")

if __name__ == "__main__":
    try:
        answer = get_claude_response("¿Qué tareas debería hacer hoy?")
        print("Respuesta de Claude:\n", answer)
    except Exception as e:
        print("Error:", e)
