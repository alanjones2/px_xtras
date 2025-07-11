import streamlit as st
import pandas as pd
import plotly_xtras as ph

st.title("Waffle Chart Tests")

# --- Test with DataFrame ---
st.header("Waffle Chart from DataFrame")
waffle_data = {'Others': 49, 'Reform': 5, 'LD': 72, 'Conservative': 121, 'Labour': 403}
waffle_df = pd.DataFrame(list(waffle_data.items()), columns=['Party', 'Seats'])

fig1 = ph.waffle(
    df=waffle_df,
    category_col='Party',
    value_col='Seats',
    title="UK MPs by Party",
    local_colors=['#808080', '#12B6CF', '#FDBB30', '#0087dc', '#d50000']
)
st.plotly_chart(fig1)

# --- Test with Custom Grid Width ---
st.header("Waffle Chart with Custom Grid Width")
fig2 = ph.waffle(
    df=waffle_df,
    category_col='Party',
    value_col='Seats',
    title="UK MPs by Party (Custom Grid)",
    grid_width=20,
    fig_height=500,
    local_colors=['#808080', '#12B6CF', '#FDBB30', '#0087dc', '#d50000']
)
st.plotly_chart(fig2)