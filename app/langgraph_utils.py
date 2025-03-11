"""
langgraph_utils.py
------------------
Integra LangGraph para generar respuestas automáticas.

- Implementa un grafo simple para devolver respuestas usando LangGraph.
- Se conecta con `main.py` para generar respuestas a los mensajes.
"""
from langgraph.graph import Graph
#from langchain.experimental.graph import Graph
from langchain.schema.runnable import RunnableLambda
from langchain_ollama import OllamaLLM
from app.vector_store import buscar_respuesta

# Configurar el modelo Mistral con Ollama
modelo = OllamaLLM(model="mistral")

def limpiar_texto(texto):
    print('Limpiando texto...')
    """Limpia el texto del usuario."""
    print(texto.strip().lower())
    return texto.strip().lower()

def buscar_informacion(texto):
    print('buscando chunks similares...')
    """Busca fragmentos relevantes en la base de datos vectorial."""
    resultados = buscar_respuesta(texto) #Lista con los 3 chunks más relevantes
    contexto = " ".join([r.page_content for r in resultados])
    print({"contexto": contexto if contexto else "No encontré información relevante.", "pregunta": texto})
    return {"contexto": contexto if contexto else "No encontré información relevante.", "pregunta": texto} #Para pasarle tanto el contexto como la pregunta al siguiente nodo.

def generar_respuesta(inputs): #inputs -> contexto y pregunta
    print('generando respuesta con IA...')
    """Usa LangChain con Mistral (Ollama) para generar una respuesta."""
    
    contexto = inputs["contexto"]
    pregunta = inputs["pregunta"]
    
    prompt = f"""
    Responde la siguiente pregunta con base en la información proporcionada:

    Pregunta: {pregunta}

    Información relevante:
    {contexto}

    Si la información no es suficiente, responde "No encontré información relevante en la web del ayuntamiento."
    """

    respuesta = modelo.invoke(prompt)
    print(respuesta)
    return respuesta


def generate_response(message: str) -> str: #Ej: ¿Cuándo tiene lugar el taller de circo para niños?
    """Genera una respuesta usando LangGraph con pasos encadenados."""
    graph = Graph()

    graph.add_node("limpiar", RunnableLambda(limpiar_texto)) 
    graph.add_node("buscar", RunnableLambda(buscar_informacion)) 
    graph.add_node("responder", RunnableLambda(generar_respuesta)) 

    graph.set_entry_point("limpiar") #output: pregunta limpia
    graph.add_edge("limpiar", "buscar") #output: diccionario con 'context' y 'pregunta'
    graph.add_edge("buscar", "responder") #output: respuesta

    runnable = graph.compile()  # Compila el gráfico para ejecutarlo
    return runnable.invoke(message)  # Ejecuta el gráfico con un input    











