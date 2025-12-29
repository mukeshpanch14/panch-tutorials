# User Input Widgets - Part 1 - Deep Dive

## Overview

Streamlit provides a rich set of widgets for collecting user input. This guide covers basic input widgets including text inputs, numbers, dates, buttons, and checkboxes.

## Text Input Widgets

### st.text_input()

Single-line text input:

```python
import streamlit as st

# Basic text input
name = st.text_input("Enter your name")

# With default value
name = st.text_input("Enter your name", value="John Doe")

# With placeholder
name = st.text_input("Enter your name", placeholder="Type here...")

# With help text
name = st.text_input(
    "Enter your name",
    help="Enter your full name"
)

# With max length
name = st.text_input("Enter your name", max_chars=50)

# With type (password)
password = st.text_input("Password", type="password")

# Using the value
if name:
    st.write(f"Hello, {name}!")
```

### st.text_area()

Multi-line text input:

```python
import streamlit as st

# Basic text area
description = st.text_area("Enter description")

# With default value
description = st.text_area(
    "Enter description",
    value="Default text"
)

# With height
description = st.text_area(
    "Enter description",
    height=200
)

# With placeholder
description = st.text_area(
    "Enter description",
    placeholder="Type your description here..."
)

# With help text
description = st.text_area(
    "Enter description",
    help="Enter a detailed description"
)

# Using the value
if description:
    st.write(f"Description: {description}")
```

## Number Input Widgets

### st.number_input()

Numeric input with increment/decrement buttons:

```python
import streamlit as st

# Basic number input
age = st.number_input("Enter your age")

# With default value
age = st.number_input("Enter your age", value=25)

# With min and max
age = st.number_input("Enter your age", min_value=0, max_value=120)

# With step
price = st.number_input("Price", min_value=0.0, value=10.0, step=0.5)

# Integer only
count = st.number_input("Count", min_value=0, value=0, step=1, format="%d")

# Float with format
price = st.number_input("Price", value=10.0, format="%.2f")

# Using the value
if age:
    st.write(f"You are {age} years old")
```

### st.slider()

Slider for selecting a value from a range:

```python
import streamlit as st

# Basic slider
value = st.slider("Select a value", 0, 100)

# With default value
value = st.slider("Select a value", 0, 100, 50)

# Float slider
price = st.slider("Price", 0.0, 100.0, 50.0)

# With step
value = st.slider("Select a value", 0, 100, 50, step=5)

# Range slider (returns tuple)
range_values = st.slider(
    "Select a range",
    0, 100, (25, 75)
)
st.write(f"Range: {range_values[0]} to {range_values[1]}")

# With format
value = st.slider("Temperature", 0, 100, 25, format="%d°C")

# Using the value
st.write(f"Selected value: {value}")
```

## Date and Time Inputs

### st.date_input()

Date picker:

```python
import streamlit as st
from datetime import date

# Basic date input
selected_date = st.date_input("Select a date")

# With default value
selected_date = st.date_input(
    "Select a date",
    value=date.today()
)

# With min and max dates
selected_date = st.date_input(
    "Select a date",
    min_value=date(2020, 1, 1),
    max_value=date(2030, 12, 31)
)

# Date range (returns tuple)
date_range = st.date_input(
    "Select date range",
    value=(date.today(), date.today())
)

# Using the value
if selected_date:
    st.write(f"Selected date: {selected_date}")
```

### st.time_input()

Time picker:

```python
import streamlit as st
from datetime import time

# Basic time input
selected_time = st.time_input("Select a time")

# With default value
selected_time = st.time_input(
    "Select a time",
    value=time(12, 0)
)

# Using the value
if selected_time:
    st.write(f"Selected time: {selected_time}")
```

## Button Widgets

### st.button()

Clickable button:

```python
import streamlit as st

# Basic button
if st.button("Click me"):
    st.write("Button clicked!")

# Button with state
if "clicked" not in st.session_state:
    st.session_state.clicked = False

if st.button("Toggle"):
    st.session_state.clicked = not st.session_state.clicked

if st.session_state.clicked:
    st.write("State: ON")
else:
    st.write("State: OFF")

# Button with styling
if st.button("Submit", type="primary"):
    st.success("Submitted!")

# Disabled button
if st.button("Disabled", disabled=True):
    st.write("This won't execute")

# Button with use_container_width
st.button("Wide button", use_container_width=True)
```

### st.download_button()

Button to download files:

```python
import streamlit as st
import pandas as pd

# Download dataframe as CSV
df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
csv = df.to_csv(index=False)

st.download_button(
    label="Download CSV",
    data=csv,
    file_name="data.csv",
    mime="text/csv"
)

# Download text file
text_data = "Hello, World!"
st.download_button(
    label="Download Text",
    data=text_data,
    file_name="hello.txt",
    mime="text/plain"
)

# Download binary file
with open("image.jpg", "rb") as f:
    image_data = f.read()
    
st.download_button(
    label="Download Image",
    data=image_data,
    file_name="image.jpg",
    mime="image/jpeg"
)
```

