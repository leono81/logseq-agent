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

- [ ] **Configurar Pydantic AI y OpenAI**
    - [ ] Crear un nuevo archivo `agent.py`.
    - [ ] Configurar el cliente de OpenAI con la API key (usando variables de entorno).
- [ ] **Definir las "Herramientas" (Tools) con Pydantic**
    - [ ] Crear un modelo `AppendToLogseq(BaseModel)` para la acción de añadir contenido.
    - [ ] Crear un modelo `ReadLogseqPage(BaseModel)` para la acción de leer una página.
- [ ] **Crear el Agente Básico**
    - [ ] Crear una función `run_agent(prompt: str)` que:
        - [ ] Tome un prompt de usuario.
        - [ ] Use `pydantic_ai` para convertir el prompt en una de nuestras herramientas (un objeto Pydantic).
        - [ ] Invoque la función correspondiente del `LogseqManager` con los datos del objeto.
- [ ] **Probar el flujo completo**
    - [ ] Probar prompts como: "añade una idea a mi página de 'Inbox': pensar en la estructura del agente".
    - [ ] Probar prompts como: "qué hay en mi página de 'Tareas'".

## Fase 3: Capacidades Avanzadas

- [ ] **Implementar Búsqueda y Recuperación (RAG)**
    - [ ] Crear una función en `LogseqManager` para buscar un término en todos los archivos.
- [ ] **Añadir Herramientas Más Complejas**
    - [ ] Modelo Pydantic para `CreateTask(BaseModel)` que añada un bloque con `[TODO]`.
    - [ ] Modelo Pydantic para `FindInLogseq(BaseModel)` que use la función de búsqueda.
- [ ] **Manejo de Bloques Específicos**
    - [ ] Investigar cómo referenciar y editar bloques específicos (puede requerir `uuid` o parseo más complejo).
- [ ] **Implementar Confirmación de Usuario**
    - [ ] Añadir un paso de confirmación antes de ejecutar acciones de escritura o borrado.

## Fase 4: Observabilidad y Pulido

- [ ] **Integrar Logfire**
    - [ ] Añadir `logfire.configure()` al inicio.
    - [ ] Usar `logfire.instrument_openai()` para trazar las llamadas al LLM.
    - [ ] Añadir spans personalizados a nuestras funciones clave en `LogseqManager` y `agent.py`.
- [ ] **Crear una Interfaz de Usuario (CLI)**
    - [ ] Usar `argparse` o `typer` para crear una interfaz de línea de comandos simple para interactuar con el agente.