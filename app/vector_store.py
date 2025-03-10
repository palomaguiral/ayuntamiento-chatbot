"""
para gestionar las búsquedas.
"""

from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Inicializar el almacén vectorial
vector_db = Chroma(persist_directory="./db")

def almacenar_documento(texto: str):
    """Divide el texto en fragmentos y almacena en la base de datos vectorial."""
    embeddings = OpenAIEmbeddings()  # Usamos embeddings de OpenAI
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    documentos = splitter.split_text(texto)

    vector_db.add_texts(documentos, embedding=embeddings)

def buscar_respuesta(pregunta: str):
    """Busca en la base de datos vectorial la información más relevante para la pregunta."""
    embeddings = OpenAIEmbeddings()
    resultados = vector_db.similarity_search(pregunta, k=3)  # Busca los 3 mejores resultados
    return resultados
