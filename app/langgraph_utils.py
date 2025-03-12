# -*- coding: utf-8 -*-
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
    
    if not resultados: #No hay contenido relevante con respecto a la pregunta del usuario
        print({"contexto": "No encontré información relevante.", "pregunta": texto, "fuentes": []})
        return {"contexto": "No encontré información relevante.", "pregunta": texto, "fuentes": []}

    contexto = " ".join([r.page_content for r in resultados])
    fuentes = [r.metadata.get("source", "Fuente desconocida") for r in resultados]
    
    print({"contexto": contexto, "pregunta": texto, "fuentes": fuentes})
    return {"contexto": contexto, "pregunta": texto, "fuentes": fuentes}  #Para pasarle tanto el contexto como la pregunta al siguiente nodo.

def generar_respuesta(inputs): #inputs -> contexto y pregunta
    print('generando respuesta con IA...')
    """Usa LangChain con Mistral (Ollama) para generar una respuesta."""
    
    contexto = inputs["contexto"]
    pregunta = inputs["pregunta"]
    fuentes = inputs["fuentes"]

    # 🚨 Si el contexto es "No encontré información relevante.", devolvemos eso directamente (= Menos llamadas innecesarias al modelo )
    if contexto == "No encontré información relevante.":
        print("🚀 No se invoca al modelo porque no hay información relevante.")
        print("No encontré información relevante.")
        return "No encontré información relevante."
    
    prompt = f"""
    Responde la siguiente pregunta con base en la información proporcionada:

    Pregunta: {pregunta}

    Información relevante:
    {contexto}

    Si la información no es suficiente, responde "No encontré información relevante en la web del ayuntamiento."
    """

    respuesta = modelo.invoke(prompt)
    
    # Agregar fuentes al final de la respuesta
    if fuentes:
        respuesta += "\n\nFuentes:\n" + "\n".join(f"- {fuente}" for fuente in set(fuentes))


    print(respuesta)
    return respuesta


def generate_response(message: str) -> str: #Ej: ¿Cuándo tiene lugar el taller de circo para niños?
    """Genera una respuesta usando LangGraph con pasos encadenados."""
    graph = Graph()

    graph.add_node("limpiar", RunnableLambda(limpiar_texto)) 
    graph.add_node("buscar", RunnableLambda(buscar_informacion)) 
    graph.add_node("responder", RunnableLambda(generar_respuesta)) 

    graph.set_entry_point("limpiar") #output: pregunta limpia (Str)
    graph.add_edge("limpiar", "buscar") #output: diccionario con 'context', 'pregunta' y 'fuentes'
    graph.add_edge("buscar", "responder") #output: respuesta (Str)

    graph.set_finish_point("responder") #que la salida del grafo sea el nodo "responder"

    runnable = graph.compile()  # Compila el gráfico para ejecutarlo
    resultado = runnable.invoke(message)
    print(f"🔴 Resultado final del grafo: {resultado}")

    return resultado  # Ejecuta el gráfico con un input    











