"""
TEST DE ESTRÉS - Múltiples reservas simultáneas
================================================

Ejecuta MUCHAS reservas de citas a la vez para probar la robustez.

Uso:
    python test_estres.py --usuarios 10      # 10 usuarios simultáneos
    python test_estres.py --usuarios 50      # 50 usuarios simultáneos
"""

import sys
import time
import argparse
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

# Setup paths
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


def crear_cita(usuario_id, config):
    """
    Crea una cita para un usuario.
    Devuelve (usuario_id, exito, tiempo, paciente)
    """
    start_time = time.time()
    driver = None
    
    try:
        # Chrome en headless
        chrome_options = Options()
        chrome_options.add_argument('--headless=new')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=1920,1080')
        
        # Deshabilitar logs
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        
        prefs = {
            'credentials_enable_service': False,
            'profile.password_manager_enabled': False,
        }
        chrome_options.add_experimental_option('prefs', prefs)
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.set_page_load_timeout(10)
        driver.implicitly_wait(2)
        
        # Page Objects
        login_page = LoginPage(driver, config)
        appointment_page = AppointmentPage(driver, config)
        
        # Login
        env_config = config['environments'][config['active_environment']]
        username = env_config['username']
        password = env_config['password']
        
        login_page.open()
        login_page.login_with_credentials(username, password)
        
        if not login_page.is_login_successful():
            raise Exception("Login falló")
        
        # Generar paciente
        generator = SyntheticPatientGenerator()
        patient = generator.generate_patient()
        
        medical_notes = (
            f"PACIENTE: {patient['full_name']} | "
            f"SANGRE: {patient['blood_type']} | "
            f"ALERGIAS: {patient['allergies']}"
        )
        
        # Llenar formulario
        appointment_page.fill_appointment_form(
            comment=medical_notes,
            visit_date="30/01/2025"
        )
        
        # Verificar
        if not appointment_page.is_appointment_confirmed():
            raise Exception("Confirmación no encontrada")
        
        elapsed = time.time() - start_time
        return (usuario_id, True, elapsed, patient['full_name'])
        
    except Exception as e:
        elapsed = time.time() - start_time
        return (usuario_id, False, elapsed, str(e))
        
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass


def main():
    parser = argparse.ArgumentParser(description='Test de estrés')
    parser.add_argument('--usuarios', type=int, default=10, help='Número de usuarios simultáneos')
    args = parser.parse_args()
    
    num_usuarios = args.usuarios
    
    print("\n" + "="*70)
    print(f"  ⚡ TEST DE ESTRÉS: {num_usuarios} usuarios simultáneos")
    print("="*70)
    
    config = load_config()
    
    print(f"\n🚀 Iniciando {num_usuarios} reservas en paralelo...")
    print(f"   Esto puede tardar un tiempo...\n")
    
    resultados = []
    start_total = time.time()
    
    # Ejecutar en paralelo
    with ThreadPoolExecutor(max_workers=min(num_usuarios, 10)) as executor:
        futures = [executor.submit(crear_cita, i+1, config) for i in range(num_usuarios)]
        
        for future in as_completed(futures):
            usuario_id, exito, tiempo, info = future.result()
            resultados.append((usuario_id, exito, tiempo, info))
            
            # Progress
            completados = len(resultados)
            porcentaje = (completados / num_usuarios) * 100
            
            if exito:
                print(f"✅ Usuario {usuario_id:3d} | {tiempo:5.2f}s | {info}")
            else:
                print(f"❌ Usuario {usuario_id:3d} | {tiempo:5.2f}s | Error: {info[:50]}")
            
            print(f"   Progreso: {completados}/{num_usuarios} ({porcentaje:.1f}%)", end='\r')
    
    total_time = time.time() - start_total
    
    # Estadísticas
    print("\n\n" + "="*70)
    print("  📊 RESULTADOS DEL TEST DE ESTRÉS")
    print("="*70)
    
    exitosos = sum(1 for _, exito, _, _ in resultados if exito)
    fallidos = num_usuarios - exitosos
    
    tiempos = [tiempo for _, exito, tiempo, _ in resultados if exito]
    
    print(f"\n✅ Exitosos: {exitosos}/{num_usuarios} ({(exitosos/num_usuarios)*100:.1f}%)")
    print(f"❌ Fallidos:  {fallidos}/{num_usuarios} ({(fallidos/num_usuarios)*100:.1f}%)")
    
    if tiempos:
        print(f"\n⏱️  Tiempos:")
        print(f"   Promedio: {sum(tiempos)/len(tiempos):.2f}s")
        print(f"   Mínimo:   {min(tiempos):.2f}s")
        print(f"   Máximo:   {max(tiempos):.2f}s")
    
    print(f"\n🎯 Tiempo total: {total_time:.2f}s")
    print(f"📈 Throughput: {num_usuarios/total_time:.2f} reservas/segundo")
    
    print("\n" + "="*70)
    
    if exitosos == num_usuarios:
        print("✅ ¡TODOS LOS TESTS PASARON! Sistema robusto. 🎉")
    elif exitosos >= num_usuarios * 0.9:
        print("⚠️  La mayoría pasaron, pero hay algunos fallos.")
    else:
        print("❌ Muchos fallos - revisar configuración.")
    
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
