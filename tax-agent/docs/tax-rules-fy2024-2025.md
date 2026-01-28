## Income Tax Computation Engine — FY 2024-25 (AY 2025-26)

### Overview

This module implements Indian Income Tax calculations for salaried, resident individuals for Financial Year 2024-25.

The engine provides:

* Accurate tax calculations for **Old Regime** and **New Regime**
* Support for standard deductions and key sections (80C, 80D)
* Health & Education cess calculation (4%)
* Input validation with clear error reporting
* A reproducible, stateless, deterministic API

---

### Supported Features

| Feature            | Description                                            | Notes                                   |
| ------------------ | ------------------------------------------------------ | --------------------------------------- |
| Financial Year     | FY 2024-25 (AY 2025-26)                                | Only this FY supported in MVP           |
| Residential Status | Resident Individual                                    | Non-resident not supported              |
| Employment Type    | Salaried only                                          | Others excluded                         |
| Income Types       | Salary income                                          | No capital gains, business income, etc. |
| Tax Regimes        | Old & New                                              | Both calculated & compared              |
| Standard Deduction | ₹50,000                                                | Applies to both regimes                 |
| Deductions         | Section 80C (max ₹1,50,000), Section 80D (max ₹25,000) | Senior citizen limits excluded          |

---

### Input Data Model

```python
{
    "financial_year": "2024-25",
    "gross_salary": float,
    "deductions": {
        "80C": float,  # ≤ 1,50,000
        "80D": float   # ≤ 25,000
    }
}
```

---

### Validation Rules

* `gross_salary` must be ≥ 0
* `deductions["80C"]` must be between 0 and ₹1,50,000
* `deductions["80D"]` must be between 0 and ₹25,000
* `financial_year` must be "2024-25"

If any validation fails, an error is returned and no computation is performed.

---

### Tax Slabs

**Old Regime Slabs (Resident < 60 years):**

| Income Range (₹)     | Tax Rate (%) |
| -------------------- | ------------ |
| 0 – 2,50,000         | 0            |
| 2,50,001 – 5,00,000  | 5            |
| 5,00,001 – 10,00,000 | 20           |
| Above 10,00,000      | 30           |

**New Regime Slabs:**

| Income Range (₹)      | Tax Rate (%) |
| --------------------- | ------------ |
| 0 – 3,00,000          | 0            |
| 3,00,001 – 6,00,000   | 5            |
| 6,00,001 – 9,00,000   | 10           |
| 9,00,001 – 12,00,000  | 15           |
| 12,00,001 – 15,00,000 | 20           |
| Above 15,00,000       | 30           |

---

### Calculation Details

* **Taxable Income** = `gross_salary` – `standard_deduction` – sum of allowed deductions
* Apply slabs to taxable income to calculate base tax
* Apply Health & Education Cess @ 4% on tax amount
* Total tax = base tax + cess

---

### Outputs

```python
{
    "taxable_income": float,
    "slab_wise_tax": [  # List of dicts per slab
        {"slab": "0-2.5L", "tax": float},
        {"slab": "2.5-5L", "tax": float},
        ...
    ],
    "cess": float,
    "total_tax": float
}
```

---

### Known Limitations

* No support for senior citizens’ special slabs
* No surcharge calculations
* No rebate under section 87A (can be added later)
* No HRA or other complex exemptions
* Only resident salaried individuals supported

---

### Usage Notes

* Input data must be validated before invoking this engine
* This engine **does not** file ITR or interact with any external systems
* Must be integrated with an agent that collects and verifies inputs
