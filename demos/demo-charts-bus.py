import streamlit as st
import pandas as pd
from plotly_xtras import waterfall, waffle, dumbbell, line_range, plotly_chart

st.set_page_config(page_title="Custom Business Charts", layout="wide")
st.title("📊 Business Chart Gallery with Custom Plotly Extensions")

st.markdown("This app demonstrates custom chart types for business analytics using Plotly and Streamlit.")

# Section: Waterfall Chart
st.header("💧 Waterfall Chart – Profit Breakdown")
wf_data = pd.DataFrame({
    "Category": ["Revenue", "COGS", "Operating Expenses", "Taxes", "Net Profit"],
    "Value": [100000, -40000, -20000, -10000, 30000]
})
fig_wf = waterfall(df=wf_data, category_col="Category", value_col="Value", title="Company Profit Waterfall")
st.components.v1.html(plotly_chart(fig_wf), height=500)

# Section: Waffle Chart
st.header("🧇 Waffle Chart – Customer Segments")
waffle_data = {
    "Enterprise": 40,
    "SMB": 35,
    "Freelancers": 15,
    "Non-profit": 10
}
fig_waffle = waffle(data=waffle_data, title="Customer Base Composition")
st.components.v1.html(plotly_chart(fig_waffle), height=500)

# Section: Dumbbell Chart
st.header("🏋️ Dumbbell Chart – Sales Comparison Q1 vs Q2")
db_data = pd.DataFrame({
    "Region": ["North", "South", "East", "West"],
    "Q1 Sales": [50000, 42000, 37000, 60000],
    "Q2 Sales": [55000, 46000, 39000, 65000]
})
fig_db = dumbbell(df=db_data, category_col="Region", value1_col="Q1 Sales", value2_col="Q2 Sales",
                  label1="Q1", label2="Q2", title="Regional Sales Performance")
st.components.v1.html(plotly_chart(fig_db), height=500)

# Section: Line Range Chart
st.header("📏 Line Range Chart – Salary Range by Role")
lr_data = pd.DataFrame({
    "Role": ["Data Scientist", "Product Manager", "Engineer", "Designer"],
    "Min Salary": [90000, 95000, 85000, 70000],
    "Max Salary": [140000, 150000, 130000, 100000]
})
fig_lr = line_range(df=lr_data, category_col="Role", value1_col="Min Salary", value2_col="Max Salary",
                    title="Salary Ranges by Role")
st.components.v1.html(plotly_chart(fig_lr), height=500)

st.markdown("---")
st.caption("All charts generated using custom Plotly helper functions from `plotly_xtras.py`.")
