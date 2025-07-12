import streamlit as st
import pandas as pd
from plotly_extras_0_2 import lollipop_chart

st.set_page_config(page_title="Lollipop Chart Demo", layout="wide")
st.title("🍭 Lollipop Charts – Business & Social Science Examples")

st.markdown("""
Lollipop charts offer a clean way to show quantitative comparisons. Below are two use cases:
- One in a **business setting**
- Another in a **social science context**
""")

# --- Business Use Case: Revenue per Product ---
st.header("📈 Business Example – Revenue per Product")

products = ["Product A", "Product B", "Product C", "Product D"]
revenue = [120000, 95000, 78000, 143000]  # in USD

fig_business = lollipop_chart(
    categories=products,
    values=revenue,
    title="Revenue by Product",
    stick_color="gray",
    marker_color="green"
)

st.plotly_chart(fig_business, use_container_width=True)


# --- Social Science Use Case: Literacy Rate by Region ---
st.header("📊 Social Science Example – Literacy Rate by Region")

regions = ["North", "South", "East", "West"]
literacy_rates = [91.2, 85.6, 88.9, 83.4]  # in percentage

fig_social = lollipop_chart(
    categories=regions,
    values=literacy_rates,
    title="Literacy Rate by Region (%)",
    stick_color="lightgray",
    marker_color="blue"
)

st.plotly_chart(fig_social, use_container_width=True)

st.markdown("---")
st.caption("Lollipop charts rendered using a custom Plotly helper function.")
