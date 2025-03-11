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



import os
import requests
from bs4 import BeautifulSoup
import nest_asyncio
from langchain_community.document_loaders import SitemapLoader, WebBaseLoader

# Configurar USER_AGENT para evitar bloqueos
os.environ["USER_AGENT"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# Aplicar nest_asyncio para evitar errores en Jupyter/Spyder
nest_asyncio.apply()

def obtener_sitemap_url(base_url):
    """Intenta encontrar el sitemap de la web."""
    posibles_sitemaps = [
        f"{base_url}/sitemap.xml",
        f"{base_url}/sitemap_index.xml"
    ]
    
    for sitemap in posibles_sitemaps:
        try:
            response = requests.get(sitemap, timeout=5)
            if response.status_code == 200:
                return sitemap
        except requests.RequestException:
            continue
    return None

def obtener_enlaces(url):
    """Extrae todos los enlaces internos de una página web."""
    try:
        response = requests.get(url, timeout=5, headers={"User-Agent": os.getenv("USER_AGENT")})
        soup = BeautifulSoup(response.text, "html.parser")
        
        enlaces = set()
        for a in soup.find_all("a", href=True):
            link = a["href"]
            if link.startswith("/") or link.startswith(url):  # Solo enlaces internos
                full_link = url + link if link.startswith("/") else link
                enlaces.add(full_link)

        return list(enlaces)
    except requests.RequestException:
        return []

def obtener_contenido_web(url: str):
    """Scrapea contenido de una web usando SitemapLoader si hay sitemap.xml,
       o extrae enlaces manualmente y usa WebBaseLoader si no lo hay.
    """
    texto_completo = ""

    # 1️⃣ Intentar usar SitemapLoader
    sitemap_url = obtener_sitemap_url(url)
    if sitemap_url:
        print(f"📌 Usando SitemapLoader con {sitemap_url}")
        try:
            loader = SitemapLoader(sitemap_url, continue_on_failure=True)
            documentos = loader.load()[:500]  # Limitar a 500 para evitar sobrecarga
            texto_completo = " ".join([doc.page_content for doc in documentos])
            return texto_completo
        except Exception as e:
            print(f"⚠️ Error con SitemapLoader: {e}, intentando método manual.")

    # 2️⃣ Si no hay sitemap.xml, extraer enlaces y usar WebBaseLoader
    print("📌 Usando WebBaseLoader con enlaces extraídos manualmente...")
    enlaces = obtener_enlaces(url)
    documentos = []

    for link in enlaces[:50]:  # Limitar a 50 enlaces para evitar sobrecarga
        try:
            loader = WebBaseLoader(link)
            documentos.extend(loader.load())
        except Exception as e:
            print(f"⚠️ Error al cargar {link}: {e}")

    texto_completo = " ".join([doc.page_content for doc in documentos])
    return texto_completo
