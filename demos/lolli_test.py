import plotly.graph_objects as go
import streamlit as st
import pandas as pd
import plotly_extras_0_2 as pxs

def draw_lollipop_chart(categories, values, title="Lollipop Chart", stick_color='gray', marker_color='blue'):
    """
    Draws a lollipop chart using Plotly.

    Parameters:
        categories (list): List of category labels (x-axis).
        values (list): List of numerical values (y-axis).
        title (str): Title of the chart.
    """
    if len(categories) != len(values):
        raise ValueError("Length of categories and values must match.")

    fig = go.Figure()

    # Add vertical lines (sticks of the lollipops)
    for i, (x, y) in enumerate(zip(categories, values)):
        fig.add_trace(go.Scatter(
            x=[x, x],
            y=[0, y],
            mode='lines',
            line=dict(color=stick_color, width=2),
            showlegend=False
        ))

    # Add markers (lollipop heads)
    fig.add_trace(go.Scatter(
        x=categories,
        y=values,
        mode='markers',
        marker=dict(color=marker_color, size=10),
        name='Value'
    ))

    fig.update_layout(
        title=title,
        xaxis_title="Category",
        yaxis_title="Value",
        template="plotly_white",
        showlegend=False,
    )

    return fig



categories = ['A', 'B', 'C', 'D']
values = [10, 25, 15, 30]
fig = draw_lollipop_chart(categories, values, title="Sample Lollipop Chart")

st.plotly_chart(fig)

