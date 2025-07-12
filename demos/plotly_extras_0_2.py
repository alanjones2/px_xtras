"""
plotly_extras_0_2.py

A library of helper functions for creating advanced visualizations using Plotly.

MIT License

Copyright (c) 2025 Alan Jones

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import plotly.graph_objects as go
import pandas as pd
import numpy as np
import matplotlib.colors as mcolors
import json
import math
from typing import List, Tuple, Dict, Optional


def plotly_chart(fig: go.Figure) -> str:
    """
    Converts a Plotly figure into an embeddable HTML string.

    Args:
        fig (go.Figure): The Plotly figure to convert.

    Returns:
        str: An HTML string containing the Plotly chart.
        
    Use st.component to display the chart in Streamlit, 
    e.g. st.components.v1.html(html_string, height=600)
    """
    return fig.to_html(include_plotlyjs='cdn', full_html=False)


def get_color_gradient(start_color: str, end_color: str, num_colors: int) -> List[str]:
    """
    Generate a list of colors forming a gradient between two colors.

    Args:
        start_color (str): The starting color (name, hex, or RGB tuple).
        end_color (str): The ending color (name, hex, or RGB tuple).
        num_colors (int): The number of discrete colors to generate.

    Returns:
        List[str]: A list of hex color codes forming the gradient.
    """
    start_rgb = mcolors.to_rgb(start_color)
    end_rgb = mcolors.to_rgb(end_color)
    gradient = [
        tuple(start_rgb[i] + (end_rgb[i] - start_rgb[i]) * t for i in range(3))
        for t in [i / (num_colors - 1) for i in range(num_colors)]
    ]
    return ['#%02x%02x%02x' % (int(r * 255), int(g * 255), int(b * 255)) for r, g, b in gradient]


def get_section_bounds(x: float = 1, y: int = 4) -> List[Tuple[float, float]]:
    """
    Returns a list of (start, end) tuples for each of the y sections of a bar of length x.

    Args:
        x (float): Total length of the bar.
        y (int): Number of equal sections.

    Returns:
        List[Tuple[float, float]]: List of (start, end) points for each section.
    """
    section_length = x / y
    return [(i * section_length, (i + 1) * section_length) for i in range(y)]


def find_midpoints(x: int, y: int) -> List[float]:
    """
    Returns a list of midpoints for each of the y sections of a bar of length x.

    Args:
        x (int): Total length of the bar.
        y (int): Number of equal sections.

    Returns:
        List[float]: Midpoints of each section.
    """
    indices = range(1, y + 1)
    return [((2 * i - 1) * x) / (2 * y) for i in indices]


def waterfall(
    df: Optional[pd.DataFrame] = None,
    category_col: Optional[str] = None,
    value_col: Optional[str] = None,
    labels: Optional[List[str]] = None,
    data: Optional[List[float]] = None,
    title: str = "",
    annotation: Optional[List[str]] = None,
    icolor: str = "Green",
    dcolor: str = "Red",
    tcolor: str = "Blue",
    ccolor: str = "Dark Grey",
    color: Optional[str] = None,
    measure: Optional[List[str]] = None
) -> go.Figure:
    """
    Create a waterfall chart using Plotly.

    Args:
        df (pd.DataFrame, optional): DataFrame to extract data from.
        category_col (str, optional): Column name for categories. Defaults to the first column if df is provided.
        value_col (str, optional): Column name for values. Defaults to the second column if df is provided.
        labels (List[str], optional): A list of labels for the data points. Ignored if df is provided.
        data (List[float], optional): A list of numerical values for the data points. Ignored if df is provided.
        title (str, optional): The title of the chart. Defaults to an empty string.
        annotation (List[str], optional): A list of annotations for each data point. Defaults to None.
        icolor (str, optional): Color for increasing values. Defaults to "Green".
        dcolor (str, optional): Color for decreasing values. Defaults to "Red".
        tcolor (str, optional): Color for the total value. Defaults to "Blue".
        ccolor (str, optional): Connector line color. Defaults to 'Dark Grey'.
        color (str, optional): Common color for all elements. Defaults to None.
        measure (List[str], optional): A list specifying whether each data point is 'relative' or 'total'. Defaults to None.

    Returns:
        go.Figure: A Plotly Figure containing the waterfall chart.
    """
    if df is not None:
        if category_col and category_col not in df.columns:
            raise ValueError(f"Column '{category_col}' not found in DataFrame.")
        if value_col and value_col not in df.columns:
            raise ValueError(f"Column '{value_col}' not found in DataFrame.")
        
        category_col = category_col or df.columns[0]
        value_col = value_col or df.columns[1]
        labels = df[category_col].tolist()
        data = df[value_col].tolist()
    elif not (labels and data):
        raise ValueError("Provide either a DataFrame or labels and data lists.")

    if measure is None:
        measure = ['relative'] * (len(labels) - 1) + ['total']
    
    if color:
        icolor = dcolor = tcolor = ccolor = color

    waterfall_params = {
        "orientation": "v",
        "measure": measure,
        "textposition": "outside",
        "y": data,
        "x": labels,
        "connector": {"line": {"color": ccolor}},
        "decreasing": {"marker": {"color": dcolor}},
        "increasing": {"marker": {"color": icolor}},
        "totals": {"marker": {"color": tcolor}}
    }

    if annotation is not None:
        waterfall_params["text"] = annotation
    

    fig = go.Figure(go.Waterfall(**waterfall_params)).update_layout(title=title)

    return fig


def waffle(
    df: Optional[pd.DataFrame] = None,
    category_col: Optional[str] = None,
    value_col: Optional[str] = None,
    data: Optional[Dict[str, int]] = None,
    title: str = "",
    local_colors: Optional[List[str]] = None,
    startcolor: str = 'lightblue',
    endcolor: str = 'darkblue',
    fig_height: int = 600,
    tile_gap: int = 2,
    grid_width: Optional[int] = None,
) -> go.Figure:
    """
    Create a waffle chart using Plotly.

    Args:
        df (pd.DataFrame, optional): DataFrame to extract data from.
        category_col (str, optional): Column name for categories. Defaults to the first column if df is provided.
        value_col (str, optional): Column name for values. Defaults to the second column if df is provided.
        data (Dict[str, int], optional): A dictionary where keys are categories and values are counts. Ignored if df is provided.
        title (str, optional): The title of the chart. Defaults to an empty string.
        local_colors (List[str], optional): A list of colors for the categories. Defaults to a gradient.
        startcolor (str, optional): Starting color for the gradient. Defaults to 'lightblue'.
        endcolor: str = 'darkblue',
        fig_height: int = 600,
        tile_gap: int = 2,
        grid_width: Optional[int] = None,
    Returns:
        go.Figure: A Plotly Figure containing the waffle chart.
    """
    if df is not None:
        if category_col and category_col not in df.columns:
            raise ValueError(f"Column '{category_col}' not found in DataFrame.")
        if value_col and value_col not in df.columns:
            raise ValueError(f"Column '{value_col}' not found in DataFrame.")

        category_col = category_col or df.columns[0]
        value_col = value_col or df.columns[1]
        data = dict(zip(df[category_col], df[value_col]))
    elif data is None:
        raise ValueError("Provide either a DataFrame or a data dictionary.")

    if local_colors is None:
        local_colors = get_color_gradient(startcolor, endcolor, len(data))

    total = sum(data.values())
    number_of_values = len(data.values())
    cat = [idx for idx, count in enumerate(data.values()) for _ in range(count)]

    width = grid_width or math.ceil(math.sqrt(total))
    height = math.ceil(total / width)

    padding_length = width * height - len(cat)
    cat = [np.nan] * padding_length + cat
    b = np.array(cat).reshape((-1, width))

    ranges = get_section_bounds(1, number_of_values)
    colorscale = []
    for i in range(number_of_values):
        colorscale.append([ranges[i][0], local_colors[i % len(local_colors)]])
        colorscale.append([ranges[i][1], local_colors[i % len(local_colors)]])

    fig = go.Figure(data=go.Heatmap(
        z=np.fliplr(b),
        xgap=tile_gap,
        ygap=tile_gap,
        colorbar=dict(
            thickness=20,
            tickvals=find_midpoints(number_of_values - 1, number_of_values),
            ticktext=list(data.keys()),
            outlinecolor='black',
            outlinewidth=0,
        ),
        colorscale=colorscale,
        autocolorscale=False,
    ))

    fig.update_layout(
        title=title,
        xaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
        yaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
        yaxis_scaleanchor="x",
        height=fig_height,
    )
    return fig


def dumbbell(
    df: Optional[pd.DataFrame] = None,
    category_col: Optional[str] = None,
    value1_col: Optional[str] = None,
    value2_col: Optional[str] = None,
    categories: Optional[List[str]] = None,
    values1: Optional[List[float]] = None,
    values2: Optional[List[float]] = None,
    label1: str = "",
    label2: str = "",
    title: str = "Dumbbell Chart",
    orientation: str = 'h',
    marker_color1: str = 'blue',
    marker_color2: str = 'orange',
    line_color: str = 'gray',
    marker_size: int = 10,
    line_width: int = 2
) -> go.Figure:
    """
    Draws a dumbbell chart using Plotly.

    Args:
        df (pd.DataFrame, optional): DataFrame to extract data from.
        category_col (str, optional): Column name for categories. Defaults to the first column if df is provided.
        value1_col (str, optional): Column name for the first value set. Defaults to the second column if df is provided.
        value2_col (str, optional): Column name for the second value set. Defaults to the third column if df is provided.
        categories (List[str], optional): List of category labels. Ignored if df is provided.
        values1 (List[float], optional): First set of numerical values. Ignored if df is provided.
        values2 (List[float], optional): Second set of numerical values. Ignored if df is provided.
        label1 (str, optional): Label for the first value set.
        label2 (str, optional): Label for the second value set.
        title (str, optional): Chart title.
        orientation (str, optional): 'h' for horizontal (default), 'v' for vertical.
        marker_color1 (str, optional): Color for the first set of markers. Defaults to 'blue'.
        marker_color2 (str, optional): Color for the second set of markers. Defaults to 'orange'.
        line_color: str = 'gray',
        marker_size: int = 10,
        line_width: int = 2

    Returns:
        go.Figure: The resulting dumbbell chart.
    """
    if df is not None:
        if category_col and category_col not in df.columns:
            raise ValueError(f"Column '{category_col}' not found in DataFrame.")
        if value1_col and value1_col not in df.columns:
            raise ValueError(f"Column '{value1_col}' not found in DataFrame.")
        if value2_col and value2_col not in df.columns:
            raise ValueError(f"Column '{value2_col}' not found in DataFrame.")

        category_col = category_col or df.columns[0]
        value1_col = value1_col or df.columns[1]
        value2_col = value2_col or df.columns[2]
        categories = df[category_col].tolist()
        values1 = df[value1_col].tolist()
        values2 = df[value2_col].tolist()
    elif not (categories and values1 and values2):
        raise ValueError("Provide either a DataFrame or all three lists: categories, values1, and values2.")

    if not (len(categories) == len(values1) == len(values2)):
        raise ValueError("All input lists must have the same length.")

    fig = go.Figure()
    showlegend = bool(label1 and label2)

    
    x_markers1, y_markers1 = (values1, categories) if orientation == 'h' else (categories, values1)
    x_markers2, y_markers2 = (values2, categories) if orientation == 'h' else (categories, values2)

"""
plotly_extras_0_2.py

