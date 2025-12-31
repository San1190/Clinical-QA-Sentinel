"""
Test de Flujo Completo: Login + Generación de Paciente + Reserva de Cita
==========================================================================

ESTE ES EL TEST MAESTRO - La pieza que une todo el puzzle

¿Qué hace este test?
--------------------
Simula el trabajo real de un administrativo en Visual Limes:
1. Abre la aplicación de CURA Healthcare
2. Inicia sesión con credenciales válidas
3. GENERA datos de un paciente sintético (usando TU generador)
4. Reserva una cita médica con esos datos
5. Verifica que todo funcionó correctamente

¿Por qué es importante?
-----------------------
- Es un test END-TO-END (de principio a fin)
- Prueba la INTEGRACIÓN de múltiples componentes
- Usa DATOS DINÁMICOS (no hardcodeados)
- Simula un CASO DE USO REAL

Arquitectura utilizada:
-----------------------
✓ Page Object Model (LoginPage, AppointmentPage)
✓ Generación de datos sintéticos (SyntheticPatientGenerator)
✓ Fixtures de pytest (driver, config)
✓ Assertions claras y descriptivas
"""

import pytest
import logging
from pages.login_page import LoginPage
from pages.appointment_page import AppointmentPage
from src.patient_data_generator import SyntheticPatientGenerator

# Configuramos el logger para ver mensajes en consola
# Esto nos ayuda a depurar si algo falla
logger = logging.getLogger(__name__)


class TestAppointmentFlow:
    """
    Suite de tests para el flujo completo de reserva de citas.
    
    Agrupa todos los tests relacionados con appointments.
    Por ahora solo tenemos uno, pero podríamos añadir más:
    - test_appointment_without_readmission
    - test_appointment_with_medicare
    - test_cancel_appointment
    etc.
    """
    
    @pytest.mark.smoke
    @pytest.mark.integration
    def test_make_appointment_with_synthetic_data(self, driver, config):
        """
        Test principal: Crear cita médica usando datos sintéticos generados.
        
        FLUJO COMPLETO PASO A PASO:
        ---------------------------
        
        FASE 1: PREPARACIÓN
        → Instanciar Page Objects
        → Obtener credenciales desde config
        
        FASE 2: AUTENTICACIÓN
        → Navegar a la página de login
        → Iniciar sesión con credenciales válidas
        → Verificar que el login fue exitoso
        
        FASE 3: GENERACIÓN DE DATOS
        → Crear instancia del generador de pacientes
        → Generar un paciente sintético completo
        → Formatear datos para el formulario
        
        FASE 4: RESERVA DE CITA
        → Rellenar formulario de appointment
        → Enviar la reserva
        → Verificar confirmación
        
        Args:
            driver: Fixture de Selenium WebDriver (del conftest.py)
            config: Fixture de configuración (del conftest.py)
        """
        
        # ====================================================================
        # FASE 1: PREPARACIÓN - Instanciar Page Objects
        # ====================================================================
        
        logger.info("=" * 70)
        logger.info("🚀 INICIANDO TEST: Flujo Completo de Cita Médica")
        logger.info("=" * 70)
        
        # Creamos instancias de nuestros Page Objects
        # Cada uno encapsula la lógica de una página específica
        login_page = LoginPage(driver, config)
        appointment_page = AppointmentPage(driver, config)
        
        logger.info("✓ Page Objects instanciados correctamente")
        
        # ====================================================================
        # FASE 2: AUTENTICACIÓN - Login en la aplicación
        # ====================================================================
        
        logger.info("\n--- FASE 1: AUTENTICACIÓN ---")
        
        # Obtenemos las credenciales desde la configuración
        # Esto viene del config.json → environments → demo
        # No hardcodeamos credenciales en el test (buena práctica)
        env_config = config.get('environments', {}).get(config.get('active_environment', 'demo'))
        username = env_config.get('username')
        password = env_config.get('password')
        
        logger.info(f"Usuario de prueba: {username}")
        
        # Navegamos a la home de CURA y hacemos login
        # El flujo en CURA es: Home → Click "Make Appointment" → Login
        # Pero LoginPage.open() ya maneja este flujo
        login_page.open()
        logger.info("✓ Página de login abierta")
        
        # Ejecutamos el login
        # login_with_credentials() es un método de alto nivel que:
        # 1. Escribe username
        # 2. Escribe password
        # 3. Hace click en login
        login_page.login_with_credentials(username, password)
        logger.info("✓ Credenciales ingresadas y login ejecutado")
        
        # Verificamos que el login fue exitoso
        # is_login_successful() busca el indicador de éxito
        assert login_page.is_login_successful(), "❌ Login falló - no se encontró indicador de éxito"
        logger.info("✓ Login exitoso - usuario autenticado")
        
        # ====================================================================
        # FASE 3: GENERACIÓN DE DATOS SINTÉTICOS
        # ====================================================================
        
        logger.info("\n--- FASE 2: GENERACIÓN DE DATOS SINTÉTICOS ---")
        
        # AQUÍ ES DONDE USAMOS TU GENERADOR DE PACIENTES
        # SyntheticPatientGenerator es la clase que creaste
        # Genera datos completamente ficticios pero realistas
        generator = SyntheticPatientGenerator()
        logger.info("✓ Generador de pacientes inicializado")
        
        # Generamos UN paciente sintético
        # generate_patient() devuelve un dict con:
        # - patient_id: ID único del paciente
        # - full_name: Nombre completo (generado con Faker)
        # - date_of_birth: Fecha de nacimiento
        # - blood_type: Tipo de sangre (distribución realista)
        # - allergies: Alergias conocidas (o "None")
        patient = generator.generate_patient()
        
        logger.info(f"✓ Paciente sintético generado:")
        logger.info(f"  → ID: {patient['patient_id']}")
        logger.info(f"  → Nombre: {patient['full_name']}")
        logger.info(f"  → Tipo Sangre: {patient['blood_type']}")
        logger.info(f"  → Alergias: {patient['allergies']}")
        
        # ====================================================================
        # FORMATEAR DATOS PARA EL FORMULARIO
        # ====================================================================
        
        # Creamos una "nota médica" con los datos del paciente
        # Este string se meterá en el campo de comentarios
        # Simula lo que un administrativo escribiría en notas
        medical_notes = (
            f"PACIENTE: {patient['full_name']} | "
            f"SANGRE: {patient['blood_type']} | "
            f"ALERGIAS: {patient['allergies']}"
        )
        
        logger.info(f"✓ Notas médicas preparadas: {medical_notes}")
        
        # ====================================================================
        # FASE 4: RESERVA DE CITA CON DATOS GENERADOS
        # ====================================================================
        
        logger.info("\n--- FASE 3: RESERVA DE CITA MÉDICA ---")
        
        # Rellenamos el formulario de cita
        # fill_appointment_form() hace TODO:
        # 1. Marca readmission checkbox
        # 2. Selecciona programa Medicaid
        # 3. Escribe fecha
        # 4. Escribe comentarios (CON LOS DATOS DEL GENERADOR)
        # 5. Click en "Book Appointment"
        appointment_page.fill_appointment_form(
            comment=medical_notes,
            visit_date="30/01/2025"  # Puedes parametrizar esto también
        )
        
        logger.info("✓ Formulario de cita completado y enviado")
        
        # ====================================================================
        # VERIFICACIÓN FINAL - ¿Se confirmó la cita?
        # ====================================================================
        
        logger.info("\n--- FASE 4: VERIFICACIÓN ---")
        
        # Verificamos que aparezca la pantalla de confirmación
        # is_appointment_confirmed() busca el header "Appointment Confirmation"
        # Si aparece = todo funcionó ✓
        # Si NO aparece = el test falla ✗
        is_confirmed = appointment_page.is_appointment_confirmed()
        
        # ASSERTION PRINCIPAL DEL TEST
        # Si esto falla, pytest marcará el test como FAILED
        assert is_confirmed, "❌ La cita NO se confirmó - no se encontró pantalla de confirmación"
        
        logger.info("✅ ¡CITA CONFIRMADA EXITOSAMENTE!")
        logger.info(f"✅ Paciente {patient['full_name']} tiene cita programada")
        
        logger.info("\n" + "=" * 70)
        logger.info("🎉 TEST COMPLETADO CON ÉXITO")
        logger.info("=" * 70)


