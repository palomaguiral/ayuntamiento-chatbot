import sys
import os
# Agregar el directorio raíz del proyecto al sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


import pytest
from fastapi.testclient import TestClient
from app.main import app, get_db
from app.database import Base, engine, SessionLocal
from app.langgraph_utils import generate_response
from app.crud import save_chat
from sqlalchemy.orm import Session

# Configuración de la base de datos de prueba
def override_get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# --- PRUEBAS DE LA API ---

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"mensaje": "El chatbot está en ejecución. Documentación disponible en /docs/."}

def test_chat_endpoint():
    response = client.post("/chat/", json={"message": "Hola"})
    assert response.status_code == 200
    assert "response" in response.json()

# --- PRUEBAS DE FUNCIONALIDAD ---

def test_generate_response():
    message = "¿Cuál es el horario del ayuntamiento?"
    print('ejecuto la función...')
    response = generate_response(message)
    print(response)
    assert isinstance(response, str)
    assert len(response) > 0
    

# --- PRUEBAS DE BASE DE DATOS ---

def test_save_chat():
    db: Session = next(override_get_db())
    chat_entry = save_chat(db, "Hola", "Hola, ¿cómo puedo ayudarte?")
    assert chat_entry.id is not None
    assert chat_entry.user_message == "Hola"
    assert chat_entry.bot_response == "Hola, ¿cómo puedo ayudarte?"


test_generate_response()