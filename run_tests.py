# ============================================================================
# Clinical-QA-Sentinel - Automated Test Runner
# ============================================================================
# Purpose: Quick verification that all components are working correctly
# Usage: python run_tests.py
# ============================================================================

import os
import sys
from pathlib import Path

# ANSI color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def print_header(text):
    """Print a formatted header"""
    print(f"\n{Colors.CYAN}{'='*70}{Colors.END}")
    print(f"{Colors.CYAN}{Colors.BOLD}{text}{Colors.END}")
    print(f"{Colors.CYAN}{'='*70}{Colors.END}\n")


def print_success(text):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")


def print_error(text):
    """Print error message"""
    print(f"{Colors.RED}✗ {text}{Colors.END}")


def print_info(text):
    """Print info message"""
    print(f"{Colors.BLUE}ℹ {text}{Colors.END}")


def check_dependencies():
    """Check if all required Python packages are installed"""
    print_header("Checking Dependencies")
    
    dependencies = {
        'selenium': 'Selenium WebDriver',
        'faker': 'Faker data generation',
        'csv': 'CSV handling (built-in)',
        'logging': 'Logging (built-in)'
    }
    
    all_installed = True
    
    for package, description in dependencies.items():
        try:
            __import__(package)
            print_success(f"{description} - Installed")
        except ImportError:
            print_error(f"{description} - NOT INSTALLED")
            all_installed = False
    
    return all_installed


def check_project_structure():
    """Verify project directory structure"""
    print_header("Checking Project Structure")
    
    required_dirs = ['src', 'tests', 'data', 'docs']
    required_files = [
        'README.md',
        'ARCHITECTURE.md',
        'requirements.txt',
        '.gitignore',
        'LICENSE',
        'src/auth_stress_test.py',
        'src/patient_data_generator.py'
    ]
    
    all_exist = True
    
    print_info("Checking directories...")
    for directory in required_dirs:
        if os.path.isdir(directory):
            print_success(f"Directory '{directory}/' exists")
        else:
            print_error(f"Directory '{directory}/' NOT FOUND")
            all_exist = False
    
    print_info("\nChecking files...")
    for file in required_files:
        if os.path.isfile(file):
            print_success(f"File '{file}' exists")
        else:
            print_error(f"File '{file}' NOT FOUND")
            all_exist = False
    
    return all_exist


def test_patient_generator():
    """Test the patient data generator"""
    print_header("Testing Patient Data Generator")
    
    try:
        # Import the module
        print_info("Importing patient_data_generator module...")
        sys.path.insert(0, 'src')
        from patient_data_generator import SyntheticPatientGenerator, PatientDataExporter
        
        print_success("Module imported successfully")
        
        # Create generator
        print_info("Creating patient generator instance...")
        generator = SyntheticPatientGenerator(seed=12345)  # Use seed for reproducibility
        print_success("Generator created")
        
        # Generate test data
        print_info("Generating 10 test patients...")
        patients = generator.generate_patients_batch(10)
        print_success(f"Generated {len(patients)} patients")
        
        # Validate data
        print_info("Validating generated data...")
        
        if len(patients) == 10:
            print_success("Correct number of patients generated")
        else:
            print_error(f"Expected 10 patients, got {len(patients)}")
            return False
        
        # Check first patient has all required fields
        required_fields = ['patient_id', 'full_name', 'date_of_birth', 'blood_type', 'allergies']
        first_patient = patients[0]
        
        for field in required_fields:
            if field in first_patient:
                print_success(f"Field '{field}' present in patient data")
            else:
                print_error(f"Field '{field}' MISSING in patient data")
                return False
        
        # Display sample patient
        print_info("\nSample patient record:")
        print(f"  ID:            {first_patient['patient_id']}")
        print(f"  Name:          {first_patient['full_name']}")
        print(f"  Date of Birth: {first_patient['date_of_birth']}")
        print(f"  Blood Type:    {first_patient['blood_type']}")
        print(f"  Allergies:     {first_patient['allergies']}")
        
        return True
        
    except Exception as e:
        print_error(f"Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def check_git_status():
    """Check Git repository status"""
    print_header("Checking Git Repository")
    
    if os.path.isdir('.git'):
        print_success("Git repository initialized")
        
        # Check if we can run git commands
        try:
            import subprocess
            result = subprocess.run(['git', 'status', '--short'], 
                                   capture_output=True, text=True, timeout=5)
            
            if result.returncode == 0:
                print_success("Git is working correctly")
                
                # Check for commits
                result = subprocess.run(['git', 'log', '--oneline', '-1'], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0 and result.stdout.strip():
                    print_success(f"Initial commit exists: {result.stdout.strip()}")
                else:
                    print_error("No commits found")
                    return False
            else:
                print_error("Git command failed")
                return False
                
        except Exception as e:
            print_error(f"Could not run git commands: {str(e)}")
            return False
        
        return True
    else:
        print_error("Git repository NOT initialized")
        return False


def generate_test_report(results):
    """Generate final test report"""
    print_header("Test Summary")
    
    total_tests = len(results)
    passed_tests = sum(results.values())
    failed_tests = total_tests - passed_tests
    
    print(f"Total Tests:  {total_tests}")
    print(f"Passed:       {Colors.GREEN}{passed_tests}{Colors.END}")
    print(f"Failed:       {Colors.RED}{failed_tests}{Colors.END}")
    print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%\n")
    
    if failed_tests == 0:
        print(f"{Colors.GREEN}{Colors.BOLD}✓ ALL TESTS PASSED! Framework is ready to use.{Colors.END}\n")
        return True
    else:
        print(f"{Colors.RED}{Colors.BOLD}✗ Some tests failed. Please review the output above.{Colors.END}\n")
        return False


def main():
    """Main test runner"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}")
    print("="*70)
    print("  CLINICAL-QA-SENTINEL - AUTOMATED TEST SUITE")
    print("  Version 1.0.0")
    print("="*70)
    print(f"{Colors.END}\n")
    
    # Dictionary to store test results
    results = {}
    
    # Run all tests
    results['Dependencies'] = check_dependencies()
    results['Project Structure'] = check_project_structure()
    results['Patient Generator'] = test_patient_generator()
    results['Git Repository'] = check_git_status()
    
    # Generate report
    all_passed = generate_test_report(results)
    
    # Exit code
    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