A library of helper functions for creating advanced visualizations using Plotly.

MIT License

Copyright (c) 2025 Alan Jones

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import plotly.graph_objects as go
import pandas as pd
import numpy as np
import matplotlib.colors as mcolors
import json
import math
from typing import List, Tuple, Dict, Optional


def plotly_chart(fig: go.Figure) -> str:
    """
    Converts a Plotly figure into an embeddable HTML string.

    Args:
        fig (go.Figure): The Plotly figure to convert.

    Returns:
        str: An HTML string containing the Plotly chart.
        
    Use st.component to display the chart in Streamlit, 
    e.g. st.components.v1.html(html_string, height=600)
    """
    return fig.to_html(include_plotlyjs='cdn', full_html=False)


def get_color_gradient(start_color: str, end_color: str, num_colors: int) -> List[str]:
    """
    Generate a list of colors forming a gradient between two colors.

    Args:
        start_color (str): The starting color (name, hex, or RGB tuple).
        end_color (str): The ending color (name, hex, or RGB tuple).
        num_colors (int): The number of discrete colors to generate.

    Returns:
        List[str]: A list of hex color codes forming the gradient.
    """
    start_rgb = mcolors.to_rgb(start_color)
    end_rgb = mcolors.to_rgb(end_color)
    gradient = [
        tuple(start_rgb[i] + (end_rgb[i] - start_rgb[i]) * t for i in range(3))
        for t in [i / (num_colors - 1) for i in range(num_colors)]
    ]
    return ['#%02x%02x%02x' % (int(r * 255), int(g * 255), int(b * 255)) for r, g, b in gradient]


