"""
Appointment Page Object - Página de Reserva de Citas Médicas
=============================================================
Page Object Model para la página de citas de CURA Healthcare.

Este archivo encapsula TODA la lógica de interacción con la página
de reserva de citas. Siguiendo el patrón POM, NO ponemos selectores
en los tests, sino que los centralizamos aquí.
"""

from selenium.webdriver.common.by import By
from typing import Tuple, Optional
from pages.base_page import BasePage


class AppointmentPage(BasePage):
    """
    Clase que representa la página de reserva de citas.
    
    ¿Qué hace esta clase?
    ---------------------
    - Encapsula TODOS los elementos de la página (botones, inputs, etc.)
    - Proporciona métodos de NEGOCIO (fill_appointment_form, etc.)
    - Oculta la complejidad de Selenium al test
    
    ¿Por qué es útil?
    -----------------
    Si la web cambia, SOLO modificas AQUÍ, no en 50 tests diferentes.
    Esto es arquitectura profesional y mantenible.
    """
    
    # ========================================================================
    # CONSTRUCTOR - Inicialización de la Página
    # ========================================================================
    
    def __init__(self, driver, config):
        """
        Constructor de la página de citas.
        
        ¿Qué hace?
        ----------
        1. Llama al constructor de BasePage (herencia)
        2. Carga los locators (selectores) desde config.json
        3. Los convierte a formato Selenium (By.ID, By.XPATH, etc.)
        
        Args:
            driver: El navegador de Selenium (WebDriver)
            config: Diccionario con toda la configuración del proyecto
        """
        # Llamamos al constructor del padre (BasePage)
        # Esto inicializa driver, logger, timeouts, etc.
        super().__init__(driver, config)
        
        # Obtenemos la sección de locators para appointment_page del config.json
        # Si no existe, usamos un diccionario vacío {}
        locators_config = config.get('locators', {}).get('appointment_page', {})
        
        # ====================================================================
        # PARSEAR LOCATORS - Convertir strings del JSON a formato Selenium
        # ====================================================================
        
        # Checkbox de "Readmisión Hospitalaria"
        # En la web de CURA: "Apply for hospital readmission"
        self.READMISSION_CHECK = self._parse_locator(
            locators_config.get('readmission_check')
        )
        
        # Radio button para seleccionar programa de salud (Medicaid, Medicare, None)
        # Usamos Medicaid por defecto en el tutorial
        self.MEDICAID_RADIO = self._parse_locator(
            locators_config.get('medicaid_radio')
        )
        
        # Input de fecha de visita
        # Formato esperado: DD/MM/YYYY
        self.VISIT_DATE_INPUT = self._parse_locator(
            locators_config.get('visit_date_input')
        )
        
        # Textarea de comentarios
        # AQUÍ es donde metemos los datos del paciente generado
        self.COMMENT_INPUT = self._parse_locator(
            locators_config.get('comment_input')
        )
        
        # Botón de "Book Appointment" (Reservar Cita)
        self.BOOK_BUTTON = self._parse_locator(
            locators_config.get('book_btn')
        )
        
        # Header de confirmación (para verificar que funcionó)
        # Muestra "Appointment Confirmation" cuando todo va bien
        self.CONFIRMATION_HEADER = self._parse_locator(
            locators_config.get('confirmation_header')
        )
    
    # ========================================================================
    # MÉTODO AUXILIAR - Parsear Locators desde Config
    # ========================================================================
    
    def _parse_locator(self, locator_config: Optional[any]) -> Optional[Tuple[str, str]]:
        """
        Convierte un locator del config.json a formato Selenium.
        
        ¿Por qué existe este método?
        -----------------------------
        En config.json tenemos strings como "id:txt-username"
        Selenium necesita tuplas como (By.ID, "txt-username")
        Este método hace la conversión.
        
        Formatos soportados:
        --------------------
        1. String: "id:username" → (By.ID, "username")
        2. String: "xpath://div[@class='error']" → (By.XPATH, "//div[@class='error']")
        3. Dict: {"by": "ID", "value": "username"} → (By.ID, "username")
        
        Args:
            locator_config: String o dict con el locator desde config.json
            
        Returns:
            Tupla (By.METHOD, "value") que Selenium entiende
            None si el locator es inválido
        """
        # Si no hay locator configurado, devolver None
        if not locator_config:
            return None
        
        # Diccionario de mapeo: string → constante de Selenium
        # Convierte "ID" → By.ID, "XPATH" → By.XPATH, etc.
        by_mapping = {
            'ID': By.ID,
            'NAME': By.NAME,
            'CLASS_NAME': By.CLASS_NAME,
            'CLASS': By.CLASS_NAME,  # Atajo
            'TAG_NAME': By.TAG_NAME,
            'LINK_TEXT': By.LINK_TEXT,
            'PARTIAL_LINK_TEXT': By.PARTIAL_LINK_TEXT,
            'CSS_SELECTOR': By.CSS_SELECTOR,
            'CSS': By.CSS_SELECTOR,  # Atajo
            'XPATH': By.XPATH
        }
        
        # FORMATO 1: String con formato "type:value"
        # Ejemplo: "id:btn-login" → ["id", "btn-login"]
        if isinstance(locator_config, str) and ':' in locator_config:
            # Separamos por el primer ":" que encontremos
            parts = locator_config.split(':', 1)
            by_method = parts[0].upper()  # "id" → "ID"
            value = parts[1] if len(parts) > 1 else ''  # "btn-login"
            
            # Buscamos la constante de Selenium correspondiente
            by_constant = by_mapping.get(by_method)
            
            # Si encontramos el método Y hay un valor, devolvemos la tupla
            if by_constant and value:
                return (by_constant, value)
        
        # FORMATO 2: Diccionario con keys 'by' y 'value'
        # Ejemplo: {"by": "ID", "value": "btn-login"}
        elif isinstance(locator_config, dict):
            by_method = locator_config.get('by', '').upper()
            value = locator_config.get('value', '')
            
            by_constant = by_mapping.get(by_method)
            if by_constant and value:
                return (by_constant, value)
        
        # Si llegamos aquí, el formato no es válido
        return None
    
    # ========================================================================
    # MÉTODOS DE NEGOCIO - Acciones de Alto Nivel
    # ========================================================================
    
    def fill_appointment_form(self, comment: str, visit_date: str = "30/01/2025") -> None:
        """
        Rellena el formulario completo de cita médica.
        
        ¿Qué hace este método?
        -----------------------
        Este es el método MAESTRO que ejecuta TODO el flujo de reserva:
        1. Marca el checkbox de readmisión
        2. Selecciona el programa de salud (Medicaid)
        3. Escribe la fecha de visita
        4. Escribe el comentario (AQUÍ van los datos del paciente)
        5. Hace click en "Book Appointment"
        
        ¿Por qué es útil?
        -----------------
        En lugar de tener 5 líneas en el test, tenemos 1 sola:
        appointment_page.fill_appointment_form(comment="Paciente X")
        
        Esto hace los tests MÁS LEGIBLES y MANTENIBLES.
        
        Args:
            comment: Comentario/notas médicas (datos del paciente sintético)
            visit_date: Fecha de la visita en formato DD/MM/YYYY
        """
        # PASO 1: Marcar checkbox de readmisión
        # Esto simula que el paciente ya estuvo hospitalizado antes
        self.logger.info("Marcando checkbox de readmisión hospitalaria...")
        self.click(self.READMISSION_CHECK)
        
        # PASO 2: Seleccionar programa de salud (Medicaid)
        # Radio button - solo uno puede estar seleccionado
        self.logger.info("Seleccionando programa de salud: Medicaid...")
        self.click(self.MEDICAID_RADIO)
        
        # PASO 3: Escribir fecha de visita
        # La web de CURA espera formato DD/MM/YYYY
        self.logger.info(f"Ingresando fecha de visita: {visit_date}...")
        self.type_text(self.VISIT_DATE_INPUT, visit_date, clear_first=True)
        
        # PASO 4: Escribir comentario con datos del paciente
        # AQUÍ ES DONDE METEMOS LOS DATOS DEL GENERADOR
        # Ejemplo: "Patient: John Doe | Blood: O+ | Allergy: Penicillin"
        self.logger.info(f"Ingresando comentarios médicos: {comment[:50]}...")
        self.type_text(self.COMMENT_INPUT, comment, clear_first=True)
        
        # PASO 5: Click en botón de reservar
        # Esto envía el formulario
        self.logger.info("Haciendo click en 'Book Appointment'...")
        
        # IMPORTANTE: Hacer scroll al botón antes de hacer click
        # A veces el botón no es clickable si no está visible
        try:
            book_button_element = self.find_element(self.BOOK_BUTTON)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", book_button_element)
            import time
            time.sleep(0.5)  # Pequeña pausa después del scroll
        except Exception as e:
            self.logger.warning(f"No se pudo hacer scroll al botón: {e}")
        
        # Ahora sí, hacer click
        self.click(self.BOOK_BUTTON)
        
        # IMPORTANTE: Esperar a que la página cambie después del submit
        # La app de CURA en Heroku puede ser LENTA
        self.logger.info("Esperando a que el formulario se envíe...")
        time.sleep(3)  # Aumentado a 3 segundos para dar tiempo al submit
        
        self.logger.info("✅ Formulario de cita completado")
    
    def is_appointment_confirmed(self, timeout: int = 10) -> bool:
        """
        Verifica si la cita fue confirmada exitosamente.
        
        ¿Qué hace?
        ----------
        Busca el header "Appointment Confirmation" en la página.
        Si aparece = cita creada correctamente ✓
        Si NO aparece = algo falló ✗
        
        NOTA: Timeout aumentado a 10 segundos porque la app de CURA
        en Heroku (servidor gratuito) puede ser LENTA.
        
        ¿Cómo lo usa el test?
        ---------------------
        assert appointment_page.is_appointment_confirmed(), "La cita no se confirmó"
        
        Args:
            timeout: Segundos a esperar a que aparezca la confirmación (default 10)
            
        Returns:
            True si la cita fue confirmada
            False si NO se confirmó (error)
        """
        try:
            # Intentamos encontrar el header de confirmación
            # is_element_present viene de BasePage
            confirmed = self.is_element_present(
                self.CONFIRMATION_HEADER,
                timeout=timeout
            )
            
            if confirmed:
                self.logger.info("✅ Confirmación de cita detectada - ¡ÉXITO!")
                return True
            else:
                # Si no se encuentra, loggear la URL actual para debugging
                current_url = self.get_current_url()
                self.logger.warning(f"⚠️ NO se encontró confirmación de cita - URL actual: {current_url}")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Error al verificar confirmación: {e}")
            return False
        """
        Verifica si la cita fue confirmada exitosamente.
        
        ¿Qué hace?
        ----------
        Busca el header "Appointment Confirmation" en la página.
        Si aparece = cita creada correctamente ✓
        Si NO aparece = algo falló ✗
        
        ¿Cómo lo usa el test?
        ---------------------
        assert appointment_page.is_appointment_confirmed(), "La cita no se confirmó"
        
        Args:
            timeout: Segundos a esperar a que aparezca la confirmación
            
        Returns:
            True si la cita fue confirmada
            False si NO se confirmó (error)
        """
        try:
            # Intentamos encontrar el header de confirmación
            # is_element_present viene de BasePage
            confirmed = self.is_element_present(
                self.CONFIRMATION_HEADER,
                timeout=timeout
            )
            
            if confirmed:
                self.logger.info("✅ Confirmación de cita detectada - ¡ÉXITO!")
                return True
            else:
                self.logger.warning("⚠️ NO se encontró confirmación de cita")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Error al verificar confirmación: {e}")
            return False
    
    def get_confirmation_details(self) -> dict:
        """
        Obtiene los detalles de la confirmación de cita.
        
        MÉTODO BONUS (no está en el tutorial, pero es útil)
        
        ¿Qué hace?
        ----------
        Extrae información de la página de confirmación:
        - Facility (hospital)
        - Programa de salud
        - Fecha de visita
        - Comentario
        
        Returns:
            Diccionario con los detalles de la cita confirmada
        """
        # Este método está preparado para futuras expansiones
        # Por ahora solo retornamos un dict básico
        self.logger.info("Extrayendo detalles de la confirmación...")
        
        return {
            'confirmed': self.is_appointment_confirmed(),
            'url': self.get_current_url()
        }
