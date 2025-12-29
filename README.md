# Clinical-QA-Sentinel 🏥

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Healthcare](https://img.shields.io/badge/sector-HealthTech-green.svg)](https://github.com/San1190/Clinical-QA-Sentinel)
[![pytest](https://img.shields.io/badge/testing-pytest-blue.svg)](https://docs.pytest.org/)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)

> **Enterprise-Grade QA Automation Framework for Healthcare Systems**

Clinical-QA-Sentinel is a comprehensive Quality Assurance automation framework specifically designed for healthcare applications. Built with security, compliance, and reliability at its core, this framework enables rigorous testing of medical systems while maintaining GDPR/HIPAA compliance standards.

---

## 🎯 Overview

In the healthcare sector, software quality is not just about functionality—it's about patient safety. Clinical-QA-Sentinel provides healthcare organizations with robust testing tools that ensure medical applications meet the highest standards of reliability, security, and compliance.

### ⭐ Key Features

- **🔐 Security-First Approach**: Built-in GDPR/HIPAA compliance mechanisms
- **🤖 Automated Testing**: Selenium-based authentication and workflow testing with Page Object Model
- **📊 Synthetic Data Generation**: Realistic test data without compromising patient privacy
- **📝 Comprehensive Audit Trails**: Detailed logging for regulatory compliance
- **🏗️ Page Object Model**: Maintainable and scalable test architecture
- **🧪 pytest Framework**: Professional testing with HTML reports and screenshots
- **⚙️ Configuration Management**: Environment-based settings with JSON and .env support
- **⏱️ Explicit Waits**: No time.sleep() - production-ready wait strategies
- **🐳 Docker Support**: Containerized execution for portability
- **🚀 CI/CD Ready**: Seamless integration with continuous deployment pipelines

---

## 📁 Project Structure

```
Clinical-QA-Sentinel/
├── config/
│   └── config.json              # Centralized configuration
├── pages/                        # Page Object Model
│   ├── base_page.py             # Base page with reusable methods
│   └── login_page.py            # Login page object
├── tests/                        # pytest test suites
│   └── test_authentication.py   # Authentication tests
├── src/                          # Core automation scripts
│   ├── auth_stress_test.py      # Authentication security auditing
│   └── patient_data_generator.py # Synthetic patient data generator
├── utils/                        # Utilities and helpers
│   └── config_loader.py         # Configuration management
├── reports/                      # Test reports and HTML output
├── screenshots/                  # Test failure screenshots
├── data/                         # Test data storage
├── docs/                         # Additional documentation
├── conftest.py                   # pytest configuration
├── Dockerfile                    # Docker containerization
├── docker-compose.yml           # Multi-service orchestration
├── requirements.txt              # Python dependencies
├── MIGRATION_GUIDE.md           # Migration documentation
└── ARCHITECTURE.md              # Technical architecture
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Chrome/Chromium browser
- ChromeDriver (automatically managed with webdriver-manager)
- Docker (optional, for containerized execution)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/San1190/Clinical-QA-Sentinel.git
   cd Clinical-QA-Sentinel
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment** (optional)
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

4. **Verify installation**
   ```bash
   python utils/config_loader.py
   ```

---

## 🔧 Usage

### Running Tests with pytest

**Basic test execution**:
```bash
pytest tests/ -v
```

**Generate HTML report with screenshots**:
```bash
pytest tests/ --html=reports/test_report.html --self-contained-html -v
```

**Run specific test markers**:
```bash
pytest -m smoke              # Smoke tests only
pytest -m authentication     # Authentication tests
pytest -m regression         # Regression suite
```

**Run with coverage**:
```bash
pytest tests/ --cov=src --cov-report=html
```

### Using Page Object Model

```python
from pages.login_page import LoginPage

def test_login(driver, config):
    # Create page object
    login_page = LoginPage(driver, config)
    
    # Use business-focused methods
    login_page.open()
    login_page.login_with_credentials("user@example.com", "password")
    
    # Verify with built-in methods
    assert login_page.is_login_successful()
```

### Configuration Management

**Edit `config/config.json`** for settings:
```json
{
  "active_environment": "demo",
  "timeouts": {
    "page_load_timeout": 10,
    "element_wait_timeout": 5
  }
}
```

**Use environment variables**:
```bash
export ENVIRONMENT=test
export HEADLESS_MODE=true
pytest tests/
```

### Generate Patient Data

```bash
python src/patient_data_generator.py
```

**Output**: `dummy_patients.csv` with 100 synthetic patient records

**Data Fields**:
- Patient ID (unique identifier)
- Full Name
- Date of Birth
- Blood Type (medically accurate distribution)
- Known Allergies

---

## 🐳 Docker Usage

### Build Image

```bash
docker build -t clinical-qa-sentinel .
```

### Run Tests

```bash
docker run --rm -v ${PWD}/reports:/app/reports clinical-qa-sentinel
```

### Docker Compose

```bash
# Run test suite
docker-compose up qa-tests

# Generate patient data
docker-compose --profile data-gen up data-generator

# Run with Selenium Grid
docker-compose --profile grid up
```

---

## 📊 Core Components

### 1. Page Object Model Architecture

**BasePage** ([`pages/base_page.py`](pages/base_page.py)):
- Reusable wait methods (`wait_for_element_visible`, `wait_for_element_clickable`)
- Element interaction (`click`, `type_text`, `get_text`)
- Screenshot capture
- Navigation utilities

**LoginPage** ([`pages/login_page.py`](pages/login_page.py)):
- Centralized locators from configuration
- Business-focused methods (`login_with_credentials`)
- Login result verification (`get_login_result`)
- Method chaining support

### 2. Authentication Security Auditor

**File**: [`src/auth_stress_test.py`](src/auth_stress_test.py)

A comprehensive authentication testing tool that simulates real-world login scenarios for healthcare portals.

**Features**:
- Multi-user authentication testing
- HIPAA-compliant audit logging
- Session isolation and security
- Detailed pass/fail reporting

**Usage**:
```bash
python src/auth_stress_test.py
```

**Output**: `login_audit.log` with detailed audit trail

### 3. Synthetic Patient Data Generator

**File**: [`src/patient_data_generator.py`](src/patient_data_generator.py)

Generates realistic, GDPR-compliant synthetic patient records for testing purposes.

**Features**:
- 100% synthetic data (no real patient information)
- Medically accurate blood type distribution (O+ 38%, A+ 35%, etc.)
- Realistic allergy profiles with clinical relationships
- Configurable dataset sizes
- Age-appropriate demographics

**Usage**:
```bash
python src/patient_data_generator.py
```

---

## 📋 Use Cases

### Healthcare Portal Testing
- Validate authentication workflows
- Test role-based access control (RBAC)
- Verify audit trail functionality
- Security penetration testing

### Database Load Testing
- Populate test databases with realistic data
- Performance benchmarking
- Stress testing medical information systems
- Data migration validation

### Compliance Validation
- GDPR compliance verification
- HIPAA security rule testing
- Audit log completeness checks
- Data privacy assessments

### Development & Staging
- Safe test data for development environments
- Demo data for stakeholder presentations
- Training datasets for ML models
- Integration testing scenarios

---

## 🏗️ Architecture

Clinical-QA-Sentinel follows enterprise-grade design patterns:

- **Page Object Model (POM)**: UI test organization with centralized locators
- **Configuration Management**: Environment-based settings (dev/test/staging/prod)
- **Data-Driven Testing**: Parametrized tests with pytest
- **Explicit Wait Strategies**: No `time.sleep()`, production-ready waits
- **Modular Design**: Reusable components and utilities
- **Separation of Concerns**: Clear responsibility boundaries

For detailed architectural information, see [ARCHITECTURE.md](ARCHITECTURE.md).

For migration from legacy code, see [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md).

---

## 📋 Requirements

### Python Packages

```
selenium>=4.16.0
webdriver-manager>=4.0.1
faker>=22.0.0
python-dotenv>=1.0.0
pytest>=7.4.0
pytest-html>=4.1.0
pytest-xdist>=3.5.0
pytest-cov>=4.1.0
```

Install all dependencies:
```bash
pip install -r requirements.txt
```

### System Requirements

- **OS**: Windows 10+, macOS 10.14+, Linux (Ubuntu 20.04+)
- **RAM**: Minimum 4GB
- **Browser**: Chrome/Chromium (latest stable version)
- **Docker**: Optional, for containerized execution

---

## 🔒 Security & Compliance

### Data Privacy

- ✅ **No Real Patient Data**: All generated data is 100% synthetic
- ✅ **Anonymization**: User identifiers are anonymized in logs
- ✅ **Secure Sessions**: Browser sessions use incognito mode
- ✅ **Audit Trails**: Complete logging for compliance verification
- ✅ **Environment Variables**: Sensitive data externalized

### Compliance Standards

- **GDPR**: General Data Protection Regulation
- **HIPAA**: Health Insurance Portability and Accountability Act
- **ISO 27001**: Information Security Management
- **PCI DSS**: Payment Card Industry Data Security Standard

---

## 🧪 Testing Best Practices

### Before Running Tests

1. **Environment Setup**: Ensure test environment is isolated from production
2. **Configuration Review**: Verify URLs and credentials in `config/config.json`
3. **Backup Validation**: Confirm audit logs are being captured

### Test Execution

```bash
# Run all tests with verbose output
pytest tests/ -v

# Run with HTML report
pytest tests/ --html=reports/test_report.html --self-contained-html

# Run in parallel (faster execution)
pytest tests/ -n auto

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

### After Test Completion

1. **Log Analysis**: Review `login_audit.log` for anomalies
2. **Report Review**: Open `reports/test_report.html` in browser
3. **Screenshot Review**: Check `screenshots/` for failure captures
4. **Data Cleanup**: Remove temporary test data if applicable

---

## 🤝 Contributing

We welcome contributions from the healthcare QA community!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Code Standards

- Follow PEP 8 style guidelines
- Include docstrings for all functions/classes
- Add unit tests for new features
- Update documentation as needed
- Use type hints for function signatures

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📞 Support & Contact

For questions, issues, or feature requests:

- **Issues**: [GitHub Issues](https://github.com/San1190/Clinical-QA-Sentinel/issues)
- **Discussions**: [GitHub Discussions](https://github.com/San1190/Clinical-QA-Sentinel/discussions)
- **Email**: santiago.developer@healthtech.com

---

## 🔄 Roadmap

### Current Features (v1.0)
- ✅ Authentication testing framework with POM
- ✅ Synthetic patient data generation
- ✅ Audit logging system
- ✅ pytest integration with HTML reports
- ✅ Configuration management
- ✅ Docker containerization

### Planned Features (v1.1)
- 🔲 API testing capabilities with REST support
- 🔲 Integration with CI/CD platforms (Jenkins, GitLab CI, GitHub Actions)
- 🔲 Test result dashboards with trends
- 🔲 Multi-language support (Spanish, French)
- 🔲 Performance metrics collection

### Future Enhancements (v2.0)
- 🔲 AI-powered test generation
- 🔲 Visual regression testing
- 🔲 Cloud deployment options (AWS, Azure, GCP)
- 🔲 Advanced reporting with Allure
- 🔲 Mobile app testing support

---

## ⚡ Quick Command Reference

```bash
# Configuration
python utils/config_loader.py              # Test configuration loading

# Data Generation
python src/patient_data_generator.py       # Generate 100 patient records

# Testing
pytest tests/ -v                           # Run all tests
pytest tests/ --html=reports/report.html   # HTML report
pytest -m smoke                            # Smoke tests only

# Docker
docker build -t clinical-qa-sentinel .     # Build image
docker-compose up qa-tests                 # Run tests in container

# Code Quality
pytest tests/ --cov=src                    # Coverage report
pylint src/ tests/                         # Linting
```

---

## 🎓 Learning Resources

- **Page Object Model**: [Selenium Docs](https://www.selenium.dev/documentation/test_practices/encouraged/page_object_models/)
- **pytest**: [pytest Documentation](https://docs.pytest.org/)
- **Docker**: [Docker Get Started](https://docs.docker.com/get-started/)
- **HIPAA Compliance**: [HHS.gov HIPAA](https://www.hhs.gov/hipaa/)

---

<p align="center">
  <strong>Built with ❤️ for Healthcare Quality Assurance</strong>
</p>

<p align="center">
  Made with security, compliance, and patient safety in mind
</p>

<p align="center">
  <a href="https://github.com/San1190/Clinical-QA-Sentinel">⭐ Star this repo if you find it useful!</a>
</p>
