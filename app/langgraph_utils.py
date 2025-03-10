"""
langgraph_utils.py
------------------
Integra LangGraph para generar respuestas automáticas.

- Implementa un grafo simple para devolver respuestas usando LangGraph.
- Se conecta con `main.py` para generar respuestas a los mensajes.
"""

from langgraph.graph import Graph
from langchain.chat_models import ChatOpenAI
from app.vector_store import buscar_respuesta

def limpiar_texto(texto):
    """Limpia el texto del usuario."""
    return texto.strip().lower()

def buscar_informacion(texto):
    """Busca fragmentos relevantes en la base de datos vectorial."""
    resultados = buscar_respuesta(texto)
    contexto = " ".join([r.page_content for r in resultados])
    return contexto if contexto else "No encontré información relevante."

def generar_respuesta(contexto, pregunta):
    """Usa GPT para generar una respuesta basada en el contexto recuperado."""
    modelo = ChatOpenAI(model_name="gpt-4", temperature=0)
    
    prompt = f"""
    Responde la siguiente pregunta con base en la información proporcionada:
    
    Pregunta: {pregunta}
    
    Información relevante:
    {contexto}
    
    Si la información no es suficiente, responde "No encontré información relevante en la web del ayuntamiento."
    """
    
    respuesta = modelo.predict(prompt)
    return respuesta

def generate_response(message: str) -> str:
    """Genera una respuesta usando LangGraph con pasos encadenados."""
    graph = Graph()

    graph.add_step("limpiar", limpiar_texto)
    graph.add_step("buscar", buscar_informacion)
    graph.add_step("responder", generar_respuesta)

    graph.set_entry_point("limpiar")
    graph.add_edge("limpiar", "buscar")
    graph.add_edge("buscar", "responder")

    return graph.run(message)
