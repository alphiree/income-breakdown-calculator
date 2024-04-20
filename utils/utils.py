from typing import Union

import streamlit as st


def monthlyincome_form(key: str) -> Union[float, float, bool]:

    with st.form(key=key):

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

        submit_button = st.form_submit_button(label="Calculate")

    return basic_salary, allowance, submit_button
