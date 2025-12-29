# Layout and Containers - Deep Dive

## Overview

Streamlit provides powerful layout tools to organize your app's UI. This guide covers sidebars, columns, containers, tabs, and best practices for responsive design.

## Sidebar

### st.sidebar

The sidebar is a persistent panel on the left side of your app:

```python
import streamlit as st

# Sidebar widgets
st.sidebar.title("Navigation")
st.sidebar.button("Home")
st.sidebar.button("About")
st.sidebar.button("Contact")

# Main content
st.title("Main Content")
st.write("This is the main area")
```

### Sidebar Best Practices

```python
import streamlit as st

# Navigation in sidebar
st.sidebar.title("Menu")
page = st.sidebar.radio("Navigate", ["Home", "Dashboard", "Settings"])

# Filters in sidebar
st.sidebar.header("Filters")
category = st.sidebar.selectbox("Category", ["All", "A", "B", "C"])
date_range = st.sidebar.date_input("Date Range")

# Settings in sidebar
st.sidebar.header("Settings")
theme = st.sidebar.selectbox("Theme", ["Light", "Dark"])
language = st.sidebar.selectbox("Language", ["English", "Spanish"])

# Main content area
st.title(f"Page: {page}")
st.write(f"Category: {category}")
```

### Sidebar Configuration

```python
import streamlit as st

# Configure sidebar state
st.set_page_config(initial_sidebar_state="expanded")  # or "collapsed"

# Sidebar with custom width (via config.toml)
# .streamlit/config.toml:
# [ui]
# hideSidebarNav = false
```

## Columns

### st.columns()

Create multiple columns for side-by-side layout:

```python
import streamlit as st

# Basic columns
col1, col2 = st.columns(2)

with col1:
    st.write("Column 1")
    st.button("Button 1")

with col2:
    st.write("Column 2")
    st.button("Button 2")
```

### Column Widths

```python
import streamlit as st

# Custom widths
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    st.write("Narrow column")

with col2:
    st.write("Wide column")

with col3:
    st.write("Narrow column")
```

### Column Examples

```python
import streamlit as st

# Metrics in columns
col1, col2, col3, col4 = st.columns(4)

col1.metric("Temperature", "70°F", "1.2°F")
col2.metric("Wind", "9 mph", "-8%")
col3.metric("Humidity", "86%", "4%")
col4.metric("Pressure", "30.15 in", "0.05 in")

# Form inputs in columns
col1, col2 = st.columns(2)

with col1:
    name = st.text_input("First Name")

with col2:
    surname = st.text_input("Last Name")
```

## Containers

### st.container()

Container for grouping elements without visual separation:

```python
import streamlit as st

# Basic container
with st.container():
    st.write("Content in container")
    st.button("Button in container")

# Container with border (using markdown)
with st.container():
    st.markdown("""
    <div style='border: 1px solid #ccc; padding: 10px; border-radius: 5px;'>
        <h3>Container Content</h3>
    </div>
    """, unsafe_allow_html=True)
```

### st.expander()

Collapsible container:

```python
import streamlit as st

# Basic expander
with st.expander("Click to expand"):
    st.write("Hidden content")
    st.image("image.jpg")

# Expanded by default
with st.expander("Always expanded", expanded=True):
    st.write("This is expanded by default")

# Multiple expanders
with st.expander("Section 1"):
    st.write("Content 1")

with st.expander("Section 2"):
    st.write("Content 2")
```

### Practical Container Examples

```python
import streamlit as st

# Settings panel
with st.expander("⚙️ Settings"):
    theme = st.selectbox("Theme", ["Light", "Dark"])
    language = st.selectbox("Language", ["EN", "ES", "FR"])
    notifications = st.checkbox("Enable notifications")

# Help section
with st.expander("❓ Help"):
    st.markdown("""
    ### How to use this app:
    1. Enter your data
    2. Click process
    3. View results
    """)

# Advanced options
with st.expander("🔧 Advanced Options", expanded=False):
    st.slider("Threshold", 0, 100, 50)
    st.checkbox("Enable debug mode")
```

## Tabs

### st.tabs()

Create tabbed interface:

```python
import streamlit as st

# Basic tabs
tab1, tab2, tab3 = st.tabs(["Tab 1", "Tab 2", "Tab 3"])

with tab1:
    st.write("Content of tab 1")

with tab2:
    st.write("Content of tab 2")

with tab3:
    st.write("Content of tab 3")
```

### Tab Examples

```python
import streamlit as st
import pandas as pd

# Dashboard with tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "📈 Charts", "📋 Data", "⚙️ Settings"])

with tab1:
    st.header("Overview")
    st.metric("Total Users", "1,234", "12%")
    st.metric("Revenue", "$50K", "5%")

with tab2:
    st.header("Charts")
    df = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})
    st.line_chart(df)

with tab3:
    st.header("Data")
    st.dataframe(df)

with tab4:
    st.header("Settings")
    st.selectbox("Theme", ["Light", "Dark"])
```

## Empty Placeholders

