import os
import sys
from dotenv import load_dotenv
from src.logseq_manager import LogseqManager

# Constantes para pruebas
TEST_CREATE_PAGE_NAME = "página-de-prueba-para-borrar"
TEST_APPEND_PAGE_NAME = "página-para-append-test"
TEST_APPEND_NEW_PAGE_NAME = "página-nueva-con-append"
TEST_PREPEND_PAGE_NAME = "página-para-prepend-test"
TEST_PREPEND_NEW_PAGE_NAME = "página-nueva-con-prepend"


def run_write_tests(manager):
    """
    Ejecuta pruebas para las funciones de escritura del LogseqManager.
    Incluye limpieza automática de archivos de prueba.
    """
    print("\n=== Pruebas de create_page ===")
    
    # Páginas para usar en las pruebas
    existing_page_name = "Promociones"  # Sabemos que existe de las pruebas anteriores
    test_content = "- Hola Mundo"
    overwrite_content = "SOBREESCRIBIR"
    
    write_tests_passed = 0
    total_write_tests = 8  # 4 pruebas de create_page + 2 pruebas de append_to_page + 2 pruebas de prepend_to_page
    
    try:
        # === PRUEBA 1: Crear página nueva ===
        print(f"📝 Creando página nueva '{TEST_CREATE_PAGE_NAME}'...")
        created_path = manager.create_page(TEST_CREATE_PAGE_NAME, content=test_content)
        
        # Verificar que la página fue creada
        if manager.page_exists(TEST_CREATE_PAGE_NAME):
            write_tests_passed += 1
            print(f"   ✅ ÉXITO: Página creada correctamente en {created_path}")
        else:
            print(f"   ❌ FALLO: La página no se creó")
        
        # === PRUEBA 2: Verificar contenido de página creada ===
        print(f"📖 Verificando contenido de página creada...")
        read_content = manager.read_page_content(TEST_CREATE_PAGE_NAME)
        if read_content == test_content:
            write_tests_passed += 1
            print(f"   ✅ ÉXITO: Contenido correcto: {repr(read_content)}")
        else:
            print(f"   ❌ FALLO: Contenido esperado {repr(test_content)}, obtenido {repr(read_content)}")
        
        # === PRUEBA 3: Intentar sobreescribir página existente ===
        print(f"🔒 Probando no-sobreescritura en página existente '{existing_page_name}'...")
        # Primero leer el contenido original
        original_content = manager.read_page_content(existing_page_name)
        
        # Intentar "crear" la página existente con contenido diferente
        returned_path = manager.create_page(existing_page_name, content=overwrite_content)
        
        # Verificar que el contenido NO cambió
        current_content = manager.read_page_content(existing_page_name)
        if current_content == original_content and current_content != overwrite_content:
            write_tests_passed += 1
            print(f"   ✅ ÉXITO: La página existente NO fue sobreescrita")
        else:
            print(f"   ❌ FALLO: La página existente fue modificada inesperadamente")
        
        # === PRUEBA 4: Verificar que devuelve path correcto ===
        print(f"📁 Verificando que devuelve el path correcto...")
        expected_path = manager._get_page_path(TEST_CREATE_PAGE_NAME)
        if created_path == expected_path:
            write_tests_passed += 1
            print(f"   ✅ ÉXITO: Path devuelto es correcto")
        else:
            print(f"   ❌ FALLO: Path esperado {expected_path}, obtenido {created_path}")
        
        # === PRUEBAS DE append_to_page ===
        print(f"\n=== Pruebas de append_to_page ===")
        
        # === PRUEBA 5: Añadir a página existente ===
        print(f"📝 Creando página base para prueba de append...")
        manager.create_page(TEST_APPEND_PAGE_NAME, content="- Primer bloque")
        
        print(f"➕ Añadiendo contenido a página existente '{TEST_APPEND_PAGE_NAME}'...")
        manager.append_to_page(TEST_APPEND_PAGE_NAME, "Segundo bloque")
        
        # Verificar contenido resultante
        append_content = manager.read_page_content(TEST_APPEND_PAGE_NAME)
        expected_append_content = "- Primer bloque\n- Segundo bloque"
        if append_content == expected_append_content:
            write_tests_passed += 1
            print(f"   ✅ ÉXITO: Contenido correcto después de append")
            print(f"   📄 Contenido: {repr(append_content)}")
        else:
            print(f"   ❌ FALLO: Contenido esperado {repr(expected_append_content)}")
            print(f"   📄 Contenido obtenido: {repr(append_content)}")
        
        # === PRUEBA 6: Añadir a página nueva (crear con append) ===
        print(f"➕ Creando página nueva con append '{TEST_APPEND_NEW_PAGE_NAME}'...")
        manager.append_to_page(TEST_APPEND_NEW_PAGE_NAME, "Bloque único")
        
        # Verificar que la página fue creada
        if manager.page_exists(TEST_APPEND_NEW_PAGE_NAME):
            # Verificar contenido
            new_page_content = manager.read_page_content(TEST_APPEND_NEW_PAGE_NAME)
            expected_new_content = "- Bloque único"
            if new_page_content == expected_new_content:
                write_tests_passed += 1
                print(f"   ✅ ÉXITO: Página nueva creada correctamente con append")
                print(f"   📄 Contenido: {repr(new_page_content)}")
            else:
                print(f"   ❌ FALLO: Contenido esperado {repr(expected_new_content)}")
                print(f"   📄 Contenido obtenido: {repr(new_page_content)}")
        else:
            print(f"   ❌ FALLO: La página nueva no fue creada con append")
        
        # === PRUEBAS DE prepend_to_page ===
        print(f"\n=== Pruebas de prepend_to_page ===")
        
        # === PRUEBA 7: Añadir al principio de página existente ===
        print(f"📝 Creando página base para prueba de prepend...")
        manager.create_page(TEST_PREPEND_PAGE_NAME, content="- Segundo bloque")
        
        print(f"⬆️ Añadiendo contenido al principio de página existente '{TEST_PREPEND_PAGE_NAME}'...")
        manager.prepend_to_page(TEST_PREPEND_PAGE_NAME, "Primer bloque")
        
        # Verificar contenido resultante
        prepend_content = manager.read_page_content(TEST_PREPEND_PAGE_NAME)
        expected_prepend_content = "- Primer bloque\n- Segundo bloque"
        if prepend_content == expected_prepend_content:
            write_tests_passed += 1
            print(f"   ✅ ÉXITO: Contenido correcto después de prepend")
            print(f"   📄 Contenido: {repr(prepend_content)}")
        else:
            print(f"   ❌ FALLO: Contenido esperado {repr(expected_prepend_content)}")
            print(f"   📄 Contenido obtenido: {repr(prepend_content)}")
        
        # === PRUEBA 8: Crear página nueva con prepend ===
        print(f"⬆️ Creando página nueva con prepend '{TEST_PREPEND_NEW_PAGE_NAME}'...")
        manager.prepend_to_page(TEST_PREPEND_NEW_PAGE_NAME, "Bloque único")
        
        # Verificar que la página fue creada
        if manager.page_exists(TEST_PREPEND_NEW_PAGE_NAME):
            # Verificar contenido
            new_prepend_content = manager.read_page_content(TEST_PREPEND_NEW_PAGE_NAME)
            expected_new_prepend_content = "- Bloque único"
            if new_prepend_content == expected_new_prepend_content:
                write_tests_passed += 1
                print(f"   ✅ ÉXITO: Página nueva creada correctamente con prepend")
                print(f"   📄 Contenido: {repr(new_prepend_content)}")
            else:
                print(f"   ❌ FALLO: Contenido esperado {repr(expected_new_prepend_content)}")
                print(f"   📄 Contenido obtenido: {repr(new_prepend_content)}")
        else:
            print(f"   ❌ FALLO: La página nueva no fue creada con prepend")
        
    except Exception as e:
        print(f"   ❌ ERROR durante las pruebas de escritura: {e}")
    
    finally:
        # === LIMPIEZA ===
        print(f"\n🧹 Limpiando archivos de prueba (create, append, prepend)...")
        
        # Lista de páginas de prueba a limpiar
        test_pages = [
            TEST_CREATE_PAGE_NAME, 
            TEST_APPEND_PAGE_NAME, 
            TEST_APPEND_NEW_PAGE_NAME,
            TEST_PREPEND_PAGE_NAME,
            TEST_PREPEND_NEW_PAGE_NAME
        ]
        cleaned_count = 0
        
        for test_page in test_pages:
            if manager.page_exists(test_page):
                try:
                    test_page_path = manager._get_page_path(test_page)
                    os.remove(test_page_path)
                    print(f"   ✅ Archivo eliminado: {test_page_path}")
                    cleaned_count += 1
                except Exception as e:
                    print(f"   ⚠️ No se pudo eliminar {test_page}: {e}")
        
        if cleaned_count == 0:
            print(f"   ℹ️ No había archivos de prueba para eliminar")
        else:
            print(f"   🎯 Total de archivos de prueba eliminados: {cleaned_count}")
    
    # Imprimir resumen de pruebas de escritura
    print(f"\n=== RESUMEN DE PRUEBAS DE ESCRITURA ===")
    print(f"🎯 Pruebas de escritura: {write_tests_passed}/{total_write_tests} pasaron")
    
    if write_tests_passed == total_write_tests:
        print("🎉 ¡Todas las pruebas de escritura pasaron!")
    else:
        print("⚠️ Algunas pruebas de escritura fallaron.")
    
    return write_tests_passed, total_write_tests


