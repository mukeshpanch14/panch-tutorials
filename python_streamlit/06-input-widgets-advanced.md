# User Input Widgets - Part 2 - Deep Dive

## Overview

This guide covers advanced input widgets including selection widgets, file uploader, color picker, and form handling for complex user interactions.

## Selection Widgets

### st.selectbox()

Single selection dropdown:

```python
import streamlit as st

# Basic selectbox
option = st.selectbox("Choose an option", ["Option 1", "Option 2", "Option 3"])

# With default index
option = st.selectbox(
    "Choose an option",
    ["Option 1", "Option 2", "Option 3"],
    index=0
)

# With placeholder
option = st.selectbox(
    "Choose an option",
    ["Option 1", "Option 2", "Option 3"],
    placeholder="Select an option..."
)

# With help text
option = st.selectbox(
    "Choose an option",
    ["Option 1", "Option 2", "Option 3"],
    help="Select one option from the list"
)

# Using the value
st.write(f"You selected: {option}")
```

### st.multiselect()

Multiple selection dropdown:

```python
import streamlit as st

# Basic multiselect
options = st.multiselect(
    "Choose options",
    ["Option 1", "Option 2", "Option 3", "Option 4"]
)

# With default selections
options = st.multiselect(
    "Choose options",
    ["Option 1", "Option 2", "Option 3", "Option 4"],
    default=["Option 1"]
)

# With max selections
options = st.multiselect(
    "Choose options (max 2)",
    ["Option 1", "Option 2", "Option 3", "Option 4"],
    max_selections=2
)

# Using the values
if options:
    st.write(f"Selected: {', '.join(options)}")
else:
    st.write("No options selected")
```

### st.radio()

Radio button selection:

```python
import streamlit as st

# Basic radio
option = st.radio("Choose an option", ["Option 1", "Option 2", "Option 3"])

# With default index
option = st.radio(
    "Choose an option",
    ["Option 1", "Option 2", "Option 3"],
    index=0
)

# Horizontal layout
option = st.radio(
    "Choose an option",
    ["Option 1", "Option 2", "Option 3"],
    horizontal=True
)

# With help text
option = st.radio(
    "Choose an option",
    ["Option 1", "Option 2", "Option 3"],
    help="Select one option"
)

# Using the value
st.write(f"You selected: {option}")
```

## File Uploader

### st.file_uploader()

Upload files to your app:

```python
import streamlit as st
import pandas as pd

# Basic file uploader
uploaded_file = st.file_uploader("Choose a file")

# With file types
uploaded_file = st.file_uploader(
    "Choose a CSV file",
    type=["csv"]
)

# Multiple file types
uploaded_file = st.file_uploader(
    "Choose a file",
    type=["csv", "txt", "xlsx"]
)

# Multiple files
uploaded_files = st.file_uploader(
    "Choose files",
    accept_multiple_files=True
)

# With help text
uploaded_file = st.file_uploader(
    "Upload your data",
    type=["csv"],
    help="Upload a CSV file with your data"
)

# Processing uploaded file
if uploaded_file is not None:
    # Read CSV
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
        st.dataframe(df)
    
    # Read text
    elif uploaded_file.name.endswith('.txt'):
        text = uploaded_file.read().decode("utf-8")
        st.text(text)
    
    # Display file info
    st.write(f"File name: {uploaded_file.name}")
    st.write(f"File size: {uploaded_file.size} bytes")
    st.write(f"File type: {uploaded_file.type}")
```

### Processing Different File Types

```python
import streamlit as st
import pandas as pd
import json

uploaded_file = st.file_uploader("Choose a file", type=["csv", "json", "txt"])

if uploaded_file is not None:
    file_extension = uploaded_file.name.split('.')[-1].lower()
    
    if file_extension == 'csv':
        df = pd.read_csv(uploaded_file)
        st.dataframe(df)
    
    elif file_extension == 'json':
        data = json.load(uploaded_file)
        st.json(data)
    
    elif file_extension == 'txt':
        text = uploaded_file.read().decode("utf-8")
        st.text(text)
```

## Color Picker

### st.color_picker()

Color selection widget:

