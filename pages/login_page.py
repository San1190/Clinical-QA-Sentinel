"""
Login Page Object - Healthcare Portal Authentication
====================================================
Page Object for the login page of the healthcare portal.

Encapsulates all login page elements and interactions following
the Page Object Model design pattern.
"""

from selenium.webdriver.common.by import By
from typing import Tuple, Optional
from pages.base_page import BasePage


class LoginPage(BasePage):
    """
    Page Object representing the Login Page.
    
    Provides methods for interacting with login form elements
    and verification of login results.
    """
    
    # ========================================================================
    # Page Locators - All element selectors centralized here
    # ========================================================================
    
    def __init__(self, driver, config):
        super().__init__(driver, config)
        
        # Load locators from configuration
        locators_config = config.get('locators', {}).get('login_page', {})
        
        # Convert config locators to Selenium By tuples
        self.USERNAME_FIELD = self._parse_locator(locators_config.get('username_input'))
        self.PASSWORD_FIELD = self._parse_locator(locators_config.get('password_input'))
        self.LOGIN_BUTTON = self._parse_locator(locators_config.get('login_button'))
        self.ERROR_MESSAGE = self._parse_locator(locators_config.get('error_message'))
        self.SUCCESS_INDICATOR = self._parse_locator(locators_config.get('success_indicator'))
        
        # Fallback to hardcoded locators if not in config (for backwards compatibility)
        if not self.USERNAME_FIELD:
            self.USERNAME_FIELD = (By.ID, "txt-username")
        if not self.PASSWORD_FIELD:
            self.PASSWORD_FIELD = (By.ID, "txt-password")
        if not self.LOGIN_BUTTON:
            self.LOGIN_BUTTON = (By.ID, "btn-login")
        if not self.SUCCESS_INDICATOR:
            self.SUCCESS_INDICATOR = (By.ID, "appointment")
    
    def _parse_locator(self, locator_config: Optional[any]) -> Optional[Tuple[str, str]]:
        """
        Parse locator from configuration.
        
        Supports two formats:
        1. Dictionary: {'by': 'ID', 'value': 'username'}
        2. String: 'id:username' or 'class:text-danger'
        
        Args:
            locator_config: Dict with 'by' and 'value' keys OR string "type:value"
            
        Returns:
            Tuple of (By.METHOD, "value") or None
        """
        if not locator_config:
            return None
        
        # Map string to By constant
        by_mapping = {
            'ID': By.ID,
            'NAME': By.NAME,
            'CLASS_NAME': By.CLASS_NAME,
            'CLASS': By.CLASS_NAME,  # Shorthand
            'TAG_NAME': By.TAG_NAME,
            'LINK_TEXT': By.LINK_TEXT,
            'PARTIAL_LINK_TEXT': By.PARTIAL_LINK_TEXT,
            'CSS_SELECTOR': By.CSS_SELECTOR,
            'CSS': By.CSS_SELECTOR,  # Shorthand
            'XPATH': By.XPATH
        }
        
        # Format 1: String format "id:txt-username"
        if isinstance(locator_config, str) and ':' in locator_config:
            parts = locator_config.split(':', 1)
            by_method = parts[0].upper()
            value = parts[1] if len(parts) > 1 else ''
            
            by_constant = by_mapping.get(by_method)
            if by_constant and value:
                return (by_constant, value)
        
        # Format 2: Dictionary format {'by': 'ID', 'value': 'username'}
        elif isinstance(locator_config, dict):
            by_method = locator_config.get('by', '').upper()
            value = locator_config.get('value', '')
            
            by_constant = by_mapping.get(by_method)
            if by_constant and value:
                return (by_constant, value)
        
        return None
    
    # ========================================================================
    # Page Actions - Business-focused methods
    # ========================================================================
    
    def open(self) -> 'LoginPage':
        """
        Navigate to the login page.
        
        IMPORTANTE: En CURA Healthcare, el flujo es:
        1. Ir a la home (portal_url)
        2. Click en el botón "Make Appointment"
        3. Esto nos lleva a la página de login
        
        Returns:
            self: For method chaining
        """
        # PASO 1: Navegar a la home de CURA
        portal_url = self.config.get('portal_url')
        self.navigate_to(portal_url)
        self.logger.info(f"Navegado a la home: {portal_url}")
        
        # PASO 2: Click en "Make Appointment" para acceder al login
        # Este botón está en la homepage y nos lleva a la pantalla de login
        try:
            # Obtenemos el locator del botón desde config.json
            homepage_locators = self.config.get('locators', {}).get('homepage', {})
            make_appointment_btn = self._parse_locator(
                homepage_locators.get('make_appointment_button')
            )
            
            if make_appointment_btn:
                self.logger.info("Haciendo click en 'Make Appointment'...")
                self.click(make_appointment_btn)
                self.logger.info("✓ Click en 'Make Appointment' exitoso - Ahora en página de login")
            else:
                self.logger.warning("No se encontró locator para 'Make Appointment' en config")
                
        except Exception as e:
            self.logger.error(f"Error al hacer click en 'Make Appointment': {e}")
            # Intentamos continuar de todos modos
        
        return self
    
    def enter_username(self, username: str) -> 'LoginPage':
        """
        Enter username into the username field.
        
        Args:
            username: Username to enter
            
        Returns:
            self: For method chaining
        """
        self.type_text(self.USERNAME_FIELD, username, clear_first=True)
        self.logger.info(f"Entered username: {username}")
        return self
    
    def enter_password(self, password: str) -> 'LoginPage':
        """
        Enter password into the password field.
        
        Args:
            password: Password to enter
            
        Returns:
            self: For method chaining
        """
        self.type_text(self.PASSWORD_FIELD, password, clear_first=True)
        self.logger.debug("Entered password (hidden for security)")
        return self
    
    def click_login_button(self) -> None:
        """Click the login/submit button"""
        self.click(self.LOGIN_BUTTON)
        self.logger.info("Clicked login button")
    
    def login_with_credentials(self, username: str, password: str) -> None:
        """
        Perform complete login workflow.
        
        Args:
            username: Username to login with
            password: Password to login with
        """
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()
        self.logger.info(f"Attempted login for user: {username}")
    
    # ========================================================================
    # Page Verification Methods
    # ========================================================================
    
    def is_login_successful(self, timeout: int = 5) -> bool:
        """
        Check if login was successful by looking for success indicator.
        
        Args:
            timeout: Time to wait for success indicator
            
        Returns:
            bool: True if success element appears (successful login)
        """
        try:
            success_present = self.is_element_present(self.SUCCESS_INDICATOR, timeout=timeout)
            
            if success_present:
                self.logger.info("Login successful - success indicator detected")
                return True
            
            # Also check URL change (alternative success indicator)
            current_url = self.get_current_url()
            if 'appointment' in current_url or 'dashboard' in current_url or 'home' in current_url:
                self.logger.info("Login successful - URL changed")
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error checking login success: {e}")
            return False
    
    def is_error_displayed(self, timeout: int = 3) -> bool:
        """
        Check if any error message is displayed.
        
        Args:
            timeout: Time to wait for error
            
        Returns:
            bool: True if error message present
        """
        return self.is_element_visible(self.ERROR_MESSAGE, timeout=timeout)
    
    def get_error_message(self) -> Optional[str]:
        """
        Get the text of the error message.
        
        Returns:
            str or None: Error message text
        """
        try:
            if self.is_error_displayed():
                return self.get_text(self.ERROR_MESSAGE)
            return None
        except Exception:
            return None
    
    def is_invalid_credentials_error(self, timeout: int = 3) -> bool:
        """
        Check if invalid credentials error is displayed.
        
        Args:
            timeout: Time to wait for error
            
        Returns:
            bool: True if invalid credentials error shown
        """
        # Check specific error element
        if self.is_element_present(self.ERROR_INVALID_CREDENTIALS, timeout=timeout):
            return True
        
        # Check for error text in page source
        page_source = self.get_page_source().lower()
        invalid_phrases = [
            'invalid username or password',
            'invalid credentials',
            'incorrect username or password',
            'login failed'
        ]
        
        return any(phrase in page_source for phrase in invalid_phrases)
    
    def is_account_locked_error(self, timeout: int = 3) -> bool:
        """
        Check if account locked error is displayed.
        
        Args:
            timeout: Time to wait for error
            
        Returns:
            bool: True if account locked error shown
        """
        # Check specific error element
        if self.is_element_present(self.ERROR_ACCOUNT_LOCKED, timeout=timeout):
            return True
        
        # Check for error text in page source
        page_source = self.get_page_source().lower()
        locked_phrases = [
            'account has been locked',
            'account locked',
            'account is locked',
            'too many failed attempts'
        ]
        
        return any(phrase in page_source for phrase in locked_phrases)
    
    def get_login_result(self) -> str:
        """
        Determine the result of the login attempt.
        
        Returns:
            str: One of 'SUCCESS', 'FAIL_INVALID_CREDENTIALS', 
                 'FAIL_ACCOUNT_LOCKED', or 'UNKNOWN'
        """
        # Check for success first
        if self.is_login_successful(timeout=3):
            return 'SUCCESS'
        
        # Check for specific error types
        if self.is_account_locked_error():
            return 'FAIL_ACCOUNT_LOCKED'
        
        if self.is_invalid_credentials_error():
            return 'FAIL_INVALID_CREDENTIALS'
        
        # If we're still on login page but no specific error
        if self.is_on_login_page():
            return 'FAIL_UNKNOWN'
        
        return 'UNKNOWN'
    
    def is_on_login_page(self) -> bool:
        """
        Check if we're currently on the login page.
        
        Returns:
            bool: True if on login page
        """
        # Check for presence of login form elements
        username_present = self.is_element_present(self.USERNAME_FIELD, timeout=2)
        password_present = self.is_element_present(self.PASSWORD_FIELD, timeout=2)
        
        # Check URL
        current_url = self.get_current_url()
        login_in_url = 'login' in current_url.lower()
        
        return (username_present and password_present) or login_in_url
    
    # ========================================================================
    # Utility Methods
    # ========================================================================
    
    def clear_login_form(self) -> 'LoginPage':
        """
        Clear both username and password fields.
        
        Returns:
            self: For method chaining
        """
        self.type_text(self.USERNAME_FIELD, "", clear_first=True)
        self.type_text(self.PASSWORD_FIELD, "", clear_first=True)
        self.logger.debug("Login form cleared")
        return self
