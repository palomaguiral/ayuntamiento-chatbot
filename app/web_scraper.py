from langchain_community.document_loaders import WebBaseLoader

"""
Nota.
WebBaseLoader solo extrae el contenido de la URL específica que le proporcionas.
No sigue enlaces ni hace scraping recursivo dentro de la misma web.


def obtener_contenido_web(url: str):
    #Usa LangChain para extraer contenido de una página web.
    loader = WebBaseLoader(url)
    documentos = loader.load()
    
    # Unimos todos los documentos en un solo string
    texto = " ".join([doc.page_content for doc in documentos])

    return texto
"""


"""
1. Obtener todas las URLs del SiteMap
2. Extraer el contenido de cada una de als URLs
3. Dentro del contenido de cada una de esas URLs del SiteMap, detectamos si hay más URLs (buscamos el patrón https://)
4. Extraemos el contenido también de estas nuevas URLs.


Nota: Al guardar los documentos guardamos su contenido (page_content) y la URL de la que proviene (metadata={"source": ...})
"""

import re
import os
import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from langchain.schema import Document

# Configurar USER_AGENT para evitar bloqueos
os.environ["USER_AGENT"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

def get_sitemap_urls(sitemap_url, limit=50):
    """Obtiene las URLs del sitemap.xml si está disponible."""
    try:
        response = requests.get(sitemap_url, timeout=10)
        if response.status_code != 200:
            raise Exception("No se pudo obtener el sitemap")
        
        root = ET.fromstring(response.text)
        namespace = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        urls = [elem.text for elem in root.findall(".//ns:loc", namespace)]
        
        return urls[:limit]  # Limitar el número de URLs a procesar
    except Exception as e:
        print(f"⚠️ No se encontró sitemap.xml o hubo un error: {e}")
        return None

def extract_text_from_url(url):
    """Extrae el contenido de una página web eliminando scripts y elementos irrelevantes."""
    try:
        response = requests.get(url, timeout=10, headers={"User-Agent": os.getenv("USER_AGENT")})
        if response.status_code != 200:
            print(f"⚠️ No se pudo obtener el contenido de {url}")
            return None
        
        soup = BeautifulSoup(response.text, "html.parser")

        # Eliminar elementos no relevantes
        for script in soup(["script", "style", "header", "footer", "nav"]):
            script.decompose()

        # Obtener texto limpio
        text = soup.get_text(separator=" ", strip=True)
        return text[:5000]  # Limitar a 5000 caracteres para evitar respuestas muy largas
    
    except Exception as e:
        print(f"❌ Error al procesar {url}: {e}")
        return None

def obtener_contenido_web(url: str, limit=50):
    """Scrapea contenido de una web usando sitemap si existe, 
       o extrae enlaces manualmente si no lo hay.
    """
    documents = []
    
    # 1️⃣ Intentar usar SitemapLoader
    sitemap_url = f"{url}/sitemap.xml"
    urls = get_sitemap_urls(sitemap_url, limit)
    
    # 2️⃣ Extraer contenido de las URLs encontradas
    for page_url in urls:
        text = extract_text_from_url(page_url)
        if text:
            documents.append(Document(page_content=text, metadata={"source": page_url}))

    print(f"✅ Se extrajo contenido de {len(documents)} páginas.")

    # 3️⃣ Extraer URLs dentro del contenido obtenido
    url_pattern = r"https?://[^\s]+"  # Expresión regular para detectar URLs adicionales
    new_documents = []

    for doc in documents:
        found_urls = re.findall(url_pattern, doc.page_content)  # Extrae URLs del contenido
        for found_url in found_urls:
            if found_url not in urls:  # Evita procesar URLs ya extraídas
                new_text = extract_text_from_url(found_url)
                if new_text:
                    new_documents.append(Document(page_content=new_text, metadata={"source": found_url}))

    # 4️⃣ Agregar los nuevos documentos extraídos
    documents.extend(new_documents)

    print(f"✅ Se extrajo contenido adicional de {len(new_documents)} URLs detectadas dentro del contenido.")

    return documents
