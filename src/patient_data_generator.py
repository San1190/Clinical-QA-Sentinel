"""
Healthcare Test Data Generator - Synthetic Patient Records
===========================================================
Purpose: Generate realistic synthetic patient data for healthcare system testing
Compliance: GDPR/HIPAA compliant - NO REAL PATIENT DATA
Author: QA Automation Team
Version: 1.0.0
Last Updated: 2025-12-29

IMPORTANT NOTICE:
This tool generates SYNTHETIC data only for testing purposes.
All generated records are completely fictional and do not represent real individuals.
Use this data exclusively for:
- Load testing database systems
- QA automation testing
- Performance benchmarking
- Development environment setup

NEVER use this tool to generate data that could be confused with real patient records.
"""

import csv
import random
from datetime import datetime, timedelta
from typing import List, Dict
from faker import Faker


# ============================================================================
# MEDICAL DATA CONSTANTS - Realistic Healthcare Reference Data
# ============================================================================

class MedicalDataConstants:
    """
    Reference data for generating realistic medical information.
    
    All data based on standard medical classifications and
    common healthcare system requirements.
    """
    
    # ABO Blood Group System (ISO 3166)
    BLOOD_TYPES: List[str] = [
        'A+', 'A-',
        'B+', 'B-',
        'AB+', 'AB-',
        'O+', 'O-'
    ]
    
    # Blood type distribution (approximate global percentages)
    BLOOD_TYPE_WEIGHTS: List[float] = [
        0.35,  # A+ (35%)
        0.06,  # A- (6%)
        0.09,  # B+ (9%)
        0.02,  # B- (2%)
        0.04,  # AB+ (4%)
        0.01,  # AB- (1%)
        0.38,  # O+ (38%)
        0.05   # O- (5%)
    ]
    
    # Common medication allergies (clinically significant)
    COMMON_ALLERGIES: List[str] = [
        'Penicillin',
        'Amoxicillin',
        'Sulfonamides',
        'Cephalosporins',
        'Aspirin',
        'Ibuprofen',
        'Latex',
        'Contrast Dye',
        'Codeine',
        'Morphine',
        'Tetracycline',
        'Erythromycin',
        'Vancomycin',
        'Ciprofloxacin',
        'Local Anesthetics'
    ]
    
    # Allergy combinations (some patients have multiple allergies)
    MULTI_ALLERGY_COMBINATIONS: List[List[str]] = [
        ['Penicillin', 'Amoxicillin', 'Cephalosporins'],  # Beta-lactam cross-reactivity
        ['Aspirin', 'Ibuprofen'],  # NSAIDs sensitivity
        ['Codeine', 'Morphine'],  # Opioid sensitivity
        ['Sulfonamides', 'Contrast Dye'],  # Sulfa allergy group
    ]
    
    # Probability that a patient has no known allergies
    NO_ALLERGY_PROBABILITY: float = 0.40  # 40% of patients
    
    # Probability that a patient has multiple allergies
    MULTIPLE_ALLERGY_PROBABILITY: float = 0.15  # 15% of patients


# ============================================================================
# PATIENT DATA GENERATOR
# ============================================================================

