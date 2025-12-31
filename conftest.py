"""
pytest Configuration and Fixtures
==================================
Centralized pytest configuration including:
- WebDriver fixtures with automatic cleanup
- Screenshot capture on test failure
- HTML report customization
- Test configuration management
"""

import pytest
import logging
from datetime import datetime
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from utils.config_loader import load_config


# ============================================================================
# pytest Configuration
# ============================================================================

def pytest_configure(config):
    """pytest configuration hook"""
    # Ensure output directories exist
    Path("reports").mkdir(exist_ok=True)
    Path("screenshots").mkdir(exist_ok=True)
    Path("logs").mkdir(exist_ok=True)


# ============================================================================
# Fixtures - WebDriver Management
# ============================================================================

@pytest.fixture(scope="function")
def config():
    """
    Load application configuration.
    
    Returns:
        dict: Application configuration
    """
    return load_config()


@pytest.fixture(scope="function")
def driver(config):
    """
    Create and configure WebDriver instance.
    
    Automatically:
    - Initializes with security settings
    - Maximizes window
    - Sets timeouts
    - Cleans up after test
    
    Args:
        config: Configuration fixture
        
    Yields:
        WebDriver: Configured Selenium WebDriver
    """
    # Get browser configuration
    browser_config = config.get('browser', {})
    browser_name = browser_config.get('name', 'chrome').lower()
    headless = browser_config.get('headless', False)
    browser_options_list = browser_config.get('options', [])
    
    # Currently supports Chrome (can be extended for Firefox, Edge, etc.)
    if browser_name == 'chrome':
        options = ChromeOptions()
        
        # Apply configured options
        for option in browser_options_list:
            options.add_argument(option)
        
        # Configure Chrome options
        chrome_options = ChromeOptions()
        
        # ============================================================================
        # MODO HEADLESS: Siempre activo para evitar popups de Google
        # ============================================================================
        # Headless = Chrome sin ventana visible
        # Ventajas: 
        #   - NO aparecen popups de Google (no hay UI)
        #   - Tests más rápidos
        #   - Se puede ejecutar en servidores sin pantalla (CI/CD)
        chrome_options.add_argument('--headless=new')  # Modo headless moderno
        chrome_options.add_argument('--disable-gpu')  # Requerido en Windows
        
        # Opciones adicionales para estabilidad
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--disable-popup-blocking') # This is the key for popup blocking
        chrome_options.add_argument('--disable-notifications')
        
        # Deshabilitar gestor de contraseñas (por si acaso)
        prefs = {
            'credentials_enable_service': False,
            'profile.password_manager_enabled': False,
            'profile.default_content_setting_values.notifications': 2,
        }
        chrome_options.add_experimental_option('prefs', prefs)
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation', 'enable-logging'])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Window size (importante incluso en headless)
        chrome_options.add_argument('--window-size=1920,1080')
        
        # Initialize driver
        service = Service(ChromeDriverManager().install())
        web_driver = webdriver.Chrome(service=service, options=chrome_options)
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")
    
    # Configure timeouts
    timeouts = config.get('timeouts', {})
    web_driver.set_page_load_timeout(timeouts.get('page_load_timeout', 10))
    web_driver.implicitly_wait(timeouts.get('implicit_wait', 2))
    
    # Maximize window - This is now handled by --window-size argument in headless mode
    # The original window_size config and maximize_window() call are now redundant
    # as a fixed window size is set for headless mode.
    
    yield web_driver
    
    # Cleanup
    web_driver.quit()


# ============================================================================
# Fixtures - Screenshot and Reporting
# ============================================================================

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture screenshots on test failure.
    
    pytest hook that extends test outcome with:
    - Screenshot capture on failure
    - Extra data for HTML report
    """
    outcome = yield
    report = outcome.get_result()
    
    # Only capture for test call (not setup/teardown)
    if report.when == 'call':
        # Get driver fixture if it exists
        driver_fixture = None
        for fixture_name in item.fixturenames:
            if fixture_name == 'driver':
                driver_fixture = item.funcargs.get('driver')
                break
        
        # Capture screenshot on failure
        if report.failed and driver_fixture:
            screenshot_dir = Path("screenshots")
            screenshot_dir.mkdir(exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            test_name = item.name.replace(" ", "_").replace("/", "_")
            screenshot_name = f"{test_name}_{timestamp}.png"
            screenshot_path = screenshot_dir / screenshot_name
            
            try:
                driver_fixture.save_screenshot(str(screenshot_path))
                
                # Add screenshot to HTML report
                extra = getattr(report, 'extra', [])
                extra.append(pytest_html.extras.image(str(screenshot_path)))
                report.extra = extra
                
                logging.info(f"Screenshot captured: {screenshot_path}")
            except Exception as e:
                logging.error(f"Failed to capture screenshot: {e}")


# ============================================================================
# HTML Report Customization
# ============================================================================

# NOTA: Estos hooks de pytest-html están comentados porque causan errores
# Para usarlos, primero instala: pip install pytest-html
# Y luego descomenta las siguientes funciones

# def pytest_html_report_title(report):
#     """Customize HTML report title"""
#     report.title = "Clinical-QA-Sentinel Test Report"


# @pytest.hookimpl(optionalhook=True)
# def pytest_html_results_summary(prefix, summary, postfix):
#     """Add custom information to HTML report summary"""
#     prefix.extend([f"<p>Test Environment: {load_config().get('active_environment')}</p>"])


# ============================================================================
# Test Markers
# ============================================================================

def pytest_configure(config):
    """Register custom markers"""
    config.addinivalue_line(
        "markers", "smoke: mark test as a smoke test"
    )
    config.addinivalue_line(
        "markers", "regression: mark test as a regression test"
    )
    config.addinivalue_line(
        "markers", "authentication: mark test as authentication-related"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )


# Import pytest-html extras if available
try:
    import pytest_html
except ImportError:
    pytest_html = None

