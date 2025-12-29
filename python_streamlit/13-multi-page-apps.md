# Multi-page Apps - Deep Dive

## Overview

Streamlit's multi-page app feature allows you to organize your application into multiple pages with automatic navigation. This guide covers the Pages API, creating multiple pages, navigation, routing, sharing state, and building complex multi-page applications.

## Pages API: st.set_page_config()

### Basic Page Configuration

```python
import streamlit as st

st.set_page_config(
    page_title="My App",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("My App")
```

### Page Configuration Options

```python
import streamlit as st

st.set_page_config(
    page_title="Dashboard",  # Browser tab title
    page_icon="📊",  # Favicon emoji or image
    layout="wide",  # "wide" or "centered"
    initial_sidebar_state="expanded",  # "expanded" or "collapsed"
    menu_items={
        "Get Help": "https://streamlit.io",
        "Report a bug": "https://github.com/streamlit/streamlit",
        "About": "This is a multi-page app"
    }
)
```

## Creating Multiple Pages

### Directory Structure

For multi-page apps, create a `pages/` directory:

```
my_app/
├── app.py              # Main app
└── pages/
    ├── 1_Home.py       # Page 1
    ├── 2_Dashboard.py # Page 2
    └── 3_About.py      # Page 3
```

### Main App (app.py)

```python
import streamlit as st

st.set_page_config(
    page_title="My Multi-page App",
    page_icon="🏠",
    layout="wide"
)

st.title("Welcome to My App")
st.sidebar.success("Select a page above")
```

### Page Files

#### pages/1_Home.py

```python
import streamlit as st

st.set_page_config(
    page_title="Home",
    page_icon="🏠"
)

st.title("Home Page")
st.write("Welcome to the home page!")
```

#### pages/2_Dashboard.py

```python
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Dashboard",
    page_icon="📊"
)

st.title("Dashboard")
df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
st.dataframe(df)
```

#### pages/3_About.py

```python
import streamlit as st

st.set_page_config(
    page_title="About",
    page_icon="ℹ️"
)

st.title("About")
st.write("This is the about page.")
```

## Navigation Between Pages

### Automatic Navigation

Streamlit automatically creates navigation based on page files:

- Files in `pages/` appear in the sidebar
- Page order is determined by filename (alphabetical/numerical)
- Clicking a page navigates to it

### Custom Navigation

```python
import streamlit as st

# In main app or any page
st.sidebar.title("Navigation")

if st.sidebar.button("Home"):
    st.switch_page("pages/1_Home.py")

if st.sidebar.button("Dashboard"):
    st.switch_page("pages/2_Dashboard.py")
```

### Using st.switch_page()

```python
import streamlit as st

page = st.selectbox("Go to page", ["Home", "Dashboard", "About"])

if page == "Home":
    st.switch_page("pages/1_Home.py")
elif page == "Dashboard":
    st.switch_page("pages/2_Dashboard.py")
elif page == "About":
    st.switch_page("pages/3_About.py")
```

## Page Routing and Organization

### Naming Convention

Page files should be named with numbers for ordering:

```
pages/
├── 1_Home.py
├── 2_Dashboard.py
├── 3_Analytics.py
└── 4_Settings.py
```

### Nested Pages (Subdirectories)

You can organize pages in subdirectories:

```
pages/
├── 1_Home.py
├── Analytics/
│   ├── 1_Overview.py
│   └── 2_Reports.py
└── Settings/
    ├── 1_General.py
    └── 2_Advanced.py
```

### Page Icons and Titles

The page title and icon come from `st.set_page_config()`:

```python
# pages/1_Home.py
import streamlit as st

st.set_page_config(
    page_title="Home Page",  # Shown in navigation
    page_icon="🏠"  # Shown in navigation
)
```

## Sharing State Across Pages

### Using Session State

Session state is shared across all pages:

```python
# pages/1_Home.py
import streamlit as st

if "user_data" not in st.session_state:
    st.session_state.user_data = {}

name = st.text_input("Enter your name")
if st.button("Save"):
    st.session_state.user_data["name"] = name
    st.success("Name saved!")
```

```python
# pages/2_Dashboard.py
import streamlit as st

st.title("Dashboard")

# Access shared state
if "user_data" in st.session_state:
    name = st.session_state.user_data.get("name", "Guest")
    st.write(f"Welcome, {name}!")
else:
    st.write("Welcome, Guest!")
```

### Shared Data

```python
# app.py - Initialize shared data
import streamlit as st

if "shared_data" not in st.session_state:
    st.session_state.shared_data = {
        "users": [],
        "settings": {}
    }
```

```python
# pages/1_Users.py - Modify shared data
import streamlit as st

user = st.text_input("Add user")
if st.button("Add"):
    st.session_state.shared_data["users"].append(user)
```

```python
# pages/2_Settings.py - Access shared data
import streamlit as st

st.write(f"Total users: {len(st.session_state.shared_data['users'])}")
```

