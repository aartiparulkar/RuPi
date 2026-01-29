from enum import Enum

class AgentState(Enum):
    COLLECTING_INPUTS = "collecting_inputs"
    INPUT_COMPLETE = "input_complete"
    ELIGIBILITY_CHECK = "eligibility_check"
    TAX_COMPUTED = "tax_computed"
    REGIME_DECIDED = "regime_decided"      
    EXPLANATION_READY = "explanation_ready"
    COMPLETED = "completed"
    ERROR = "error"