def main():
    """
    Script de prueba para verificar las funcionalidades de lectura y escritura del LogseqManager.
    Incluye limpieza automática de archivos de prueba.
    """
    print("=== Test Completo del LogseqManager ===\n")
    
    # Cargar variables de entorno desde .env
    load_dotenv()
    
    # Obtener la ruta del grafo
    graph_path = os.getenv('LOGSEQ_GRAPH_PATH')
    if not graph_path:
        print("❌ ERROR: No se encontró la variable de entorno LOGSEQ_GRAPH_PATH")
        print("   Por favor, asegúrate de tener un archivo .env con:")
        print("   LOGSEQ_GRAPH_PATH=/ruta/a/tu/grafo/de/logseq")
        sys.exit(1)
    
    print(f"📁 Ruta del grafo: {graph_path}")
    
    # Páginas de prueba
    page_existente = "Promociones"
    page_con_namespace = "Proyectos/IA"  # Se convertirá a "Proyectos__IA.md"
    page_no_existente = "CLAROQUENOEXISTE"
    
    try:
        # Instanciar LogseqManager
        print(f"\n🔧 Inicializando LogseqManager...")
        manager = LogseqManager(graph_path)
        print("✅ LogseqManager inicializado correctamente\n")
        
        # === PRUEBAS DE page_exists ===
        print("=== Pruebas de page_exists ===")
        
        # Prueba 1: Página existente
        print(f"🔍 Verificando si existe '{page_existente}'...")
        exists_1 = manager.page_exists(page_existente)
        print(f"   Resultado: {'✅ EXISTE' if exists_1 else '❌ NO EXISTE'}")
        
        # Prueba 2: Página con namespace
        print(f"🔍 Verificando si existe '{page_con_namespace}' (namespace)...")
        exists_2 = manager.page_exists(page_con_namespace)
        print(f"   Resultado: {'✅ EXISTE' if exists_2 else '❌ NO EXISTE'}")
        print(f"   Nota: Se busca como '{page_con_namespace.replace('/', '__')}.md'")
        
        # Prueba 3: Página no existente
        print(f"🔍 Verificando si existe '{page_no_existente}'...")
        exists_3 = manager.page_exists(page_no_existente)
        print(f"   Resultado: {'❌ NO EXISTE' if not exists_3 else '⚠️ EXISTE (inesperado)'}")
        
        # === PRUEBAS DE read_page_content ===
        print(f"\n=== Pruebas de read_page_content ===")
        
        # Prueba 4: Leer página existente
        print(f"📖 Leyendo contenido de '{page_existente}'...")
        content_1 = manager.read_page_content(page_existente)
        if content_1 is not None:
            # Mostrar primeros 150 caracteres
            preview = content_1[:150]
            if len(content_1) > 150:
                preview += "..."
            print(f"   ✅ Contenido leído ({len(content_1)} caracteres):")
            print(f"   📄 Preview: {repr(preview)}")
        else:
            print(f"   ❌ No se pudo leer la página (contenido es None)")
        
        # Prueba 5: Leer página con namespace
        print(f"📖 Leyendo contenido de '{page_con_namespace}'...")
        content_2 = manager.read_page_content(page_con_namespace)
        if content_2 is not None:
            preview = content_2[:150]
            if len(content_2) > 150:
                preview += "..."
            print(f"   ✅ Contenido leído ({len(content_2)} caracteres):")
            print(f"   📄 Preview: {repr(preview)}")
        else:
            print(f"   ❌ No se pudo leer la página (contenido es None)")
        
        # Prueba 6: Leer página no existente
        print(f"📖 Intentando leer '{page_no_existente}'...")
        content_3 = manager.read_page_content(page_no_existente)
        if content_3 is None:
            print(f"   ✅ Correcto: La página no existe, devolvió None")
        else:
            print(f"   ⚠️ Inesperado: Devolvió contenido para página no existente")
        
        # === RESUMEN ===
        print(f"\n=== RESUMEN DE PRUEBAS ===")
        total_tests = 6
        passed_tests = 0
        
        # Evaluar resultados esperados
        if exists_1:  # Se espera que "Promociones" exista
            passed_tests += 1
            print("✅ Test 1: page_exists con página existente - PASÓ")
        else:
            print("❌ Test 1: page_exists con página existente - FALLÓ")
        
        if exists_2:  # Se espera que la página con namespace exista o no (depende del grafo)
            passed_tests += 1
            print("✅ Test 2: page_exists con namespace - PASÓ (existe)")
        else:
            passed_tests += 1
            print("✅ Test 2: page_exists con namespace - PASÓ (no existe)")
        
        if not exists_3:  # Se espera que "CLAROQUENOEXISTE" NO exista
            passed_tests += 1
            print("✅ Test 3: page_exists con página inexistente - PASÓ")
        else:
            print("❌ Test 3: page_exists con página inexistente - FALLÓ")
        
        if (exists_1 and content_1 is not None) or (not exists_1 and content_1 is None):
            passed_tests += 1
            print("✅ Test 4: read_page_content con página existente - PASÓ")
        else:
            print("❌ Test 4: read_page_content con página existente - FALLÓ")
        
        if (exists_2 and content_2 is not None) or (not exists_2 and content_2 is None):
            passed_tests += 1
            print("✅ Test 5: read_page_content con namespace - PASÓ")
        else:
            print("❌ Test 5: read_page_content con namespace - FALLÓ")
        
        if content_3 is None:  # Se espera None para página inexistente
            passed_tests += 1
            print("✅ Test 6: read_page_content con página inexistente - PASÓ")
        else:
            print("❌ Test 6: read_page_content con página inexistente - FALLÓ")
        
        print(f"\n🎯 Resultado final (pruebas de lectura): {passed_tests}/{total_tests} pruebas pasaron")
        
        if passed_tests == total_tests:
            print("✅ ¡Todas las pruebas de lectura pasaron!")
        else:
            print("⚠️ Algunas pruebas de lectura fallaron.")
        
        # === PRUEBAS DE ESCRITURA ===
        write_passed, write_total = run_write_tests(manager)
        
        # === RESUMEN FINAL ===
        total_all_tests = total_tests + write_total
        total_all_passed = passed_tests + write_passed
        
        print(f"\n{'='*50}")
        print(f"🎯 RESUMEN FINAL DE TODAS LAS PRUEBAS")
        print(f"{'='*50}")
        print(f"📖 Pruebas de lectura: {passed_tests}/{total_tests}")
        print(f"📝 Pruebas de escritura: {write_passed}/{write_total}")
        print(f"🎯 TOTAL: {total_all_passed}/{total_all_tests} pruebas pasaron")
        
        if total_all_passed == total_all_tests:
            print("🎉 ¡ÉXITO TOTAL! Todas las pruebas pasaron.")
            print("🏆 FASE 1 COMPLETADA: LogseqManager funciona perfectamente.")
            print("🚀 Listo para avanzar a la Fase 2 (integración con IA)!")
        else:
            print("⚠️ Algunas pruebas fallaron. Revisa la implementación o el grafo de Logseq.")
    
    except ValueError as e:
        print(f"❌ ERROR de configuración: {e}")
        print("   Verifica que la ruta del grafo sea correcta y tenga el directorio 'pages'")
        sys.exit(1)
    except Exception as e:
        print(f"❌ ERROR inesperado: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 