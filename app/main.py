"""
main.py
-------
Define la API con FastAPI.

- Contiene el endpoint `/chat/` para recibir un mensaje y devolver una respuesta.
- Usa SQLAlchemy para registrar las conversaciones en la base de datos.
- Usa LangGraph para generar respuestas automáticas.
"""
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.database import SessionLocal, engine
from app.langgraph_utils import generate_response
from app.web_scraper import obtener_contenido_web
from app.vector_store import almacenar_documentos

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependencia para la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/actualizar/")
def actualizar_bd(url: str):
    """Obtiene contenido de una web y lo almacena en la base de datos vectorial."""
    documentos = obtener_contenido_web(url)
    almacenar_documentos(documentos)
    return {"mensaje": "Información almacenada con éxito."}

@app.post("/chat/", response_model=schemas.ChatResponse)
def chat(request: schemas.ChatRequest, db: Session = Depends(get_db)):
    response_text = generate_response(request.message)
    return crud.save_chat(db, request.message, response_text)