```python
import streamlit as st

# Basic color picker
color = st.color_picker("Pick a color", "#00f900")

# With default value
color = st.color_picker("Pick a color", value="#FF5733")

# With help text
color = st.color_picker(
    "Pick a color",
    value="#FF5733",
    help="Select a color for your theme"
)

# Using the color
st.markdown(
    f'<div style="background-color: {color}; padding: 20px; border-radius: 5px;">'
    f'<p style="color: white;">Selected color: {color}</p>'
    f'</div>',
    unsafe_allow_html=True
)
```

## Form Handling

### st.form()

Create forms that batch widget interactions:

```python
import streamlit as st

with st.form("my_form"):
    name = st.text_input("Name")
    email = st.text_input("Email")
    age = st.number_input("Age", min_value=0, max_value=120)
    
    submitted = st.form_submit_button("Submit")
    
    if submitted:
        if name and email:
            st.success(f"Form submitted for {name}!")
        else:
            st.error("Please fill all fields")
```

### Why Use Forms?

Forms prevent the app from rerunning on every widget interaction. All widgets inside a form only trigger a rerun when the submit button is clicked.

**Without form (reruns on every change):**
```python
name = st.text_input("Name")  # Reruns when typing
email = st.text_input("Email")  # Reruns when typing
if st.button("Submit"):  # Reruns when clicked
    st.write(f"Hello {name}")
```

**With form (reruns only on submit):**
```python
with st.form("my_form"):
    name = st.text_input("Name")  # Doesn't rerun
    email = st.text_input("Email")  # Doesn't rerun
    submitted = st.form_submit_button("Submit")  # Reruns only on submit
    if submitted:
        st.write(f"Hello {name}")
```

### Complex Form Example

```python
import streamlit as st
from datetime import date

with st.form("registration_form"):
    st.subheader("Personal Information")
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone")
    birthday = st.date_input("Birthday", max_value=date.today())
    
    st.subheader("Preferences")
    newsletter = st.checkbox("Subscribe to newsletter")
    notifications = st.checkbox("Enable notifications")
    theme = st.selectbox("Theme", ["Light", "Dark", "Auto"])
    
    st.subheader("Additional Information")
    bio = st.text_area("Bio", placeholder="Tell us about yourself...")
    
    submitted = st.form_submit_button("Register")
    
    if submitted:
        # Validation
        if not name or not email:
            st.error("Name and email are required!")
        else:
            st.success("Registration successful!")
            st.json({
                "name": name,
                "email": email,
                "phone": phone,
                "birthday": str(birthday),
                "newsletter": newsletter,
                "notifications": notifications,
                "theme": theme,
                "bio": bio
            })
```

## Widget Behavior and Callbacks

### Understanding Widget Behavior

Widgets return their current value on each rerun:

```python
import streamlit as st

# Widget value persists across reruns
option = st.selectbox("Choose", ["A", "B", "C"])

# This runs every rerun, but option keeps its value
st.write(f"Current selection: {option}")

# Changing the option triggers a rerun with new value
if option == "A":
    st.write("You chose A")
```

### Widget State Management

```python
import streamlit as st

# Initialize state
if "selected_items" not in st.session_state:
    st.session_state.selected_items = []

# Widget that updates state
new_item = st.text_input("Add item")
if st.button("Add"):
    if new_item:
        st.session_state.selected_items.append(new_item)
        st.rerun()  # Explicitly rerun to update display

# Display state
st.write("Items:")
for item in st.session_state.selected_items:
    st.write(f"- {item}")
```

### Conditional Widgets

```python
import streamlit as st

show_advanced = st.checkbox("Show advanced options")

if show_advanced:
    advanced_option = st.selectbox(
        "Advanced option",
        ["Option 1", "Option 2", "Option 3"]
    )
    st.write(f"Advanced option: {advanced_option}")
```

## Practical Examples

### Example 1: Data Filtering Interface

