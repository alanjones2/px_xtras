import streamlit as st
import pandas as pd
from plotly_xtras import waterfall, waffle, dumbbell, line_range, plotly_chart

st.set_page_config(page_title="Social Science Charts", layout="wide")
st.title("🔍 Social Science Visualizations with Custom Charts")

st.markdown("This app demonstrates social science data visualizations using custom Plotly chart extensions.")

# Section: Waterfall Chart
st.header("💧 Waterfall Chart – Household Budget Analysis")
wf_data = pd.DataFrame({
    "Category": ["Income", "Housing", "Food", "Transport", "Healthcare", "Remaining Budget"],
    "Value": [3000, -900, -500, -300, -400, 900]
})
fig_wf = waterfall(df=wf_data, category_col="Category", value_col="Value", title="Monthly Household Budget Flow")
st.components.v1.html(plotly_chart(fig_wf), height=500)

# Section: Waffle Chart
st.header("🧇 Waffle Chart – Education Levels in Population")
waffle_data = {
    "No High School": 10,
    "High School Graduate": 30,
    "Some College": 25,
    "Bachelor's Degree": 20,
    "Graduate Degree": 15
}
fig_waffle = waffle(data=waffle_data, title="Education Attainment in Population")
st.components.v1.html(plotly_chart(fig_waffle), height=500)

# Section: Dumbbell Chart
st.header("🏋️ Dumbbell Chart – Gender Pay Gap by Sector")
db_data = pd.DataFrame({
    "Sector": ["Healthcare", "Education", "Engineering", "Finance", "Government"],
    "Men's Salary": [80000, 60000, 95000, 120000, 70000],
    "Women's Salary": [72000, 58000, 85000, 105000, 69000]
})
fig_db = dumbbell(df=db_data, category_col="Sector", value1_col="Women's Salary", value2_col="Men's Salary",
                  label1="Women", label2="Men", title="Gender Pay Gap by Sector")
st.components.v1.html(plotly_chart(fig_db), height=500)

# Section: Line Range Chart
st.header("📏 Line Range Chart – Income Inequality by Region")
lr_data = pd.DataFrame({
    "Region": ["Urban", "Suburban", "Rural"],
    "Bottom 10%": [12000, 15000, 10000],
    "Top 10%": [150000, 120000, 80000]
})
fig_lr = line_range(df=lr_data, category_col="Region", value1_col="Bottom 10%", value2_col="Top 10%",
                    title="Income Range by Region")
st.components.v1.html(plotly_chart(fig_lr), height=500)

st.markdown("---")
st.caption("Charts are based on fictional but realistic social science data. Powered by `plotly_xtras.py`.")