def get_section_bounds(x: float = 1, y: int = 4) -> List[Tuple[float, float]]:
    """
    Returns a list of (start, end) tuples for each of the y sections of a bar of length x.

    Args:
        x (float): Total length of the bar.
        y (int): Number of equal sections.

    Returns:
        List[Tuple[float, float]]: List of (start, end) points for each section.
    """
    section_length = x / y
    return [(i * section_length, (i + 1) * section_length) for i in range(y)]


def find_midpoints(x: int, y: int) -> List[float]:
    """
    Returns a list of midpoints for each of the y sections of a bar of length x.

    Args:
        x (int): Total length of the bar.
        y (int): Number of equal sections.

    Returns:
        List[float]: Midpoints of each section.
    """
    indices = range(1, y + 1)
    return [((2 * i - 1) * x) / (2 * y) for i in indices]


def waterfall(
    df: Optional[pd.DataFrame] = None,
    category_col: Optional[str] = None,
    value_col: Optional[str] = None,
    labels: Optional[List[str]] = None,
    data: Optional[List[float]] = None,
    title: str = "",
    annotation: Optional[List[str]] = None,
    icolor: str = "Green",
    dcolor: str = "Red",
    tcolor: str = "Blue",
    ccolor: str = "Dark Grey",
    color: Optional[str] = None,
    measure: Optional[List[str]] = None
) -> go.Figure:
    """
    Create a waterfall chart using Plotly.

    Args:
        df (pd.DataFrame, optional): DataFrame to extract data from.
        category_col (str, optional): Column name for categories. Defaults to the first column if df is provided.
        value_col (str, optional): Column name for values. Defaults to the second column if df is provided.
        labels (List[str], optional): A list of labels for the data points. Ignored if df is provided.
        data (List[float], optional): A list of numerical values for the data points. Ignored if df is provided.
        title (str, optional): The title of the chart. Defaults to an empty string.
        annotation (List[str], optional): A list of annotations for each data point. Defaults to None.
        icolor (str, optional): Color for increasing values. Defaults to "Green".
        dcolor (str, optional): Color for decreasing values. Defaults to "Red".
        tcolor (str, optional): Color for the total value. Defaults to "Blue".
        ccolor (str, optional): Connector line color. Defaults to 'Dark Grey'.
        color (str, optional): Common color for all elements. Defaults to None.
        measure (List[str], optional): A list specifying whether each data point is 'relative' or 'total'. Defaults to None.

    Returns:
        go.Figure: A Plotly Figure containing the waterfall chart.
    """
    if df is not None:
        if category_col and category_col not in df.columns:
            raise ValueError(f"Column '{category_col}' not found in DataFrame.")
        if value_col and value_col not in df.columns:
            raise ValueError(f"Column '{value_col}' not found in DataFrame.")
        
        category_col = category_col or df.columns[0]
        value_col = value_col or df.columns[1]
        labels = df[category_col].tolist()
        data = df[value_col].tolist()
    elif not (labels and data):
        raise ValueError("Provide either a DataFrame or labels and data lists.")

    if measure is None:
        measure = ['relative'] * (len(labels) - 1) + ['total']
    
    if color:
        icolor = dcolor = tcolor = ccolor = color

    waterfall_params = {
        "orientation": "v",
        "measure": measure,
        "textposition": "outside",
        "y": data,
        "x": labels,
        "connector": {"line": {"color": ccolor}},
        "decreasing": {"marker": {"color": dcolor}},
        "increasing": {"marker": {"color": icolor}},
        "totals": {"marker": {"color": tcolor}}
    }

    if annotation is not None:
        waterfall_params["text"] = annotation
    

    fig = go.Figure(go.Waterfall(**waterfall_params)).update_layout(title=title)

    return fig


