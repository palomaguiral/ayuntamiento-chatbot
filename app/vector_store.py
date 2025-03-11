"""
para gestionar las búsquedas.
"""

from langchain.vectorstores import Chroma
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Configurar embeddings con Ollama
embeddings = OllamaEmbeddings(model="mistral")

# Inicializar el almacén vectorial
vector_db = Chroma(persist_directory="./db", embedding_function=embeddings) #los datos se guardan de forma persistente en la carpeta ./db.


def almacenar_documento(texto: str):
    """Divide el texto y lo guarda en la base de datos vectorial."""
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    documentos = splitter.split_text(texto)

    vector_db.add_texts(documentos)

def buscar_respuesta(pregunta: str):
    """Busca en la base de datos vectorial la información más relevante."""
    resultados = vector_db.similarity_search(pregunta, k=3)  # Busca los 3 mejores resultados
    return resultados
