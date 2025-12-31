"""
MODO DEMO VISUAL - Ver TODO lo que hace el test
================================================

Este script ejecuta el mismo flujo pero CON VENTANA VISIBLE
y hace PAUSAS para que veas cada paso.

Ejecutar: python demo_visual.py
"""

import sys
import logging
import time
from pathlib import Path

# Configurar logging MUY verbose
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Añadir rutas
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from pages.login_page import LoginPage
from pages.appointment_page import AppointmentPage
from src.patient_data_generator import SyntheticPatientGenerator
from utils.config_loader import load_config


def pause(mensaje, segundos=1):
    """Pausa con cuenta regresiva - RÁPIDA"""
    print(f"\n⏸️  {mensaje}")
    for i in range(segundos, 0, -1):
        print(f"   Continuando en {i}...", end='\r')
        time.sleep(1)
    print("   ✓ Continuando...       ")


def main():
    driver = None
    
    try:
        print("\n" + "="*70)
        print("  🎬 DEMO VISUAL: Flujo de Appointment")
        print("  Verás TODO en pantalla paso a paso")
        print("="*70)
        
        # ================================================================
        # 1. CONFIGURAR CHROME CON VENTANA VISIBLE
        # ================================================================
        
        print("\n📋 Cargando configuración...")
        config = load_config()
        
        print("🌐 Inicializando Chrome (CON VENTANA VISIBLE)...")
        chrome_options = Options()
        # NO HEADLESS - Quieres verlo
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--disable-extensions')
        
        # Deshabilitar gestor de contraseñas
        prefs = {
            'credentials_enable_service': False,
            'profile.password_manager_enabled': False,
        }
        chrome_options.add_experimental_option('prefs', prefs)
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        print("✓ Chrome abierto - MIRA LA VENTANA")
        pause("Observa la ventana de Chrome que se abrió", 1)
        
        # ================================================================
        # 2. INSTANCIAR PAGE OBJECTS
        # ================================================================
        
        print("\n🏗️  Creando Page Objects...")
        login_page = LoginPage(driver, config)
        appointment_page = AppointmentPage(driver, config)
        print("✓ Page Objects listos")
        
        # ================================================================
        # 3. LOGIN
        # ================================================================
        
        print("\n🔐 FASE: AUTENTICACIÓN")
        env_config = config['environments'][config['active_environment']]
        username = env_config['username']
        password = env_config['password']
        
        print(f"   Usuario: {username}")
        print(f"   Password: {password}")
        
        login_page.open()
        pause("Mira: Se abrió la página de CURA y clickeó 'Make Appointment'", 1)
        
        login_page.login_with_credentials(username, password)
        pause("Mira: Se escribió username y password, se hizo click en Login", 1)
        
        if not login_page.is_login_successful():
            raise Exception("❌ Login falló")
        
        print("✅ Login exitoso - Ahora estás en el formulario de appointment")
        pause("Mira: Ya estamos en la página del formulario", 1)
        
        # ================================================================
        # 4. GENERAR PACIENTE
        # ================================================================
        
        print("\n👤 FASE: GENERACIÓN DE PACIENTE SINTÉTICO")
        generator = SyntheticPatientGenerator()
        patient = generator.generate_patient()
        
        print("\n📋 PACIENTE GENERADO:")
        print(f"   ├─ ID: {patient['patient_id']}")
        print(f"   ├─ Nombre: {patient['full_name']}")
        print(f"   ├─ Sangre: {patient['blood_type']}")
        print(f"   └─ Alergias: {patient['allergies']}")
        
        medical_notes = (
            f"PACIENTE: {patient['full_name']} | "
            f"SANGRE: {patient['blood_type']} | "
            f"ALERGIAS: {patient['allergies']}"
        )
        
        print(f"\n📝 Notas médicas que se escribirán:")
        print(f"   {medical_notes}")
        
        pause("Ahora vamos a llenar el formulario - OBSERVA LA PANTALLA", 3)
        
        # ================================================================
        # 5. LLENAR FORMULARIO PASO A PASO
        # ================================================================
        
        print("\n📝 FASE: LLENANDO FORMULARIO")
        
        print("   1. Marcando checkbox 'Hospital Readmission'...")
        # Marcar checkbox
        appointment_page.click(appointment_page.READMISSION_CHECK)
        pause("   ✓ Mira: Checkbox MARCADO", 2)
        
        print("   2. Seleccionando 'Medicaid'...")
        appointment_page.click(appointment_page.MEDICAID_RADIO)
        pause("   ✓ Mira: Radio button MEDICAID seleccionado", 2)
        
        print("   3. Escribiendo fecha '30/01/2025'...")
        appointment_page.type_text(appointment_page.VISIT_DATE_INPUT, "30/01/2025", clear_first=True)
        pause("   ✓ Mira: Fecha ESCRITA en el campo", 2)
        
        print("   4. Escribiendo comentarios médicos...")
        print(f"      '{medical_notes}'")
        appointment_page.type_text(appointment_page.COMMENT_INPUT, medical_notes, clear_first=True)
        pause("   ✓ Mira: COMENTARIOS con datos del paciente escritos", 3)
        
        print("\n✅ FORMULARIO COMPLETAMENTE LLENO")
        print("   Ahora vamos a enviarlo...")
        pause("   Observa: Se va a enviar el formulario", 2)
        
        # ================================================================
        # 6. ENVIAR FORMULARIO
        # ================================================================
        
        print("\n📤 Enviando formulario con JavaScript...")
        driver.execute_script("""
            var form = document.querySelector('form');
            if (form) {
                form.submit();
            }
        """)
        print("   ✓ Formulario enviado")
        
        pause("   Espera: La página está navegando a la confirmación...", 4)
        
        # ================================================================
        # 7. VERIFICAR CONFIRMACIÓN
        # ================================================================
        
        print("\n🔍 FASE: VERIFICACIÓN")
        
        current_url = driver.current_url
        print(f"   URL actual: {current_url}")
        
        if appointment_page.is_appointment_confirmed():
            print("\n" + "="*70)
            print("  ✅✅✅ ¡CITA CONFIRMADA EXITOSAMENTE! ✅✅✅")
            print(f"  ✅ Paciente: {patient['full_name']}")
            print(f"  ✅ Cita programada para: 30/01/2025")
            print("="*70)
            print("\n🎉 DEMOSTRACIÓN VISUAL COMPLETADA 🎉")
            print("\nAhora puedes ver exactamente qué hizo el test.")
            print("La página de confirmación está visible en Chrome.")
        else:
            print("\n❌ No se encontró confirmación")
            print(f"   URL: {current_url}")
        
        pause("\n\nPresiona ENTER para cerrar el navegador...", 999)
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Demostración interrumpida por el usuario")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        if driver:
            input("\nPresiona ENTER para cerrar Chrome...")
            driver.quit()
            print("✓ Chrome cerrado")


if __name__ == "__main__":
    main()
