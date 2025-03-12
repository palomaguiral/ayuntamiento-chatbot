# -*- coding: utf-8 -*-
"""
models.py
---------
Define los modelos de base de datos con SQLAlchemy utilizando el enfoque de
"Declarative Mapping".

- Define la tabla `chat_messages` para almacenar los mensajes del usuario y las respuestas del chatbot.
- Usa `DeclarativeBase` de SQLAlchemy para mapear las clases a tablas.
"""

from sqlalchemy import Column, Integer, String, DateTime, func
from .database import Base

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    user_message = Column(String, index=True)
    bot_response = Column(String)
    timestamp = Column(DateTime, default=func.now())
