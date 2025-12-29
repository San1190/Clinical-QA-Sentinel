"""
CURA Healthcare - Test Completo
================================
Login + Agendar Cita Completa
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import json


def load_config():
    with open('config/config.json', 'r') as f:
        return json.load(f)


def test_cura_full_flow():
    """Login y agendar cita completa"""
    
    config = load_config()
    username = config['environments']['demo']['username']
    password = config['environments']['demo']['password']
    url = config['portal_url']
    
    print("\nCURA Healthcare - Test Completo")
    print("-" * 50)
    
    # Chrome sin distracciones
    options = Options()
    options.add_argument('--start-maximized')
    options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False
    })
    options.add_argument('--disable-notifications')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    wait = WebDriverWait(driver, 10)
    
    try:
        # 1. Home
        print("1. Navegando a home...")
        driver.get(url)
        
        # 2. Make Appointment
        print("2. Click 'Make Appointment'...")
        wait.until(EC.element_to_be_clickable((By.ID, "btn-make-appointment"))).click()
        
        # 3. Login
        print("3. Login...")
        wait.until(EC.presence_of_element_located((By.ID, "txt-username"))).send_keys(username)
        driver.find_element(By.ID, "txt-password").send_keys(password)
        driver.find_element(By.ID, "btn-login").click()
        
        # 4. Llenar formulario de appointment
        print("4. Llenando formulario...")
        wait.until(EC.presence_of_element_located((By.ID, "combo_facility")))
        
        # Facility
        Select(driver.find_element(By.ID, "combo_facility")).select_by_value("Hongkong CURA Healthcare Center")
        
        # Readmission
        driver.find_element(By.ID, "chk_hospotal_readmission").click()
        
        # Program (Medicaid)
        driver.find_element(By.ID, "radio_program_medicaid").click()
        
        # Visit Date
        driver.find_element(By.ID, "txt_visit_date").send_keys("31/12/2025")
        
        # Comment
        driver.find_element(By.ID, "txt_comment").send_keys("Test automatizado con Selenium")
        
        # 5. Book appointment
        print("5. Agendando cita...")
        driver.find_element(By.ID, "btn-book-appointment").click()
        
        # 6. Verificar confirmación
        print("6. Verificando confirmación...")
        confirmation = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h2")))
        
        if "Appointment Confirmation" in driver.page_source:
            print("\n✓ ÉXITO: Cita agendada correctamente")
            print(f"  URL: {driver.current_url}")
            
            # Screenshot
            driver.save_screenshot("screenshots/cita_confirmada.png")
            print(f"  Screenshot: screenshots/cita_confirmada.png")
            
            # Pausa para ver
            import time
            print("\n  Puedes ver la confirmación en el navegador")
            print("  Cerrando en 3 segundos...")
            time.sleep(3)
            
            return True
        else:
            print("\n✗ ERROR: No se encontró confirmación")
            driver.save_screenshot("screenshots/error.png")
            return False
            
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        driver.save_screenshot("screenshots/error.png")
        return False
        
    finally:
        driver.quit()
        print("  Navegador cerrado\n")


if __name__ == "__main__":
    success = test_cura_full_flow()
    exit(0 if success else 1)
