from dataclasses import dataclass
from typing import Optional, List, Dict

@dataclass
class UserProfile:
    financial_year: str
    age: int
    is_resident: bool
    employment_type: str  # e.g., 'salaried'

@dataclass
class IncomeDetails:
    gross_salary: float

@dataclass
class DeductionDetails:
    sec_80c: float = 0.0
    sec_80d: float = 0.0
    standard_deduction_applicable: bool = True

@dataclass
class TaxComputationInput:
    user_profile: UserProfile
    income_details: IncomeDetails
    deduction_details: DeductionDetails

@dataclass
class SlabTax:
    slab_range: str
    tax_amount: float

@dataclass
class TaxComputationResult:
    taxable_income: float
    slab_wise_tax: List[SlabTax]
    cess: float
    total_tax: float
