# 🚀 Migration Guide - Professional Refactoring

## Overview

Clinical-QA-Sentinel has been refactored from a functional prototype to an **enterprise-grade QA framework**. This guide explains the changes and how to use the new architecture.

---

## ✨ What Changed?

### Before (Old Architecture)
- Hardcoded URLs and config in Python code
- Direct `driver.find_element()` calls in tests
- Manual wait times with `time.sleep()`
- Text log files only
- No containerization

### After (New Architecture)
- ✅ **Configuration Management**: JSON config + environment variables
- ✅ **Page Object Model**: Centralized locators, reusable page classes
- ✅ **pytest Framework**: Professional testing with HTML reports
- ✅ **Explicit Waits**: No more `time.sleep()`, uses WebDriverWait
- ✅ **Docker Support**: Run anywhere with containers

---

## 📁 New Project Structure

```
Clinical-QA-Sentinel/
├── config/
│   └── config.json          # ← All configuration centralized here
├── pages/
│   ├── __init__.py
│   ├── base_page.py         # ← Base class for all pages
│   └── login_page.py        # ← Login page object
├── tests/
│   ├── __init__.py
│   └── test_authentication.py  # ← pytest test suite
├── utils/
│   ├── __init__.py
│   └── config_loader.py     # ← Configuration management
├── src/                      # ← Original scripts (still work)
│   ├── auth_stress_test.py
│   └── patient_data_generator.py
├── conftest.py              # ← pytest configuration
├── Dockerfile               # ← Docker containerization
├── docker-compose.yml       # ← Docker orchestration
├── .env.example             # ← Environment variables template
└── requirements.txt         # ← Updated dependencies
```

---

## 🔄 Migration Steps

### Step 1: Install New Dependencies

```powershell
pip install -r requirements.txt
```

**New packages**:
- `python-dotenv` - Environment variable support
- `pytest-cov` - Code coverage reporting

### Step 2: Test Configuration Loader

```powershell
python utils/config_loader.py
```

**Expected output**:
```
======================================================================
Configuration Loader - Test Run
======================================================================

Active Environment: demo
Portal URL: http://hospital-demo.com/login
Browser: chrome
Test Users:
  1. dr.test.valid@hospital-demo.com - Expected: SUCCESS
  2. dr.test.invalid@hospital-demo.com - Expected: FAIL_INVALID_CREDENTIALS
  3. dr.test.locked@hospital-demo.com - Expected: FAIL_ACCOUNT_LOCKED

Configuration loaded successfully! ✓
```

### Step 3: Run New pytest Suite

```powershell
pytest tests/ -v
```

For HTML report:
```powershell
pytest tests/ --html=reports/test_report.html --self-contained-html
```

---

## 📝 How to Use Each Component

### 1. Configuration Management

**Edit config/config.json** to change settings:

```json
{
  "active_environment": "demo",  # ← Change to: dev, test, staging, demo
  "timeouts": {
    "page_load_timeout": 10,     # ← Adjust timeouts
    "element_wait_timeout": 5
  }
}
```

**For sensitive data**, create `.env` file (copy from `.env.example`):
```bash
ENVIRONMENT=test
PORTAL_URL=https://my-custom-url.com/login
HEADLESS_MODE=true
```

### 2. Page Object Model

**Write tests using page objects**:

```python
from pages.login_page import LoginPage

def test_login(driver, config):
    login_page = LoginPage(driver, config)
    login_page.open()
    login_page.enter_username("user@example.com")
    login_page.enter_password("password123")
    login_page.click_login_button()
    
    assert login_page.is_login_successful()
```

**No more**:
```python
# ❌ OLD WAY - Don't do this
driver.find_element(By.ID, "username").send_keys("user")
time.sleep(2)  # BAD!
```

**Instead**:
```python
# ✅ NEW WAY - Do this
login_page.enter_username("user")  # Waits built-in!
```

### 3. pytest Tests