### st.empty()

Placeholder for dynamic content:

```python
import streamlit as st
import time

# Placeholder for updating content
placeholder = st.empty()

for i in range(10):
    placeholder.write(f"Count: {i}")
    time.sleep(0.5)

# Final message
placeholder.success("Done!")
```

### Practical Empty Examples

```python
import streamlit as st

# Loading indicator
loading = st.empty()

if st.button("Process"):
    loading.info("Processing...")
    # Do processing
    time.sleep(2)
    loading.success("Complete!")

# Dynamic content
content = st.empty()

if st.button("Toggle"):
    if "show" not in st.session_state:
        st.session_state.show = False
    st.session_state.show = not st.session_state.show
    
    if st.session_state.show:
        content.write("Content is visible!")
    else:
        content.write("Content is hidden.")
```

## Layout Best Practices

### 1. Responsive Design

```python
import streamlit as st

# Use columns for responsive layout
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Metric 1", "100")

with col2:
    st.metric("Metric 2", "200")

with col3:
    st.metric("Metric 3", "300")

# Use use_container_width for charts
df = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})
st.line_chart(df, use_container_width=True)
```

### 2. Organizing Complex Layouts

```python
import streamlit as st

# Header
st.title("Dashboard")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Page", ["Home", "Analytics", "Settings"])

# Main content area
if page == "Home":
    # Use columns for metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Users", "1K")
    col2.metric("Revenue", "$10K")
    col3.metric("Growth", "5%")
    
    # Use tabs for different views
    tab1, tab2 = st.tabs(["Chart", "Table"])
    with tab1:
        st.line_chart(data)
    with tab2:
        st.dataframe(data)
```

### 3. Nested Layouts

```python
import streamlit as st

# Main columns
col1, col2 = st.columns([2, 1])

with col1:
    st.header("Main Content")
    
    # Nested tabs
    tab1, tab2 = st.tabs(["View 1", "View 2"])
    with tab1:
        st.write("Content 1")
    with tab2:
        st.write("Content 2")

with col2:
    st.header("Sidebar")
    
    # Nested expander
    with st.expander("Filters"):
        st.checkbox("Filter 1")
        st.checkbox("Filter 2")
```

## Practical Examples

### Example 1: Dashboard Layout

```python
import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# Sidebar
st.sidebar.title("Dashboard Controls")
date_range = st.sidebar.date_input("Date Range")
category = st.sidebar.multiselect("Categories", ["A", "B", "C"])

# Main area
st.title("Sales Dashboard")

# Metrics row
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Sales", "$100K", "10%")
col2.metric("Orders", "1,234", "5%")
col3.metric("Customers", "567", "8%")
col4.metric("Avg Order", "$81", "2%")

# Charts and data tabs
tab1, tab2, tab3 = st.tabs(["📈 Charts", "📊 Data", "🔍 Analysis"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Sales Over Time")
        st.line_chart(data)
    with col2:
        st.subheader("By Category")
        st.bar_chart(data)

with tab2:
    st.dataframe(data)

with tab3:
    with st.expander("Detailed Analysis"):
        st.write("Analysis content")
```

### Example 2: Form Layout

```python
import streamlit as st

st.title("Registration Form")

# Personal info in columns
col1, col2 = st.columns(2)
with col1:
    first_name = st.text_input("First Name")
    email = st.text_input("Email")

with col2:
    last_name = st.text_input("Last Name")
    phone = st.text_input("Phone")

# Address
st.subheader("Address")
address = st.text_area("Street Address")

col1, col2, col3 = st.columns(3)
with col1:
    city = st.text_input("City")
with col2:
    state = st.selectbox("State", ["CA", "NY", "TX"])
with col3:
    zip_code = st.text_input("ZIP Code")

# Preferences in expander
with st.expander("Preferences (Optional)"):
    newsletter = st.checkbox("Subscribe to newsletter")
    notifications = st.checkbox("Enable notifications")

if st.button("Submit"):
    st.success("Registration successful!")
```

## Common Pitfalls

### Pitfall 1: Forgetting `with` Statement

**Problem:**
```python
col1, col2 = st.columns(2)
col1.write("Content")  # Wrong! Not using 'with'
```

**Solution:**
```python
col1, col2 = st.columns(2)
with col1:
    st.write("Content")  # Correct!
```

### Pitfall 2: Nested Containers Incorrectly

**Problem:**
```python
with st.container():
    col1, col2 = st.columns(2)
col1.write("Content")  # Wrong! Outside context
```

**Solution:**
```python
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        st.write("Content")  # Correct!
```

## Next Steps

Now that you can organize layouts:

- [Data Visualization](./08-data-visualization.md) - Create charts and graphs
- [Session State](./09-session-state.md) - Manage app state

## References

- [Layout API](https://docs.streamlit.io/develop/api-reference/layout)
- [Sidebar API](https://docs.streamlit.io/develop/api-reference/layout/st.sidebar)
- [Columns API](https://docs.streamlit.io/develop/api-reference/layout/st.columns)

