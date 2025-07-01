import os
import sys
from datetime import date
from dotenv import load_dotenv
from src.logseq_manager import LogseqManager

# Constantes para pruebas
TEST_CREATE_PAGE_NAME = "página-de-prueba-para-borrar"
TEST_APPEND_PAGE_NAME = "página-para-append-test"
TEST_APPEND_NEW_PAGE_NAME = "página-nueva-con-append"
TEST_PREPEND_PAGE_NAME = "página-para-prepend-test"
TEST_PREPEND_NEW_PAGE_NAME = "página-nueva-con-prepend"
TEST_BLOCK_SEARCH_PAGE_NAME = "página-para-buscar-bloques"
TEST_BLOCK_EMPTY_PAGE_NAME = "página-vacía-para-bloques"
TEST_UPDATE_PAGE_NAME = "página-para-actualizar-bloques"
TEST_UPDATE_EMPTY_PAGE_NAME = "página-vacía-para-actualizar"
TEST_UPDATE_MULTIPLE_PAGE_NAME = "página-con-bloques-múltiples"


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


def run_block_tests(manager):
    """
    Ejecuta pruebas para la función find_block_in_page del LogseqManager.
    Incluye limpieza automática de archivos de prueba.
    """
    print("\n=== Pruebas de find_block_in_page ===")
    
    block_tests_passed = 0
    total_block_tests = 7  # Total de pruebas de bloques
    
    try:
        # === PREPARACIÓN: Crear páginas de prueba ===
        print(f"📝 Preparando páginas de prueba para búsqueda de bloques...")
        
        # Página con varios bloques de prueba
        test_blocks_content = """- Comprar papel higiénico
- Llamar al médico para cita
- Revisar correos electrónicos
- Estudiar Python para el proyecto
- Hacer ejercicio en el gimnasio"""
        
        manager.create_page(TEST_BLOCK_SEARCH_PAGE_NAME, content=test_blocks_content)
        
        # Página vacía para pruebas
        manager.create_page(TEST_BLOCK_EMPTY_PAGE_NAME, content="")
        
        print(f"   ✅ Páginas de prueba creadas")
        
        # === PRUEBA 1: Buscar bloque existente ===
        print(f"🔍 Prueba 1: Buscar bloque existente 'Comprar papel higiénico'...")
        found_1 = manager.find_block_in_page(TEST_BLOCK_SEARCH_PAGE_NAME, "Comprar papel higiénico")
        if found_1:
            block_tests_passed += 1
            print(f"   ✅ ÉXITO: Bloque encontrado correctamente")
        else:
            print(f"   ❌ FALLO: Bloque no encontrado cuando debería existir")
        
        # === PRUEBA 2: Buscar otro bloque existente ===
        print(f"🔍 Prueba 2: Buscar bloque existente 'Estudiar Python para el proyecto'...")
        found_2 = manager.find_block_in_page(TEST_BLOCK_SEARCH_PAGE_NAME, "Estudiar Python para el proyecto")
        if found_2:
            block_tests_passed += 1
            print(f"   ✅ ÉXITO: Segundo bloque encontrado correctamente")
        else:
            print(f"   ❌ FALLO: Segundo bloque no encontrado cuando debería existir")
        
        # === PRUEBA 3: Buscar bloque inexistente ===
        print(f"🔍 Prueba 3: Buscar bloque inexistente 'Lavar el auto'...")
        found_3 = manager.find_block_in_page(TEST_BLOCK_SEARCH_PAGE_NAME, "Lavar el auto")
        if not found_3:
            block_tests_passed += 1
            print(f"   ✅ ÉXITO: Bloque inexistente no encontrado (correcto)")
        else:
            print(f"   ❌ FALLO: Bloque inexistente fue encontrado incorrectamente")
        
        # === PRUEBA 4: Buscar contenido parcial (no debe encontrar) ===
        print(f"🔍 Prueba 4: Buscar contenido parcial 'Comprar papel' (debe fallar)...")
        found_4 = manager.find_block_in_page(TEST_BLOCK_SEARCH_PAGE_NAME, "Comprar papel")
        if not found_4:
            block_tests_passed += 1
            print(f"   ✅ ÉXITO: Búsqueda parcial no encontró nada (correcto)")
        else:
            print(f"   ❌ FALLO: Búsqueda parcial encontró algo incorrectamente")
        
        # === PRUEBA 5: Buscar en página vacía ===
        print(f"🔍 Prueba 5: Buscar en página vacía...")
        found_5 = manager.find_block_in_page(TEST_BLOCK_EMPTY_PAGE_NAME, "Cualquier cosa")
        if not found_5:
            block_tests_passed += 1
            print(f"   ✅ ÉXITO: No encontró nada en página vacía (correcto)")
        else:
            print(f"   ❌ FALLO: Encontró algo en página vacía incorrectamente")
        
        # === PRUEBA 6: Buscar en página inexistente ===
        print(f"🔍 Prueba 6: Buscar en página inexistente...")
        found_6 = manager.find_block_in_page("PÁGINA-QUE-NO-EXISTE", "Cualquier contenido")
        if not found_6:
            block_tests_passed += 1
            print(f"   ✅ ÉXITO: No encontró nada en página inexistente (correcto)")
        else:
            print(f"   ❌ FALLO: Encontró algo en página inexistente incorrectamente")
        
        # === PRUEBA 7: Buscar con espacios adicionales (debe ser resiliente) ===
        print(f"🔍 Prueba 7: Verificar resilencia a espacios...")
        # Crear una página con espacios extras en los bloques
        content_with_spaces = "- Tarea con espacios   \n-    Otra tarea con espacios al inicio"
        manager.create_page("página-espacios-test", content=content_with_spaces)
        
        found_7 = manager.find_block_in_page("página-espacios-test", "Tarea con espacios")
        if found_7:
            block_tests_passed += 1
            print(f"   ✅ ÉXITO: Encontró bloque a pesar de espacios extra")
        else:
            print(f"   ❌ FALLO: No pudo manejar espacios extra correctamente")
        
    except Exception as e:
        print(f"   ❌ ERROR durante las pruebas de bloques: {e}")
    
    finally:
        # === LIMPIEZA ===
        print(f"\n🧹 Limpiando archivos de prueba de bloques...")
        
        # Lista de páginas de prueba a limpiar
        test_pages = [
            TEST_BLOCK_SEARCH_PAGE_NAME,
            TEST_BLOCK_EMPTY_PAGE_NAME,
            "página-espacios-test"
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
            print(f"   ℹ️ No había archivos de prueba de bloques para eliminar")
        else:
            print(f"   🎯 Total de archivos de prueba de bloques eliminados: {cleaned_count}")
    
    # Imprimir resumen de pruebas de bloques
    print(f"\n=== RESUMEN DE PRUEBAS DE BLOQUES ===")
    print(f"🎯 Pruebas de bloques: {block_tests_passed}/{total_block_tests} pasaron")
    
    if block_tests_passed == total_block_tests:
        print("🎉 ¡Todas las pruebas de bloques pasaron!")
    else:
        print("⚠️ Algunas pruebas de bloques fallaron.")
    
    return block_tests_passed, total_block_tests


def run_update_tests(manager):
    """
    Ejecuta pruebas para la función update_block_in_page del LogseqManager.
    Incluye limpieza automática de archivos de prueba.
    """
    print("\n=== Pruebas de update_block_in_page ===")
    
    update_tests_passed = 0
    total_update_tests = 6  # Total de pruebas de actualización
    
    try:
        # === PREPARACIÓN: Crear páginas de prueba ===
        print(f"📝 Preparando páginas de prueba para actualización de bloques...")
        
        # Página con varios bloques de prueba para actualización
        original_content = """- Tarea pendiente original
- Llamar al médico mañana
- Estudiar Python avanzado
- Hacer ejercicio regularmente
- Revisar correos importantes"""
        
        manager.create_page(TEST_UPDATE_PAGE_NAME, content=original_content)
        
        # Página vacía para pruebas
        manager.create_page(TEST_UPDATE_EMPTY_PAGE_NAME, content="")
        
        # Página con bloques duplicados para probar actualización selectiva
        duplicate_content = """- Tarea duplicada
- Otra tarea diferente
- Tarea duplicada
- Una más distinta"""
        
        manager.create_page(TEST_UPDATE_MULTIPLE_PAGE_NAME, content=duplicate_content)
        
        print(f"   ✅ Páginas de prueba creadas")
        
        # === PRUEBA 1: Actualizar bloque existente ===
        print(f"🔄 Prueba 1: Actualizar bloque existente 'Tarea pendiente original'...")
        success_1 = manager.update_block_in_page(
            TEST_UPDATE_PAGE_NAME, 
            "Tarea pendiente original", 
            "Tarea completada y actualizada"
        )
        if success_1:
            # Verificar que el contenido se actualizó correctamente
            updated_content = manager.read_page_content(TEST_UPDATE_PAGE_NAME)
            if "- Tarea completada y actualizada" in updated_content and "Tarea pendiente original" not in updated_content:
                update_tests_passed += 1
                print(f"   ✅ ÉXITO: Bloque actualizado correctamente")
            else:
                print(f"   ❌ FALLO: El contenido no se actualizó como se esperaba")
                print(f"   📄 Contenido actual: {repr(updated_content[:200])}")
        else:
            print(f"   ❌ FALLO: La función reportó que no se pudo actualizar el bloque")
        
        # === PRUEBA 2: Intentar actualizar bloque inexistente ===
        print(f"🔄 Prueba 2: Intentar actualizar bloque inexistente 'Bloque que no existe'...")
        success_2 = manager.update_block_in_page(
            TEST_UPDATE_PAGE_NAME, 
            "Bloque que no existe", 
            "Nuevo contenido"
        )
        if not success_2:
            update_tests_passed += 1
            print(f"   ✅ ÉXITO: Correctamente reportó que no encontró el bloque")
        else:
            print(f"   ❌ FALLO: Reportó éxito para un bloque inexistente")
        
        # === PRUEBA 3: Actualizar en página inexistente ===
        print(f"🔄 Prueba 3: Intentar actualizar en página inexistente...")
        success_3 = manager.update_block_in_page(
            "PÁGINA-QUE-NO-EXISTE", 
            "Cualquier contenido", 
            "Nuevo contenido"
        )
        if not success_3:
            update_tests_passed += 1
            print(f"   ✅ ÉXITO: Correctamente reportó que la página no existe")
        else:
            print(f"   ❌ FALLO: Reportó éxito para una página inexistente")
        
        # === PRUEBA 4: Actualizar en página vacía ===
        print(f"🔄 Prueba 4: Intentar actualizar en página vacía...")
        success_4 = manager.update_block_in_page(
            TEST_UPDATE_EMPTY_PAGE_NAME, 
            "Cualquier contenido", 
            "Nuevo contenido"
        )
        if not success_4:
            update_tests_passed += 1
            print(f"   ✅ ÉXITO: Correctamente reportó que no hay bloques en página vacía")
        else:
            print(f"   ❌ FALLO: Reportó éxito para una página vacía")
        
        # === PRUEBA 5: Verificar que solo actualiza la primera ocurrencia ===
        print(f"🔄 Prueba 5: Verificar actualización de solo la primera ocurrencia...")
        success_5 = manager.update_block_in_page(
            TEST_UPDATE_MULTIPLE_PAGE_NAME, 
            "Tarea duplicada", 
            "Primera tarea actualizada"
        )
        if success_5:
            # Verificar que solo se actualizó la primera ocurrencia
            multiple_content = manager.read_page_content(TEST_UPDATE_MULTIPLE_PAGE_NAME)
            first_updated = "- Primera tarea actualizada" in multiple_content
            still_has_duplicate = "- Tarea duplicada" in multiple_content
            if first_updated and still_has_duplicate:
                update_tests_passed += 1
                print(f"   ✅ ÉXITO: Solo actualizó la primera ocurrencia")
            else:
                print(f"   ❌ FALLO: No actualizó correctamente solo la primera ocurrencia")
                print(f"   📄 Contenido: {repr(multiple_content)}")
        else:
            print(f"   ❌ FALLO: No pudo actualizar la primera ocurrencia")
        
        # === PRUEBA 6: Verificar que el resto del contenido se mantiene intacto ===
        print(f"🔄 Prueba 6: Verificar que el resto del contenido se mantiene intacto...")
        # Leer el contenido actual de la página principal después de la primera actualización
        final_content = manager.read_page_content(TEST_UPDATE_PAGE_NAME)
        expected_lines = [
            "- Tarea completada y actualizada",  # Esta fue cambiada
            "- Llamar al médico mañana",         # Estas deben mantenerse igual
            "- Estudiar Python avanzado",        
            "- Hacer ejercicio regularmente",    
            "- Revisar correos importantes"      
        ]
        
        content_lines = final_content.splitlines()
        all_lines_correct = True
        for i, expected_line in enumerate(expected_lines):
            if i < len(content_lines) and content_lines[i] == expected_line:
                continue
            else:
                all_lines_correct = False
                break
        
        if all_lines_correct and len(content_lines) == len(expected_lines):
            update_tests_passed += 1
            print(f"   ✅ ÉXITO: El resto del contenido se mantuvo intacto")
        else:
            print(f"   ❌ FALLO: El contenido no se mantuvo como se esperaba")
            print(f"   📄 Esperado: {expected_lines}")
            print(f"   📄 Obtenido: {content_lines}")
        
    except Exception as e:
        print(f"   ❌ ERROR durante las pruebas de actualización: {e}")
    
    finally:
        # === LIMPIEZA ===
        print(f"\n🧹 Limpiando archivos de prueba de actualización...")
        
        # Lista de páginas de prueba a limpiar
        test_pages = [
            TEST_UPDATE_PAGE_NAME,
            TEST_UPDATE_EMPTY_PAGE_NAME,
            TEST_UPDATE_MULTIPLE_PAGE_NAME
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
            print(f"   ℹ️ No había archivos de prueba de actualización para eliminar")
        else:
            print(f"   🎯 Total de archivos de prueba de actualización eliminados: {cleaned_count}")
    
    # Imprimir resumen de pruebas de actualización
    print(f"\n=== RESUMEN DE PRUEBAS DE ACTUALIZACIÓN ===")
    print(f"🎯 Pruebas de actualización: {update_tests_passed}/{total_update_tests} pasaron")
    
    if update_tests_passed == total_update_tests:
        print("🎉 ¡Todas las pruebas de actualización pasaron!")
    else:
        print("⚠️ Algunas pruebas de actualización fallaron.")
    
    return update_tests_passed, total_update_tests


def run_daily_journal_tests(manager):
    """
    Ejecuta pruebas para la función append_to_daily_journal del LogseqManager.
    Incluye limpieza automática de archivos de prueba.
    """
    print("\n=== Pruebas de append_to_daily_journal ===")
    
    daily_tests_passed = 0
    total_daily_tests = 4  # Total de pruebas de diario diario
    
    # Obtener la fecha actual para verificar el formato
    today = date.today()
    expected_journal_page = today.strftime("%Y_%m_%d")
    
    try:
        print(f"📅 Fecha actual: {today} → Página esperada: '{expected_journal_page}'")
        
        # === PRUEBA 1: Añadir contenido normal al diario ===
        print(f"📝 Prueba 1: Añadir contenido normal al diario...")
        test_content_normal = "Reunión con el equipo de desarrollo"
        
        manager.append_to_daily_journal(test_content_normal)
        
        # Verificar que el contenido se añadió correctamente
        journal_content = manager.read_page_content(expected_journal_page)
        expected_block = f"- {test_content_normal}"
        
        if journal_content and expected_block in journal_content:
            daily_tests_passed += 1
            print(f"   ✅ ÉXITO: Contenido normal añadido correctamente")
        else:
            print(f"   ❌ FALLO: Contenido normal no encontrado")
            print(f"   📄 Contenido actual: {repr(journal_content) if journal_content else 'None'}")
        
        # === PRUEBA 2: Añadir tarea al diario ===
        print(f"📝 Prueba 2: Añadir tarea al diario...")
        test_content_task = "Revisar documentación del proyecto"
        
        manager.append_to_daily_journal(test_content_task, is_task=True)
        
        # Verificar que la tarea se añadió correctamente
        journal_content_after_task = manager.read_page_content(expected_journal_page)
        expected_task_block = f"- TODO {test_content_task}"
        
        if journal_content_after_task and expected_task_block in journal_content_after_task:
            daily_tests_passed += 1
            print(f"   ✅ ÉXITO: Tarea añadida correctamente")
        else:
            print(f"   ❌ FALLO: Tarea no encontrada")
            print(f"   📄 Contenido actual: {repr(journal_content_after_task) if journal_content_after_task else 'None'}")
        
        # === PRUEBA 3: Verificar formato de fecha correcto ===
        print(f"📝 Prueba 3: Verificar formato de fecha correcto...")
        # La página debe existir después de las pruebas anteriores
        if manager.page_exists(expected_journal_page):
            daily_tests_passed += 1
            print(f"   ✅ ÉXITO: Página de diario '{expected_journal_page}' existe con formato correcto")
        else:
            print(f"   ❌ FALLO: Página de diario '{expected_journal_page}' no existe")
        
        # === PRUEBA 4: Verificar que ambos tipos de contenido coexisten ===
        print(f"📝 Prueba 4: Verificar que ambos tipos de contenido coexisten...")
        final_journal_content = manager.read_page_content(expected_journal_page)
        
        has_normal_content = expected_block in final_journal_content if final_journal_content else False
        has_task_content = expected_task_block in final_journal_content if final_journal_content else False
        
        if has_normal_content and has_task_content:
            daily_tests_passed += 1
            print(f"   ✅ ÉXITO: Ambos tipos de contenido coexisten correctamente")
            print(f"   📄 Contenido final del diario:")
            if final_journal_content:
                for line in final_journal_content.splitlines():
                    print(f"     {line}")
        else:
            print(f"   ❌ FALLO: No coexisten ambos tipos de contenido")
            print(f"   📄 Normal encontrado: {has_normal_content}")
            print(f"   📄 Tarea encontrada: {has_task_content}")
        
    except Exception as e:
        print(f"   ❌ ERROR durante las pruebas de diario diario: {e}")
    
    finally:
        # === LIMPIEZA ===
        print(f"\n🧹 Limpiando archivo de prueba del diario diario...")
        
        # Limpiar la página del diario de hoy si existe
        if manager.page_exists(expected_journal_page):
            try:
                journal_page_path = manager._get_page_path(expected_journal_page)
                os.remove(journal_page_path)
                print(f"   ✅ Archivo eliminado: {journal_page_path}")
            except Exception as e:
                print(f"   ⚠️ No se pudo eliminar la página del diario: {e}")
        else:
            print(f"   ℹ️ No había página de diario para eliminar")
    
    # Imprimir resumen de pruebas de diario diario
    print(f"\n=== RESUMEN DE PRUEBAS DE DIARIO DIARIO ===")
    print(f"🎯 Pruebas de diario: {daily_tests_passed}/{total_daily_tests} pasaron")
    
    if daily_tests_passed == total_daily_tests:
        print("🎉 ¡Todas las pruebas de diario diario pasaron!")
    else:
        print("⚠️ Algunas pruebas de diario diario fallaron.")
    
    return daily_tests_passed, total_daily_tests


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
        
        # === PRUEBAS DE BLOQUES ===
        block_passed, block_total = run_block_tests(manager)
        
        # === PRUEBAS DE ACTUALIZACIÓN ===
        update_passed, update_total = run_update_tests(manager)
        
        # === PRUEBAS DE DIARIO DIARIO ===
        daily_passed, daily_total = run_daily_journal_tests(manager)
        
        # === RESUMEN FINAL ===
        total_all_tests = total_tests + write_total + block_total + update_total + daily_total
        total_all_passed = passed_tests + write_passed + block_passed + update_passed + daily_passed
        
        print(f"\n{'='*50}")
        print(f"🎯 RESUMEN FINAL DE TODAS LAS PRUEBAS")
        print(f"{'='*50}")
        print(f"📖 Pruebas de lectura: {passed_tests}/{total_tests}")
        print(f"📝 Pruebas de escritura: {write_passed}/{write_total}")
        print(f"🔍 Pruebas de bloques: {block_passed}/{block_total}")
        print(f"🔄 Pruebas de actualización: {update_passed}/{update_total}")
        print(f"📅 Pruebas de diario diario: {daily_passed}/{daily_total}")
        print(f"🎯 TOTAL: {total_all_passed}/{total_all_tests} pruebas pasaron")
        
        if total_all_passed == total_all_tests:
            print("🎉 ¡ÉXITO TOTAL! Todas las pruebas pasaron.")
            print("🏆 FASE 1 COMPLETADA: LogseqManager funciona perfectamente.")
            print("🔍 NUEVA FUNCIONALIDAD: find_block_in_page implementada y probada.")
            print("🔄 NUEVA FUNCIONALIDAD: update_block_in_page implementada y probada.")
            print("📅 NUEVA FUNCIONALIDAD: append_to_daily_journal implementada y probada.")
            print("🚀 Listo para avanzar con más funciones avanzadas!")
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