# Session State and State Management - Deep Dive

## Overview

Session state allows you to store and persist data across app reruns. This guide covers understanding session state, initializing state, reading and writing state, state management patterns, and common pitfalls.

## Understanding st.session_state

### What is Session State?

`st.session_state` is a dictionary-like object that persists data for the duration of a user's session. Unlike regular variables, values in session state survive app reruns.

```python
import streamlit as st

# Regular variable (resets on rerun)
counter = 0

# Session state (persists across reruns)
if "counter" not in st.session_state:
    st.session_state.counter = 0

st.write(f"Counter: {st.session_state.counter}")
```

### How Session State Works

```python
import streamlit as st

# Session state is a dictionary
st.write(type(st.session_state))  # <class 'streamlit.runtime.state.session_state.SessionState'>

# You can check if a key exists
if "my_key" in st.session_state:
    st.write("Key exists!")

# You can iterate over keys
for key in st.session_state.keys():
    st.write(f"{key}: {st.session_state[key]}")
```

## Initializing State

### Basic Initialization

```python
import streamlit as st

# Check before initializing
if "counter" not in st.session_state:
    st.session_state.counter = 0

# Use the value
st.write(f"Counter: {st.session_state.counter}")
```

### Initialization Pattern

```python
import streamlit as st

# Initialize multiple values
if "initialized" not in st.session_state:
    st.session_state.initialized = True
    st.session_state.counter = 0
    st.session_state.items = []
    st.session_state.user_data = {}
```

### Using st.session_state.get()

```python
import streamlit as st

# Get with default value
counter = st.session_state.get("counter", 0)

# Get with default (dictionary)
user_data = st.session_state.get("user_data", {"name": "Guest"})
```

## Reading and Writing State

### Reading State

```python
import streamlit as st

# Direct access
if "name" in st.session_state:
    name = st.session_state.name

# Using get()
name = st.session_state.get("name", "Guest")

# Check existence
if "name" in st.session_state:
    st.write(f"Hello, {st.session_state.name}")
```

### Writing State

```python
import streamlit as st

# Direct assignment
st.session_state.counter = 10

# Update dictionary
if "user_data" not in st.session_state:
    st.session_state.user_data = {}
st.session_state.user_data["name"] = "Alice"

# Append to list
if "items" not in st.session_state:
    st.session_state.items = []
st.session_state.items.append("New item")
```

### State Updates Trigger Reruns

```python
import streamlit as st

if "counter" not in st.session_state:
    st.session_state.counter = 0

# This button click updates state and triggers rerun
if st.button("Increment"):
    st.session_state.counter += 1  # Triggers rerun

st.write(f"Counter: {st.session_state.counter}")
```

## State Persistence Across Reruns

### Persistence Example

```python
import streamlit as st

# Initialize
if "items" not in st.session_state:
    st.session_state.items = []

# Add item
new_item = st.text_input("New item")
if st.button("Add"):
    if new_item:
        st.session_state.items.append(new_item)
        st.rerun()  # Explicit rerun to update display

# Display items
st.write("Items:")
for item in st.session_state.items:
    st.write(f"- {item}")
```

### Complex State Objects

```python
import streamlit as st

# Initialize complex state
if "app_state" not in st.session_state:
    st.session_state.app_state = {
        "user": None,
        "filters": {},
        "data": None,
        "view": "list"
    }

# Update nested state
st.session_state.app_state["filters"]["category"] = "A"
st.session_state.app_state["filters"]["date"] = "2024-01-01"

# Access nested state
filters = st.session_state.app_state["filters"]
st.write(f"Filters: {filters}")
```

## State Management Patterns

### Pattern 1: Simple Counter

```python
import streamlit as st

if "counter" not in st.session_state:
    st.session_state.counter = 0

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Decrement"):
        st.session_state.counter -= 1

with col2:
    st.write(f"Count: {st.session_state.counter}")

with col3:
    if st.button("Increment"):
        st.session_state.counter += 1
```

### Pattern 2: Shopping Cart

```python
import streamlit as st

# Initialize cart
if "cart" not in st.session_state:
    st.session_state.cart = []

# Add to cart
item = st.text_input("Item name")
if st.button("Add to Cart"):
    if item:
        st.session_state.cart.append(item)

# Display cart
st.subheader("Shopping Cart")
if st.session_state.cart:
    for i, item in enumerate(st.session_state.cart):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"{i+1}. {item}")
        with col2:
            if st.button("Remove", key=f"remove_{i}"):
                st.session_state.cart.pop(i)
                st.rerun()
else:
    st.write("Cart is empty")
```

### Pattern 3: Multi-Step Form

