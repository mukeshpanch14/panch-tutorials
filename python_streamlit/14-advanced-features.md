# Advanced Features - Deep Dive

## Overview

This guide covers advanced Streamlit features including custom components, JavaScript integration, custom HTML/CSS, theming, custom metrics, progress indicators, and loading states.

## Custom Components

### Introduction to Custom Components

Custom components allow you to extend Streamlit with React/JavaScript functionality:

```python
import streamlit as st
import streamlit.components.v1 as components

# HTML component
components.html("""
<div style="background-color: #f0f0f0; padding: 20px; border-radius: 5px;">
    <h2>Custom HTML Component</h2>
    <p>This is a custom HTML component</p>
</div>
""", height=200)
```

### Using Streamlit Components

```python
import streamlit as st
import streamlit.components.v1 as components

# Embed external content
components.iframe("https://example.com", height=600)

# Custom HTML
components.html("""
<script>
    console.log("Hello from JavaScript!");
</script>
<div id="myDiv">Hello World</div>
""", height=200)
```

## Streamlit Components API

### Creating Custom Components

While creating full custom components requires React/TypeScript, you can use HTML/CSS:

```python
import streamlit as st
import streamlit.components.v1 as components

# Interactive HTML component
components.html("""
<div>
    <button onclick="increment()">Click me</button>
    <p id="count">0</p>
</div>
<script>
    let count = 0;
    function increment() {
        count++;
        document.getElementById('count').textContent = count;
    }
</script>
""", height=150)
```

## JavaScript Integration

### Basic JavaScript

```python
import streamlit as st
import streamlit.components.v1 as components

components.html("""
<script>
    // JavaScript code here
    alert("Hello from JavaScript!");
</script>
""")
```

### JavaScript with Streamlit Communication

```python
import streamlit as st
import streamlit.components.v1 as components

# Component that sends data back to Streamlit
components.html("""
<script src="https://cdn.jsdelivr.net/npm/@streamlit/streamlit-component-lib@latest/dist/streamlit-component-lib.js"></script>
<script>
    function sendData() {
        Streamlit.setComponentValue({value: "Hello from JS!"});
    }
</script>
<button onclick="sendData()">Send Data</button>
""", height=100)
```

## Custom HTML/CSS

### Inline HTML

```python
import streamlit as st

st.markdown("""
<div style="background-color: #f0f0f0; padding: 20px; border-radius: 10px;">
    <h2 style="color: #333;">Custom Styled Content</h2>
    <p>This is custom HTML with CSS styling</p>
</div>
""", unsafe_allow_html=True)
```

### Custom CSS

```python
import streamlit as st

st.markdown("""
<style>
.custom-container {
    background-color: #f0f0f0;
    padding: 20px;
    border-radius: 10px;
    margin: 10px 0;
}
.custom-title {
    color: #333;
    font-size: 24px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="custom-container">
    <h2 class="custom-title">Custom Styled Title</h2>
    <p>Content with custom styling</p>
</div>
""", unsafe_allow_html=True)
```

### Advanced Styling

```python
import streamlit as st

st.markdown("""
<style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom colors */
    .stApp {
        background-color: #f5f5f5;
    }
    
    /* Custom button */
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)
```

## Theming and Customization

### Theme Configuration

Create `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"
```

### Dynamic Theming

```python
import streamlit as st

theme = st.selectbox("Theme", ["Light", "Dark"])

if theme == "Dark":
    st.markdown("""
    <style>
    .stApp {
        background-color: #1e1e1e;
        color: #ffffff;
    }
    </style>
    """, unsafe_allow_html=True)
```

## Custom Metrics and KPIs

### Custom Metric Display

```python
import streamlit as st

# Standard metrics
col1, col2, col3 = st.columns(3)
col1.metric("Revenue", "$100K", "10%")
col2.metric("Users", "1,234", "5%")
col3.metric("Growth", "5%", "-2%")
```

### Custom KPI Cards

```python
import streamlit as st

def kpi_card(title, value, change=None):
    st.markdown(f"""
    <div style="background-color: #f0f0f0; padding: 15px; border-radius: 5px; margin: 10px 0;">
        <h3 style="margin: 0; color: #666;">{title}</h3>
        <h2 style="margin: 5px 0; color: #333;">{value}</h2>
        {f'<p style="margin: 0; color: #4CAF50;">{change}</p>' if change else ''}
    </div>
    """, unsafe_allow_html=True)

kpi_card("Total Revenue", "$100,000", "+10%")
kpi_card("Active Users", "1,234", "+5%")
```

## Progress Bars and Status Indicators

### st.progress()

