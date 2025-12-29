"""
Base Page Object - Foundation for all Page Objects
===================================================
Implements common functionality shared across all pages:
- WebDriver management
- Reusable wait methods
- Screenshot capture
- Common page actions

All page objects should inherit from this class.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
from typing import Tuple, Optional, List
import logging
from datetime import datetime
from pathlib import Path


class BasePage:
    """
    Base class for all Page Objects.
    
    Provides common functionality:
    - Element location with waits
    - Element interaction (click, type, etc.)
    - Screenshot capture
    - Page validation
    """
    
    def __init__(self, driver: webdriver.Remote, config: dict):
        """
        Initialize the base page.
        
        Args:
            driver: Selenium WebDriver instance
            config: Configuration dictionary
        """
        self.driver = driver
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Extract timeout values from config
        self.default_timeout = config.get('timeouts', {}).get('element_wait_timeout', 5)
        self.page_load_timeout = config.get('timeouts', {}).get('page_load_timeout', 10)
        
        # Screenshot configuration
        self.screenshots_dir = Path(config.get('reporting', {}).get('screenshots_dir', 'screenshots'))
        self.screenshots_dir.mkdir(exist_ok=True)
    
    # ========================================================================
    # Element Location Methods
    # ========================================================================
    
    def find_element(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> WebElement:
        """
        Find an element with explicit wait.
        
        Args:
            locator: Tuple of (By.METHOD, "value")
            timeout: Wait timeout in seconds (uses default if None)
            
        Returns:
            WebElement
            
        Raises:
            TimeoutException: If element not found within timeout
        """
        timeout = timeout or self.default_timeout
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return element
        except TimeoutException:
            self.logger.error(f"Element not found: {locator} within {timeout}s")
            raise
    
    def find_elements(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> List[WebElement]:
        """
        Find multiple elements with explicit wait.
        
        Args:
            locator: Tuple of (By.METHOD, "value")
            timeout: Wait timeout in seconds
            
        Returns:
            List of WebElements
        """
        timeout = timeout or self.default_timeout
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return self.driver.find_elements(*locator)
        except TimeoutException:
            self.logger.warning(f"No elements found: {locator} within {timeout}s")
            return []
    
    def wait_for_element_visible(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> WebElement:
        """
        Wait for an element to be visible.
        
        Args:
            locator: Tuple of (By.METHOD, "value")
            timeout: Wait timeout in seconds
            
        Returns:
            WebElement when visible
        """
        timeout = timeout or self.default_timeout
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
    
    def wait_for_element_clickable(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> WebElement:
        """
        Wait for an element to be clickable.
        
        Args:
            locator: Tuple of (By.METHOD, "value")
            timeout: Wait timeout in seconds
            
        Returns:
            WebElement when clickable
        """
        timeout = timeout or self.default_timeout
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
    
    def is_element_present(self, locator: Tuple[str, str], timeout: int = 2) -> bool:
        """
        Check if an element is present on the page.
        
        Args:
            locator: Tuple of (By.METHOD, "value")
            timeout: Wait timeout in seconds (short by default)
            
        Returns:
            bool: True if element found, False otherwise
        """
        try:
            self.find_element(locator, timeout=timeout)
            return True
        except TimeoutException:
            return False
    
    def is_element_visible(self, locator: Tuple[str, str], timeout: int = 2) -> bool:
        """
        Check if an element is visible on the page.
        
        Args:
            locator: Tuple of (By.METHOD, "value")
            timeout: Wait timeout in seconds
            
        Returns:
            bool: True if element visible, False otherwise
        """
        try:
            self. wait_for_element_visible(locator, timeout=timeout)
            return True
        except TimeoutException:
            return False
    
    # ========================================================================
    # Element Interaction Methods
    # ========================================================================
    
    def click(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> None:
        """
        Click an element after waiting for it to be clickable.
        
        Args:
            locator: Tuple of (By.METHOD, "value")
            timeout: Wait timeout in seconds
        """
        element = self.wait_for_element_clickable(locator, timeout)
        element.click()
        self.logger.debug(f"Clicked element: {locator}")
    
    def type_text(self, locator: Tuple[str, str], text: str, clear_first: bool = True, timeout: Optional[int] = None) -> None:
        """
        Type text into an input field.
        
        Args:
            locator: Tuple of (By.METHOD, "value")
            text: Text to type
            clear_first: Clear field before typing
            timeout: Wait timeout in seconds
        """
        element = self.wait_for_element_visible(locator, timeout)
        
        if clear_first:
            element.clear()
        
        element.send_keys(text)
        self.logger.debug(f"Typed text into element: {locator}")
    
    def get_text(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> str:
        """
        Get text from an element.
        
        Args:
            locator: Tuple of (By.METHOD, "value")
            timeout: Wait timeout in seconds
            
        Returns:
            str: Element text
        """
        element = self.wait_for_element_visible(locator, timeout)
        return element.text
    
    def get_attribute(self, locator: Tuple[str, str], attribute: str, timeout: Optional[int] = None) -> Optional[str]:
        """
        Get an attribute value from an element.
        
        Args:
            locator: Tuple of (By.METHOD, "value")
            attribute: Attribute name
            timeout: Wait timeout in seconds
            
        Returns:
            str or None: Attribute value
        """
        element = self.find_element(locator, timeout)
        return element.get_attribute(attribute)
    
    # ========================================================================
    # Wait Utilities
    # ========================================================================
    
    def wait_for_url_to_be(self, url: str, timeout: Optional[int] = None) -> bool:
        """
        Wait for the current URL to be a specific value.
        
        Args:
            url: Expected URL
            timeout: Wait timeout in seconds
            
        Returns:
            bool: True if URL matches
        """
        timeout = timeout or self.default_timeout
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.url_to_be(url)
            )
            return True
        except TimeoutException:
            self.logger.error(f"URL did not change to: {url}")
            return False
    
    def wait_for_url_contains(self, url_fragment: str, timeout: Optional[int] = None) -> bool:
        """
        Wait for the current URL to contain a specific string.
        
        Args:
            url_fragment: String that should be in URL
            timeout: Wait timeout in seconds
            
        Returns:
            bool: True if URL contains fragment
        """
        timeout = timeout or self.default_timeout
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.url_contains(url_fragment)
            )
            return True
        except TimeoutException:
            self.logger.error(f"URL does not contain: {url_fragment}")
            return False
    
    def wait_for_text_in_element(self, locator: Tuple[str, str], text: str, timeout: Optional[int] = None) -> bool:
        """
        Wait for specific text to appear in an element.
        
        Args:
            locator: Tuple of (By.METHOD, "value")
            text: Text to wait for
            timeout: Wait timeout in seconds
            
        Returns:
            bool: True if text found
        """
        timeout = timeout or self.default_timeout
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.text_to_be_present_in_element(locator, text)
            )
            return True
        except TimeoutException:
            self.logger.error(f"Text '{text}' not found in element: {locator}")
            return False
    
    # ========================================================================
    # Screenshot and Diagnostic Methods
    # ========================================================================
    
    def take_screenshot(self, name: str = None) -> str:
        """
        Take a screenshot of the current page.
        
        Args:
            name: Optional screenshot name (timestamp used if not provided)
            
        Returns:
            str: Path to screenshot file
        """
        if name is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            name = f"screenshot_{timestamp}"
        
        # Ensure .png extension
        if not name.endswith('.png'):
            name += '.png'
        
        screenshot_path = self.screenshots_dir / name
        
        try:
            self.driver.save_screenshot(str(screenshot_path))
            self.logger.info(f"Screenshot saved: {screenshot_path}")
            return str(screenshot_path)
        except Exception as e:
            self.logger.error(f"Failed to save screenshot: {e}")
            return ""
    
    def get_current_url(self) -> str:
        """Get the current page URL"""
        return self.driver.current_url
    
    def get_page_title(self) -> str:
        """Get the current page title"""
        return self.driver.title
    
    def get_page_source(self) -> str:
        """Get the complete page source"""
        return self.driver.page_source
    
    # ========================================================================
    # Navigation Methods
    # ========================================================================
    
    def navigate_to(self, url: str) -> None:
        """
        Navigate to a specific URL.
        
        Args:
            url: URL to navigate to
        """
        self.logger.info(f"Navigating to: {url}")
        self.driver.get(url)
    
    def refresh_page(self) -> None:
        """Refresh the current page"""
        self.driver.refresh()
        self.logger.debug("Page refreshed")
    
    def go_back(self) -> None:
        """Navigate back in browser history"""
        self.driver.back()
        self.logger.debug("Navigated back")
    
    def go_forward(self) -> None:
        """Navigate forward in browser history"""
        self.driver.forward()
        self.logger.debug("Navigated forward")