```python
import streamlit as st

# Initialize form state
if "form_step" not in st.session_state:
    st.session_state.form_step = 1
    st.session_state.form_data = {}

# Step 1: Personal Info
if st.session_state.form_step == 1:
    st.subheader("Step 1: Personal Information")
    name = st.text_input("Name")
    email = st.text_input("Email")
    
    if st.button("Next"):
        if name and email:
            st.session_state.form_data["name"] = name
            st.session_state.form_data["email"] = email
            st.session_state.form_step = 2
            st.rerun()
        else:
            st.error("Please fill all fields")

# Step 2: Preferences
elif st.session_state.form_step == 2:
    st.subheader("Step 2: Preferences")
    theme = st.selectbox("Theme", ["Light", "Dark"])
    notifications = st.checkbox("Enable notifications")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back"):
            st.session_state.form_step = 1
            st.rerun()
    with col2:
        if st.button("Submit"):
            st.session_state.form_data["theme"] = theme
            st.session_state.form_data["notifications"] = notifications
            st.session_state.form_step = 3
            st.rerun()

# Step 3: Summary
elif st.session_state.form_step == 3:
    st.subheader("Step 3: Summary")
    st.json(st.session_state.form_data)
    if st.button("Start Over"):
        st.session_state.form_step = 1
        st.session_state.form_data = {}
        st.rerun()
```

### Pattern 4: State Class

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
    
    def add_filter(self, key, value):
        st.session_state.app_state["filters"][key] = value
    
    def clear_filters(self):
        st.session_state.app_state["filters"] = {}

# Usage
state = AppState()
state.set_data([1, 2, 3])
state.add_filter("category", "A")
data = state.get_data()
```

## Common State Management Pitfalls

### Pitfall 1: Not Initializing State

**Problem:**
```python
st.session_state.counter += 1  # Error if counter doesn't exist!
```

**Solution:**
```python
if "counter" not in st.session_state:
    st.session_state.counter = 0
st.session_state.counter += 1
```

### Pitfall 2: Modifying Lists/Dicts Directly

**Problem:**
```python
items = st.session_state.items
items.append("new")  # Doesn't trigger rerun properly
```

**Solution:**
```python
st.session_state.items.append("new")  # Direct modification
# Or
st.session_state.items = st.session_state.items + ["new"]
```

### Pitfall 3: State Not Updating Display

**Problem:**
```python
st.session_state.counter += 1
# Display might not update immediately
```

**Solution:**
```python
st.session_state.counter += 1
st.rerun()  # Explicit rerun if needed
```

## Building Interactive Apps with State

### Example: Todo App

```python
import streamlit as st

st.title("Todo App")

# Initialize state
if "todos" not in st.session_state:
    st.session_state.todos = []

# Add todo
new_todo = st.text_input("New todo")
if st.button("Add"):
    if new_todo:
        st.session_state.todos.append({
            "id": len(st.session_state.todos),
            "text": new_todo,
            "done": False
        })
        st.rerun()

# Display todos
st.subheader("Todos")
for i, todo in enumerate(st.session_state.todos):
    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        if st.checkbox("", value=todo["done"], key=f"done_{i}"):
            st.session_state.todos[i]["done"] = True
        else:
            st.session_state.todos[i]["done"] = False
    with col2:
        if todo["done"]:
            st.markdown(f"~~{todo['text']}~~")
        else:
            st.write(todo["text"])
    with col3:
        if st.button("Delete", key=f"delete_{i}"):
            st.session_state.todos.pop(i)
            st.rerun()
```

### Example: Data Filter App

```python
import streamlit as st
import pandas as pd

# Sample data
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame({
        "Name": ["Alice", "Bob", "Charlie"],
        "Age": [25, 30, 35],
        "City": ["NYC", "LA", "NYC"]
    })

# Filters in state
if "filters" not in st.session_state:
    st.session_state.filters = {
        "min_age": 0,
        "cities": []
    }

# Update filters
st.sidebar.header("Filters")
st.session_state.filters["min_age"] = st.sidebar.slider("Min Age", 0, 100, 0)
st.session_state.filters["cities"] = st.sidebar.multiselect(
    "Cities",
    st.session_state.data["City"].unique()
)

# Apply filters
filtered_data = st.session_state.data.copy()
filtered_data = filtered_data[filtered_data["Age"] >= st.session_state.filters["min_age"]]

if st.session_state.filters["cities"]:
    filtered_data = filtered_data[filtered_data["City"].isin(st.session_state.filters["cities"])]

st.dataframe(filtered_data)
```

## Best Practices

1. **Initialize early**: Check and initialize state at the beginning of your script
2. **Use descriptive keys**: Use clear, descriptive keys for state variables
3. **Group related state**: Use dictionaries to group related state
4. **Clear state when needed**: Provide ways to reset state
5. **Avoid deep nesting**: Keep state structure simple

## Next Steps

Now that you understand session state:

- [Caching and Performance](./10-caching-performance.md) - Optimize with caching
- [Working with Data](./11-working-with-data.md) - Load and process data

## References

- [Session State API](https://docs.streamlit.io/develop/api-reference/execution-state/st.session_state)
- [State Management Guide](https://docs.streamlit.io/develop/concepts/architecture)

