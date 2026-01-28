from models.taxModels import UserProfile, IncomeDetails, DeductionDetails, TaxComputationInput
from validation.validator import validate_input, ValidationError
from computation.computeTax import compute_tax

def get_float(prompt: str) -> float:
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("Value cannot be negative. Please enter again.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

def main():
    print("=== Personal Finance Tax Agent (FY 2024-25) ===")

    # Collect inputs
    gross_salary = get_float("Enter your gross annual salary (₹): ")
    sec_80c = get_float("Enter deductions under Section 80C (₹): ")
    sec_80d = get_float("Enter deductions under Section 80D (₹): ")

    # For simplicity, fixed inputs for age, resident, employment type, FY
    user_profile = UserProfile(
        financial_year="FY 2024-25",
        age=30,
        is_resident=True,
        employment_type="salaried"
    )
    income_details = IncomeDetails(gross_salary=gross_salary)
    deduction_details = DeductionDetails(sec_80c=sec_80c, sec_80d=sec_80d, standard_deduction_applicable=True)

    data = TaxComputationInput(user_profile=user_profile, income_details=income_details, deduction_details=deduction_details)

    # Validate input
    try:
        validate_input(data)
    except ValidationError as e:
        print(f"Input validation error: {e}")
        return

    # Compute tax for both regimes
    for regime in ["old", "new"]:
        result = compute_tax(data, regime)
        print(f"\n--- {regime.capitalize()} Regime Tax Computation ---")
        print(f"Taxable Income: ₹{result.taxable_income}")
        print("Slab-wise Tax:")
        for slab in result.slab_wise_tax:
            print(f"  {slab.slab_range}: ₹{slab.tax_amount}")
        print(f"Cess (4%): ₹{result.cess}")
        print(f"Total Tax Payable: ₹{result.total_tax}")

if __name__ == "__main__":
    main()
