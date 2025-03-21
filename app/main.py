# -*- coding: utf-8 -*-
"""
main.py
-------
Define la API con FastAPI.

- Contiene el endpoint `/chat/` para recibir un mensaje y devolver una respuesta.
- Usa SQLAlchemy para registrar las conversaciones en la base de datos.
- Usa LangGraph para generar respuestas automáticas.

Ejecución: uvicorn app.main:app --reload
"""
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.database import SessionLocal, engine, run_migrations
from app.langgraph_utils import generate_response
from app.web_scraper import obtener_contenido_web
from app.vector_store import almacenar_documentos

#-----------------------------------------------------------------------------------------------
#models.Base.metadata.create_all(bind=engine) #crea las tablas en la base de datos si no existen.
"""
Esta línea no maneja cambios en la base de datos después de que la tabla se haya creado. 
Si agregas una nueva columna en el futuro, no se actualizará automáticamente. 
Por eso, Alembic es una mejor opción para gestionar cambios.
"""
#-----------------------------------------------------------------------------------------------
# Ejecutar migraciones antes de iniciar la API
run_migrations()


app = FastAPI()

# Dependencia para la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    """Muestra un mensaje indicando que el chatbot está en ejecución."""
    return {"mensaje": "El chatbot está en ejecución. Documentación disponible en /docs/."}

@app.get("/actualizar/")
def actualizar_bd(url: str): #https://www.valencia.es
    """Obtiene contenido de una web y lo almacena en la base de datos vectorial."""
    documentos = obtener_contenido_web(url)
    almacenar_documentos(documentos)
    return {"mensaje": "Información almacenada con éxito."}

@app.post("/chat/", response_model=schemas.ChatResponse)
def chat(request: schemas.ChatRequest, db: Session = Depends(get_db)):
    response_text = generate_response(request.message)
    crud.save_chat(db, request.message, response_text)
    return schemas.ChatResponse(response=response_text) #convertir el string en un objeto ChatResponse antes de devolverlo en el endpoint
