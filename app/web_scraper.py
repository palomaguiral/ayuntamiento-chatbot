import requests
from bs4 import BeautifulSoup

def obtener_contenido_web(url: str) -> str:
    """Obtiene el contenido de una página web y lo devuelve como texto limpio."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Lanza un error si la petición falla

        soup = BeautifulSoup(response.text, "html.parser")

        # Extraer el contenido del texto (ajusta según la estructura de la web)
        texto = ' '.join([p.get_text() for p in soup.find_all("p")])
        
        return texto
    except requests.RequestException as e:
        return f"Error al obtener la web: {e}"
