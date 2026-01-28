from fastapi import APIRouter, HTTPException
from datetime import datetime, timezone

from src.api.schema import TaxComputeRequest, TaxComputeResponse
from src.models.taxModels import (
    UserProfile,
    IncomeDetails,
    DeductionDetails,
    TaxComputationInput
)
from src.validation.validator import validate_input, ValidationError
from src.computation.computeTax import compute_tax

router = APIRouter(prefix="/api/v1/tax", tags=["Tax"])

@router.post("/compute", response_model=TaxComputeResponse)
def compute_tax_api(request: TaxComputeRequest):

    if request.regime not in ["old", "new"]:
        raise HTTPException(status_code=400, detail="Invalid tax regime")

    try:
        user_profile = UserProfile(
            financial_year=request.financial_year,
            age=request.user_profile.age,
            is_resident=request.user_profile.is_resident,
            employment_type=request.user_profile.employment_type
        )

        income_details = IncomeDetails(
            gross_salary=request.income_details.gross_salary
        )

        deduction_details = DeductionDetails(
            sec_80c=request.deduction_details.sec_80c,
            sec_80d=request.deduction_details.sec_80d,
            standard_deduction_applicable=request.deduction_details.standard_deduction_applicable
        )

        data = TaxComputationInput(
            user_profile=user_profile,
            income_details=income_details,
            deduction_details=deduction_details
        )

        validate_input(data)

        result = compute_tax(data, request.regime)

        return {
            "status": "success",
            "data": {
                "taxable_income": result.taxable_income,
                "slab_wise_tax": result.slab_wise_tax,
                "cess": result.cess,
                "total_tax": result.total_tax
            },
            "meta": {
                "regime": request.regime,
                "financial_year": request.financial_year,
                "computed_at": datetime.now(timezone.utc).isoformat()
            }
        }

    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception:
        raise HTTPException(status_code=500, detail="Tax computation failed")
