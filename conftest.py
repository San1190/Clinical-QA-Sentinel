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
        
        # Headless mode if configured
        if headless:
            options.add_argument('--headless')
        
        # Initialize driver
        service = Service(ChromeDriverManager().install())
        web_driver = webdriver.Chrome(service=service, options=options)
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")
    
    # Configure timeouts
    timeouts = config.get('timeouts', {})
    web_driver.set_page_load_timeout(timeouts.get('page_load_timeout', 10))
    web_driver.implicitly_wait(timeouts.get('implicit_wait', 2))
    
    # Maximize window
    window_size = browser_config.get('window_size', {})
    if window_size:
        web_driver.set_window_size(
            window_size.get('width', 1920),
            window_size.get('height', 1080)
        )
    else:
        web_driver.maximize_window()
    
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

def pytest_html_report_title(report):
    """Customize HTML report title"""
    report.title = "Clinical-QA-Sentinel Test Report"


@pytest.hookimpl(optionalhook=True)
def pytest_html_results_summary(prefix, summary, postfix):
    """Add custom information to HTML report summary"""
    prefix.extend([f"<p>Test Environment: {load_config().get('active_environment')}</p>"])


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
