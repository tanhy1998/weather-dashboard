import os
import json
from typing import Any

# CHANGED: dict[str, str] -> dict[str, Any] 
# (Because temperature is a float, humidity is an int)
def load_data(file_path: str) -> list[dict[str, Any]]:
    """Load JSON data. Returns an empty list if file doesn't exist."""
    if not os.path.exists(file_path):
        return []

    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, ValueError):
        return []

def save_favourite(file_path: str, data: list[dict[str, Any]]) -> None:
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

def get_favorites(data: list[dict[str, Any]]) -> str:
    if not data:
        return "No favorites saved yet."
    # Added a bullet point for better reading
    return "\n".join(f"- {obj['city']}" for obj in data)