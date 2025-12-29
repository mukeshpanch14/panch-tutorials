# Core Concepts and App Structure - Deep Dive

## Overview

Understanding how Streamlit works internally is crucial for building effective applications. This guide covers the script execution model, rerun mechanism, app lifecycle, and best practices for organizing your code.

## How Streamlit Works

### Script Execution Model

Streamlit uses a unique execution model where your Python script runs from top to bottom every time a user interacts with your app.

```python
import streamlit as st

# This runs every time
st.title("My App")

# This runs every time
name = st.text_input("Enter name")

# This runs every time
if name:
    st.write(f"Hello, {name}!")
```

**Key Points:**
- The entire script executes on each interaction
- Widgets maintain their values between reruns
- Variables are reset unless stored in session state
- The script runs synchronously from top to bottom

### Rerun Model

When a user interacts with a widget, Streamlit:

1. Captures the new widget value
2. Reruns the entire script
3. Updates the UI with new outputs
4. Waits for the next interaction

```python
import streamlit as st

# Initial run: counter doesn't exist
if "counter" not in st.session_state:
    st.session_state.counter = 0

# Every rerun: button is checked
if st.button("Increment"):
    st.session_state.counter += 1  # This triggers a rerun

# Every rerun: current value is displayed
st.write(f"Counter: {st.session_state.counter}")
```

## App Lifecycle

### 1. Initialization

When the app first loads:

```python
import streamlit as st

# This runs once on first load
if "initialized" not in st.session_state:
    st.session_state.initialized = True
    st.session_state.data = load_expensive_data()  # Load once
    st.write("App initialized!")
```

### 2. User Interaction

When user interacts with widgets:

```python
import streamlit as st

# Widget value changes
option = st.selectbox("Choose", ["A", "B", "C"])

# Script reruns with new value
if option == "A":
    st.write("You chose A")
elif option == "B":
    st.write("You chose B")
```

### 3. State Updates

State changes trigger reruns:

```python
import streamlit as st

if "count" not in st.session_state:
    st.session_state.count = 0

# Clicking button updates state and triggers rerun
if st.button("Click me"):
    st.session_state.count += 1

st.write(f"Clicked {st.session_state.count} times")
```

## Understanding State and Reruns

### Widget State

Widgets automatically maintain their state:

```python
import streamlit as st

# This value persists across reruns
name = st.text_input("Name", value="Default")

# Even if script reruns, the input keeps its value
st.write(f"Current name: {name}")
```

### Session State

Use `st.session_state` for custom state:

```python
import streamlit as st

# Initialize
if "items" not in st.session_state:
    st.session_state.items = []

# Add item
new_item = st.text_input("New item")
if st.button("Add"):
    st.session_state.items.append(new_item)

# Display items
for item in st.session_state.items:
    st.write(f"- {item}")
```

### State Persistence

State persists for the session duration:

```python
import streamlit as st

# This persists across page refreshes (in same session)
if "user_preferences" not in st.session_state:
    st.session_state.user_preferences = {
        "theme": "light",
        "language": "en"
    }

# Update preferences
theme = st.selectbox("Theme", ["light", "dark"])
st.session_state.user_preferences["theme"] = theme
```

## Basic App Structure

### Simple Structure

```python
import streamlit as st

# 1. Configuration
st.set_page_config(page_title="My App", layout="wide")

# 2. Imports and setup
import pandas as pd
import numpy as np

# 3. Helper functions
def load_data():
    return pd.DataFrame({"A": [1, 2, 3]})

# 4. Main app logic
def main():
    st.title("My App")
    df = load_data()
    st.dataframe(df)

# 5. Run app
if __name__ == "__main__":
    main()
```

### Organized Structure

```python
import streamlit as st
from utils import data_loader, processors, visualizers

# Configuration
st.set_page_config(
    page_title="Data Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Constants
DATA_PATH = "data/sales.csv"

# Helper functions
@st.cache_data
def load_data():
    return data_loader.load_csv(DATA_PATH)

def process_data(df):
    return processors.clean_data(df)

def create_visualization(df):
    return visualizers.create_chart(df)

# Main app
def main():
    st.title("Sales Dashboard")
    
    # Load data
    df = load_data()
    
    # Process data
    processed_df = process_data(df)
    
    # Display
    st.dataframe(processed_df)
    st.plotly_chart(create_visualization(processed_df))

if __name__ == "__main__":
    main()
```

## Code Organization Best Practices

### 1. Separate Concerns

**Bad:**
```python
import streamlit as st
import pandas as pd
import plotly.express as px

# Everything in one file
df = pd.read_csv("data.csv")
df = df.dropna()
df = df.groupby("category").sum()
fig = px.bar(df, x="category", y="sales")
st.plotly_chart(fig)
```

**Good:**
```python
# app.py
import streamlit as st
from utils.data import load_and_process
from utils.viz import create_chart

df = load_and_process("data.csv")
fig = create_chart(df)
st.plotly_chart(fig)
```

### 2. Use Functions

```python
import streamlit as st

def display_header():
    st.title("My App")
    st.markdown("---")

def get_user_input():
    name = st.text_input("Name")
    age = st.slider("Age", 0, 100)
    return name, age

def display_results(name, age):
    if name and age:
        st.success(f"Hello {name}, you are {age} years old!")

# Main app
display_header()
name, age = get_user_input()
display_results(name, age)
```

### 3. Modular Structure

```
app/
├── app.py           # Main entry point
├── pages/           # Multi-page apps
├── utils/
│   ├── data.py      # Data loading/processing
│   ├── viz.py       # Visualizations
│   └── helpers.py   # Helper functions
└── config.py        # Configuration
```

### 4. Use Classes for Complex State

```python
import streamlit as st

class AppState:
    def __init__(self):
        if "app_state" not in st.session_state:
            st.session_state.app_state = {
                "data": None,
                "filters": {},
                "selected_items": []
            }
    
    def get_data(self):
        return st.session_state.app_state["data"]
    
    def set_data(self, data):
        st.session_state.app_state["data"] = data

# Usage
state = AppState()
state.set_data([1, 2, 3])
data = state.get_data()
```

## Common Patterns

### Pattern 1: Conditional Rendering

```python
import streamlit as st

show_details = st.checkbox("Show details")

if show_details:
    st.write("Detailed information here")
    st.dataframe(df)
else:
    st.write("Summary information")
```

### Pattern 2: Multi-step Forms

```python
import streamlit as st

if "step" not in st.session_state:
    st.session_state.step = 1

if st.session_state.step == 1:
    name = st.text_input("Name")
    if st.button("Next"):
        st.session_state.name = name
        st.session_state.step = 2
        st.rerun()

elif st.session_state.step == 2:
    st.write(f"Hello, {st.session_state.name}!")
    if st.button("Back"):
        st.session_state.step = 1
        st.rerun()
```

### Pattern 3: Data Loading with Caching

```python
import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    # Expensive operation
    return pd.read_csv("large_file.csv")

df = load_data()  # Cached after first run
st.dataframe(df)
```

## Common Pitfalls

### Pitfall 1: Not Understanding Reruns

**Problem:**
```python
counter = 0
if st.button("Increment"):
    counter += 1  # This won't work!
st.write(counter)  # Always shows 0
```

**Solution:**
```python
if "counter" not in st.session_state:
    st.session_state.counter = 0

if st.button("Increment"):
    st.session_state.counter += 1

st.write(st.session_state.counter)
```

### Pitfall 2: Expensive Operations Without Caching

**Problem:**
```python
def load_data():
    return pd.read_csv("large_file.csv")  # Runs every rerun!

df = load_data()
```

**Solution:**
```python
@st.cache_data
def load_data():
    return pd.read_csv("large_file.csv")  # Cached!

df = load_data()
```

### Pitfall 3: Not Initializing State

**Problem:**
```python
st.session_state.items.append(item)  # Error if items doesn't exist
```

**Solution:**
```python
if "items" not in st.session_state:
    st.session_state.items = []

st.session_state.items.append(item)
```

## Best Practices

1. **Initialize state early**: Check and initialize session state at the beginning
2. **Use caching**: Cache expensive operations
3. **Organize code**: Use functions and modules
4. **Handle errors**: Use try-except blocks
5. **Test locally**: Test thoroughly before deploying

## Next Steps

Now that you understand Streamlit's core concepts:

- [Displaying Data](./04-displaying-data.md) - Learn how to display text and data
- [Input Widgets](./05-input-widgets-basic.md) - Create interactive widgets

## References

- [Streamlit Architecture](https://docs.streamlit.io/develop/concepts/architecture)
- [Session State](https://docs.streamlit.io/develop/api-reference/execution-state/st.session_state)
- [Caching](https://docs.streamlit.io/develop/api-reference/performance/st.cache_data)