class SyntheticPatientGenerator:
    """
    Generates realistic synthetic patient records for healthcare system testing.
    
    Features:
    - Unique patient IDs
    - Realistic demographic data
    - Medically accurate blood type distribution
    - Clinically relevant allergy information
    - Age-appropriate patient profiles
    """
    
    def __init__(self, locale: str = 'en_US', seed: int = None):
        """
        Initialize the patient data generator.
        
        Args:
            locale: Locale for name generation (default: en_US for international compatibility)
            seed: Random seed for reproducible test data (optional)
        """
        self.faker = Faker(locale)
        
        # Set seed for reproducibility if provided
        if seed is not None:
            Faker.seed(seed)
            random.seed(seed)
        
        self.generated_ids: set = set()
        
    def _generate_unique_patient_id(self) -> str:
        """
        Generate a unique patient identifier following healthcare standards.
        
        Format: PT-YYYYMMDD-NNNN
        - PT: Patient prefix
        - YYYYMMDD: Registration date (randomized)
        - NNNN: Sequential number
        
        Returns:
            str: Unique patient ID
        """
        while True:
            # Random registration date within last 10 years
            days_ago = random.randint(0, 3650)
            reg_date = datetime.now() - timedelta(days=days_ago)
            date_part = reg_date.strftime('%Y%m%d')
            
            # Sequential number (4 digits)
            seq_number = random.randint(1000, 9999)
            
            patient_id = f"PT-{date_part}-{seq_number}"
            
            # Ensure uniqueness
            if patient_id not in self.generated_ids:
                self.generated_ids.add(patient_id)
                return patient_id
    
    def _generate_realistic_age(self) -> int:
        """
        Generate a realistic patient age based on healthcare demographics.
        
        Age distribution weighted to reflect typical patient populations:
        - Children (0-17): 20%
        - Adults (18-64): 50%
        - Seniors (65+): 30%
        
        Returns:
            int: Patient age in years
        """
        age_group = random.choices(
            ['child', 'adult', 'senior'],
            weights=[0.20, 0.50, 0.30]
        )[0]
        
        if age_group == 'child':
            return random.randint(0, 17)
        elif age_group == 'adult':
            return random.randint(18, 64)
        else:  # senior
            return random.randint(65, 95)
    
    def _generate_date_of_birth(self, age: int) -> str:
        """
        Calculate date of birth from age.
        
        Args:
            age: Patient age in years
            
        Returns:
            str: Date of birth in ISO format (YYYY-MM-DD)
        """
        today = datetime.now()
        birth_year = today.year - age
        
        # Random month and day
        birth_month = random.randint(1, 12)
        
        # Handle different month lengths
        if birth_month in [1, 3, 5, 7, 8, 10, 12]:
            max_day = 31
        elif birth_month in [4, 6, 9, 11]:
            max_day = 30
        else:  # February
            max_day = 29 if birth_year % 4 == 0 else 28
        
        birth_day = random.randint(1, max_day)
        
        dob = datetime(birth_year, birth_month, birth_day)
        return dob.strftime('%Y-%m-%d')
    
    def _generate_blood_type(self) -> str:
        """
        Generate blood type with realistic distribution.
        
        Uses actual global blood type frequency distribution
        to create statistically accurate test datasets.
        
        Returns:
            str: Blood type (e.g., 'O+', 'AB-')
        """
        return random.choices(
            MedicalDataConstants.BLOOD_TYPES,
            weights=MedicalDataConstants.BLOOD_TYPE_WEIGHTS
        )[0]
    
    def _generate_allergies(self) -> str:
        """
        Generate realistic allergy information.
        
        Simulates real-world scenarios:
        - ~40% of patients have no known allergies
        - ~45% have a single allergy
        - ~15% have multiple related allergies
        
        Returns:
            str: Comma-separated allergy list or 'None'
        """
        # Determine if patient has allergies
        if random.random() < MedicalDataConstants.NO_ALLERGY_PROBABILITY:
            return 'None'
        
        # Determine if patient has multiple allergies
        if random.random() < MedicalDataConstants.MULTIPLE_ALLERGY_PROBABILITY:
            # Use a clinically related allergy combination
            allergy_group = random.choice(MedicalDataConstants.MULTI_ALLERGY_COMBINATIONS)
            
            # Sometimes include additional unrelated allergies
            if random.random() < 0.3:
                extra_allergy = random.choice(MedicalDataConstants.COMMON_ALLERGIES)
                if extra_allergy not in allergy_group:
                    allergy_group.append(extra_allergy)
            
            return ', '.join(allergy_group)
        else:
            # Single allergy
            return random.choice(MedicalDataConstants.COMMON_ALLERGIES)
    
    def generate_patient(self) -> Dict[str, str]:
        """
        Generate a complete synthetic patient record.
        
        Returns:
            Dict containing all patient fields
        """
        # Generate age first (affects name generation context)
        age = self._generate_realistic_age()
        
        # Generate patient data
        patient = {
            'patient_id': self._generate_unique_patient_id(),
            'full_name': self.faker.name(),
            'date_of_birth': self._generate_date_of_birth(age),
            'blood_type': self._generate_blood_type(),
            'allergies': self._generate_allergies()
        }
        
        return patient
    
    def generate_patients_batch(self, count: int) -> List[Dict[str, str]]:
        """
        Generate multiple patient records.
        
        Args:
            count: Number of patient records to generate
            
        Returns:
            List of patient dictionaries
        """
        return [self.generate_patient() for _ in range(count)]


