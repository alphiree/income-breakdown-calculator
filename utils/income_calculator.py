"""
This module provides a class for calculating income and contributions for employees in the
Philippines.
"""

import os
import sys
from datetime import datetime

import pandas as pd

sys.path.insert(1, "/".join(os.path.realpath("").split("/")))
from config.contributions import PAGIBIG, PHILHEALTH, SSS  # pylint: disable=C0413
from config.ph_tax import DATA  # pylint: disable=C0413


class IncomeCalculator:
    """
    A class that calculates income and contributions for employees in the Philippines.
    """

    def __init__(
        self,
        basic_salary: float,
        allowance: float,
        night_differential: float | None = None,
    ):
        """
        Initialize the IncomeCalculator class.

        Args:
            basic_salary (float): The basic salary of the employee.
            allowance (float): The allowance of the employee.
            night_differential (float, optional): The night differential of the employee. Defaults
            to None.
        """
        self.salary = basic_salary
        self.allowance = allowance
        self.night_differential = night_differential
        self.sss = SSS[str(datetime.today().year)]
        self.philhealth = PHILHEALTH[str(datetime.today().year)]
        self.pagibig = PAGIBIG[str(datetime.today().year)]

    def salary_credit(self, ref: dict) -> float:
        """
        Calculate the salary credit based on the given reference.

        Args:
            ref (dict): The reference for salary credit calculation.

        Returns:
            float: The calculated salary credit.
        """
        if self.salary < ref["Minimum"]:
            return ref["Minimum"]
        if self.salary > ref["Maximum"]:
            return ref["Maximum"]

        return self.salary

    def compute_contributions(self) -> dict:
        """
        Compute the contributions for SSS, PhilHealth, and PAGIBIG.

        Returns:
            dict: A dictionary containing the computed contributions.
        """
        contributions_provider = {
            "SSS": self.sss,
            "PhilHealth": self.philhealth,
            "PAGIBIG": self.pagibig,
        }

        for name, values in contributions_provider.items():
            if isinstance(values, list):
                for ranges in values:
                    if (
                        ranges["Salary Range"][0]
                        <= self.salary
                        <= ranges["Salary Range"][1]
                    ):
                        values = ranges

            if name == "PAGIBIG" and self.salary >= values["Maximum"]:
                contributions_provider[name] = {
                    "Total Contribution": round(
                        self.salary_credit(ref=values)
                        * values["Contribution Rate"]
                        * 2,
                        2,
                    ),
                    "Employer Contribution": round(
                        self.salary_credit(ref=values) * values["Employer"] * 2, 2
                    ),
                    "Employee Contribution": round(
                        self.salary_credit(ref=values) * values["Employee"] * 2, 2
                    ),
                }
            else:
                contributions_provider[name] = {
                    "Total Contribution": round(
                        self.salary_credit(ref=values) * values["Contribution Rate"], 2
                    ),
                    "Employer Contribution": round(
                        self.salary_credit(ref=values) * values["Employer"], 2
                    ),
                    "Employee Contribution": round(
                        self.salary_credit(ref=values) * values["Employee"], 2
                    ),
                }
        return contributions_provider

    @staticmethod
    def compute_tax(taxable_income: float) -> tuple[float, float]:
        """
        Compute the tax based on the given taxable income.

        Args:
            taxable_income (float): The taxable income.

        Returns:
            float: The computed tax.
        """
        data = pd.DataFrame(DATA)
        income = taxable_income * 12
        for index, row in data.iterrows():
            if row["Minimum"] <= income <= row["Maximum"]:
                if index == 0:
                    return 0.0, 0.0
                excess = data.at[index - 1, "Maximum"]
                yearly_tax = round(
                    ((income - excess) * row["Excess"]) + row["Additional"], 2
                )
                monthly_tax = round(yearly_tax / 12, 2)
        return yearly_tax, monthly_tax

    def compute_netincome(self) -> dict:
        """
        Compute the net income based on the given inputs.

        Returns:
            dict: A dictionary containing the computed net income and other details.
        """
        contributions = self.compute_contributions()
        total_employee_contribition = sum(
            [value["Employee Contribution"] for value in contributions.values()]
        )

        night_differential = (
            self.night_differential if self.night_differential is not None else 0
        )

        taxable_income = self.salary - total_employee_contribition + night_differential

        yearly_tax, monthly_tax = self.compute_tax(taxable_income)

        monthly_netincome = round(
            (
                self.salary
                + self.allowance
                + night_differential
                - monthly_tax
                - total_employee_contribition
            ),
            2,
        )

        netincome_smmary = {
            "Basic Salary": float(self.salary),
            "Allowance": float(self.allowance),
            "SSS Contribution": contributions["SSS"]["Employee Contribution"],
            "PhilHealth Contribution": contributions["PhilHealth"][
                "Employee Contribution"
            ],
            "PAGIBIG Contribution": contributions["PAGIBIG"]["Employee Contribution"],
            "Total Employee Contribution": total_employee_contribition,
            "Taxable Income": taxable_income,
            "Monthly Tax": monthly_tax,
            "Yearly Tax": yearly_tax,
            "Monthly Net Income": monthly_netincome,
            "Monthly Gross Income": self.salary + self.allowance + night_differential,
        }

        if self.night_differential is not None:
            netincome_smmary["Night Differential"] = night_differential

        return netincome_smmary