def waffle(
    df: Optional[pd.DataFrame] = None,
    category_col: Optional[str] = None,
    value_col: Optional[str] = None,
    data: Optional[Dict[str, int]] = None,
    title: str = "",
    local_colors: Optional[List[str]] = None,
    startcolor: str = 'lightblue',
    endcolor: str = 'darkblue',
    fig_height: int = 600,
    tile_gap: int = 2,
    grid_width: Optional[int] = None,
) -> go.Figure:
    """
    Create a waffle chart using Plotly.

    Args:
        df (pd.DataFrame, optional): DataFrame to extract data from.
        category_col (str, optional): Column name for categories. Defaults to the first column if df is provided.
        value_col (str, optional): Column name for values. Defaults to the second column if df is provided.
        data (Dict[str, int], optional): A dictionary where keys are categories and values are counts. Ignored if df is provided.
        title (str, optional): The title of the chart. Defaults to an empty string.
        local_colors (List[str], optional): A list of colors for the categories. Defaults to a gradient.
        startcolor (str, optional): Starting color for the gradient. Defaults to 'lightblue'.
        endcolor: str = 'darkblue',
        fig_height: int = 600,
        tile_gap: int = 2,
        grid_width: Optional[int] = None,
    Returns:
        go.Figure: A Plotly Figure containing the waffle chart.
    """
    if df is not None:
        if category_col and category_col not in df.columns:
            raise ValueError(f"Column '{category_col}' not found in DataFrame.")
        if value_col and value_col not in df.columns:
            raise ValueError(f"Column '{value_col}' not found in DataFrame.")

        category_col = category_col or df.columns[0]
        value_col = value_col or df.columns[1]
        data = dict(zip(df[category_col], df[value_col]))
    elif data is None:
        raise ValueError("Provide either a DataFrame or a data dictionary.")

    if local_colors is None:
        local_colors = get_color_gradient(startcolor, endcolor, len(data))

    total = sum(data.values())
    number_of_values = len(data.values())
    cat = [idx for idx, count in enumerate(data.values()) for _ in range(count)]

    width = grid_width or math.ceil(math.sqrt(total))
    height = math.ceil(total / width)

    padding_length = width * height - len(cat)
    cat = [np.nan] * padding_length + cat
    b = np.array(cat).reshape((-1, width))

    ranges = get_section_bounds(1, number_of_values)
    colorscale = []
    for i in range(number_of_values):
        colorscale.append([ranges[i][0], local_colors[i % len(local_colors)]])
        colorscale.append([ranges[i][1], local_colors[i % len(local_colors)]])

    fig = go.Figure(data=go.Heatmap(
        z=np.fliplr(b),
        xgap=tile_gap,
        ygap=tile_gap,
        colorbar=dict(
            thickness=20,
            tickvals=find_midpoints(number_of_values - 1, number_of_values),
            ticktext=list(data.keys()),
            outlinecolor='black',
            outlinewidth=0,
        ),
        colorscale=colorscale,
        autocolorscale=False,
    ))

    fig.update_layout(
        title=title,
        xaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
        yaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
        yaxis_scaleanchor="x",
        height=fig_height,
    )
    return fig


