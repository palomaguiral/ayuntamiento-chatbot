"""
crud.py
-------
Contiene funciones para interactuar con la base de datos.

- `save_chat(db, user_message, bot_response)`: Guarda un mensaje en la base de datos.
- Usa SQLAlchemy para realizar operaciones en la base de datos.
"""

from sqlalchemy.orm import Session
from .models import ChatMessage

def save_chat(db: Session, user_message: str, bot_response: str):
    chat = ChatMessage(user_message=user_message, bot_response=bot_response)
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat
