from src.agent.states import AgentState
from src.models.taxModels import (
    UserProfile, IncomeDetails, DeductionDetails, TaxComputationInput
)
from src.validation.validator import validate_input, ValidationError
from src.computation.computeTax import compute_tax
from src.llm.base_llm import BaseLLM

class TaxAgentOrchestrator:
    def __init__(self):
        self.state = AgentState.COLLECTING_INPUTS
        self.data = {
            "gross_salary": None,
            "sec_80c": None,
            "sec_80d": None
        }

    def update_from_user(self, user_message: dict):
        """
        user_message is structured input from UI or LLM extraction
        """
        for key in self.data:
            if key in user_message and user_message[key] is not None:
                self.data[key] = user_message[key]

        if all(value is not None for value in self.data.values()):
            self.state = AgentState.INPUT_COMPLETE

    def build_tax_input(self) -> TaxComputationInput:
        return TaxComputationInput(
            user_profile=UserProfile(
                financial_year="FY 2024-25",
                age=30,
                is_resident=True,
                employment_type="salaried"
            ),
            income_details=IncomeDetails(
                gross_salary=self.data["gross_salary"]
            ),
            deduction_details=DeductionDetails(
                sec_80c=self.data["sec_80c"],
                sec_80d=self.data["sec_80d"],
                standard_deduction_applicable=True
            )
        )

    def execute(self):
        if self.state != AgentState.INPUT_COMPLETE:
            return {"status": "awaiting_input", "missing": self.get_missing_fields()}

        try:
            tax_input = self.build_tax_input()
            validate_input(tax_input)
        except ValidationError as e:
            self.state = AgentState.ERROR
            return {"status": "error", "message": str(e)}

        # Deterministic computation
        old_result = compute_tax(tax_input, "old")
        new_result = compute_tax(tax_input, "new")

        self.state = AgentState.COMPLETED

        return {
            "status": "completed",
            "old_regime": old_result,
            "new_regime": new_result
        }

    def get_missing_fields(self):
        return [k for k, v in self.data.items() if v is None]
