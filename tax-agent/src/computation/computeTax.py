from typing import List
from src.models.taxModels import TaxComputationInput, TaxComputationResult, SlabTax
from src.rules import fy2024_25

def apply_standard_deduction(gross_salary: float, applicable: bool) -> float:
    if applicable:
        return max(0.0, gross_salary - fy2024_25.STANDARD_DEDUCTION)
    return gross_salary

def calculate_taxable_income(data: TaxComputationInput, regime: str) -> float:
    income_after_std_deduction = apply_standard_deduction(
        data.income_details.gross_salary,
        data.deduction_details.standard_deduction_applicable
    )
    
    if regime == 'old':
        income_after_std_deduction -= data.deduction_details.sec_80c
        income_after_std_deduction -= data.deduction_details.sec_80d
        
    return max(0.0, income_after_std_deduction)  # Taxable income cannot be negative

def calculate_slab_wise_tax(taxable_income: float, slabs: List[tuple]) -> List[SlabTax]:
    slab_taxes = []
    lower_limit = 0.0
    
    for upper_limit, rate in slabs:
        if taxable_income <= lower_limit:
            tax_for_slab = 0.0
        else:
            taxable_amount = min(taxable_income, upper_limit) - lower_limit
            tax_for_slab = taxable_amount * rate
        slab_range_str = f"{int(lower_limit)}-{int(upper_limit) if upper_limit != float('inf') else '∞'}"
        slab_taxes.append(SlabTax(slab_range=slab_range_str, tax_amount=round(tax_for_slab, 2)))
        lower_limit = upper_limit
    
    return slab_taxes

def calculate_total_tax(slab_taxes: List[SlabTax]) -> float:
    total = sum(slab.tax_amount for slab in slab_taxes)
    return round(total, 2)

def calculate_cess(tax: float) -> float:
    return round(tax * fy2024_25.CESS_RATE, 2)

def compute_tax(data: TaxComputationInput, regime: str) -> TaxComputationResult:
    """
    regime: 'old' or 'new'
    """
    if regime == "old":
        slabs = fy2024_25.OLD_REGIME_SLABS
    elif regime == "new":
        slabs = fy2024_25.NEW_REGIME_SLABS
    else:
        raise ValueError("Invalid regime specified. Choose 'old' or 'new'.")

    taxable_income = calculate_taxable_income(data, regime)
    slab_wise_tax = calculate_slab_wise_tax(taxable_income, slabs)
    total_tax = calculate_total_tax(slab_wise_tax)
    cess = calculate_cess(total_tax)
    total_tax_including_cess = round(total_tax + cess, 2)

    return TaxComputationResult(
        taxable_income=round(taxable_income, 2),
        slab_wise_tax=slab_wise_tax,
        cess=cess,
        total_tax=total_tax_including_cess
    )
