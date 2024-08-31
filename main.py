"""
This file contains a Streamlit application for computing the net income breakdown for Filipinos.

The application allows users to input their monthly basic income, non-taxable allowance, and choose
whether to include night differential rate. It then calculates the net income and provides a
breakdown of the income components including basic salary, allowance, night differential, gross
income, employee contributions, monthly tax, and monthly net income.
"""

from datetime import datetime

import streamlit as st

from config.site_config import div_configs
from utils.income_calculator import IncomeCalculator
from utils.utils import SessionState

## ======================================================================================= ##
## SITE TITLE
st.set_page_config(
    initial_sidebar_state="collapsed",
    page_title="PH Income Breakdown Calculator",
    page_icon=":dollar:",
)

## ======================================================================================= ##
## SITE CONFIGURATION

st.markdown(div_configs["hide_github_icon"], unsafe_allow_html=True)
st.markdown(div_configs["hide_streamlit_style"], unsafe_allow_html=True)


## ======================================================================================= ##
## SITE CONTENTS


title = st.container()
features = st.expander("Features", expanded=False)
contents = st.container()
results = st.container()

button = SessionState(key="button_clicked", default_state=False)

with title:
    st.title(":dollar: PH Income Breakdown Calculator")
    st.subheader("A simple calculator for computing Net Income for Filipinos")
    st.markdown(
        f"""
        > UPDATED AS OF {datetime.today().strftime('%B')} {datetime.today().year}
        """
    )


with contents:
    basic_salary = st.number_input(
        label="Monthly Basic Income (PHP)",
        min_value=1000,
        max_value=None,
        value="min",
        step=1000,
    )
    allowance = st.number_input(
        label="Non-Taxable Allowance (De-minimis) (PHP)",
        min_value=0,
        max_value=None,
        value="min",
        step=1000,
    )
    nightdf_allow = st.checkbox("Night Differential Rate?")
    if nightdf_allow:
        night_differential_rate = st.number_input(
            label="Night Differential Rate (%)",
            min_value=0,
            max_value=100,
            value="min",
            step=1,
        )
        night_differential_value = basic_salary * (night_differential_rate / 100)
        income_calculator = IncomeCalculator(
            basic_salary=basic_salary,
            allowance=allowance,
            night_differential=night_differential_value,
        )

    else:
        income_calculator = IncomeCalculator(
            basic_salary=basic_salary, allowance=allowance
        )

    income_details = income_calculator.compute_netincome()

    submit_button = st.button(
        label="Calculate", type="primary", on_click=button.sessionstate_true
    )


with results:
    if submit_button or button.check_sessionstate():
        st.subheader("NET INCOME")
        st.markdown(
            f"""
        ### Monthly Net Income: ₱ {income_details['Monthly Net Income']:,}
        """
        )

        monthly_tab, daily_tab, hourly_tab, yearly_tab = st.tabs(
            ["Monthly", "Daily", "Hourly", "Yearly"]
        )

        with monthly_tab:
            with st.expander("Income Breakdown", expanded=False):

                st.markdown(
                    f"""
                #### Breakdown:
                | Details | Amount |
                |---------|--------|
                | Basic Salary | ₱ {income_details['Basic Salary']:,} |
                | Allowance | ₱ {income_details['Allowance']:,} |
                | Night Differential | ₱ {float(income_details.get('Night Differential', 0)):,} |
                | <span style="color:green"> **Gross Income** </span> | <span style="color:green"> **₱ {income_details['Monthly Gross Income']:,}** </span>|
                | SSS Contribution | ₱ {income_details['SSS Contribution']:,} |
                | PhilHealth Contribution | ₱ {income_details['PhilHealth Contribution']:,} |
                | PAGIBIG Contribution | ₱ {income_details['PAGIBIG Contribution']:,} |
                | <span style="color:red"> **Total Employee Contribution** </span> | <span style="color:red"> **₱ {income_details['Total Employee Contribution']:,}** </span> |
                | <span style="color:red"> **Monthly Tax** </span> | <span style="color:red"> **₱ {income_details['Monthly Tax']:,}** </span> |
                | <span style="color:green"> **Monthly Net Income** </span> | <span style="color:green"> **₱ {income_details['Monthly Net Income']:,}** </span> |
                """,
                    unsafe_allow_html=True,
                )

        with daily_tab:
            st.markdown(
                f"""
            #### Daily Rate (Gross): ₱ {round((income_details['Monthly Gross Income']*12/261),2):,}
            """
            )
            st.markdown(
                f"""
            #### Daily Rate (Net): ₱ {round((income_details['Monthly Net Income']*12/261),2):,}
            """
            )
            st.divider()
            st.markdown(
                """
            #### 🎉 Additional Holiday Rates:
            """
            )

            if income_details["Monthly Tax"] == 0:
                daily_basic = round((income_details["Basic Salary"] * 12 / 261), 2)
            else:
                daily_basic = (
                    round((income_details["Basic Salary"] * 12 / 261), 2) * 0.8
                )

            st.markdown(
                f"""
            ##### Regular Holiday: + ₱{round(daily_basic,2):,} per day
            """
            )
            st.markdown(
                f"""
            ##### Special Non-Working Holiday: + ₱ {round(daily_basic * .3,2):,} per day
            """
            )

        with hourly_tab:
            working_hours = st.number_input(
                label="How many hours do you work in a day?",
                min_value=1,
                max_value=24,
                value=8,
                step=1,
            )
            st.markdown(
                f"""
            #### Hourly Rate (Gross): ₱ {round((income_details['Monthly Gross Income']*12/261/working_hours),2):,}
            """
            )
            st.markdown(
                f"""
            #### Hourly Rate (Net): ₱ {round((income_details['Monthly Net Income']*12/261/working_hours),2):,}
            """
            )

        with yearly_tab:
            st.markdown(
                f"""
            #### Yearly Rate (Gross): ₱ {round((income_details['Monthly Gross Income']*12),2):,}
            """
            )
            st.markdown(
                f"""
            #### Yearly Rate (Net): ₱ {round(((income_details['Monthly Gross Income']*12) - (income_details["Yearly Tax"]) - (income_details["Total Employee Contribution"]*12)),2):,}
            """
            )
