import streamlit as st
import pandas as pd
import plotly_xtras as px

st.set_page_config(layout="wide")

st.title("Business Performance Demo: Dumbbell Chart")

st.markdown("""
This demo illustrates how a dumbbell chart can be used to compare performance metrics between two periods.
In this business scenario, we are comparing customer satisfaction scores (out of 10) for different aspects of our service between Q1 and Q2 of this year.
This type of chart is excellent for highlighting changes and identifying areas of improvement or decline.
""")

# --- Fictional Business Data ---
satisfaction_data = {
    'Feature': [
        "Ease of Use",
        "Product Features",
        "Customer Support",
        "Pricing",
        "Overall Value"
    ],
    'Q1 Score': [7.5, 8.0, 6.5, 7.0, 7.2],
    'Q2 Score': [8.5, 8.2, 7.8, 7.5, 8.1]
}
satisfaction_df = pd.DataFrame(satisfaction_data)

# --- Create the Dumbbell Chart ---
st.header("Customer Satisfaction: Q1 vs Q2 2023")

fig = px.dumbbell(
    df=satisfaction_df,
    category_col='Feature',
    value1_col='Q1 Score',
    value2_col='Q2 Score',
    label1='Q1 2023',
    label2='Q2 2023',
    title="Change in Customer Satisfaction Scores"
)

# Customize layout for better readability
fig.update_layout(
    xaxis_title="Satisfaction Score (out of 10)",
    yaxis_title="Service Feature",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.subheader("Data Table")
st.dataframe(satisfaction_df, use_container_width=True)