# ============================================================================
# CSV EXPORT FUNCTIONALITY
# ============================================================================

class PatientDataExporter:
    """
    Handles exporting synthetic patient data to various formats.
    """
    
    # CSV field definitions
    CSV_FIELDNAMES: List[str] = [
        'patient_id',
        'full_name',
        'date_of_birth',
        'blood_type',
        'allergies'
    ]
    
    # Human-readable headers for CSV
    CSV_HEADERS: Dict[str, str] = {
        'patient_id': 'Patient ID',
        'full_name': 'Full Name',
        'date_of_birth': 'Date of Birth',
        'blood_type': 'Blood Type',
        'allergies': 'Known Allergies'
    }
    
    @staticmethod
    def export_to_csv(
        patients: List[Dict[str, str]], 
        filename: str,
        include_header_row: bool = True
    ) -> None:
        """
        Export patient data to CSV file.
        
        Args:
            patients: List of patient dictionaries
            filename: Output CSV filename
            include_header_row: Whether to include header row (default: True)
        """
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(
                    csvfile,
                    fieldnames=PatientDataExporter.CSV_FIELDNAMES,
                    extrasaction='ignore'
                )
                
                if include_header_row:
                    # Write human-readable headers
                    writer.writerow(PatientDataExporter.CSV_HEADERS)
                
                # Write patient data
                writer.writerows(patients)
            
            print(f"✓ Successfully exported {len(patients)} patient records to '{filename}'")
            
        except IOError as e:
            print(f"✗ ERROR: Failed to write CSV file - {str(e)}")
            raise
        except Exception as e:
            print(f"✗ UNEXPECTED ERROR during CSV export - {str(e)}")
            raise
    
    @staticmethod
    def print_sample_data(patients: List[Dict[str, str]], sample_size: int = 5) -> None:
        """
        Print sample patient records to console for verification.
        
        Args:
            patients: List of patient dictionaries
            sample_size: Number of records to display (default: 5)
        """
        print("\n" + "="*80)
        print("SAMPLE PATIENT RECORDS (for verification)")
        print("="*80)
        
        for i, patient in enumerate(patients[:sample_size], 1):
            print(f"\nPatient #{i}:")
            print(f"  ID:              {patient['patient_id']}")
            print(f"  Name:            {patient['full_name']}")
            print(f"  Date of Birth:   {patient['date_of_birth']}")
            print(f"  Blood Type:      {patient['blood_type']}")
            print(f"  Allergies:       {patient['allergies']}")
        
        if len(patients) > sample_size:
            print(f"\n... and {len(patients) - sample_size} more records")
        
        print("="*80 + "\n")


# ============================================================================
# DATA STATISTICS AND VALIDATION
# ============================================================================

