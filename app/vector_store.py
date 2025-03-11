"""
vector_store.py
--

Permite gestionar la búsqueda de información relevante utilizando un almacén vectorial 
basado en el modelo de embeddings de Hugging Face. 
Utiliza la librería langchain para manejar embeddings y almacenamiento vectorial con Chroma.
"""

from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Cargar modelo de embeddings desde Hugging Face (No me funcionan los de Ollama con from langchain_ollama.embeddings import OllamaEmbeddings)
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Inicializar el almacÃ©n vectorial
vector_db = Chroma(persist_directory="./db", embedding_function=embeddings) #los datos se guardan de forma persistente en la carpeta ./db.


def almacenar_documentos(documentos):
    """Divide el texto y lo guarda en la base de datos vectorial."""
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50) #necesario porque los modelos de embeddings tienen un lÃ­mite de tokens
    
    textos = [doc.page_content for doc in documentos]
    metadata = [doc.metadata for doc in documentos]

    chunks = splitter.split_text("\n".join(textos)) # 
    vector_db.add_texts(chunks, metadatas=metadata)

def buscar_respuesta(pregunta: str):
    """Busca en la base de datos vectorial la informaciÃ³n mÃ¡s relevante."""
    resultados = vector_db.similarity_search(pregunta, k=3)  # Busca los 3 mejores resultados
    return resultados #Es una lista
