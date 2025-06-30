# Agente de IA para Logseq

Un agente de IA en Python para interactuar con bases de conocimiento de Logseq.

## Configuración del Entorno

### Requisitos
- Python 3.11+
- Acceso a un grafo de Logseq

### Instalación

1. **Clonar el repositorio** (si es necesario)
2. **Configurar el entorno virtual:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # En Linux/macOS
   # venv\Scripts\activate   # En Windows
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno:**
   Crear un archivo `.env` con:
   ```
   LOGSEQ_GRAPH_PATH=/ruta/a/tu/grafo/de/logseq
   OPENAI_API_KEY=tu_api_key_de_openai
   ```

## Estructura del Proyecto

```
logseq/
├── src/                    # Código fuente principal
│   ├── __init__.py        # Inicialización del paquete
│   └── logseq_manager.py  # Gestor de archivos de Logseq
├── tests/                 # Tests unitarios
├── docs/                  # Documentación
├── venv/                  # Entorno virtual de Python
├── requirements.txt       # Dependencias del proyecto
└── README.md             # Este archivo
```

## Uso Básico

```python
from src.logseq_manager import LogseqManager
import os

# Cargar la ruta del grafo desde variable de entorno
graph_path = os.getenv('LOGSEQ_GRAPH_PATH')
manager = LogseqManager(graph_path)

# Ejemplo de uso (cuando se implementen los métodos)
# content = manager.read_page_content('Mi Página')
# manager.append_to_page('Inbox', 'Nueva idea')
```

## Estado del Desarrollo

Este proyecto está en **Fase 1: La Base - El Gestor de Archivos**

✅ Configuración del Entorno  
✅ Clase LogseqManager (esqueleto)  
⏳ Implementar Funciones de Lectura  
⏳ Implementar Funciones de Escritura

Ver `task.md` para el roadmap completo.

## Dependencias Principales

- **pydantic**: Para validación de datos y modelado
- **openai**: Cliente para la API de OpenAI  
- **logfire**: Para observabilidad y logging
- **python-dotenv**: Manejo de variables de entorno
- **pytest**: Framework de testing 