def dumbbell(
    df: Optional[pd.DataFrame] = None,
    category_col: Optional[str] = None,
    value1_col: Optional[str] = None,
    value2_col: Optional[str] = None,
    categories: Optional[List[str]] = None,
    values1: Optional[List[float]] = None,
    values2: Optional[List[float]] = None,
    label1: str = "",
    label2: str = "",
    title: str = "Dumbbell Chart",
    orientation: str = 'h',
    marker_color1: str = 'blue',
    marker_color2: str = 'orange',
    line_color: str = 'gray',
    marker_size: int = 10,
    line_width: int = 2
) -> go.Figure:
    """
    Draws a dumbbell chart using Plotly.

    Args:
        df (pd.DataFrame, optional): DataFrame to extract data from.
        category_col (str, optional): Column name for categories. Defaults to the first column if df is provided.
        value1_col (str, optional): Column name for the first value set. Defaults to the second column if df is provided.
        value2_col (str, optional): Column name for the second value set. Defaults to the third column if df is provided.
        categories (List[str], optional): List of category labels. Ignored if df is provided.
        values1 (List[float], optional): First set of numerical values. Ignored if df is provided.
        values2 (List[float], optional): Second set of numerical values. Ignored if df is provided.
        label1 (str, optional): Label for the first value set.
        label2 (str, optional): Label for the second value set.
        title (str, optional): Chart title.
        orientation (str, optional): 'h' for horizontal (default), 'v' for vertical.
        marker_color1 (str, optional): Color for the first set of markers. Defaults to 'blue'.
        marker_color2 (str, optional): Color for the second set of markers. Defaults to 'orange'.
        line_color: str = 'gray',
        marker_size: int = 10,
        line_width: int = 2

    Returns:
        go.Figure: The resulting dumbbell chart.
    """
    if df is not None:
        if category_col and category_col not in df.columns:
            raise ValueError(f"Column '{category_col}' not found in DataFrame.")
        if value1_col and value1_col not in df.columns:
            raise ValueError(f"Column '{value1_col}' not found in DataFrame.")
        if value2_col and value2_col not in df.columns:
            raise ValueError(f"Column '{value2_col}' not found in DataFrame.")

        category_col = category_col or df.columns[0]
        value1_col = value1_col or df.columns[1]
        value2_col = value2_col or df.columns[2]
        categories = df[category_col].tolist()
        values1 = df[value1_col].tolist()
        values2 = df[value2_col].tolist()
    elif not (categories and values1 and values2):
        raise ValueError("Provide either a DataFrame or all three lists: categories, values1, and values2.")

    if not (len(categories) == len(values1) == len(values2)):
        raise ValueError("All input lists must have the same length.")

    fig = go.Figure()
    showlegend = bool(label1 and label2)

    
    x_markers1, y_markers1 = (values1, categories) if orientation == 'h' else (categories, values1)
    x_markers2, y_markers2 = (values2, categories) if orientation == 'h' else (categories, values2)

    for cat, val1, val2 in zip(categories, values1, values2):
        x_line_vals, y_line_vals = ([val1, val2], [cat, cat]) if orientation == 'h' else ([cat, cat], [val1, val2])
        fig.add_trace(go.Scatter(x=x_line_vals, y=y_line_vals, mode='lines', line=dict(color=line_color, width=line_width), showlegend=False))

    fig.add_trace(go.Scatter(x=x_markers1, y=y_markers1, mode='markers', marker=dict(color=marker_color1, size=marker_size), name=label1, showlegend=showlegend))
    fig.add_trace(go.Scatter(x=x_markers2, y=y_markers2, mode='markers', marker=dict(color=marker_color2, size=marker_size), name=label2, showlegend=showlegend))

    for cat, val1, val2 in zip(categories, values1, values2):
        if orientation == 'h':
            # Determine which value is smaller/larger for correct label placement
            if val1 < val2:
                xanchor1, xshift1 = 'right', -5
                xanchor2, xshift2 = 'left', 5
            else:  # val1 >= val2
                xanchor1, xshift1 = 'left', 5
                xanchor2, xshift2 = 'right', -5

            fig.add_annotation(x=val1, y=cat, text=str(val1), showarrow=False, font=dict(color=marker_color1), xanchor=xanchor1, yanchor='middle', xshift=xshift1)
            fig.add_annotation(x=val2, y=cat, text=str(val2), showarrow=False, font=dict(color=marker_color2), xanchor=xanchor2, yanchor='middle', xshift=xshift2)
        else:
            # Determine which value is smaller/larger for correct label placement
            if val1 < val2:
                yanchor1, yshift1 = 'top', -5
                yanchor2, yshift2 = 'bottom', 5
            else:  # val1 >= val2
                yanchor1, yshift1 = 'bottom', 5
                yanchor2, yshift2 = 'top', -5

            fig.add_annotation(x=cat, y=val1, text=str(val1), showarrow=False, font=dict(color=marker_color1), yanchor=yanchor1, xanchor='center', yshift=yshift1)
            fig.add_annotation(x=cat, y=val2, text=str(val2), showarrow=False, font=dict(color=marker_color2), yanchor=yanchor2, xanchor='center', yshift=yshift2)

    fig.update_layout(
        title=title,
        xaxis_title="Value" if orientation == 'h' else "Category",
        yaxis_title="Category" if orientation == 'h' else "Value",
        template="plotly_white"
    )

    return fig


