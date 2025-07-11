import streamlit as st
import pandas as pd
import plotly_xtras as ph

st.title("Dumbbell Chart Tests")

# --- Test with DataFrame ---
st.header("Standard Dumbbell Chart from DataFrame")
df = pd.DataFrame({
    'Product': ['Product A', 'Product B', 'Product C', 'Product D'],
    'Before': [120, 90, 150, 110],
    'After': [135, 95, 160, 120]
})

fig1 = ph.dumbbell(
    df=df,
    category_col='Product',
    value1_col='Before',
    value2_col='After',
    label1="2022",
    label2="2023",
    title="Sales Comparison (Horizontal)"
)
st.plotly_chart(fig1)

# --- Test Vertical Orientation ---
st.header("Vertical Dumbbell Chart")
fig2 = ph.dumbbell(
    df=df,
    category_col='Product',
    value1_col='Before',
    value2_col='After',
    label1="2022",
    label2="2023",
    title="Sales Comparison (Vertical)",
    orientation='v'
)
st.plotly_chart(fig2)

# --- Test Customization Parameters ---
st.header("Customized Dumbbell Chart")
fig3 = ph.dumbbell(
    df=df,
    category_col='Product',
    value1_col='Before',
    value2_col='After',
    label1="2022",
    label2="2023",
    title="Customized Sales Comparison",
    marker_color1='#FF0000',  # Red
    marker_color2='#0000FF',  # Blue
    line_color='#00FF00',    # Green
    marker_size=15,
    line_width=4
)
st.plotly_chart(fig3)