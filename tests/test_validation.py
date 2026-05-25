"""
Test script to validate the AIJobBasic Pydantic model.

Tests both valid data that passes validation and invalid data that should fail.
This demonstrates how the model detects data drift and constraint violations.
"""

from data_models.ai_job_basic import AIJobBasic
from pydantic import ValidationError


def test_valid_data():
    """Test with valid data - should pass."""
    print("\n✓ Testing VALID data:")
    print("-" * 50)
    
    valid_record = {
        "job_id": 0,
        "job_role": "Data Analyst",
        "industry": "Technology",
        "country": "Canada",
        "year": 2021,
        "automation_risk_percent": 26.22,
    }
    
    try:
        job = AIJobBasic(**valid_record)
        print(f"✅ SUCCESS: {job}")
    except ValidationError as e:
        print(f"❌ FAILED: {e}")


def test_invalid_automation_risk():
    """Test with out-of-range automation_risk_percent."""
    print("\n✗ Testing INVALID automation_risk_percent (>100):")
    print("-" * 50)
    
    invalid_record = {
        "job_id": 1,
        "job_role": "Accountant",
        "industry": "Finance",
        "country": "Brazil",
        "year": 2020,
        "automation_risk_percent": 150.5,  # Invalid: > 100
    }
    
    try:
        job = AIJobBasic(**invalid_record)
        print(f"✅ Unexpectedly passed: {job}")
    except ValidationError as e:
        print(f"✅ CAUGHT VALIDATION ERROR (expected):")
        print(f"   {e.errors()[0]['msg']}")


def test_invalid_industry():
    """Test with invalid industry value."""
    print("\n✗ Testing INVALID industry value:")
    print("-" * 50)
    
    invalid_record = {
        "job_id": 2,
        "job_role": "Teacher",
        "industry": "RealEstate",  # Invalid: not in allowed values
        "country": "USA",
        "year": 2020,
        "automation_risk_percent": 31.3,
    }
    
    try:
        job = AIJobBasic(**invalid_record)
        print(f"✅ Unexpectedly passed: {job}")
    except ValidationError as e:
        print(f"✅ CAUGHT VALIDATION ERROR (expected):")
        error_msg = e.errors()[0]['msg']
        print(f"   {error_msg}")


def test_invalid_country():
    """Test with invalid country value."""
    print("\n✗ Testing INVALID country value:")
    print("-" * 50)
    
    invalid_record = {
        "job_id": 3,
        "job_role": "Software Engineer",
        "industry": "Technology",
        "country": "France",  # Invalid: not in allowed values
        "year": 2022,
        "automation_risk_percent": 8.54,
    }
    
    try:
        job = AIJobBasic(**invalid_record)
        print(f"✅ Unexpectedly passed: {job}")
    except ValidationError as e:
        print(f"✅ CAUGHT VALIDATION ERROR (expected):")
        error_msg = e.errors()[0]['msg']
        print(f"   {error_msg}")


def test_invalid_year():
    """Test with out-of-range year."""
    print("\n✗ Testing INVALID year (outside 2020-2026 range):")
    print("-" * 50)
    
    invalid_record = {
        "job_id": 4,
        "job_role": "Marketing Specialist",
        "industry": "Retail",
        "country": "Germany",
        "year": 2019,  # Invalid: < 2020
        "automation_risk_percent": 19.86,
    }
    
    try:
        job = AIJobBasic(**invalid_record)
        print(f"✅ Unexpectedly passed: {job}")
    except ValidationError as e:
        print(f"✅ CAUGHT VALIDATION ERROR (expected):")
        print(f"   {e.errors()[0]['msg']}")


def test_missing_required_field():
    """Test with missing required field."""
    print("\n✗ Testing MISSING required field (job_role):")
    print("-" * 50)
    
    invalid_record = {
        "job_id": 5,
        # "job_role": "Financial Analyst",  # Missing!
        "industry": "Finance",
        "country": "Singapore",
        "year": 2020,
        "automation_risk_percent": 59.48,
    }
    
    try:
        job = AIJobBasic(**invalid_record)
        print(f"✅ Unexpectedly passed: {job}")
    except ValidationError as e:
        print(f"✅ CAUGHT VALIDATION ERROR (expected):")
        print(f"   Field: {e.errors()[0]['loc'][0]}")
        print(f"   Error: {e.errors()[0]['msg']}")


def test_wrong_type():
    """Test with wrong data type."""
    print("\n✗ Testing WRONG data type (job_id as string):")
    print("-" * 50)
    
    invalid_record = {
        "job_id": "zero",  # Invalid: should be int
        "job_role": "HR Manager",
        "industry": "Education",
        "country": "Germany",
        "year": 2025,
        "automation_risk_percent": 33.16,
    }
    
    try:
        job = AIJobBasic(**invalid_record)
        print(f"✅ Unexpectedly passed: {job}")
    except ValidationError as e:
        print(f"✅ CAUGHT VALIDATION ERROR (expected):")
        print(f"   Field: {e.errors()[0]['loc'][0]}")
        print(f"   Error: {e.errors()[0]['msg']}")


def test_negative_automation_risk():
    """Test with negative automation_risk_percent."""
    print("\n✗ Testing NEGATIVE automation_risk_percent:")
    print("-" * 50)
    
    invalid_record = {
        "job_id": 6,
        "job_role": "Data Analyst",
        "industry": "Technology",
        "country": "Canada",
        "year": 2023,
        "automation_risk_percent": -5.0,  # Invalid: < 0
    }
    
    try:
        job = AIJobBasic(**invalid_record)
        print(f"✅ Unexpectedly passed: {job}")
    except ValidationError as e:
        print(f"✅ CAUGHT VALIDATION ERROR (expected):")
        print(f"   {e.errors()[0]['msg']}")


if __name__ == "__main__":
    print("=" * 50)
    print("PYDANTIC VALIDATION TEST SUITE")
    print("=" * 50)
    
    # Test valid data
    test_valid_data()
    
    # Test various invalid data scenarios
    test_invalid_automation_risk()
    test_invalid_industry()
    test_invalid_country()
    test_invalid_year()
    test_missing_required_field()
    test_wrong_type()
    test_negative_automation_risk()
    
    print("\n" + "=" * 50)
    print("VALIDATION TESTING COMPLETE")
    print("=" * 50)
