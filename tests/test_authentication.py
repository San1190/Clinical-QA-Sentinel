"""
Authentication Test Suite
==========================
pytest-based authentication tests using Page Object Model.

This demonstrates the professional refactoring with:
- Configuration management (no hardcoded values)
- Page Object Model (clean test logic)
- pytest fixtures (WebDriver management)
- Explicit waits (no time.sleep())
"""

import pytest
from pages.login_page import LoginPage


class TestAuthentication:
    """
    Test suite for healthcare portal authentication.
    
    Uses Page Object Model for maintainable, readable tests.
    """
    
    @pytest.mark.authentication
    @pytest.mark.smoke
    def test_valid_user_can_login(self, driver, config):
        """
        Test that a valid user can successfully log in.
        
        Scenario:
        1. Navigate to login page
        2. Enter valid credentials
        3. Click login button
        4. Verify dashboard appears (successful login)
        """
        # Get valid test user from config
        test_users = config.get('test_users', [])
        valid_user = next((u for u in test_users if u['expected_result'] == 'SUCCESS'), None)
        
        if not valid_user:
            pytest.skip("No valid test user configured")
        
        # Use Page Object Model
        login_page = LoginPage(driver, config)
        
        # Execute test steps
        login_page.open()
        login_page.login_with_credentials(
            username=valid_user['username'],
            password=valid_user['password']
        )
        
        # Verify result
        assert login_page.is_login_successful(), "Expected successful login but dashboard not found"
    
    @pytest.mark.authentication
    def test_invalid_password_shows_error(self, driver, config):
        """
        Test that invalid password displays appropriate error.
        
        Scenario:
        1. Navigate to login page
        2. Enter username with wrong password
        3. Click login button
        4. Verify error message appears
        """
        # Get invalid password test user from config
        test_users = config.get('test_users', [])
        invalid_user = next((u for u in test_users if u['expected_result'] == 'FAIL_INVALID_CREDENTIALS'), None)
        
        if not invalid_user:
            pytest.skip("No invalid credentials test user configured")
        
        # Use Page Object Model
        login_page = LoginPage(driver, config)
        
        # Execute test steps
        login_page.open()
        login_page.login_with_credentials(
            username=invalid_user['username'],
            password=invalid_user['password']
        )
        
        # Verify result
        result = login_page.get_login_result()
        assert result == 'FAIL_INVALID_CREDENTIALS', f"Expected invalid credentials error, got: {result}"
    
    @pytest.mark.authentication
    def test_locked_account_shows_error(self, driver, config):
        """
        Test that locked account displays appropriate error.
        
        Scenario:
        1. Navigate to login page
        2. Attempt login with locked account
        3. Verify account locked error appears
        """
        # Get locked account test user from config
        test_users = config.get('test_users', [])
        locked_user = next((u for u in test_users if u['expected_result'] == 'FAIL_ACCOUNT_LOCKED'), None)
        
        if not locked_user:
            pytest.skip("No locked account test user configured")
        
        # Use Page Object Model
        login_page = LoginPage(driver, config)
        
        # Execute test steps
        login_page.open()
        login_page.login_with_credentials(
            username=locked_user['username'],
            password=locked_user['password']
        )
        
        # Verify result
        result = login_page.get_login_result()
        assert result == 'FAIL_ACCOUNT_LOCKED', f"Expected account locked error, got: {result}"
    
    @pytest.mark.authentication
    def test_login_form_elements_present(self, driver, config):
        """
        Test that all login form elements are present.
        
        Scenario:
        1. Navigate to login page
        2. Verify username field exists
        3. Verify password field exists
        4. Verify login button exists
        """
        login_page = LoginPage(driver, config)
        login_page.open()
        
        # Verify form elements
        assert login_page.is_element_present(login_page.USERNAME_FIELD), "Username field not found"
        assert login_page.is_element_present(login_page.PASSWORD_FIELD), "Password field not found"
        assert login_page.is_element_present(login_page.LOGIN_BUTTON), "Login button not found"


# ============================================================================
# Parametrized Tests (Data-Driven Testing)
# ============================================================================

@pytest.mark.authentication
@pytest.mark.parametrize("test_user_type", [
    "SUCCESS",
    "FAIL_INVALID_CREDENTIALS",
    "FAIL_ACCOUNT_LOCKED"
])
def test_authentication_scenarios(driver, config, test_user_type):
    """
    Parametrized test covering multiple authentication scenarios.
    
    This single test function runs multiple times with different data,
    demonstrating data-driven testing approach.
    """
    # Get test user matching the expected result
    test_users = config.get('test_users', [])
    test_user = next((u for u in test_users if u['expected_result'] == test_user_type), None)
    
    if not test_user:
        pytest.skip(f"No test user configured for: {test_user_type}")
    
    # Execute test
    login_page = LoginPage(driver, config)
    login_page.open()
    login_page.login_with_credentials(
        username=test_user['username'],
        password=test_user['password']
    )
    
    # Verify expected result
    actual_result = login_page.get_login_result()
    assert actual_result == test_user_type, f"Expected {test_user_type}, got {actual_result}"


if __name__ == "__main__":
    # Allow running tests directly
    pytest.main([__file__, "-v", "--html=reports/test_report.html", "--self-contained-html"])
