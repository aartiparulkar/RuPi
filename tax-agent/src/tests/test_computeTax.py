import pytest
from src.models.taxModels import (
    UserProfile, IncomeDetails, DeductionDetails, TaxComputationInput
)
from src.computation.computeTax import compute_tax
from src.validation.validator import validate_input, ValidationError

def build_input(
    gross_salary, sec_80c=0, sec_80d=0, std_deduction=True,
    fy="FY 2024-25", age=30, resident=True, employment="salaried"
):
    return TaxComputationInput(
        user_profile=UserProfile(
            financial_year=fy,
            age=age,
            is_resident=resident,
            employment_type=employment
        ),
        income_details=IncomeDetails(
            gross_salary=gross_salary
        ),
        deduction_details=DeductionDetails(
            sec_80c=sec_80c,
            sec_80d=sec_80d,
            standard_deduction_applicable=std_deduction
        )
    )

def test_validate_input_valid():
    data = build_input(700000, 100000, 20000)
    # Should not raise exception
    validate_input(data)
    
def test_validate_input_invalid_80c():
    data = build_input(700000, 200000, 20000)  # 80C above limit
    with pytest.raises(ValidationError):
        validate_input(data)

def test_old_regime_tax_basic():
    data = build_input(500000, 50000, 0)
    validate_input(data)
    result = compute_tax(data, "old")
    assert result.taxable_income == 400000  # 500000 - 50000 std - 50000 deductions
    # Verify slab-wise tax sum matches total tax minus cess (4%)
    slab_sum = sum(slab.tax_amount for slab in result.slab_wise_tax)
    cess = result.cess
    assert abs(result.total_tax - (slab_sum + cess)) < 0.01

def test_new_regime_tax_basic():
    data = build_input(750000, 0, 0, std_deduction=True)
    validate_input(data)
    result = compute_tax(data, "new")
    assert result.taxable_income == 700000  # 750000 - 50000 std deduction
    slab_sum = sum(slab.tax_amount for slab in result.slab_wise_tax)
    cess = result.cess
    assert abs(result.total_tax - (slab_sum + cess)) < 0.01

def test_zero_tax_income():
    data = build_input(300000, 0, 0)
    validate_input(data)
    result = compute_tax(data, "old")
    assert result.taxable_income == 250000
    assert result.total_tax == 0

def test_boundary_slab():
    data = build_input(500000, 0, 0)
    validate_input(data)
    result = compute_tax(data, "old")
    assert result.taxable_income == 450000
    assert result.total_tax == 10400  # 5% on 250000 + 20% on 50000 + 4% cess
    
def test_max_deductions():
    data = build_input(1500000, 150000, 25000)
    validate_input(data)
    result_old = compute_tax(data, "old")
    result_new = compute_tax(data, "new")
    # Check taxable income doesn't go below zero
    assert result_old.taxable_income >= 0
    assert result_new.taxable_income >= 0

def test_negative_salary():
    data = build_input(-10000, 0, 0)
    with pytest.raises(ValidationError):
        validate_input(data)
