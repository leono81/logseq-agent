import os
import dotenv
import openai
import logfire
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


class SearchInPages(BaseModel):
    """
    Herramienta para buscar un término en TODAS las páginas de Logseq.
    """
    query: str = Field(
        ..., 
        description="El término de búsqueda. Ej: 'Inteligencia Artificial', 'receta de cocina'"
    )


class CreateTask(BaseModel):
    """
    Herramienta para crear una nueva tarea (TODO) en una página de Logseq.
    """
    page_title: str = Field(
        ..., 
        description="El título de la página donde se creará la tarea. Ej: 'Tareas', 'Proyectos/Mi App'"
    )
    content: str = Field(
        ..., 
        description="La descripción de la tarea a crear. Ej: 'Llamar a mamá', 'Revisar el informe'"
    )


class MarkTaskAsDone(BaseModel):
    """
    Herramienta para marcar una tarea existente como completada (DONE) en una página.
    """
    page_title: str = Field(
        ..., 
        description="El título de la página donde está la tarea a marcar como hecha. Ej: 'Tareas'"
    )
    task_content: str = Field(
        ..., 
        description="El contenido exacto de la tarea a marcar como hecha, sin el 'TODO'. Ej: 'Comprar leche'"
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
        output_type=Union[AppendToPage, ReadPageContent, SearchInPages, CreateTask, MarkTaskAsDone],
        system_prompt=(
            "Eres un asistente de IA especializado en Logseq, un sistema de toma de notas basado en bloques. "
            "Tu tarea es interpretar las solicitudes del usuario y convertirlas en acciones específicas de Logseq.\n\n"
            "Tienes cinco herramientas disponibles:\n\n"
            "1. **CreateTask**: Úsala cuando el usuario quiera crear una TAREA, un PENDIENTE o un TODO. Es la opción preferida para acciones.\n"
            "   - 'Añade la tarea de llamar a mamá' → CreateTask(page_title='Tareas', content='Llamar a mamá')\n"
            "   - 'TODO: Revisar el informe' → CreateTask(page_title='Tareas', content='Revisar el informe')\n"
            "   - 'Recordarme comprar leche' → CreateTask(page_title='Tareas', content='Comprar leche')\n"
            "   - 'Tengo que estudiar para el examen' → CreateTask(page_title='Tareas', content='Estudiar para el examen')\n\n"
            "2. **MarkTaskAsDone**: Úsala cuando el usuario quiera MARCAR COMO HECHA, COMPLETAR o FINALIZAR una tarea existente.\n"
            "   - 'Marca como hecha la tarea de comprar leche' → MarkTaskAsDone(page_title='Tareas', task_content='Comprar leche')\n"
            "   - 'Ya he revisado el informe' → MarkTaskAsDone(page_title='Tareas', task_content='Revisar el informe')\n"
            "   - 'Completé la tarea de llamar al médico' → MarkTaskAsDone(page_title='Tareas', task_content='Llamar al médico')\n"
            "   - 'Terminé de estudiar para el examen' → MarkTaskAsDone(page_title='Tareas', task_content='Estudiar para el examen')\n\n"
            "3. **AppendToPage**: Úsala cuando el usuario quiera AÑADIR, GUARDAR, ANOTAR contenido general (NO tareas).\n"
            "   - 'Apunta que tengo reunión mañana' → AppendToPage(page_title='Agenda', content='Reunión mañana')\n"
            "   - 'Guarda esta idea: usar IA para organizar notas' → AppendToPage(page_title='Ideas', content='Usar IA para organizar notas')\n"
            "   - 'Anota este pensamiento...' → AppendToPage(page_title='Notas', content='[pensamiento]')\n\n"
            "4. **ReadPageContent**: Úsala cuando el usuario quiera LEER, VER, MOSTRAR, REVISAR o preguntar QUÉ HAY en una página específica.\n"
            "   - '¿Qué hay en mis Tareas?' → ReadPageContent(page_title='Tareas')\n"
            "   - 'Muéstrame mis ideas' → ReadPageContent(page_title='Ideas')\n"
            "   - 'Lee mi página de proyectos' → ReadPageContent(page_title='Proyectos')\n"
            "   - '¿Qué tengo anotado en mi agenda?' → ReadPageContent(page_title='Agenda')\n\n"
            "5. **SearchInPages**: Úsala cuando el usuario quiera BUSCAR, ENCONTRAR o preguntar sobre un tema en general a través de TODO el grafo.\n"
            "   - 'Busca mis notas sobre IA' → SearchInPages(query='IA')\n"
            "   - 'Encuentra dónde mencioné el \"Proyecto Apolo\"' → SearchInPages(query='Proyecto Apolo')\n"
            "   - '¿En qué páginas hablo de cocina?' → SearchInPages(query='cocina')\n"
            "   - 'Busca referencias a Python' → SearchInPages(query='Python')\n\n"
            "**IMPORTANTE:** Analiza cuidadosamente la intención del usuario:\n"
            "- Si quiere crear una TAREA/TODO/PENDIENTE → CreateTask\n"
            "- Si quiere MARCAR COMO HECHA/COMPLETAR/FINALIZAR una tarea existente → MarkTaskAsDone\n"
            "- Si quiere AGREGAR/ANOTAR contenido general → AppendToPage\n"
            "- Si quiere VER/LEER una página específica → ReadPageContent\n"
            "- Si quiere BUSCAR/ENCONTRAR en todo el grafo → SearchInPages\n\n"
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
    
    # Configurar Logfire para observabilidad
    logfire.configure()
    
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
    
    # Instrumentar PydanticAI con Logfire para observabilidad completa
    logfire.instrument_pydantic_ai()
    
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
                
                # Usar el agente para interpretar el comando con observabilidad
                print("🤔 Interpretando comando...")
                with logfire.span("procesando_comando: {prompt}", prompt=prompt):
                    result = ai_agent.run_sync(prompt)
                    
                    # Verificar que el resultado sea del tipo esperado
                    if isinstance(result.output, CreateTask):
                        task_action = result.output
                        # Formatear el contenido como una tarea TODO
                        task_content = f"TODO {task_action.content}"
                        logseq_manager.append_to_page(
                            page_title=task_action.page_title,
                            content=task_content
                        )
                        print(f"✅ ¡Tarea creada! Se añadió '{task_content}' a la página '{task_action.page_title}'.")
                        
                    elif isinstance(result.output, MarkTaskAsDone):
                        action = result.output
                        print(f"✅ Marcando tarea como hecha en '{action.page_title}'...")
                        
                        # Construir el contenido viejo y nuevo del bloque
                        old_block = f"TODO {action.task_content}"
                        new_block = f"DONE {action.task_content}"
                        
                        # Llamar a nuestro nuevo método del manager
                        success = logseq_manager.update_block_in_page(
                            action.page_title,
                            old_block,
                            new_block
                        )
                        
                        if success:
                            print(f"🎉 ¡Tarea completada! Se actualizó '{action.task_content}' en '{action.page_title}'.")
                        else:
                            print(f"❌ No pude encontrar la tarea 'TODO {action.task_content}' en la página '{action.page_title}'.")
                        
                    elif isinstance(result.output, AppendToPage):
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
                            
                    elif isinstance(result.output, SearchInPages):
                        search_action = result.output
                        print(f"🔎 Buscando '{search_action.query}' en todas las páginas...")
                        results = logseq_manager.search_in_pages(search_action.query)
                        if results:
                            print(f"✅ Encontré menciones en las siguientes {len(results)} páginas:")
                            for page_title in results:
                                print(f"  - {page_title}")
                        else:
                            print(f"❌ No encontré ninguna página que mencione '{search_action.query}'.")
                            
                    else:
                        print("❌ Lo siento, no pude entender ese comando. ¿Podrías reformularlo?")
                        print("💡 Intenta con algo como: 'Crear tarea: [descripción]', 'Añade [nota] a [página]', '¿Qué hay en [página]?' o 'Busca [término]'")
                
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