class DataStatistics:
    """
    Provides statistical analysis of generated patient data.
    Useful for validating data quality and distribution.
    """
    
    @staticmethod
    def analyze_dataset(patients: List[Dict[str, str]]) -> None:
        """
        Analyze and display statistics about the generated dataset.
        
        Args:
            patients: List of patient dictionaries
        """
        total_patients = len(patients)
        
        # Blood type distribution
        blood_type_counts = {}
        for patient in patients:
            bt = patient['blood_type']
            blood_type_counts[bt] = blood_type_counts.get(bt, 0) + 1
        
        # Allergy statistics
        patients_with_allergies = sum(
            1 for p in patients if p['allergies'] != 'None'
        )
        patients_no_allergies = total_patients - patients_with_allergies
        
        # Age distribution (approximate from birth dates)
        current_year = datetime.now().year
        age_groups = {'0-17': 0, '18-64': 0, '65+': 0}
        
        for patient in patients:
            birth_year = int(patient['date_of_birth'].split('-')[0])
            age = current_year - birth_year
            
            if age <= 17:
                age_groups['0-17'] += 1
            elif age <= 64:
                age_groups['18-64'] += 1
            else:
                age_groups['65+'] += 1
        
        # Print statistics
        print("\n" + "="*80)
        print("DATASET STATISTICS")
        print("="*80)
        print(f"Total Patients Generated: {total_patients}")
        
        print("\nBlood Type Distribution:")
        for blood_type in sorted(blood_type_counts.keys()):
            count = blood_type_counts[blood_type]
            percentage = (count / total_patients) * 100
            print(f"  {blood_type:>4}: {count:>4} patients ({percentage:>5.1f}%)")
        
        print("\nAge Group Distribution:")
        for age_range, count in age_groups.items():
            percentage = (count / total_patients) * 100
            print(f"  {age_range:>10}: {count:>4} patients ({percentage:>5.1f}%)")
        
        print("\nAllergy Statistics:")
        allergy_percentage = (patients_with_allergies / total_patients) * 100
        no_allergy_percentage = (patients_no_allergies / total_patients) * 100
        print(f"  With Allergies:    {patients_with_allergies:>4} patients ({allergy_percentage:>5.1f}%)")
        print(f"  Without Allergies: {patients_no_allergies:>4} patients ({no_allergy_percentage:>5.1f}%)")
        
        print("="*80 + "\n")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """
    Main entry point for the Synthetic Patient Data Generator.
    """
    print("\n" + "="*80)
    print("  HEALTHCARE SYNTHETIC PATIENT DATA GENERATOR")
    print("  Version 1.0.0 | GDPR/HIPAA Testing Compliant")
    print("="*80)
    
    # Configuration
    NUM_PATIENTS = 100
    OUTPUT_FILENAME = 'dummy_patients.csv'
    RANDOM_SEED = None  # Set to a number for reproducible data, None for random
    
    print(f"\nConfiguration:")
    print(f"  Number of patients: {NUM_PATIENTS}")
    print(f"  Output file:        {OUTPUT_FILENAME}")
    print(f"  Random seed:        {RANDOM_SEED if RANDOM_SEED else 'Random (not reproducible)'}")
    print(f"\nGenerating synthetic patient data...")
    
    try:
        # Initialize generator
        generator = SyntheticPatientGenerator(locale='en_US', seed=RANDOM_SEED)
        
        # Generate patient records
        patients = generator.generate_patients_batch(NUM_PATIENTS)
        
        print(f"✓ Generated {len(patients)} patient records")
        
        # Display sample data for verification
        PatientDataExporter.print_sample_data(patients, sample_size=5)
        
        # Export to CSV
        print(f"Exporting data to '{OUTPUT_FILENAME}'...")
        PatientDataExporter.export_to_csv(patients, OUTPUT_FILENAME)
        
        # Display statistics
        DataStatistics.analyze_dataset(patients)
        
        # Success message
        print("="*80)
        print("  DATA GENERATION COMPLETED SUCCESSFULLY")
        print("="*80)
        print(f"\n✓ File '{OUTPUT_FILENAME}' is ready for use in:")
        print("  - Database load testing")
        print("  - QA automation scenarios")
        print("  - Development environment setup")
        print("  - Performance benchmarking")
        print("\n⚠  REMINDER: This is SYNTHETIC data only - not real patient information")
        print("="*80 + "\n")
        
    except KeyboardInterrupt:
        print("\n\n⚠  Operation cancelled by user\n")
        
    except Exception as e:
        print(f"\n✗ CRITICAL ERROR: {str(e)}\n")
        raise


if __name__ == "__main__":
    main()
