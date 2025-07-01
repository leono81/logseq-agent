# Roadmap: Agente IA para Logseq

## Fase 1: La Base - El Gestor de Archivos (Sin IA)

- [X] **Configuración del Entorno**
    - [X] Crear estructura de directorios del proyecto.
    - [X] Inicializar un entorno virtual de Python (`venv`).
    - [X] Crear `requirements.txt` y añadir `pydantic`, `openai`, `logfire`.
    - [X] Instalar dependencias.
- [X] **Crear la clase `LogseqManager`**
    - [X] Crear el archivo `logseq_manager.py`.
    - [X] Definir la clase `LogseqManager` con un inicializador `__init__` que tome la ruta al grafo de Logseq.
- [X] **Implementar Funciones de Lectura (Read-only)**
    - [X] `_get_page_path(page_title: str) -> Path | None`: Función privada para obtener la ruta de un archivo de página.
    - [X] `page_exists(page_title: str) -> bool`: Comprueba si una página existe.
    - [X] `read_page_content(page_title: str) -> str | None`: Lee el contenido completo de una página.
- [ ] **Implementar Funciones de Escritura (Write)**
    - [X] `create_page(page_title: str, content: str = "") -> Path`: Crea una nueva página si no existe.
    - [X] `append_to_page(page_title: str, content: str, ensure_new_line: bool = True)`: Añade contenido al final de una página.
    - [X] `prepend_to_page(page_title: str, content: str, ensure_new_line: bool = True)`: Añade contenido al principio de una página (útil para "inboxes").

## Fase 2: El Cerebro - Integración de la IA

- [X] **Configurar Pydantic AI y OpenAI**
    - [X] Crear un nuevo archivo `agent.py`.
    - [X] Configurar el cliente de OpenAI con la API key (usando variables de entorno).
- [ ] **Definir las "Herramientas" (Tools) con Pydantic**
    - [X] Crear un modelo `AppendToLogseq(BaseModel)` para la acción de añadir contenido.
    - [ ] Crear un modelo `ReadLogseqPage(BaseModel)` para la acción de leer una página.
- [X] **Crear el Agente Básico**
    - [X] Crear una función `run_agent(prompt: str)` que:
        - [X] Tome un prompt de usuario.
        - [X] Use `pydantic_ai` para convertir el prompt en una de nuestras herramientas (un objeto Pydantic).
        - [X] Invoque la función correspondiente del `LogseqManager` con los datos del objeto.
- [ ] **Probar el flujo completo**
    - [X] Probar prompts como: "añade una idea a mi página de 'Inbox': pensar en la estructura del agente".
    - [X] Probar prompts como: "qué hay en mi página de 'Tareas'".

## Fase 3: Capacidades Avanzadas

- [X] **Implementar Búsqueda y Recuperación (RAG)**
    - [X] Crear una función en `LogseqManager` para buscar un término en todos los archivos.
- [X] **Añadir Herramientas Más Complejas**
    - [X] Modelo Pydantic para `CreateTask(BaseModel)` que añada un bloque con `[TODO]`.
    - [X] Modelo Pydantic para `FindInLogseq(BaseModel)` que use la función de búsqueda.
- [X] **Manejo de Bloques Específicos**
    - [X] Investigar cómo referenciar y editar bloques específicos (puede requerir `uuid` o parseo más complejo).
- [X] **Implementar Confirmación de Usuario**
    - [X] Añadir un paso de confirmación antes de ejecutar acciones de escritura o borrado.

## Fase 4: Observabilidad y Pulido

- [X] **Integrar Logfire**
    - [X] Añadir `logfire.configure()` al inicio.
    - [X] Usar `logfire.instrument_openai()` para trazar las llamadas al LLM.
    - [X] Añadir spans personalizados a nuestras funciones clave en `LogseqManager` y `agent.py`.
- [X] **Crear una Interfaz de Usuario (CLI)**
    - [X] Usar `argparse` o `typer` para crear una interfaz de línea de comandos simple para interactuar con el agente.

## Fase 5: El Agente de Flujo Diario
- [X] **Herramienta de Diario Inteligente (`SaveToJournal`)**
    - [X] `LogseqManager`: Evolucionar `append_to_journal` para aceptar fechas.
    - [X] `Agent`: Evolucionar `SaveToJournal` para manejar fechas.
    - [X] `Agent`: Inyectar la fecha actual en el `system_prompt` para dar conciencia temporal.
- [ ] **Herramienta de Eliminación Segura (`DeleteBlock`)**
    - [ ] `LogseqManager`: Crear `delete_block_from_page(page_title, content)`.
    - [ ] `Agent`: Crear la herramienta `DeleteBlock`, protegida con confirmación.

## Fase 6: El Agente Estructurado (Gestión de Conocimiento)
- [ ] **Herramienta de Contactos (`CreatePerson`)**
    - [ ] `Agent`: Crear la herramienta `CreatePerson(name, email, phone)`.
    - [ ] Esta herramienta usará `create_page` y `append_to_page` para construir una página de persona con una plantilla de propiedades.
- [ ] **Herramienta de Agenda (`ScheduleMeeting`)**
    - [ ] `Agent`: Crear la herramienta `ScheduleMeeting(topic, date, attendees)`.
    - [ ] Esta herramienta construirá un bloque estructurado con `SCHEDULED::` y enlaces a los participantes.
- [ ] **Herramienta de Metadatos (`SetBlockProperty`)**
    - [ ] `LogseqManager`: Crear `set_property_on_block(page_title, block_content, key, value)`.
    - [ ] `Agent`: Crear la herramienta `SetBlockProperty` de uso general.

## Fase 7: El Agente Outliner Definitivo
- [ ] **Herramienta de Anidación (`AddNestedBlock`)**
    - [ ] `LogseqManager`: Crear la compleja función `add_nested_block(...)`.
    - [ ] `Agent`: Crear la herramienta `AddNestedBlock` e integrarla.