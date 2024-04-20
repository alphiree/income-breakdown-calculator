"""
This file contains the tax data for the Philippines.

The `DATA` dictionary stores the tax brackets and rates for different income ranges.
It consists of the following keys:
- "Minimum": A list of minimum income thresholds for each tax bracket.
- "Maximum": A list of maximum income thresholds for each tax bracket.
- "Excess": A list of tax rates for the excess income in each tax bracket.
- "Additional": A list of additional taxes for each tax bracket.

The tax brackets are as follows:
- Bracket 1: Income between 0 and 250,000 PHP
- Bracket 2: Income between 250,001 and 400,000 PHP
- Bracket 3: Income between 400,001 and 800,000 PHP
- Bracket 4: Income between 800,001 and 2,000,000 PHP
- Bracket 5: Income between 2,000,001 and 8,000,000 PHP
- Bracket 6: Income above 8,000,000 PHP

Note: The "Maximum" value for the last bracket is set to infinity (float("inf")).
"""

DATA = {
    "Minimum": [0, 250001, 400001, 800001, 2000001, 8000001],
    "Maximum": [250000, 400000, 800000, 2000000, 8000000, float("inf")],
    "Excess": [0, 0.15, 0.2, 0.25, 0.3, 0.35],
    "Additional": [0, 0, 22500, 102500, 402500, 2202500],
}
