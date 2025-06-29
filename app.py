import streamlit as st
import pandas as pd
import numpy as np
import numpy_financial as npf
 
# Page configuration
st.set_page_config(
    page_title="Interest Rate Calculator",
    page_icon="💰",
    layout="wide",
)
 
# Utility functions
@st.cache_data
def generate_amortization(principal, annual_rate, tenure_months):
    monthly_rate = annual_rate / 12
    emi = npf.pmt(monthly_rate, tenure_months, -principal)
 
    balance = principal
    schedule = []
    for i in range(1, tenure_months + 1):
        interest = balance * monthly_rate
        principal_payment = emi - interest
        balance -= principal_payment
        schedule.append({
            "Month": i,
            "EMI": emi,
            "Principal": principal_payment,
            "Interest": interest,
            "Balance Principal": max(balance, 0),
        })
 
    df = pd.DataFrame(schedule)
    flat_rate = 12 * df["Interest"].sum() / (principal * tenure_months)
    return df, emi, flat_rate
 
# Sidebar inputs
st.sidebar.header("🔧 Input Parameters")
interest_rate = st.sidebar.number_input("Reducing Rate (%)", min_value=0.0, value=16.0, step=0.1)
principal = st.sidebar.number_input("Loan Amount (Principal)", min_value=0.0, value=125000.0, step=1000.0, format="%.2f")
tenure_years = st.sidebar.slider(
    "Loan Tenure (Years)",
    min_value=1,
    max_value=5,
    step=1,
    value=2
)
tenure = tenure_years * 12  # Convert to months

 
# Main title
st.title("💰 Interest Rate Calculator")
 
if st.sidebar.button("Calculate"):
    rate = interest_rate / 100
    schedule_df, emi, flat_rate = generate_amortization(principal, rate, tenure)
 
    # Display key metrics
    st.subheader("📈 Results")
    col1, col2, col3 = st.columns(3)
    col1.metric("Reducing Rate", f"{interest_rate:.2f}%")
    col2.metric("Flat Rate", f"{flat_rate * 100:.2f}%")
    col3.metric("EMI", f"₹{emi:,.2f}")
 
    # Charts
    with st.expander("📊 Amortization Charts", expanded=True):
        ch1, ch2 = st.columns(2)
        ch1.line_chart(schedule_df.set_index('Month')[['Balance Principal']])
        ch2.line_chart(schedule_df.set_index('Month')[['Interest', 'Principal']])
 
    # Schedule table and download
    with st.expander("🧾 Amortization Schedule", expanded=False):
        st.dataframe(
            schedule_df.style.format({
                'EMI': '₹{:.2f}',
                'Principal': '₹{:.2f}',
                'Interest': '₹{:.2f}',
                'Balance Principal': '₹{:.2f}'
            }), use_container_width=True
        )
        csv = schedule_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Schedule as CSV",
            data=csv,
            file_name='amortization_schedule.csv',
            mime='text/csv'
        )
else:
    st.info("Use the sidebar to enter loan details and click Calculate.")
