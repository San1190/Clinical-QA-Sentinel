# Clinical-QA-Sentinel 🏥

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Healthcare](https://img.shields.io/badge/sector-HealthTech-green.svg)](https://github.com/San1190/Clinical-QA-Sentinel)
[![pytest](https://img.shields.io/badge/testing-pytest-blue.svg)](https://docs.pytest.org/)
[![Tested](https://img.shields.io/badge/stress_tested-100%2F100_passed-brightgreen.svg)](https://github.com/San1190/Clinical-QA-Sentinel)

> **Enterprise-Grade QA Automation Framework for Healthcare Systems**

Clinical-QA-Sentinel is a comprehensive Quality Assurance automation framework specifically designed for healthcare applications. Battle-tested with **100% success rate** under concurrent load (100 simultaneous users), this framework ensures medical systems meet the highest standards of reliability, security, and compliance.

---

## 🎯 Overview

In healthcare, software quality isn't just about functionality—it's about patient safety. Clinical-QA-Sentinel provides organizations with robust testing tools that ensure medical applications meet the highest standards while maintaining GDPR/HIPAA compliance.

### ⭐ Key Features

- **🔐 Security-First**: Built-in GDPR/HIPAA compliance mechanisms
- **🤖 Full E2E Automation**: Complete appointment booking workflow testing
- **📊 Synthetic Patient Data**: Realistic test data without compromising privacy
- **⚡ Stress-Tested**: 100/100 success rate with concurrent users
- **🏗️ Page Object Model**: Maintainable and scalable architecture
- **🎬 Visual Demo Mode**: See automation in action with live browser
- **⏱️ Headless Execution**: CI/CD ready, no GUI required
- **🧪 pytest Framework**: Professional testing with detailed reports
- **🌐 Multi-Language Support**: Code comments in Spanish/English
- **🐳 Docker Ready**: Containerized execution

---

## 📊 Battle-Tested Performance

### Stress Test Results (Latest Run)

```
⚡ TEST: 100 Concurrent Users
✅ Success Rate: 100% (100/100 appointments booked)
⏱️  Average Time: 10.40s per booking
📈 Throughput: 0.75 bookings/second
🎯 Total Time: 133.13s
```

**Tested Scenarios:**
- ✅ Concurrent user authentication
- ✅ Simultaneous form submissions
- ✅ Race condition handling
- ✅ Session isolation
- ✅ Data integrity under load

---

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/San1190/Clinical-QA-Sentinel.git
cd Clinical-QA-Sentinel

# Install dependencies
pip install -r requirements.txt

# Verify installation
python utils/config_loader.py
```

### Run Tests

```bash
# Basic appointment flow test
pytest tests/test_appointment_flow.py -v

# All tests with HTML report
pytest tests/ --html=reports/test_report.html -v

# Run in parallel (faster)
pytest tests/ -n auto
```

### Visual Demo (See It In Action!)

```bash
# Watch the automation work step-by-step
python demo_visual.py
```

**What you'll see:**
- ✅ Chrome opens visibly
- ✅ Automatic login
- ✅ Synthetic patient generation
- ✅ Form auto-fill (checkbox, date, comments)
- ✅ Submission and confirmation

### Stress Testing

```bash
# Test with 10 concurrent users
python test_estres.py --usuarios 10

# Stress test with 100 users (proven to work!)
python test_estres.py --usuarios 100
```

**Example Output:**
```
✅ Usuario   1 | 12.33s | Gregory Orr
✅ Usuario   2 | 12.56s | Kelsey Hudson
...
✅ Usuario 100 |  8.46s | Belinda Hudson

✅ Exitosos: 100/100 (100.0%)
⏱️  Tiempo promedio: 10.40s
🎉 ¡TODOS LOS TESTS PASARON! Sistema robusto.
```

---

## 📁 Project Structure

```
Clinical-QA-Sentinel/
├── pages/                       # Page Object Model
│   ├── base_page.py            # Base class with reusable methods
│   ├── login_page.py           # Login page automation
│   └── appointment_page.py     # Appointment booking automation
├── tests/                       # pytest test suites
│   ├── test_authentication.py  # Auth tests
│   └── test_appointment_flow.py # E2E appointment tests
├── src/                         # Core automation
│   ├── patient_data_generator.py # Synthetic data generation
│   └── auth_stress_test.py     # Security auditing
├── config/
│   └── config.json             # Centralized configuration
├── demo_visual.py              # Visual demonstration script
├── test_estres.py              # Concurrent stress testing
├── conftest.py                 # pytest configuration
├── requirements.txt            # Dependencies
└── INFORME_VALIDACION.md      # Validation report (Spanish)
```

---

## 🏥 Appointment Booking Flow

### Architecture

```
┌──────────────────────┐
│   TEST LAYER         │
│  (pytest tests)      │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  PAGE OBJECTS        │
│  • LoginPage         │
│  • AppointmentPage   │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  DATA LAYER          │
│  • PatientGenerator  │
│  • ConfigLoader      │
└──────────────────────┘
```

### Example Usage

```python
from pages.login_page import LoginPage
from pages.appointment_page import AppointmentPage
from src.patient_data_generator import SyntheticPatientGenerator

def test_appointment_booking(driver, config):
    # Login
    login_page = LoginPage(driver, config)
    login_page.open()
    login_page.login_with_credentials("John Doe", "password")
    
    # Generate synthetic patient
    generator = SyntheticPatientGenerator()
    patient = generator.generate_patient()
    
    # Format medical notes
    medical_notes = (
        f"PATIENT: {patient['full_name']} | "
        f"BLOOD: {patient['blood_type']} | "
        f"ALLERGIES: {patient['allergies']}"
    )
    
    # Book appointment
    appointment_page = AppointmentPage(driver, config)
    appointment_page.fill_appointment_form(
        comment=medical_notes,
        visit_date="01/30/2025"
    )
    
    # Verify confirmation
    assert appointment_page.is_appointment_confirmed()
```

---

## 📊 Synthetic Patient Data Generation

### Features

- **100% Synthetic**: Generated with Faker, no real patient data
- **Medically Accurate**: Realistic blood type distribution
- **GDPR/HIPAA Compliant**: Privacy-safe testing data

### Generate Test Data

```bash
python src/patient_data_generator.py
```

**Output**: `dummy_patients.csv` with 100 records

**Blood Type Distribution** (medically accurate):
- O+ (38%), A+ (35%), B+ (9%), AB+ (3%)
- O- (7%), A- (6%), B- (1.5%), AB- (0.5%)

**Sample Patient Record:**
```json
{
  "patient_id": "PT-20230313-6152",
  "full_name": "Gregory Orr",
  "date_of_birth": "1985-06-15",
  "blood_type": "O+",
  "allergies": "Penicillin"
}
```

---

## 🔧 Configuration

### config.json

```json
{
  "active_environment": "demo",
  "browser": {
    "name": "chrome",
    "headless": true,
    "options": [
      "--disable-gpu",
      "--no-sandbox"
    ]
  },
  "locators": {
    "appointment_page": {
      "readmission_check": "id:chk_hospotal_readmission",
      "visit_date_input": "id:txt_visit_date",
      "comment_input": "id:txt_comment",
      "book_btn": "id:btn-book-appointment"
    }
  },
  "timeouts": {
    "page_load_timeout": 10,
    "element_wait_timeout": 5
  }
}
```

---

## 🐳 Docker Support

```bash
# Build image
docker build -t clinical-qa-sentinel .

# Run tests in container
docker run --rm -v ${PWD}/reports:/app/reports clinical-qa-sentinel

# Docker Compose
docker-compose up qa-tests
```

---

## 🔒 Security & Compliance

### Security Features

- ✅ **Headless Mode**: No GUI popups, CI/CD ready
- ✅ **Session Isolation**: Each test has isolated browser session
- ✅ **No Credentials in Code**: Environment variable support
- ✅ **Audit Logging**: Complete action logging for compliance
- ✅ **Synthetic Data Only**: Zero risk of PHI exposure

### Compliance Standards

- **GDPR**: General Data Protection Regulation
- **HIPAA**: Health Insurance Portability and Accountability Act
- **ISO 27001**: Information Security Management

---

## 📝 Quick Commands Reference

```bash
# Testing
pytest tests/test_appointment_flow.py -v        # Appointment test
pytest tests/test_authentication.py -v          # Auth test
pytest tests/ -n auto                           # Parallel execution

# Demos
python demo_visual.py                           # Visual demo
python demo_appointment_flow.py                 # Standalone demo

# Stress Testing
python test_estres.py --usuarios 10             # 10 users
python test_estres.py --usuarios 100            # 100 users (proven!)

# Data Generation
python src/patient_data_generator.py            # Generate patients

# Docker
docker build -t clinical-qa-sentinel .          # Build
docker-compose up qa-tests                      # Run in container
```

---

## 📈 Test Reports

### pytest HTML Reports

```bash
# Generate HTML report
pytest tests/ --html=reports/test_report.html --self-contained-html -v
```

**Report includes:**
- Test execution summary
- Pass/fail statistics
- Execution times
- Error screenshots

### Stress Test Reports

Automatically generated with:
- Success/failure rates
- Response time statistics (min/avg/max)
- Throughput metrics
- Patient data generated

---

## 🎓 Code Quality

### Commenting Standards

**Spanish comments** for business logic in core files
**English docstrings** for public APIs

**Example:**
```python
def fill_appointment_form(self, comment: str, visit_date: str = "30/01/2025") -> None:
    """
    Fill the complete appointment form.
    
    What this method does:
    ----------------------
    This is the MASTER method that executes the ENTIRE booking flow:
    1. Checks hospital readmission checkbox
    2. Selects health program (Medicaid)
    3. Enters visit date
    4. Enters medical notes (patient data goes here)
    5. Clicks "Book Appointment"
    
    Args:
        comment: Medical notes/comments (synthetic patient data)
        visit_date: Visit date in DD/MM/YYYY format
    """
    # PASO 1: Marcar checkbox de readmisión
    # This simulates that the patient was previously hospitalized
    self.logger.info("Marcando checkbox de readmisión hospitalaria...")
    self.click(self.READMISSION_CHECK)
```

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

### Code Standards

- Follow PEP 8
- Include docstrings
- Add tests for new features
- Spanish comments for business logic welcome
- Type hints for function signatures

---

## 🔄 Roadmap

### v1.0 (Current) ✅
- ✅ Authentication testing with POM
- ✅ Synthetic patient data generation
- ✅ **Complete appointment booking flow**
- ✅ **Visual interactive demo**
- ✅ **Concurrent stress testing (100 users proven)**
- ✅ Headless mode for CI/CD
- ✅ HTML reports

### v1.1 (Planned)
- 🔲 Firefox and Edge support
- 🔲 API testing capabilities
- 🔲 CI/CD templates (GitHub Actions, GitLab CI)
- 🔲 Dashboard with trends
- 🔲 Multi-language full support

### v2.0 (Future)
- 🔲 Visual regression testing
- 🔲 AI-powered test generation
- 🔲 Cloud deployment (AWS, Azure, GCP)
- 🔲 Mobile app testing
- 🔲 Advanced reporting with Allure

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/San1190/Clinical-QA-Sentinel/issues)
- **Discussions**: [GitHub Discussions](https://github.com/San1190/Clinical-QA-Sentinel/discussions)
- **Documentation**: See `INFORME_VALIDACION.md` for detailed validation report

---

## 📊 Proven Results

This framework has been **battle-tested** and proven to handle:

| Metric | Result |
|--------|--------|
| Concurrent Users | ✅ 100 simultaneous |
| Success Rate | ✅ 100% (100/100) |
| Average Response | ✅ 10.40 seconds |
| Throughput | ✅ 0.75 bookings/sec |
| Stability | ✅ No failures detected |

---

<p align="center">
  <strong>Built with ❤️ for Healthcare Quality Assurance</strong>
</p>

<p align="center">
  Made with security, compliance, and patient safety in mind
</p>

<p align="center">
  <strong>⚡ Stress-Tested • 🔒 HIPAA Compliant • 🎯 100% Reliable</strong>
</p>

<p align="center">
  <a href="https://github.com/San1190/Clinical-QA-Sentinel">⭐ Star this repo if you find it useful!</a>
</p>
