import streamlit as st
import pandas as pd
import numpy as np
import plotly_xtras as ph

st.title("Extra Plotly Charts")

# --- Waterfall Chart ---
st.header("Waterfall Chart")
waterfall_df = pd.DataFrame({
    'Category': ["Year beginning", "Profit1", "Loss1", "Q1", "Profit2", "Loss2", "Q2"],
    'Value': [100, 50, -20, 130, 40, -10, 160]
})
measure = ['relative','relative', 'relative','total', 'relative','relative','total']
fig_waterfall = ph.waterfall(df=waterfall_df, 
                             category_col='Category', 
                             value_col='Value', 
                             title="Profit/Loss",
                             measure=measure,
                             color='blue')
st.plotly_chart(fig_waterfall)

st.write("---")

# --- Waffle Chart ---
st.header("Waffle Chart")
waffle_data = {'Others': 54, 'LD': 72, 'Conservative': 121, 'Labour': 403}
waffle_df = pd.DataFrame(list(waffle_data.items()), columns=['Party', 'Seats'])

fig_waffle = ph.waffle(df=waffle_df, 
                       category_col='Party', 
                       value_col='Seats',
                       title='Waffle Chart of MPs',
                       local_colors=['black', 'yellow', 'blue', 'red'])
st.plotly_chart(fig_waffle)

st.write("---")

# --- Dumbbell Chart ---
st.header("Dumbbell Chart")
dumbbell_df = pd.DataFrame({
    'Country': ['USA', 'Canada', 'UK', 'Germany', 'France'],
    '2020': [10, 12, 9, 14, 11],
    '2021': [12, 15, 11, 15, 12]
})

fig_dumbbell = ph.dumbbell(df=dumbbell_df, 
                           category_col='Country', 
                           value1_col='2020', 
                           value2_col='2021',
                           label1='2020',
                           label2='2021',
                           title='Dumbbell Chart Example')
st.plotly_chart(fig_dumbbell)

# --- Vertical Dumbbell Chart ---
st.header("Vertical Dumbbell Chart")
fig_dumbbell_v = ph.dumbbell(df=dumbbell_df, 
                             category_col='Country', 
                             value1_col='2020', 
                             value2_col='2021',
                             label1='2020',
                             label2='2021',
                             title='Vertical Dumbbell Chart Example',
                             orientation='v')
st.plotly_chart(fig_dumbbell_v)

fig_range = ph.line_range(df=dumbbell_df, 
                           category_col='Country', 
                           value1_col='2020', 
                           value2_col='2021',
                           label1='2020',
                           label2='2021',
                           title='Range Chart Example')
st.plotly_chart(fig_range)