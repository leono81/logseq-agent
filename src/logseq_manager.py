import os
import pathlib
import typing


class LogseqManager:
    """
    Gestor para interactuar con un grafo de Logseq.
    
    Esta clase proporciona una interfaz para leer y escribir páginas en un grafo de Logseq,
    manejando la estructura de archivos y las operaciones básicas de contenido.
    """

    def __init__(self, graph_path: str) -> None:
        """
        Inicializa el LogseqManager con la ruta al grafo de Logseq.
        
        Args:
            graph_path: Ruta al directorio raíz del grafo de Logseq
            
        Raises:
            ValueError: Si la ruta del grafo o el subdirectorio 'pages' no existen o no son directorios
        """
        self.graph_path = pathlib.Path(graph_path)
        self.pages_path = self.graph_path / "pages"
        
        # Verificar que el grafo principal existe y es un directorio
        if not self.graph_path.exists():
            raise ValueError(f"La ruta del grafo no existe: {self.graph_path}")
        if not self.graph_path.is_dir():
            raise ValueError(f"La ruta del grafo no es un directorio: {self.graph_path}")
            
        # Verificar que el directorio 'pages' existe y es un directorio
        if not self.pages_path.exists():
            raise ValueError(f"El directorio 'pages' no existe: {self.pages_path}")
        if not self.pages_path.is_dir():
            raise ValueError(f"El directorio 'pages' no es un directorio: {self.pages_path}")

    def _get_page_path(self, page_title: str) -> pathlib.Path:
        """
        Función privada para obtener la ruta de un archivo de página.
        
        Convierte el título de página a la convención de nombres de Logseq,
        reemplazando barras (/) por doble guión bajo (__) y construyendo la ruta completa.
        
        Args:
            page_title: Título de la página a buscar
            
        Returns:
            Path al archivo de la página (no verifica si existe)
        """
        # Reemplazar barras por doble guión bajo según convención de Logseq
        safe_filename = page_title.replace("/", "__")
        
        # Construir la ruta completa con extensión .md
        page_path = self.pages_path / f"{safe_filename}.md"
        
        return page_path

    def page_exists(self, page_title: str) -> bool:
        """
        Comprueba si una página existe en el grafo.
        
        Args:
            page_title: Título de la página a verificar
            
        Returns:
            True si la página existe, False en caso contrario
        """
        # Obtener la ruta potencial del archivo
        page_path = self._get_page_path(page_title)
        
        # Verificar si el archivo realmente existe en el sistema de archivos
        return page_path.exists() and page_path.is_file()

    def read_page_content(self, page_title: str) -> typing.Optional[str]:
        """
        Lee el contenido completo de una página.
        
        Args:
            page_title: Título de la página a leer
            
        Returns:
            Contenido de la página como string si existe, None en caso contrario
        """
        # Verificar si la página existe primero
        if not self.page_exists(page_title):
            return None
        
        # Obtener la ruta del archivo
        page_path = self._get_page_path(page_title)
        
        # Leer el contenido del archivo con encoding UTF-8
        try:
            with open(page_path, 'r', encoding='utf-8') as file:
                content = file.read()
            return content
        except (IOError, OSError) as e:
            # En caso de error de lectura, devolver None
            # Esto podría ocurrir si hay problemas de permisos o el archivo se elimina
            # entre la verificación de existencia y la lectura
            return None

    def create_page(self, page_title: str, content: str = "") -> pathlib.Path:
        """
        Crea una nueva página con el contenido especificado.
        
        Si la página ya existe, no la sobrescribe y retorna la ruta existente.
        
        Args:
            page_title: Título de la nueva página
            content: Contenido inicial de la página (por defecto vacío)
            
        Returns:
            Path al archivo de la página creada o existente
        """
        # Verificar si la página ya existe
        if self.page_exists(page_title):
            # Si existe, devolver la ruta del archivo existente sin modificarlo
            return self._get_page_path(page_title)
        
        # Si no existe, crear la nueva página
        page_path = self._get_page_path(page_title)
        
        # Crear el archivo con el contenido especificado usando encoding UTF-8
        page_path.write_text(content, encoding='utf-8')
        
        # Devolver la ruta del archivo recién creado
        return page_path

    def append_to_page(self, page_title: str, content: str) -> None:
        """
        Añade contenido al final de una página existente como un bloque de Logseq.
        
        El contenido se formatea automáticamente como un bloque (con "- " al principio).
        Si la página no existe, la crea primero y luego añade el contenido.
        
        Args:
            page_title: Título de la página a modificar
            content: Contenido a añadir al final de la página (se formateará como bloque)
        """
        # Obtener la ruta del archivo
        page_path = self._get_page_path(page_title)
        
        # Formatear el contenido como un bloque de Logseq
        formatted_content = f"- {content}"
        
        # Verificar si la página existe
        if not self.page_exists(page_title):
            # Si no existe, crear la página con el contenido formateado (sin \n inicial)
            page_path.write_text(formatted_content, encoding='utf-8')
        else:
            # Si existe, añadir el contenido al final con nueva línea inicial
            with open(page_path, 'a', encoding='utf-8') as file:
                file.write(f"\n{formatted_content}")

    def prepend_to_page(self, page_title: str, content: str) -> None:
        """
        Añade contenido al principio de una página existente como un bloque de Logseq.
        
        El contenido se formatea automáticamente como un bloque (con "- " al principio).
        Si la página no existe, la crea primero con el contenido.
        Útil para implementar funcionalidad de "inbox" donde las entradas nuevas
        aparecen en la parte superior.
        
        Args:
            page_title: Título de la página a modificar
            content: Contenido a añadir al principio de la página (se formateará como bloque)
        """
        # Formatear el contenido como un bloque de Logseq
        formatted_content = f"- {content}"
        
        # Verificar si la página existe
        if not self.page_exists(page_title):
            # Si no existe, crear la página con el contenido formateado
            # Reutilizamos create_page para mantener consistencia
            self.create_page(page_title, content=formatted_content)
        else:
            # Si existe, leer contenido actual y combinar
            current_content = self.read_page_content(page_title)
            
            # Manejar el caso en que read_page_content devuelva None o cadena vacía
            if current_content is None:
                current_content = ""
            
            # Construir el nuevo contenido completo: nuevo + \n + actual
            new_content = f"{formatted_content}\n{current_content}"
            
            # Obtener la ruta del archivo y sobrescribir
            page_path = self._get_page_path(page_title)
            page_path.write_text(new_content, encoding='utf-8')

    def search_in_pages(self, query: str) -> list[str]:
        """
        Busca una cadena de texto en todas las páginas del grafo de Logseq.
        
        Realiza una búsqueda insensible a mayúsculas a través de todo el contenido
        de las páginas y devuelve una lista de títulos de páginas que contienen
        la cadena buscada.
        
        Args:
            query: Cadena de texto a buscar en las páginas
            
        Returns:
            Lista de títulos de páginas que contienen la query. 
            Lista vacía si no se encuentra nada.
            
        Example:
            Si busco "python" y se encuentra en "Ideas__Aprender.md" y "Proyectos__AgenteIA.md",
            devuelve ['Ideas/Aprender', 'Proyectos/AgenteIA']
        """
        # Lista para almacenar los títulos de páginas que contienen la query
        found_pages = []
        
        # Convertir la query a minúsculas para búsqueda insensible a mayúsculas
        query_lower = query.lower()
        
        # Iterar sobre todos los archivos .md en el directorio de páginas
        for page_file in self.pages_path.glob("*.md"):
            try:
                # Leer el contenido del archivo
                content = page_file.read_text(encoding='utf-8')
                
                # Verificar si la query existe en el contenido (insensible a mayúsculas)
                if query_lower in content.lower():
                    # Obtener el nombre del archivo sin la extensión .md
                    page_name = page_file.stem
                    
                    # Convertir de vuelta al formato legible: reemplazar __ por /
                    readable_title = page_name.replace("__", "/")
                    
                    # Añadir a la lista de resultados
                    found_pages.append(readable_title)
                    
            except (IOError, OSError, UnicodeDecodeError):
                # Si hay error leyendo el archivo (permisos, encoding, etc.),
                # simplemente omitir este archivo y continuar con el siguiente
                continue
        
        return found_pages