```python
import streamlit as st
import pandas as pd
import numpy as np

# Sample data
df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie", "David"],
    "Age": [25, 30, 35, 40],
    "City": ["NYC", "LA", "NYC", "Chicago"],
    "Score": [85, 90, 88, 92]
})

st.title("Data Filter")

# Filters
col1, col2 = st.columns(2)

with col1:
    cities = st.multiselect("Cities", df["City"].unique())
    min_age = st.slider("Min Age", 0, 100, 0)

with col2:
    min_score = st.slider("Min Score", 0, 100, 0)
    sort_by = st.selectbox("Sort by", ["Name", "Age", "Score"])

# Apply filters
filtered_df = df.copy()

if cities:
    filtered_df = filtered_df[filtered_df["City"].isin(cities)]

filtered_df = filtered_df[filtered_df["Age"] >= min_age]
filtered_df = filtered_df[filtered_df["Score"] >= min_score]

if sort_by:
    filtered_df = filtered_df.sort_values(by=sort_by)

st.dataframe(filtered_df)
```

### Example 2: File Processing App

```python
import streamlit as st
import pandas as pd

st.title("File Processor")

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    st.subheader("Data Preview")
    st.dataframe(df.head())
    
    st.subheader("Processing Options")
    
    with st.form("processing_form"):
        operation = st.selectbox(
            "Operation",
            ["Filter", "Sort", "Aggregate", "Transform"]
        )
        
        if operation == "Filter":
            column = st.selectbox("Column", df.columns)
            value = st.text_input("Value")
        
        elif operation == "Sort":
            column = st.selectbox("Sort by", df.columns)
            ascending = st.checkbox("Ascending", value=True)
        
        submitted = st.form_submit_button("Process")
        
        if submitted:
            if operation == "Filter":
                result = df[df[column] == value]
            elif operation == "Sort":
                result = df.sort_values(by=column, ascending=ascending)
            else:
                result = df
            
            st.dataframe(result)
```

### Example 3: Theme Customizer

```python
import streamlit as st

st.title("Theme Customizer")

with st.form("theme_form"):
    primary_color = st.color_picker("Primary Color", "#FF6B6B")
    background_color = st.color_picker("Background Color", "#FFFFFF")
    text_color = st.color_picker("Text Color", "#262730")
    font = st.selectbox("Font", ["sans serif", "serif", "monospace"])
    
    submitted = st.form_submit_button("Apply Theme")
    
    if submitted:
        st.success("Theme applied!")
        st.markdown(f"""
        <style>
        .stApp {{
            background-color: {background_color};
            color: {text_color};
            font-family: {font};
        }}
        </style>
        """, unsafe_allow_html=True)
```

## Best Practices

1. **Use forms for multiple inputs**: Prevents unnecessary reruns
2. **Validate file uploads**: Check file type and size
3. **Provide defaults**: Use default values for better UX
4. **Handle empty selections**: Check if multiselect/selectbox returns None
5. **Use appropriate widgets**: Choose the right widget for the use case

## Common Pitfalls

### Pitfall 1: Form Widgets Outside Form

**Problem:**
```python
with st.form("my_form"):
    name = st.text_input("Name")
submitted = st.form_submit_button("Submit")  # Wrong! Outside form
```

**Solution:**
```python
with st.form("my_form"):
    name = st.text_input("Name")
    submitted = st.form_submit_button("Submit")  # Correct! Inside form
```

### Pitfall 2: Not Handling None in Multiselect

**Problem:**
```python
options = st.multiselect("Options", ["A", "B", "C"])
for option in options:  # Error if options is None
    st.write(option)
```

**Solution:**
```python
options = st.multiselect("Options", ["A", "B", "C"])
if options:
    for option in options:
        st.write(option)
```

### Pitfall 3: File Uploader Without Check

**Problem:**
```python
uploaded_file = st.file_uploader("Upload file")
df = pd.read_csv(uploaded_file)  # Error if no file uploaded
```

**Solution:**
```python
uploaded_file = st.file_uploader("Upload file")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
```

## Next Steps

Now that you know advanced input widgets:

- [Layout and Containers](./07-layout-containers.md) - Organize your widgets
- [Session State](./09-session-state.md) - Manage app state

## References

- [Advanced Widgets API](https://docs.streamlit.io/develop/api-reference/widgets)
- [File Uploader API](https://docs.streamlit.io/develop/api-reference/widgets/st.file_uploader)
- [Forms API](https://docs.streamlit.io/develop/api-reference/control-flow/st.form)

