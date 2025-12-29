"""
CURA Healthcare Login Test - CORREGIDO
========================================
Flujo correcto: Home → Click "Make Appointment" → Login → Appointment Form
"""

from pages.login_page import LoginPage
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import logging

logging.basicConfig(level=logging.INFO)


def load_simple_config():
    """Load configuration from JSON file"""
    with open('config/config.json', 'r') as f:
        return json.load(f)


def test_cura_login():
    """Test login contra CURA Healthcare siguiendo el flujo correcto"""
    
    config = load_simple_config()
    username = config['environments']['demo']['username']
    password = config['environments']['demo']['password']
    home_url = config['portal_url']
    
    print("\n" + "="*70)
    print("🏥 CURA Healthcare - Test de Login CORREGIDO")
    print("="*70)
    print(f"🌐 Home URL: {home_url}")
    print(f"👤 Usuario: {username}")
    print(f"🔒 Password: {'*' * len(password)}")
    print("-"*70)
    
    options = Options()
    options.add_argument('--start-maximized')
    
    print("\n📦 Iniciando ChromeDriver...")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        # PASO 1: Ir a la home
        print("\n1️⃣  Navegando a la página principal...")
        driver.get(home_url)
        print(f"   ✓ Página cargada: {driver.title}")
        
        # PASO 2: Click en "Make Appointment" (esto nos lleva al login)
        print("\n2️⃣  Haciendo click en 'Make Appointment'...")
        wait = WebDriverWait(driver, 10)
        make_appointment_btn = wait.until(
            EC.element_to_be_clickable((By.ID, "btn-make-appointment"))
        )
        make_appointment_btn.click()
        print("   ✓ Botón clickeado - redirigiendo al login...")
        
        # PASO 3: Esperar que aparezca el formulario de login
        print("\n3️⃣  Esperando formulario de login...")
        username_field = wait.until(
            EC.presence_of_element_located((By.ID, "txt-username"))
        )
        print(f"   ✓ Formulario de login detectado")
        print(f"   📍 URL actual: {driver.current_url}")
        
        # PASO 4: Llenar credenciales usando el page object
        print("\n4️⃣  Llenando credenciales...")
        login_page = LoginPage(driver, config)
        
        login_page.enter_username(username)
        print(f"   ✓ Usuario ingresado: {username}")
        
        login_page.enter_password(password)
        print(f"   ✓ Contraseña ingresada: ********")
        
        # PASO 5: Click en login
        print("\n5️⃣  Haciendo login...")
        login_page.click_login_button()
        print("   ✓ Click en botón de login ejecutado")
        
        # PASO 6: Verificar que llegamos al formulario de appointment
        print("\n6️⃣  Verificando resultado...")
        import time
        time.sleep(2)
        
        # Buscar el formulario de appointment
        appointment_form = wait.until(
            EC.presence_of_element_located((By.ID, "appointment"))
        )
        
        if appointment_form:
            print("\n" + "="*70)
            print("✅ ¡LOGIN EXITOSO!")
            print("="*70)
            print(f"📍 URL final: {driver.current_url}")
            print(f"📄 Título: {driver.title}")
            print("\n🎉 ¡Estamos en el formulario de 'Make Appointment'!")
            print("   Esto significa que el login funcionó correctamente")
            
            # Screenshot
            screenshot = login_page.take_screenshot("cura_login_success")
            print(f"\n📸 Screenshot guardado: {screenshot}")
            
            print("\n💡 Observa el navegador:")
            print("   - Deberías ver el formulario para agendar cita")
            print("   - Facility dropdown")
            print("   - Visit Date")
            print("   - Comment box")
            
            input("\n⏸️  Presiona ENTER para cerrar...")
            return True
        else:
            print("\n❌ No se encontró el formulario de appointment")
            return False
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        
        # Screenshot de error
        try:
            driver.save_screenshot("screenshots/error.png")
            print("📸 Screenshot de error guardado")
        except:
            pass
        
        return False
        
    finally:
        print("\n🔚 Cerrando navegador...")
        driver.quit()


if __name__ == "__main__":
    print("\n🚀 "*25)
    print("CURA HEALTHCARE - LOGIN TEST (FLUJO CORRECTO)")
    print("🚀 "*25)
    print("\nFlujo:")
    print("  1. Home page")
    print("  2. Click 'Make Appointment'")
    print("  3. Aparece formulario de login")
    print("  4. Llenar credenciales")
    print("  5. Login")
    print("  6. ✓ Formulario de appointment")
    
    success = test_cura_login()
    
    if success:
        print("\n✅ ¡Test EXITOSO!")
        exit(0)
    else:
        print("\n❌ Test falló")
        exit(1)
