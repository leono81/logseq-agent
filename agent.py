import os
import dotenv
import openai
from typing import Union
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from src.logseq_manager import LogseqManager


class AppendToPage(BaseModel):
    """
    Herramienta para añadir un nuevo bloque de contenido al final de una página de Logseq.
    
    Esta herramienta permite al agente de IA añadir contenido como bloques (bullets) 
    al final de páginas existentes o crear páginas nuevas si no existen.
    """
    page_title: str = Field(
        ..., 
        description="El título de la página a la que se añadirá el contenido. Ej: 'Tareas', 'Ideas/Proyecto Secreto'"
    )
    content: str = Field(
        ..., 
        description="El texto a añadir como un nuevo bloque. Ej: 'Comprar leche', 'Investigar sobre pydantic-ai'"
    )


class ReadPageContent(BaseModel):
    """
    Herramienta para leer y recuperar el contenido completo de una página de Logseq.
    """
    page_title: str = Field(
        ..., 
        description="El título de la página que se debe leer. Ej: 'Tareas'"
    )


def create_logseq_agent(openai_api_key: str) -> Agent:
    """
    Crea un agente de IA específicamente diseñado para trabajar con Logseq.
    
    Args:
        openai_api_key: Clave de API de OpenAI
        
    Returns:
        Agent: Agente configurado para interpretar comandos y devolver acciones de Logseq
    """
    agent = Agent(
        'openai:gpt-4.1-mini',
        output_type=Union[AppendToPage, ReadPageContent],
        system_prompt=(
            "Eres un asistente de IA especializado en Logseq, un sistema de toma de notas basado en bloques. "
            "Tu tarea es interpretar las solicitudes del usuario y convertirlas en acciones específicas de Logseq.\n\n"
            "Tienes dos herramientas disponibles:\n\n"
            "1. **AppendToPage**: Úsala cuando el usuario quiera AÑADIR, GUARDAR, CREAR, ANOTAR o escribir algo nuevo.\n"
            "   - 'Añade \"Comprar leche\" a mis tareas' → AppendToPage(page_title='Tareas', content='Comprar leche')\n"
            "   - 'Apunta que tengo reunión mañana' → AppendToPage(page_title='Agenda', content='Reunión mañana')\n"
            "   - 'Guarda esta idea: usar IA para organizar notas' → AppendToPage(page_title='Ideas', content='Usar IA para organizar notas')\n\n"
            "2. **ReadPageContent**: Úsala cuando el usuario quiera LEER, VER, MOSTRAR, REVISAR o preguntar QUÉ HAY en una página.\n"
            "   - '¿Qué hay en mis Tareas?' → ReadPageContent(page_title='Tareas')\n"
            "   - 'Muéstrame mis ideas' → ReadPageContent(page_title='Ideas')\n"
            "   - 'Lee mi página de proyectos' → ReadPageContent(page_title='Proyectos')\n"
            "   - '¿Qué tengo anotado en mi agenda?' → ReadPageContent(page_title='Agenda')\n\n"
            "**IMPORTANTE:** Analiza cuidadosamente la intención del usuario:\n"
            "- Si quiere AGREGAR/CREAR → AppendToPage\n"
            "- Si quiere VER/LEER → ReadPageContent\n\n"
            "Si el usuario no especifica una página, usa una página lógica basada en el contexto:\n"
            "- Tareas/TODOs → 'Tareas'\n"
            "- Ideas/pensamientos → 'Ideas'\n"
            "- Notas generales → 'Notas'\n"
            "- Reuniones → 'Agenda'\n"
            "- Proyectos → 'Proyectos'"
        )
    )
    return agent


def initialize_agent():
    """
    Inicializa el agente de IA configurando las conexiones a Logseq y OpenAI.
    
    Returns:
        tuple: (logseq_manager, openai_client) - Instancias configuradas
        
    Raises:
        ValueError: Si alguna variable de entorno requerida no está definida
    """
    # Cargar variables de entorno desde .env
    dotenv.load_dotenv()
    
    # Obtener variables de entorno requeridas
    graph_path = os.getenv('LOGSEQ_GRAPH_PATH')
    openai_api_key = os.getenv('OPENAI_API_KEY')
    
    # Validar que las variables estén definidas
    if not graph_path:
        raise ValueError(
            "❌ ERROR: Variable de entorno LOGSEQ_GRAPH_PATH no encontrada.\n"
            "   Por favor, asegúrate de tener un archivo .env con:\n"
            "   LOGSEQ_GRAPH_PATH=/ruta/a/tu/grafo/de/logseq"
        )
    
    if not openai_api_key:
        raise ValueError(
            "❌ ERROR: Variable de entorno OPENAI_API_KEY no encontrada.\n"
            "   Por favor, asegúrate de tener un archivo .env con:\n"
            "   OPENAI_API_KEY=tu_clave_de_openai"
        )
    
    # Instanciar el cliente de OpenAI
    openai_client = openai.OpenAI(api_key=openai_api_key)
    
    # Instanciar nuestro gestor de Logseq
    logseq_manager = LogseqManager(graph_path=graph_path)
    
    return logseq_manager, openai_client


