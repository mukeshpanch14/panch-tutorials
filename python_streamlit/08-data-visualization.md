# Data Visualization - Deep Dive

## Overview

Streamlit provides excellent support for data visualization through native charts and integration with popular plotting libraries. This guide covers all visualization options from simple charts to complex custom visualizations.

## Native Charts

### st.line_chart()

Line chart for time series data:

```python
import streamlit as st
import pandas as pd
import numpy as np

# Basic line chart
df = pd.DataFrame({
    "x": [1, 2, 3, 4, 5],
    "y": [10, 20, 30, 40, 50]
})
st.line_chart(df)

# Multiple series
df = pd.DataFrame({
    "x": [1, 2, 3, 4, 5],
    "Series A": [10, 20, 30, 40, 50],
    "Series B": [15, 25, 35, 45, 55]
})
st.line_chart(df, x="x", y=["Series A", "Series B"])

# With options
st.line_chart(df, use_container_width=True, height=400)
```

### st.bar_chart()

Bar chart for categorical data:

```python
import streamlit as st
import pandas as pd

# Basic bar chart
df = pd.DataFrame({
    "Category": ["A", "B", "C", "D"],
    "Value": [10, 20, 30, 40]
})
st.bar_chart(df.set_index("Category"))

# Horizontal bars
st.bar_chart(df.set_index("Category"), use_container_width=True)
```

### st.area_chart()

Area chart (filled line chart):

```python
import streamlit as st
import pandas as pd

df = pd.DataFrame({
    "x": [1, 2, 3, 4, 5],
    "Series A": [10, 20, 30, 40, 50],
    "Series B": [15, 25, 35, 45, 55]
})
st.area_chart(df, x="x", y=["Series A", "Series B"])
```

## Plotly Integration

### st.plotly_chart()

Plotly provides highly interactive charts:

```python
import streamlit as st
import plotly.express as px
import pandas as pd

# Scatter plot
df = pd.DataFrame({
    "x": [1, 2, 3, 4, 5],
    "y": [10, 20, 30, 40, 50],
    "size": [10, 20, 30, 40, 50],
    "color": ["A", "B", "A", "B", "A"]
})

fig = px.scatter(df, x="x", y="y", size="size", color="color")
st.plotly_chart(fig)

# Line chart
fig = px.line(df, x="x", y="y", color="color")
st.plotly_chart(fig, use_container_width=True)

# Bar chart
fig = px.bar(df, x="x", y="y", color="color")
st.plotly_chart(fig)

# 3D scatter
fig = px.scatter_3d(df, x="x", y="y", z="size", color="color")
st.plotly_chart(fig)
```

### Advanced Plotly Examples

```python
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Subplots
from plotly.subplots import make_subplots

fig = make_subplots(rows=2, cols=2)

fig.add_trace(go.Scatter(x=[1, 2, 3], y=[4, 5, 6]), row=1, col=1)
fig.add_trace(go.Bar(x=[1, 2, 3], y=[4, 5, 6]), row=1, col=2)
fig.add_trace(go.Scatter(x=[1, 2, 3], y=[4, 5, 6]), row=2, col=1)
fig.add_trace(go.Bar(x=[1, 2, 3], y=[4, 5, 6]), row=2, col=2)

st.plotly_chart(fig, use_container_width=True)

# Custom layout
fig = px.scatter(df, x="x", y="y")
fig.update_layout(
    title="Custom Chart",
    xaxis_title="X Axis",
    yaxis_title="Y Axis",
    template="plotly_dark"
)
st.plotly_chart(fig)
```

## Matplotlib

### st.pyplot()

Display Matplotlib figures:

```python
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Basic matplotlib
fig, ax = plt.subplots()
x = np.linspace(0, 10, 100)
ax.plot(x, np.sin(x))
st.pyplot(fig)

# Multiple subplots
fig, axes = plt.subplots(2, 2, figsize=(10, 8))
axes[0, 0].plot([1, 2, 3], [1, 2, 3])
axes[0, 1].bar([1, 2, 3], [1, 2, 3])
axes[1, 0].scatter([1, 2, 3], [1, 2, 3])
axes[1, 1].hist([1, 2, 3, 4, 5])
st.pyplot(fig)
```

### Matplotlib Best Practices

```python
import streamlit as st
import matplotlib.pyplot as plt

# Clear figure to avoid memory issues
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot([1, 2, 3], [4, 5, 6])
ax.set_xlabel("X Label")
ax.set_ylabel("Y Label")
ax.set_title("Chart Title")
st.pyplot(fig)
plt.close(fig)  # Important: close figure
```

## Altair

### st.altair_chart()

Declarative statistical visualization:

```python
import streamlit as st
import altair as alt
import pandas as pd

# Basic Altair chart
df = pd.DataFrame({
    "x": [1, 2, 3, 4, 5],
    "y": [10, 20, 30, 40, 50]
})

chart = alt.Chart(df).mark_line().encode(
    x="x",
    y="y"
)
st.altair_chart(chart, use_container_width=True)

# Interactive chart
chart = alt.Chart(df).mark_circle().encode(
    x="x",
    y="y",
    size="y",
    color="x",
    tooltip=["x", "y"]
).interactive()

st.altair_chart(chart)
```

## Vega-Lite

### st.vega_lite_chart()

Vega-Lite JSON specification:

```python
import streamlit as st
import pandas as pd

df = pd.DataFrame({
    "x": [1, 2, 3, 4, 5],
    "y": [10, 20, 30, 40, 50]
})

spec = {
    "mark": "line",
    "encoding": {
        "x": {"field": "x", "type": "quantitative"},
        "y": {"field": "y", "type": "quantitative"}
    }
}

st.vega_lite_chart(df, spec, use_container_width=True)
```