## Checkbox and Toggle

### st.checkbox()

Checkbox widget:

```python
import streamlit as st

# Basic checkbox
show_details = st.checkbox("Show details")

if show_details:
    st.write("Details are shown!")

# Checkbox with default value
agree = st.checkbox("I agree to the terms", value=False)

if agree:
    st.write("Thank you for agreeing!")

# Multiple checkboxes
option1 = st.checkbox("Option 1")
option2 = st.checkbox("Option 2")
option3 = st.checkbox("Option 3")

if option1 or option2 or option3:
    st.write("At least one option selected")
```

### st.toggle()

Toggle switch (newer alternative to checkbox):

```python
import streamlit as st

# Basic toggle
enabled = st.toggle("Enable feature")

if enabled:
    st.write("Feature is enabled!")

# Toggle with default value
dark_mode = st.toggle("Dark mode", value=False)

if dark_mode:
    st.write("Dark mode is ON")
else:
    st.write("Dark mode is OFF")

# Toggle with label and value
theme = st.toggle("Theme", value=True, label_visibility="visible")
```

## Practical Examples

### Example 1: User Registration Form

```python
import streamlit as st
from datetime import date

st.title("User Registration")

with st.form("registration_form"):
    name = st.text_input("Full Name", placeholder="John Doe")
    email = st.text_input("Email", placeholder="john@example.com")
    age = st.number_input("Age", min_value=18, max_value=100, value=25)
    birthday = st.date_input("Birthday", max_value=date.today())
    agree = st.checkbox("I agree to the terms and conditions")
    
    submitted = st.form_submit_button("Register")
    
    if submitted:
        if name and email and agree:
            st.success(f"Welcome, {name}!")
        else:
            st.error("Please fill all required fields")
```

### Example 2: Calculator

```python
import streamlit as st

st.title("Simple Calculator")

col1, col2, col3 = st.columns(3)

with col1:
    num1 = st.number_input("Number 1", value=0.0)

with col2:
    operation = st.selectbox("Operation", ["+", "-", "*", "/"])

with col3:
    num2 = st.number_input("Number 2", value=0.0)

if st.button("Calculate"):
    if operation == "+":
        result = num1 + num2
    elif operation == "-":
        result = num1 - num2
    elif operation == "*":
        result = num1 * num2
    elif operation == "/":
        if num2 != 0:
            result = num1 / num2
        else:
            st.error("Division by zero!")
            result = None
    
    if result is not None:
        st.success(f"Result: {result}")
```

### Example 3: Settings Panel

```python
import streamlit as st

st.title("Settings")

# Appearance
st.subheader("Appearance")
dark_mode = st.toggle("Dark Mode")
font_size = st.slider("Font Size", 10, 24, 14)

# Notifications
st.subheader("Notifications")
email_notifications = st.checkbox("Email Notifications", value=True)
push_notifications = st.checkbox("Push Notifications", value=False)

# Privacy
st.subheader("Privacy")
share_data = st.checkbox("Share anonymous usage data", value=False)

if st.button("Save Settings"):
    st.success("Settings saved!")
    st.json({
        "dark_mode": dark_mode,
        "font_size": font_size,
        "email_notifications": email_notifications,
        "push_notifications": push_notifications,
        "share_data": share_data
    })
```

## Best Practices

1. **Provide defaults**: Use default values when appropriate
2. **Add help text**: Use `help` parameter for clarity
3. **Validate input**: Check input values before using
4. **Use appropriate widgets**: Choose the right widget for the data type
5. **Group related inputs**: Use columns or forms to organize inputs

## Common Pitfalls

### Pitfall 1: Not Checking for None

**Problem:**
```python
name = st.text_input("Name")
st.write(f"Hello, {name}!")  # Shows "Hello, None!" if empty
```

**Solution:**
```python
name = st.text_input("Name")
if name:
    st.write(f"Hello, {name}!")
```

### Pitfall 2: Button State Management

**Problem:**
```python
clicked = False
if st.button("Click"):
    clicked = True  # Won't persist!
```

**Solution:**
```python
if "clicked" not in st.session_state:
    st.session_state.clicked = False

if st.button("Click"):
    st.session_state.clicked = True
```

### Pitfall 3: Date Input Type

**Problem:**
```python
date = st.date_input("Date")
# date is a date object, not a string
```

**Solution:**
```python
date = st.date_input("Date")
date_str = date.strftime("%Y-%m-%d")  # Convert to string if needed
```

## Next Steps

Now that you know basic input widgets:

- [Input Widgets - Part 2](./06-input-widgets-advanced.md) - Learn advanced widgets and forms
- [Layout and Containers](./07-layout-containers.md) - Organize your widgets

## References

- [Input Widgets API](https://docs.streamlit.io/develop/api-reference/widgets)
- [Button API](https://docs.streamlit.io/develop/api-reference/widgets/st.button)
- [Download Button API](https://docs.streamlit.io/develop/api-reference/widgets/st.download_button)

