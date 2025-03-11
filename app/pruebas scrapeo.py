# -*- coding: utf-8 -*-
"""
Created on Tue Mar 11 14:08:57 2025

@author: I23510
"""
import os
import nest_asyncio
from langchain_community.document_loaders import SitemapLoader

# Configurar el USER_AGENT para evitar bloqueos
os.environ["USER_AGENT"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# Aplicar nest_asyncio para evitar errores en entornos interactivos
nest_asyncio.apply()

# Cargar todas las páginas del sitemap
loader = SitemapLoader("https://www.valencia.es/sitemap.xml")
documentos = loader.load()

# Unir todo el texto
texto_completo = " ".join([doc.page_content for doc in documentos])

print("Scraping completado. Longitud del texto:", len(texto_completo))



#=============================================================================


import requests
import xml.etree.ElementTree as ET
from langchain.document_loaders import WebBaseLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS

# 1. Obtener las URLs del Sitemap
def get_sitemap_urls(sitemap_url):
    response = requests.get(sitemap_url)
    if response.status_code != 200:
        raise Exception("No se pudo obtener el sitemap")
    
    root = ET.fromstring(response.text)
    namespace = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = [elem.text for elem in root.findall(".//ns:loc", namespace)]
    
    return urls

sitemap_url = "https://www.valencia.es/sitemap.xml"
urls = get_sitemap_urls(sitemap_url)
print(f"Se encontraron {len(urls)} URLs en el sitemap.")

# 2. Cargar contenido de las páginas importantes (limitamos a 10 para pruebas)
loader = WebBaseLoader(urls[:10])  # Puedes aumentar el número si lo necesitas
documents = loader.load()

# 3. Crear embeddings usando un modelo de código abierto (Hugging Face)
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# 4. Crear FAISS VectorStore con los embeddings generados
vectorstore = FAISS.from_documents(documents, embedding_model)

# 5. Hacer una consulta semántica
query = "¿Cuáles son los horarios de atención del ayuntamiento?"
results = vectorstore.similarity_search(query)

print('-------------------')
# Mostrar resultados
for result in results:
    print()
    print(result.page_content[:500])  # Muestra solo los primeros caracteres



#===========================================================================
import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.schema import Document

# 1. Obtener las URLs del Sitemap
def get_sitemap_urls(sitemap_url, limit=200):
    response = requests.get(sitemap_url)
    if response.status_code != 200:
        raise Exception("No se pudo obtener el sitemap")
    
    root = ET.fromstring(response.text)
    namespace = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = [elem.text for elem in root.findall(".//ns:loc", namespace)]
    
    return urls[:limit]  # Limitar el número de URLs a procesar

# 2. Extraer contenido de cada URL usando BeautifulSoup
def extract_text_from_url(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print(f"⚠️ No se pudo obtener el contenido de {url}")
            return None
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Eliminar elementos no relevantes (scripts, estilos, etc.)
        for script in soup(["script", "style", "header", "footer", "nav"]):
            script.decompose()
        
        # Obtener el texto limpio
        text = soup.get_text(separator=" ", strip=True)
        return text[:5000]  # Limitar a 5000 caracteres para evitar respuestas demasiado largas
    
    except Exception as e:
        print(f"❌ Error al procesar {url}: {e}")
        return None

# 3. Obtener URLs del Sitemap y extraer contenido
sitemap_url = "https://www.valencia.es/sitemap.xml"
urls = get_sitemap_urls(sitemap_url, limit=200)  # Limita a 5 para pruebas
documents = []

for url in urls:
    text = extract_text_from_url(url)
    if text:
        documents.append(Document(page_content=text, metadata={"source": url}))

print(f"✅ Se extrajo contenido de {len(documents)} páginas.")

# 4. Ver el contenido extraído
for doc in documents:
    print(f"🔹 Fuente: {doc.metadata['source']}")
    #print(f"📄 Contenido: {doc.page_content[:1000]}")  # Muestra solo los primeros 1000 caracteres
    print(f"📄 Contenido: {doc.page_content}") 
    print("\n" + "="*100 + "\n")




# ==========================================

import re
import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from langchain.schema import Document

# 1. Obtener las URLs del Sitemap
def get_sitemap_urls(sitemap_url, limit=50):
    response = requests.get(sitemap_url)
    if response.status_code != 200:
        raise Exception("No se pudo obtener el sitemap")
    
    root = ET.fromstring(response.text)
    namespace = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = [elem.text for elem in root.findall(".//ns:loc", namespace)]
    
    return urls[:limit]  # Limitar el número de URLs a procesar

# 2. Extraer contenido de cada URL usando BeautifulSoup
def extract_text_from_url(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print(f"⚠️ No se pudo obtener el contenido de {url}")
            return None
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Eliminar elementos no relevantes (scripts, estilos, etc.)
        for script in soup(["script", "style", "header", "footer", "nav"]):
            script.decompose()
        
        # Obtener el texto limpio
        text = soup.get_text(separator=" ", strip=True)
        return text[:5000]  # Limitar a 5000 caracteres para evitar respuestas demasiado largas
    
    except Exception as e:
        print(f"❌ Error al procesar {url}: {e}")
        return None

# 3. Obtener URLs del Sitemap y extraer contenido
sitemap_url = "https://www.valencia.es/sitemap.xml"
urls = get_sitemap_urls(sitemap_url, limit=5)
documents = []

for url in urls:
    text = extract_text_from_url(url)
    if text:
        documents.append(Document(page_content=text, metadata={"source": url}))

print(f"✅ Se extrajo contenido de {len(documents)} páginas.")

# 4. Detectar URLs dentro del contenido extraído y obtener su contenido
url_pattern = r"https?://[^\s]+"  # Expresión regular para detectar URLs

new_documents = []  # Almacena el contenido extraído de las nuevas URLs

for doc in documents:
    found_urls = re.findall(url_pattern, doc.page_content)  # Extrae URLs del contenido

    for found_url in found_urls:
        if found_url not in urls:  # Evita procesar URLs ya extraídas
            new_text = extract_text_from_url(found_url)
            if new_text:
                new_documents.append(Document(page_content=new_text, metadata={"source": found_url}))

# Añadir los nuevos documentos detectados
documents.extend(new_documents)

print(f"✅ Se extrajo contenido adicional de {len(new_documents)} URLs detectadas dentro del contenido.")

# 5. Ver el contenido extraído
for doc in documents:
    print(f"🔹 Fuente: {doc.metadata['source']}")
    print(f"📄 Contenido: {doc.page_content[:500]}")
    print("\n" + "="*100 + "\n")