def line_range(
    df: Optional[pd.DataFrame] = None,
    category_col: Optional[str] = None,
    value1_col: Optional[str] = None,
    value2_col: Optional[str] = None,
    categories: Optional[List[str]] = None,
    values1: Optional[List[float]] = None,
    values2: Optional[List[float]] = None,
    label1: str = "",
    label2: str = "",
    title: str = "Range Chart",
    orientation: str = 'h',
    line_color: str = 'blue',
    line_width: int = 10
) -> go.Figure:
    
    """
    Draws a range chart using Plotly.

    Args:
        df (pd.DataFrame, optional): DataFrame to extract data from.
        category_col (str, optional): Column name for categories. Defaults to the first column if df is provided.
        value1_col (str, optional): Column name for the first value set. Defaults to the second column if df is provided.
        value2_col (str, optional): Column name for the second value set. Defaults to the third column if df is provided.
        categories (List[str], optional): List of category labels. Ignored if df is provided.
        values1 (List[float], optional): First set of numerical values. Ignored if df is provided.
        values2 (List[float], optional): Second set of numerical values. Ignored if df is provided.
        label1 (str, optional): Label for the first value set.
        label2 (str, optional): Label for the second value set.
        title (str, optional): Chart title.
        orientation (str, optional): 'h' for horizontal (default), 'v' for vertical.
        line_color: str = 'gray',
        line_width: int = 2

    Returns:
        go.Figure: The resulting dumbbell chart.
    """
    marker_color1 = line_color
    marker_color2 = line_color
    marker_size = line_width
    label1 = None
    label2 = None
    return dumbbell(df, category_col, value1_col, value2_col, categories, values1, values2, label1, label2, title, orientation, marker_color1, marker_color2, line_color, marker_size, line_width)

