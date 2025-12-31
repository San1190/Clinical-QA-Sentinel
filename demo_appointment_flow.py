"""
Script de Demostración del Flujo de Appointment
===============================================

SCRIPT RÁPIDO para ejecutar el flujo completo SIN pytest
Útil para debugging y demostración.

Ejecutar con: python demo_appointment_flow.py
"""

import sys
import logging
from pathlib import Path

# Configurar logging para ver TODO lo que pasa
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================================
# AÑADIR DIRECTORIOS AL PATH (Para que encuentre los módulos)
# ============================================================================

# Añadir el directorio raíz del proyecto al path de Python
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / 'src'))

logger.info(f"Project root: {project_root}")
logger.info(f"Python path configurado correctamente")

# ============================================================================
# IMPORTAR MÓDULOS
# ============================================================================

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from webdriver_manager.chrome import ChromeDriverManager
    
    from pages.login_page import LoginPage
    from pages.appointment_page import AppointmentPage
    from src.patient_data_generator import SyntheticPatientGenerator
    from utils.config_loader import load_config
    
    logger.info("✓ Todos los módulos importados correctamente")
    
except ImportError as e:
    logger.error(f"❌ Error al importar módulos: {e}")
    logger.error("Asegúrate de haber instalado todas las dependencias")
    sys.exit(1)

# ============================================================================
# FUNCIÓN PRINCIPAL DE DEMOSTRACIÓN
# ============================================================================