## Bokeh

### st.bokeh_chart()

Bokeh interactive plots:

```python
import streamlit as st
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
import pandas as pd

# Create Bokeh figure
p = figure(width=600, height=400)
p.line([1, 2, 3, 4, 5], [6, 7, 2, 4, 5], line_width=2)

st.bokeh_chart(p, use_container_width=True)

# With data source
df = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})
source = ColumnDataSource(df)
p = figure()
p.circle("x", "y", source=source, size=10)
st.bokeh_chart(p)
```

## Graphviz

### st.graphviz_chart()

Graph visualization:

```python
import streamlit as st

# Directed graph
graph = """
digraph {
    A -> B
    B -> C
    C -> D
    D -> A
}
"""
st.graphviz_chart(graph)

# Complex graph
graph = """
graph {
    rankdir=LR;
    A [label="Start"]
    B [label="Process"]
    C [label="End"]
    A -> B -> C
}
"""
st.graphviz_chart(graph)
```

## Map Visualization

### st.map()

Display maps with markers:

```python
import streamlit as st
import pandas as pd

# Basic map
df = pd.DataFrame({
    "lat": [37.7749, 34.0522, 40.7128],
    "lon": [-122.4194, -118.2437, -74.0060],
    "name": ["San Francisco", "Los Angeles", "New York"]
})

st.map(df)

# With size
df["size"] = [100, 200, 150]
st.map(df)

# With color
df["color"] = ["red", "blue", "green"]
st.map(df)
```

### Advanced Map Examples

```python
import streamlit as st
import pandas as pd

# Map with tooltips
df = pd.DataFrame({
    "lat": [37.7749, 34.0522],
    "lon": [-122.4194, -118.2437],
    "name": ["SF", "LA"]
})

st.map(df, zoom=5)

# Multiple layers
st.map(df, use_container_width=True)
```

## Custom Visualizations

### Creating Custom Charts

```python
import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# Custom gauge chart
fig = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = 75,
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {'text': "Speed"},
    gauge = {
        'axis': {'range': [None, 100]},
        'bar': {'color': "darkblue"},
        'steps': [
            {'range': [0, 50], 'color': "lightgray"},
            {'range': [50, 100], 'color': "gray"}
        ],
        'threshold': {
            'line': {'color': "red", 'width': 4},
            'thickness': 0.75,
            'value': 90
        }
    }
))

st.plotly_chart(fig)
```

### HTML/CSS Visualizations

```python
import streamlit as st

# Custom HTML visualization
st.markdown("""
<div style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            padding: 20px; border-radius: 10px; color: white;">
    <h2>Custom Visualization</h2>
    <p>This is a custom HTML/CSS visualization</p>
</div>
""", unsafe_allow_html=True)
```

## Practical Examples

### Example 1: Dashboard with Multiple Charts

```python
import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Sales Dashboard")

# Load data
df = pd.read_csv("sales.csv")

# Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Sales", "$100K")
col2.metric("Orders", "1,234")
col3.metric("Customers", "567")
col4.metric("Growth", "5%")

# Charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("Sales Over Time")
    fig = px.line(df, x="date", y="sales")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Sales by Category")
    fig = px.bar(df, x="category", y="sales")
    st.plotly_chart(fig, use_container_width=True)

# Full width chart
st.subheader("Geographic Distribution")
st.map(df[["lat", "lon"]])
```

### Example 2: Interactive Data Explorer

```python
import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Data Explorer")

# Upload data
uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    # Chart type selector
    chart_type = st.selectbox("Chart Type", ["Line", "Bar", "Scatter"])
    
    # Column selectors
    x_col = st.selectbox("X Axis", df.columns)
    y_col = st.selectbox("Y Axis", df.columns)
    
    # Create chart
    if chart_type == "Line":
        fig = px.line(df, x=x_col, y=y_col)
    elif chart_type == "Bar":
        fig = px.bar(df, x=x_col, y=y_col)
    else:
        fig = px.scatter(df, x=x_col, y=y_col)
    
    st.plotly_chart(fig, use_container_width=True)
```

## Best Practices

1. **Use appropriate chart types**: Choose the right chart for your data
2. **Make charts interactive**: Use Plotly for better interactivity
3. **Responsive design**: Use `use_container_width=True`
4. **Clear labels**: Always label axes and add titles
5. **Color accessibility**: Use colorblind-friendly palettes

## Common Pitfalls

### Pitfall 1: Not Closing Matplotlib Figures

**Problem:**
```python
fig, ax = plt.subplots()
ax.plot([1, 2, 3], [4, 5, 6])
st.pyplot(fig)  # Memory leak!
```

**Solution:**
```python
fig, ax = plt.subplots()
ax.plot([1, 2, 3], [4, 5, 6])
st.pyplot(fig)
plt.close(fig)  # Important!
```

### Pitfall 2: Wrong Data Format

**Problem:**
```python
st.line_chart([1, 2, 3, 4, 5])  # Error!
```

**Solution:**
```python
df = pd.DataFrame({"y": [1, 2, 3, 4, 5]})
st.line_chart(df)  # Correct!
```

## Next Steps

Now that you can create visualizations:

- [Session State](./09-session-state.md) - Manage interactive state
- [Working with Data](./11-working-with-data.md) - Load and process data

## References

- [Charts API](https://docs.streamlit.io/develop/api-reference/charts)
- [Plotly Documentation](https://plotly.com/python/)
- [Matplotlib Documentation](https://matplotlib.org/)
- [Altair Documentation](https://altair-viz.github.io/)

