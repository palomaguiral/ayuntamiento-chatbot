"""
crud.py
-------
Contiene funciones para interactuar con la base de datos.

- `save_chat(db, user_message, bot_response)`: Guarda un mensaje en la base de datos.
- Usa SQLAlchemy para realizar operaciones en la base de datos.
"""

from sqlalchemy.orm import Session
from .models import ChatMessage #Es el modelo de base de datos definido en models.py (representa la tabla chat_messages).

def save_chat(db: Session, user_message: str, bot_response: str):
    chat = ChatMessage(user_message=user_message, bot_response=bot_response) #Crea un nuevo objeto ChatMessage con los datos.
    db.add(chat) #Lo agrega a la sesión con db.add(chat)
    db.commit() #Confirma los cambios en la base de datos con db.commit().
    db.refresh(chat) #Recarga el objeto desde la base de datos con db.refresh(chat).
    return chat #Devuelve el objeto chat guardado.
