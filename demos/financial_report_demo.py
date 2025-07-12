import streamlit as st
import pandas as pd
import plotly_xtras as px

st.set_page_config(layout="wide")

st.title("Financial Report Demo: Income Statement")

st.markdown("""
This demo showcases the use of a waterfall chart to visualize a company's income statement.
A waterfall chart is an excellent tool for this purpose as it clearly shows how various revenues and costs
contribute to the final net income.
""")

# --- Fictional Financial Data ---
# We use 0 for 'total' measures, as Plotly calculates them automatically.
financial_data = {
    'Category': [
        "Sales Revenue", 
        "Cost of Goods Sold", 
        "Gross Profit", 
        "R&D Expenses", 
        "Sales & Marketing", 
        "General & Admin", 
        "Operating Income", 
        "Interest Expense", 
        "Income Before Tax",
        "Taxes",
        "Net Income"
    ],
    'Value': [
        500000, 
        -200000, 
        0,          # Gross Profit (total)
        -50000, 
        -75000, 
        -40000, 
        0,          # Operating Income (total)
        -15000,
        0,          # Income Before Tax (total)
        -30000,
        0           # Net Income (total)
    ]
}
financial_df = pd.DataFrame(financial_data)

# Define the measure for each category
# 'absolute' for the starting point, 'relative' for changes, 'total' for subtotals/totals.
measure = [
    'absolute', 
    'relative', 
    'total', 
    'relative', 
    'relative', 
    'relative', 
    'total',
    'relative',
    'total',
    'relative',
    'total'
]

# --- Create the Waterfall Chart ---
st.header("Annual Income Statement (in USD)")

fig = px.waterfall(
    df=financial_df,
    category_col='Category',
    value_col='Value',
    title="Company XYZ - Fiscal Year 2023",
    measure=measure,
    icolor="rgba(0, 128, 0, 0.8)",      # Green for increases
    dcolor="rgba(255, 0, 0, 0.8)",      # Red for decreases
    tcolor="rgba(0, 0, 128, 0.8)",      # Blue for totals
    ccolor="rgba(128, 128, 128, 0.5)" # Gray for connectors
)

# Customize layout for better readability
fig.update_layout(
    yaxis_title="Amount (USD)",
    xaxis_title="Financial Category",
    yaxis_tickprefix="$",
    yaxis_tickformat=","
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.subheader("Data Table")
st.dataframe(financial_df, use_container_width=True)