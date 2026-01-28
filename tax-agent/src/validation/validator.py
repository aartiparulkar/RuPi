# src/validation/validator.py

from src.models.taxModels import TaxComputationInput
from src.rules import fy2024_25

class ValidationError(Exception):
    pass

def validate_input(data: TaxComputationInput) -> None:
    # Validate financial year
    if data.user_profile.financial_year != "FY 2024-25":
        raise ValidationError(f"Unsupported Financial Year: {data.user_profile.financial_year}")

    # Validate employment type
    if data.user_profile.employment_type.lower() != "salaried":
        raise ValidationError("Only 'salaried' employment type is supported.")

    # Validate residency
    if not data.user_profile.is_resident:
        raise ValidationError("Only resident taxpayers are supported.")

    # Validate gross salary
    if data.income_details.gross_salary < 0:
        raise ValidationError("Gross salary cannot be negative.")

    # Validate deductions - 80C
    if data.deduction_details.sec_80c < 0:
        raise ValidationError("Section 80C deduction cannot be negative.")
    if data.deduction_details.sec_80c > fy2024_25.DEDuction_LIMITS["sec_80c"]:
        raise ValidationError(f"Section 80C deduction exceeds limit of ₹{fy2024_25.DEDuction_LIMITS['sec_80c']}.")

    # Validate deductions - 80D
    if data.deduction_details.sec_80d < 0:
        raise ValidationError("Section 80D deduction cannot be negative.")
    if data.deduction_details.sec_80d > fy2024_25.DEDuction_LIMITS["sec_80d"]:
        raise ValidationError(f"Section 80D deduction exceeds limit of ₹{fy2024_25.DEDuction_LIMITS['sec_80d']}.")

    # Validate standard deduction applicable flag
    if not isinstance(data.deduction_details.standard_deduction_applicable, bool):
        raise ValidationError("Standard deduction applicable flag must be boolean.")