# ============================================================================
# TESTS ADICIONALES (Para expandir en el futuro)
# ============================================================================

class TestAppointmentValidations:
    """
    Suite adicional para validaciones del formulario.
    
    Estos tests verifican casos de error y validaciones.
    Por ahora están como ejemplos comentados.
    """
    
    @pytest.mark.skip(reason="Pendiente de implementar")
    def test_appointment_without_date_fails(self, driver, config):
        """
        Test que verifica que no se puede reservar sin fecha.
        
        CASO DE USO:
        - Llenar todo EXCEPTO la fecha
        - Intentar enviar
        - Verificar mensaje de error
        """
        # TODO: Implementar cuando tengas tiempo
        pass
    
    @pytest.mark.skip(reason="Pendiente de implementar")
    def test_appointment_past_date_fails(self, driver, config):
        """
        Test que verifica que no se puede reservar con fecha pasada.
        
        CASO DE USO:
        - Poner fecha del pasado (ej: 01/01/2020)
        - Intentar enviar
        - Verificar mensaje de error
        """
        # TODO: Implementar cuando tengas tiempo
        pass


# ============================================================================
# EJECUCIÓN DIRECTA (Sin pytest)
# ============================================================================

if __name__ == "__main__":
    """
    Permite ejecutar este archivo directamente.
    
    USO:
    python tests/test_appointment_flow.py
    
    Esto ejecutará todos los tests de este archivo con pytest.
    """
    pytest.main([
        __file__,           # Este archivo
        "-v",               # Verbose (detallado)
        "-s",               # Mostrar prints
        "--tb=short",       # Traceback corto
        "--html=reports/appointment_flow_report.html",  # Reporte HTML
        "--self-contained-html"  # HTML auto-contenido
    ])
