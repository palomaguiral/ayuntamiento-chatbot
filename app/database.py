# -*- coding: utf-8 -*-
"""
database.py
-----------
Este script configura la conexión a la base de datos usando SQLAlchemy.
Define el motor de base de datos, la sesión y el modelo base para definir las tablas.

- Usa variables de entorno para configurar la URL de la base de datos.
- Crea la sesión para interactuar con la base de datos.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from alembic import command
from alembic.config import Config
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dbname")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()



def run_migrations():
    """Ejecuta las migraciones con Alembic al iniciar la aplicación."""
    try:
        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")
    except Exception as e:
        print(f"Error al ejecutar migraciones: {e}")