```python
import streamlit as st
import time

# Basic progress bar
progress_bar = st.progress(0)

for i in range(100):
    progress_bar.progress(i + 1)
    time.sleep(0.01)

st.success("Complete!")
```

### Status Indicators

```python
import streamlit as st

# Success
st.success("Operation completed successfully!")

# Error
st.error("An error occurred!")

# Warning
st.warning("This is a warning!")

# Info
st.info("This is informational!")

# Exception
try:
    result = 1 / 0
except Exception as e:
    st.exception(e)
```

### Custom Progress Indicator

```python
import streamlit as st
import time

def custom_progress(current, total, label=""):
    percent = (current / total) * 100
    st.markdown(f"""
    <div style="background-color: #f0f0f0; padding: 10px; border-radius: 5px;">
        <div style="background-color: #4CAF50; width: {percent}%; height: 20px; border-radius: 5px;"></div>
        <p style="margin: 5px 0;">{label} {current}/{total} ({percent:.1f}%)</p>
    </div>
    """, unsafe_allow_html=True)

for i in range(10):
    custom_progress(i + 1, 10, "Processing")
    time.sleep(0.5)
```

## Spinners and Loading States

### st.spinner()

```python
import streamlit as st
import time

with st.spinner("Loading..."):
    time.sleep(2)
    st.success("Done!")
```

### Custom Loading Indicator

```python
import streamlit as st
import time

loading_placeholder = st.empty()

with loading_placeholder.container():
    st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <div class="spinner"></div>
        <p>Loading...</p>
    </div>
    <style>
    .spinner {
        border: 4px solid #f3f3f3;
        border-top: 4px solid #3498db;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
        margin: 0 auto;
    }
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    </style>
    """, unsafe_allow_html=True)
    
    time.sleep(2)

loading_placeholder.empty()
st.success("Content loaded!")
```

### Loading with Progress

```python
import streamlit as st
import time

progress_bar = st.progress(0)
status_text = st.empty()

for i in range(100):
    progress_bar.progress(i + 1)
    status_text.text(f"Processing {i+1}%")
    time.sleep(0.01)

status_text.text("Complete!")
st.success("Processing complete!")
```

## Practical Examples

### Example 1: Custom Dashboard

```python
import streamlit as st

st.markdown("""
<style>
.metric-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 20px;
    border-radius: 10px;
    color: white;
    margin: 10px 0;
}
</style>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="metric-card">
        <h3>Revenue</h3>
        <h1>$100K</h1>
        <p>+10% from last month</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <h3>Users</h3>
        <h1>1,234</h1>
        <p>+5% from last month</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <h3>Growth</h3>
        <h1>5%</h1>
        <p>-2% from last month</p>
    </div>
    """, unsafe_allow_html=True)
```

### Example 2: Interactive Component

```python
import streamlit as st
import streamlit.components.v1 as components

components.html("""
<div>
    <h3>Interactive Counter</h3>
    <button onclick="increment()" style="padding: 10px 20px; font-size: 16px;">Increment</button>
    <button onclick="decrement()" style="padding: 10px 20px; font-size: 16px;">Decrement</button>
    <p id="count" style="font-size: 24px; font-weight: bold;">0</p>
</div>
<script>
    let count = 0;
    function increment() {
        count++;
        document.getElementById('count').textContent = count;
    }
    function decrement() {
        count--;
        document.getElementById('count').textContent = count;
    }
</script>
""", height=200)
```

## Best Practices

1. **Use sparingly**: Custom components add complexity
2. **Test thoroughly**: Custom HTML/JS needs testing
3. **Security**: Be careful with `unsafe_allow_html=True`
4. **Performance**: Custom components can impact performance
5. **Accessibility**: Ensure custom components are accessible

## Common Pitfalls

### Pitfall 1: XSS Vulnerabilities

**Problem:**
```python
user_input = st.text_input("Enter HTML")
st.markdown(user_input, unsafe_allow_html=True)  # Dangerous!
```

**Solution:**
```python
# Sanitize user input or avoid unsafe_allow_html with user input
user_input = st.text_input("Enter text")
st.write(user_input)  # Safe
```

### Pitfall 2: Component Not Updating

**Problem:**
```python
# Component doesn't update when state changes
components.html("<div>Static content</div>")
```

**Solution:**
```python
# Use key to force rerender
components.html(f"<div>{st.session_state.value}</div>", key="dynamic")
```

## Next Steps

Now that you know advanced features:

- [Media and Files](./15-media-files.md) - Handle media files
- [Deployment](./17-deployment-production.md) - Deploy your app

## References

- [Custom Components](https://docs.streamlit.io/develop/components)
- [HTML Components](https://docs.streamlit.io/develop/api-reference/components)
- [Theming](https://docs.streamlit.io/develop/api-reference/configuration)