def main():
    """
    Punto de entrada principal del agente de IA.
    Crea un bucle interactivo para procesar comandos del usuario.
    """
    print("🤖 Inicializando Agente de IA para Logseq...")
    print("=" * 50)
    
    try:
        # Inicializar el agente
        logseq_manager, openai_client = initialize_agent()
        
        # Confirmar inicializaciones exitosas
        print(f"✅ LogseqManager inicializado para el grafo en: {logseq_manager.graph_path}")
        print(f"✅ Cliente de OpenAI inicializado correctamente.")
        
        # Crear el agente de IA
        ai_agent = create_logseq_agent(openai_client.api_key)
        print(f"🤖 Agente de IA creado y listo para interpretar comandos.")
        print(f"🚀 ¡Configuración lista! El agente está funcionando.")
        
        # Información adicional sobre el entorno
        print("\n" + "=" * 50)
        print("📊 Información del entorno:")
        print(f"   📁 Directorio de páginas: {logseq_manager.pages_path}")
        print(f"   🧠 Cliente OpenAI: Configurado y listo")
        print(f"   🤖 Agente IA: Especializado en Logseq")
        print("=" * 50)
        
        # Bucle interactivo principal
        print("\n🎯 ¡Agente listo! Puedes empezar a dar comandos.")
        print("💡 Ejemplos: 'Añade comprar leche a mis tareas', 'Guarda esta idea: usar IA'")
        print("📝 Escribe 'salir' para terminar.\n")
        
        while True:
            try:
                # Pedir comando al usuario
                prompt = input("🗣️  ¿Qué quieres hacer en Logseq? > ").strip()
                
                # Condición de salida
                if prompt.lower() in ['salir', 'exit', 'quit', '']:
                    print("👋 ¡Hasta la vista! Agente desconectado.")
                    break
                
                # Usar el agente para interpretar el comando
                print("🤔 Interpretando comando...")
                result = ai_agent.run_sync(prompt)
                
                # Verificar que el resultado sea del tipo esperado
                if isinstance(result.output, AppendToPage):
                    append_action = result.output
                    
                    # Ejecutar la acción usando nuestro LogseqManager
                    logseq_manager.append_to_page(
                        page_title=append_action.page_title, 
                        content=append_action.content
                    )
                    
                    # Confirmar éxito
                    print(f"✅ ¡Hecho! Se añadió '{append_action.content}' a la página '{append_action.page_title}'.")
                    
                elif isinstance(result.output, ReadPageContent):
                    read_action = result.output
                    print(f"🔎 Leyendo el contenido de la página '{read_action.page_title}'...")
                    content = logseq_manager.read_page_content(read_action.page_title)
                    if content:
                        print("\n--- Contenido de la Página ---")
                        print(content)
                        print("---------------------------\n")
                    else:
                        print(f"❌ La página '{read_action.page_title}' no existe o está vacía.")
                        
                else:
                    print("❌ Lo siento, no pude entender ese comando. ¿Podrías reformularlo?")
                    print("💡 Intenta con algo como: 'Añade [tarea] a [página]' o '¿Qué hay en [página]?'")
                
                print()  # Línea en blanco para separar comandos
                
            except KeyboardInterrupt:
                print("\n👋 ¡Hasta la vista! Agente desconectado.")
                break
            except Exception as e:
                print(f"❌ Error al procesar el comando: {e}")
                print("🔄 Intenta con otro comando o escribe 'salir' para terminar.\n")
        
    except ValueError as e:
        print(f"{e}")
        return 1
    except Exception as e:
        print(f"❌ ERROR inesperado durante la inicialización: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = main()
    exit(exit_code) 