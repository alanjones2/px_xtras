import streamlit as st
import pandas as pd
import plotly_xtras as ph

st.title("Waterfall Chart Tests")

# --- Test with DataFrame ---
st.header("Standard Waterfall Chart from DataFrame")
df = pd.DataFrame({
    'Category': ["Year beginning", "Profit1", "Loss1", "Q1", "Profit2", "Loss2", "Q2"],
    'Value': [100, 50, -20, 0, 40, -10, 0]
})

measure = ['relative', 'relative', 'relative', 'total', 'relative', 'relative', 'total']

fig1 = ph.waterfall(
    df=df,
    category_col='Category',
    value_col='Value',
    title="Profit/Loss",
    measure=measure,
    color='blue'
)
st.plotly_chart(fig1)

# --- Test with Custom Colors ---
st.header("Waterfall Chart with Custom Colors")
fig2 = ph.waterfall(
    df=df,
    category_col='Category',
    value_col='Value',
    title="Profit/Loss (Custom Colors)",
    measure=measure,
    icolor='green',
    dcolor='red',
    tcolor='black',
    ccolor='gray'
)
st.plotly_chart(fig2)

# --- Test with Absolute Measure and Annotations ---
st.header("Waterfall Chart with Absolute Measure and Annotations")
annotations = ['start', 'up', 'down', 'subtotal', 'up', 'down', 'end']
absolute_measure = ['absolute', 'relative', 'relative', 'total', 'relative', 'relative', 'total']

fig3 = ph.waterfall(
    df=df,
    category_col='Category',
    value_col='Value',
    title="Profit/Loss (Absolute Measure)",
    measure=absolute_measure,
    annotation=annotations,
    icolor='#00FF00',  # Green
    dcolor='#FF0000',  # Red
    tcolor='#000000',  # Black
    ccolor='#808080'   # Gray
)
st.plotly_chart(fig3)