## Building Complex Multi-page Applications

### Example: Data Analysis App

#### app.py

```python
import streamlit as st

st.set_page_config(
    page_title="Data Analysis App",
    page_icon="📊",
    layout="wide"
)

# Initialize shared state
if "data" not in st.session_state:
    st.session_state.data = None

st.title("Data Analysis App")
st.sidebar.success("Select a page to get started")
```

#### pages/1_Upload.py

```python
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Upload Data", page_icon="📤")

st.title("Upload Data")

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.session_state.data = df
    st.success("Data uploaded successfully!")
    st.dataframe(df.head())
```

#### pages/2_Explore.py

```python
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Explore Data", page_icon="🔍")

st.title("Explore Data")

if st.session_state.data is not None:
    df = st.session_state.data
    
    st.subheader("Data Overview")
    st.write(f"Shape: {df.shape}")
    st.dataframe(df.head())
    
    st.subheader("Statistics")
    st.dataframe(df.describe())
else:
    st.warning("Please upload data first!")
    if st.button("Go to Upload"):
        st.switch_page("pages/1_Upload.py")
```

#### pages/3_Visualize.py

```python
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Visualize", page_icon="📈")

st.title("Visualize Data")

if st.session_state.data is not None:
    df = st.session_state.data
    
    chart_type = st.selectbox("Chart Type", ["Line", "Bar", "Scatter"])
    x_col = st.selectbox("X Axis", df.columns)
    y_col = st.selectbox("Y Axis", df.columns)
    
    if chart_type == "Line":
        fig = px.line(df, x=x_col, y=y_col)
    elif chart_type == "Bar":
        fig = px.bar(df, x=x_col, y=y_col)
    else:
        fig = px.scatter(df, x=x_col, y=y_col)
    
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Please upload data first!")
```

### Example: Dashboard with Multiple Views

#### pages/1_Overview.py

```python
import streamlit as st

st.set_page_config(page_title="Overview", page_icon="📊")

st.title("Overview")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Sales", "$100K")
col2.metric("Orders", "1,234")
col3.metric("Customers", "567")
col4.metric("Growth", "5%")
```

#### pages/2_Sales.py

```python
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Sales", page_icon="💰")

st.title("Sales Analysis")

# Load or use shared data
df = pd.read_csv("sales.csv")

fig = px.line(df, x="date", y="sales")
st.plotly_chart(fig, use_container_width=True)
```

## Navigation Patterns

### Pattern 1: Sidebar Navigation

```python
import streamlit as st

st.sidebar.title("Navigation")

pages = {
    "Home": "pages/1_Home.py",
    "Dashboard": "pages/2_Dashboard.py",
    "Settings": "pages/3_Settings.py"
}

selected = st.sidebar.selectbox("Go to", list(pages.keys()))
if st.sidebar.button("Navigate"):
    st.switch_page(pages[selected])
```

### Pattern 2: Button Navigation

```python
import streamlit as st

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Home"):
        st.switch_page("pages/1_Home.py")

with col2:
    if st.button("Dashboard"):
        st.switch_page("pages/2_Dashboard.py")

with col3:
    if st.button("Settings"):
        st.switch_page("pages/3_Settings.py")
```

### Pattern 3: Tab-like Navigation

```python
import streamlit as st

tabs = st.tabs(["Home", "Dashboard", "Settings"])

with tabs[0]:
    if st.button("Go to Home"):
        st.switch_page("pages/1_Home.py")

with tabs[1]:
    if st.button("Go to Dashboard"):
        st.switch_page("pages/2_Dashboard.py")

with tabs[2]:
    if st.button("Go to Settings"):
        st.switch_page("pages/3_Settings.py")
```

## Best Practices

1. **Consistent page config**: Use consistent `st.set_page_config()` across pages
2. **Clear naming**: Use descriptive, numbered filenames
3. **Shared state**: Use session state for data shared across pages
4. **Navigation**: Provide clear navigation between pages
5. **Page organization**: Group related pages in subdirectories

## Common Pitfalls

### Pitfall 1: Page Not Found

**Problem:**
```python
st.switch_page("pages/Home.py")  # Wrong path
```

**Solution:**
```python
st.switch_page("pages/1_Home.py")  # Correct path
```

### Pitfall 2: State Not Initialized

**Problem:**
```python
# Page 2 tries to access state that doesn't exist
data = st.session_state.data  # Error!
```

**Solution:**
```python
# Initialize in main app or check in each page
if "data" not in st.session_state:
    st.session_state.data = None

data = st.session_state.data
```

## Next Steps

Now that you can create multi-page apps:

- [Advanced Features](./14-advanced-features.md) - Add custom components
- [Deployment](./17-deployment-production.md) - Deploy your multi-page app

## References

- [Multi-page Apps](https://docs.streamlit.io/develop/api-reference/utilities/st.set_page_config)
- [Page Navigation](https://docs.streamlit.io/develop/api-reference/utilities/st.switch_page)