def run_appointment_flow_demo():
    """
    Ejecuta el flujo completo de appointment como demostración.
    
    FASES:
    1. Configurar WebDriver
    2. Login
    3. Generar datos de paciente
    4. Reservar cita
    5. Verificar confirmación
    """
    
    driver = None
    
    try:
        logger.info("=" * 70)
        logger.info("🚀 DEMO: Flujo Completo de Reserva de Cita")
        logger.info("=" * 70)
        
        # ====================================================================
        # PASO 1: Cargar Configuración
        # ====================================================================
        
        logger.info("\n--- PASO 1: Cargando configuración ---")
        config = load_config()
        logger.info(f"✓ Configuración cargada - Entorno: {config['active_environment']}")
        
        # ====================================================================
        # PASO 2: Configurar WebDriver
        # ====================================================================
        
        logger.info("\n--- PASO 2: Configurando Chrome WebDriver ---")
        
        chrome_options = Options()
        # chrome_options.add_argument('--headless')  # Descomentar para modo headless
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--disable-extensions')
        
        # IMPORTANTE: Deshabilitar popups de seguridad de Chrome
        # Estos popups bloquean la ejecución automática de tests
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--disable-popup-blocking')  # Bloquear TODOS los popups
        chrome_options.add_argument('--disable-notifications')  # Sin notificaciones
        chrome_options.add_argument('--no-first-run')  # Sin wizard de primera vez
        chrome_options.add_argument('--no-default-browser-check')  # Sin check de navegador
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation', 'enable-logging'])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Deshabilitar el gestor de contraseñas de Chrome de forma AGRESIVA
        # Esto evita el popup "Cambia tu contraseña" que bloquea el script
        prefs = {
            'credentials_enable_service': False,  # Deshabilitar gestor de contraseñas
            'profile.password_manager_enabled': False,  # No guardar contraseñas
            'profile.default_content_setting_values.notifications': 2,  # Bloquear notificaciones
            'autofill.profile_enabled': False,  # Deshabilitar autocompletar
            'autofill.credit_card_enabled': False,  # Sin tarjetas
        }
        chrome_options.add_experimental_option('prefs', prefs)
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Configurar timeouts
        driver.set_page_load_timeout(config['timeouts']['page_load_timeout'])
        driver.implicitly_wait(config['timeouts']['implicit_wait'])
        
        logger.info("✓ Chrome WebDriver iniciado")
        
        # ====================================================================
        # PASO 3: Instanciar Page Objects
        # ====================================================================
        
        logger.info("\n--- PASO 3: Instanciando Page Objects ---")
        
        login_page = LoginPage(driver, config)
        appointment_page = AppointmentPage(driver, config)
        
        logger.info("✓ Page Objects creados")
        
        # ====================================================================
        # PASO 4: Autenticación (Login)
        # ====================================================================
        
        logger.info("\n--- PASO 4: Autenticación ---")
        
        # Obtener credenciales
        env_config = config['environments'][config['active_environment']]
        username = env_config['username']
        password = env_config['password']
        
        logger.info(f"Usuario: {username}")
        
        # Navegar y hacer login
        login_page.open()
        logger.info("✓ Página de login abierta")
        
        login_page.login_with_credentials(username, password)
        logger.info("✓ Login ejecutado")
        
        # Verificar éxito
        if not login_page.is_login_successful():
            raise Exception("❌ Login falló - no se encontró indicador de éxito")
        
        logger.info("✅ Login exitoso")
        
        # ====================================================================
        # PASO 5: Generar Datos Sintéticos de Paciente
        # ====================================================================
        
        logger.info("\n--- PASO 5: Generando Datos de Paciente ---")
        
        generator = SyntheticPatientGenerator()
        patient = generator.generate_patient()
        
        logger.info("✅ Paciente sintético generado:")
        logger.info(f"   → ID: {patient['patient_id']}")
        logger.info(f"   → Nombre: {patient['full_name']}")
        logger.info(f"   → Sangre: {patient['blood_type']}")
        logger.info(f"   → Alergias: {patient['allergies']}")
        
        # Formatear notas médicas
        medical_notes = (
            f"PACIENTE: {patient['full_name']} | "
            f"SANGRE: {patient['blood_type']} | "
            f"ALERGIAS: {patient['allergies']}"
        )
        
        # ====================================================================
        # PASO 6: Reservar Cita Médica
        # ====================================================================
        
        logger.info("\n--- PASO 6: Reservando Cita Médica ---")
        
        # IMPORTANTE: Cerrar cualquier popup de Google que pueda haber aparecido
        # A veces Google muestra popups de seguridad que bloquean el formulario
        try:
            from selenium.webdriver.common.by import By
            from selenium.common.exceptions import NoSuchElementException, TimeoutException
            
            logger.info("Verificando si hay popups de Google que cerrar...")
            
            # Intentar cerrar popup de "Cambia tu contraseña" si existe
            try:
                # Buscar botón "Aceptar" del popup de contraseña
                popup_accept_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Aceptar')]")
                popup_accept_btn.click()
                logger.info("✓ Popup de Google cerrado")
                import time
                time.sleep(1)  # Esperar a que desaparezca el popup
            except NoSuchElementException:
                logger.info("✓ No hay popup de Google para cerrar")
        except Exception as e:
            logger.warning(f"Error al intentar cerrar popup: {e}")
        
        # Ahora sí, rellenar el formulario de cita
        appointment_page.fill_appointment_form(
            comment=medical_notes,
            visit_date="30/01/2025"
        )
        
        logger.info("✓ Formulario de cita completado y enviado")
        
        # ====================================================================
        # PASO 7: Verificar Confirmación
        # ====================================================================
        
        logger.info("\n--- PASO 7: Verificando Confirmación ---")
        
        if appointment_page.is_appointment_confirmed():
            logger.info("✅✅✅ ¡CITA CONFIRMADA EXITOSAMENTE! ✅✅✅")
            logger.info(f"✅ Paciente {patient['full_name']} tiene cita programada")
            logger.info("\n🎉 DEMOSTRACIÓN COMPLETADA CON ÉXITO 🎉")
            return True
        else:
            logger.error("❌ No se encontró confirmación de cita")
            logger.error("Revisa los locators en config.json")
            return False
            
    except Exception as e:
        logger.error(f"\n❌ ERROR EN LA DEMOSTRACIÓN: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        # ====================================================================
        # LIMPIEZA: Cerrar navegador
        # ====================================================================
        
        if driver:
            logger.info("\n--- Cerrando navegador ---")
            input("Presiona ENTER para cerrar el navegador...")
            driver.quit()
            logger.info("✓ Navegador cerrado")


# ============================================================================
# PUNTO DE ENTRADA
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("  DEMOSTRACIÓN: Clinical-QA-Sentinel - Flujo de Appointment")
    print("  Con datos sintéticos generados dinámicamente")
    print("="*70 + "\n")
    
    success = run_appointment_flow_demo()
    
    if success:
        print("\n✅ Demostración exitosa - El framework funciona correctamente")
        sys.exit(0)
    else:
        print("\n❌ Demostración falló - Revisa los logs arriba")
        sys.exit(1)
