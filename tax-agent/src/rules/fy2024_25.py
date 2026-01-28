from typing import List, Tuple

# Define slab as tuple (upper_limit, tax_rate)
# upper_limit in INR, tax_rate in decimal fraction

OLD_REGIME_SLABS: List[Tuple[float, float]] = [
    (250000, 0.0),    # Up to 2.5L no tax
    (500000, 0.05),   # 2.5L to 5L 5%
    (1000000, 0.20),  # 5L to 10L 20%
    (float('inf'), 0.30)  # Above 10L 30%
]

NEW_REGIME_SLABS: List[Tuple[float, float]] = [
    (300000, 0.0),    # Up to 3L no tax
    (600000, 0.05),   # 3L to 6L 5%
    (900000, 0.10),   # 6L to 9L 10%
    (1200000, 0.15),  # 9L to 12L 15%
    (1500000, 0.20),  # 12L to 15L 20%
    (float('inf'), 0.30)  # Above 15L 30%
]

# Deduction limits
DEDuction_LIMITS = {
    "sec_80c": 150000,    # ₹1.5L
    "sec_80d": 25000,     # ₹25,000 (simplified, ignoring senior citizens for MVP)
}

# Standard deduction (₹50,000 fixed for both regimes for FY24-25)
STANDARD_DEDUCTION = 50000

# Cess rate (4%)
CESS_RATE = 0.04