**Run specific tests**:
```powershell
# Run all tests
pytest tests/

# Run specific file
pytest tests/test_authentication.py

# Run specific test
pytest tests/test_authentication.py::test_valid_user_can_login

# Run with markers
pytest -m smoke
pytest -m authentication
```

**Generate HTML report**:
```powershell
pytest tests/ --html=reports/test_report.html --self-contained-html
```

Open `reports/test_report.html` in browser to see:
- Pass/fail statistics
- Execution times
- Screenshots of failures
- Stack traces

### 4. Docker Usage

**Build image**:
```powershell
docker build -t clinical-qa-sentinel .
```

**Run tests in container**:
```powershell
docker run --rm -v ${PWD}/reports:/app/reports clinical-qa-sentinel
```

**Use docker-compose**:
```powershell
# Run tests
docker-compose up qa-tests

# Generate patient data
docker-compose --profile data-gen up data-generator
```

---

## 🔍 Key Differences

### Configuration

| Aspect | Old | New |
|--------|-----|-----|
| URL | Hardcoded in Python | `config.json` |
| Timeouts | Magic numbers | Centralized config |
| Test Users | Class variables | JSON array |
| Environment | Single setup | Dev/Test/Staging/Prod |

### Testing

| Aspect | Old | New |
|--------|-----|-----|
| Framework | Custom script | pytest |
| Element Location | `driver.find_element()` | Page Objects |
| Waits | `time.sleep()` | `WebDriverWait` |
| Reports | Text logs | HTML + Screenshots |
| Assertions | Manual logging | pytest asserts |

---

## 💡 Tips

### Changing Environments

Quick switch between environments:
```powershell
# In .env file
ENVIRONMENT=dev    # Uses http://localhost:8080/login
ENVIRONMENT=test   # Uses test-hospital-demo.com
ENVIRONMENT=demo   # Uses hospital-demo.com (default)
```

### Adding New Pages

1. Create new file in `pages/`:
```python
from pages.base_page import BasePage

class DashboardPage(BasePage):
    # Locators
    WELCOME_MESSAGE = (By.ID, "welcome")
    
    # Methods
    def get_welcome_text(self):
        return self.get_text(self.WELCOME_MESSAGE)
```

2. Use in tests:
```python
dashboard = DashboardPage(driver, config)
assert dashboard.get_welcome_text() == "Welcome"
```

### Custom Wait Conditions

```python
from pages.base_page import BasePage

class MyPage(BasePage):
    def wait_for_loading_complete(self):
        self.wait_for_element_visible(self.CONTENT, timeout=10)
```

---

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'pages'"

**Solution**: Make sure you're running from project root:
```powershell
cd c:\Users\sanfu\Desktop\Emprendimiento\Clinical-QA-Sentinel
pytest tests/
```

### "ConfigurationError: Configuration file not found"

**Solution**: Ensure `config/config.json` exists:
```powershell
Test-Path config/config.json  # Should return True
```

### Docker build fails

**Solution**: Ensure Docker Desktop is installed and running:
```powershell
docker --version
docker ps
```

---

## 🎓 Learning Resources

### Page Object Model
- Official Pattern: https://www.selenium.dev/documentation/test_practices/encouraged/page_object_models/

### pytest
- Getting Started: https://docs.pytest.org/en/stable/getting-started.html
- Fixtures: https://docs.pytest.org/en/stable/fixture.html

### Docker
- Docker Docs: https://docs.docker.com/get-started/

---

## ✅ Verification Checklist

After migration, verify:

- [ ] Configuration loads: `python utils/config_loader.py`
- [ ] Tests run: `pytest tests/ -v`
- [ ] HTML report generates: `pytest tests/ --html=reports/test_report.html`
- [ ] Docker builds: `docker build -t clinical-qa-sentinel .`
- [ ] No `time.sleep()` in test code (only in original src/ scripts)

---

**Migration completed!** 🎉

Your framework is now enterprise-grade and ready for production use.