def lollipop_chart(categories, values, title="Lollipop Chart", stick_color='gray', marker_color='blue'):
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



def line_range(
    df: Optional[pd.DataFrame] = None,
    category_col: Optional[str] = None,
    value1_col: Optional[str] = None,
    value2_col: Optional[str] = None,
    categories: Optional[List[str]] = None,
    values1: Optional[List[float]] = None,
    values2: Optional[List[float]] = None,
    label1: str = "",
    label2: str = "",
    title: str = "Range Chart",
    orientation: str = 'h',
    line_color: str = 'blue',
    line_width: int = 10
) -> go.Figure:
    
    """
    Draws a range chart using Plotly.

    Args:
        df (pd.DataFrame, optional): DataFrame to extract data from.
        category_col (str, optional): Column name for categories. Defaults to the first column if df is provided.
        value1_col (str, optional): Column name for the first value set. Defaults to the second column if df is provided.
        value2_col (str, optional): Column name for the second value set. Defaults to the third column if df is provided.
        categories (List[str], optional): List of category labels. Ignored if df is provided.
        values1 (List[float], optional): First set of numerical values. Ignored if df is provided.
        values2 (List[float], optional): Second set of numerical values. Ignored if df is provided.
        label1 (str, optional): Label for the first value set.
        label2 (str, optional): Label for the second value set.
        title (str, optional): Chart title.
        orientation (str, optional): 'h' for horizontal (default), 'v' for vertical.
        line_color: str = 'gray',
        line_width: int = 2

    Returns:
        go.Figure: The resulting dumbbell chart.
    """
    marker_color1 = line_color
    marker_color2 = line_color
    marker_size = line_width
    label1 = None
    label2 = None
    return dumbbell(df, category_col, value1_col, value2_col, categories, values1, values2, label1, label2, title, orientation, marker_color1, marker_color2, line_color, marker_size, line_width)

def lollipop_chart(categories, values, title="Lollipop Chart", stick_color='gray', marker_color='blue'):
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