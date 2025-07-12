import streamlit as st
import pandas as pd
from plotly_extras_0_2 import waterfall, waffle, dumbbell, line_range, plotly_chart, lollipop_chart


st.set_page_config(page_title="Climate Research Demos", layout="wide")
st.title("🌍 Climate Research Visualization Demos")

st.markdown("This app demonstrates how custom chart types can be used in climate and environmental research.")

# --- Waterfall Chart: Greenhouse Gas Emissions ---
st.header("💧 Net Greenhouse Gas Emissions – Waterfall Chart")

wf_data = pd.DataFrame({
    "Category": [
        "Gross Emissions", "Renewables Offset", "Forest Sequestration",
        "Carbon Capture", "Net Emissions"
    ],
    "Value": [1000, -200, -150, -100, 550]  # in million tons CO₂e
})

fig_wf = waterfall(df=wf_data, category_col="Category", value_col="Value", title="GHG Emission Flow (MtCO₂e)")
st.components.v1.html(plotly_chart(fig_wf), height=500)


# --- Waffle Chart: Sources of CO₂ Emissions ---
st.header("🧇 CO₂ Emission Sources – Waffle Chart")

waffle_data = {
    "Transportation": 28,
    "Industry": 24,
    "Electricity": 30,
    "Agriculture": 10,
    "Residential": 8
}

fig_waffle = waffle(data=waffle_data, title="CO₂ Emission by Sector (%)")
st.components.v1.html(plotly_chart(fig_waffle), height=500)


# --- Dumbbell Chart: CO₂ per Capita Change (2000 vs 2020) ---
st.header("🏋️ CO₂ Emissions per Capita – Dumbbell Chart")

db_data = pd.DataFrame({
    "Country": ["USA", "China", "Germany", "India", "Brazil"],
    "2000": [20.5, 3.2, 10.3, 1.1, 1.7],
    "2020": [15.0, 7.1, 8.9, 1.9, 2.4]
})

fig_db = dumbbell(df=db_data, category_col="Country", value1_col="2000", value2_col="2020",
                  label1="2000", label2="2020", title="CO₂ Emissions per Capita (tons)")
st.components.v1.html(plotly_chart(fig_db), height=500)


# --- Line Range Chart: Regional Temperature Ranges ---
st.header("📏 Temperature Ranges by Region – Line Range Chart")

lr_data = pd.DataFrame({
    "Region": ["Arctic", "Tropics", "Temperate", "Desert"],
    "Winter Low": [-40, 18, -5, 5],
    "Summer High": [5, 32, 30, 48]
})

fig_lr = line_range(df=lr_data, category_col="Region", value1_col="Winter Low", value2_col="Summer High",
                    title="Temperature Ranges by Region (°C)")
st.components.v1.html(plotly_chart(fig_lr), height=500)


# --- Lollipop Chart: Average Annual Temperature by City ---
st.header("🍭 Average Annual Temperature – Lollipop Chart")

cities = ["Oslo", "Cairo", "Mumbai", "London", "Sydney"]
avg_temps = [5.1, 24.6, 27.2, 11.3, 18.5]

fig_lolli = lollipop_chart(
    categories=cities,
    values=avg_temps,
    title="Average Annual Temperature by City (°C)",
    stick_color="darkgray",
    marker_color="tomato"
)

st.plotly_chart(fig_lolli, use_container_width=True)

st.markdown("---")
st.caption("Climate visualizations powered by custom Plotly extensions.")
