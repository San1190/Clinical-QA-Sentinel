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
        self.USERNAME_FIELD = self._parse_locator(locators_config.get('username_field'))
        self.PASSWORD_FIELD = self._parse_locator(locators_config.get('password_field'))
        self.LOGIN_BUTTON = self._parse_locator(locators_config.get('login_button'))
        self.ERROR_MESSAGE = self._parse_locator(locators_config.get('error_message'))
        self.ERROR_INVALID_CREDENTIALS = self._parse_locator(locators_config.get('error_invalid_credentials'))
        self.ERROR_ACCOUNT_LOCKED = self._parse_locator(locators_config.get('error_account_locked'))
        self.DASHBOARD_INDICATOR = self._parse_locator(locators_config.get('dashboard_indicator'))
        
        # Fallback to hardcoded locators if not in config (for backwards compatibility)
        if not self.USERNAME_FIELD:
            self.USERNAME_FIELD = (By.ID, "username")
        if not self.PASSWORD_FIELD:
            self.PASSWORD_FIELD = (By.ID, "password")
        if not self.LOGIN_BUTTON:
            self.LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
        if not self.DASHBOARD_INDICATOR:
            self.DASHBOARD_INDICATOR = (By.ID, "dashboard")
    
    def _parse_locator(self, locator_config: Optional[dict]) -> Optional[Tuple[str, str]]:
        """
        Parse locator from configuration dictionary.
        
        Args:
            locator_config: Dict with 'by' and 'value' keys
            
        Returns:
            Tuple of (By.METHOD, "value") or None
        """
        if not locator_config:
            return None
        
        by_method = locator_config.get('by', '').upper()
        value = locator_config.get('value', '')
        
        # Map string to By constant
        by_mapping = {
            'ID': By.ID,
            'NAME': By.NAME,
            'CLASS_NAME': By.CLASS_NAME,
            'TAG_NAME': By.TAG_NAME,
            'LINK_TEXT': By.LINK_TEXT,
            'PARTIAL_LINK_TEXT': By.PARTIAL_LINK_TEXT,
            'CSS_SELECTOR': By.CSS_SELECTOR,
            'XPATH': By.XPATH
        }
        
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
        
        Returns:
            self: For method chaining
        """
        portal_url = self.config.get('portal_url')
        self.navigate_to(portal_url)
        self.logger.info(f"Opened login page: {portal_url}")
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
        Check if login was successful by looking for dashboard indicator.
        
        Args:
            timeout: Time to wait for dashboard
            
        Returns:
            bool: True if dashboard appears (successful login)
        """
        try:
            dashboard_present = self.is_element_present(self.DASHBOARD_INDICATOR, timeout=timeout)
            
            if dashboard_present:
                self.logger.info("Login successful - dashboard detected")
                return True
            
            # Also check URL change (alternative success indicator)
            current_url = self.get_current_url()
            if 'dashboard' in current_url or 'home' in current_url:
                self.logger.info("Login successful - URL changed to dashboard/home")
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
