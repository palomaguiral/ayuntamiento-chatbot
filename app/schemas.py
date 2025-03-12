# -*- coding: utf-8 -*-
"""
schemas.py
----------
Define los esquemas de datos con Pydantic.

- Separa los datos de entrada y salida para la API.
- Garantiza validación de datos para los mensajes y respuestas.
"""

from pydantic import BaseModel
from datetime import datetime

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    id: int
    user_message: str
    bot_response: str
    timestamp: datetime
