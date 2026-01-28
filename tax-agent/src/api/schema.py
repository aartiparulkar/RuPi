from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

class UserProfileSchema(BaseModel):
    age: int = Field(..., ge=0)
    is_resident: bool
    employment_type: str

class IncomeDetailsSchema(BaseModel):
    gross_salary: float = Field(..., ge=0)

class DeductionDetailsSchema(BaseModel):
    sec_80c: float = Field(0.0, ge=0)
    sec_80d: float = Field(0.0, ge=0)
    standard_deduction_applicable: bool = True

class TaxComputeRequest(BaseModel):
    financial_year: str
    regime: str
    user_profile: UserProfileSchema
    income_details: IncomeDetailsSchema
    deduction_details: DeductionDetailsSchema

class SlabTaxSchema(BaseModel):
    slab_range: str
    tax_amount: float

class TaxComputeResponseData(BaseModel):
    taxable_income: float
    slab_wise_tax: List[SlabTaxSchema]
    cess: float
    total_tax: float

class TaxComputeResponse(BaseModel):
    status: str
    data: TaxComputeResponseData
    meta: dict
