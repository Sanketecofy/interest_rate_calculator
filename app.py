import streamlit as st
import pandas as pd
import numpy as np
import numpy_financial as npf

def generate_amortization(principal, annual_rate, tenure_months):
    monthly_rate = annual_rate / 12
    emi = npf.pmt(monthly_rate, tenure_months, -principal)

    balance = principal
    interest_list = []
    principal_list = []
    aum_list = []

    for _ in range(tenure_months):
        interest = balance * monthly_rate
        principal_payment = emi - interest
        balance -= principal_payment

        interest_list.append(interest)
        principal_list.append(principal_payment)
        aum_list.append(balance + principal_payment / 2)  # Mid-month approximation

    return {
        "emi": emi,
        "monthly_interest": interest_list,
        "monthly_principal": principal_list,
        "aum_list": aum_list,
        "avg_aum": np.mean(aum_list),
        "flat_rate": 12*sum(interest_list) / (principal*tenure_months)
    }

def cal_interest_rate(rate, input_vars):
    amort = generate_amortization(input_vars["principal"], rate, input_vars["tenure"])
    flat_rate = amort['flat_rate']
    return rate, flat_rate, amort

st.title("💰 Interest Rate Calculator")

# User inputs
interest_rate = st.number_input("Reducing rate (%)", value=16)
principal = st.number_input("Loan Amount (Principal)", value=125000)
tenure = st.number_input("Loan Tenure (Months)", value=24)
# Example usage

constants = {
    "final_rate": interest_rate/100
    }

if st.button("Calculate Interest Rate"):
    input_vars = {
        "principal": principal,
        "tenure": tenure
    }

    reducing_rate, flat_rate, details = cal_interest_rate(constants['final_rate'], input_vars)

    st.subheader("📈 Output")
    st.write(f"Reducing Interest Rate: **{reducing_rate * 100:.2f}%**")
    st.write(f"Flat Interest Rate : **{flat_rate * 100:.2f}%**")
    st.write(f"EMI : **{details['emi']:.4f}**")
    # st.subheader("🧾 Calculation Details")
    # st.json(details)
