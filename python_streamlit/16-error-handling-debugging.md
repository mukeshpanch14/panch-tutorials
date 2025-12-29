# Error Handling and Debugging - Deep Dive

## Overview

This guide covers exception handling in Streamlit, error messages and user feedback, debugging techniques, logging, common errors and solutions, testing Streamlit apps, and debug mode.

## Exception Handling in Streamlit

### Basic Try-Except

```python
import streamlit as st

try:
    result = 10 / 0
except ZeroDivisionError:
    st.error("Division by zero error!")
```

### Handling Multiple Exceptions

```python
import streamlit as st

try:
    value = int(st.text_input("Enter a number"))
    result = 100 / value
    st.success(f"Result: {result}")
except ValueError:
    st.error("Please enter a valid number!")
except ZeroDivisionError:
    st.error("Cannot divide by zero!")
except Exception as e:
    st.error(f"An error occurred: {str(e)}")
```

### Exception with Details

```python
import streamlit as st

try:
    # Your code here
    result = process_data()
except Exception as e:
    st.exception(e)  # Shows full traceback
```

## Error Messages and User Feedback

### Error Messages

```python
import streamlit as st

# Basic error
st.error("Something went wrong!")

# Error with details
st.error("Error: Invalid input. Please check your data.")

# Error with icon
st.error("❌ Operation failed!")
```

### Warning Messages

```python
import streamlit as st

st.warning("This is a warning message")
st.warning("⚠️ Data may be incomplete")
```

### Info Messages

```python
import streamlit as st

st.info("This is an informational message")
st.info("ℹ️ Processing your request...")
```

### Success Messages

```python
import streamlit as st

st.success("Operation completed successfully!")
st.success("✅ Data saved!")
```

### Exception Display

```python
import streamlit as st

try:
    # Code that might fail
    result = risky_operation()
except Exception as e:
    st.exception(e)  # Shows full traceback with formatting
```

## Debugging Techniques

### Print Statements

```python
import streamlit as st

# Print to console (visible in terminal)
print("Debug: Variable value =", value)

# Display in app
st.write("Debug: Variable value =", value)
```

### Debug Mode

Run Streamlit with debug mode:

```bash
streamlit run app.py --logger.level=debug
```

### Inspecting Variables

```python
import streamlit as st

# Show variable values
st.write("Debug Info:")
st.write(f"Variable x: {x}")
st.write(f"Variable y: {y}")
st.write(f"Session state: {st.session_state}")

# Show data types
st.write(f"Type of x: {type(x)}")
```

### Conditional Debugging

```python
import streamlit as st

DEBUG = st.sidebar.checkbox("Debug Mode")

if DEBUG:
    st.write("Debug information:")
    st.write(f"Session state: {st.session_state}")
    st.write(f"Variables: {locals()}")
```

## Logging in Streamlit Apps

### Basic Logging

```python
import streamlit as st
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Application started")
logger.warning("This is a warning")
logger.error("This is an error")
```

### Streamlit-Specific Logging

```python
import streamlit as st
import logging

# Create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Handler for console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)

# Use logger
logger.info("Info message")
logger.debug("Debug message")
logger.error("Error message")
```

### Logging to File

```python
import streamlit as st
import logging

# Configure file logging
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
logger.info("Application started")
```

## Common Errors and Solutions

### Error 1: Widget Outside Form

**Error:**
```
Widgets must be inside a form
```

**Solution:**
```python
# Wrong
with st.form("my_form"):
    name = st.text_input("Name")
submitted = st.form_submit_button("Submit")  # Error!

# Correct
with st.form("my_form"):
    name = st.text_input("Name")
    submitted = st.form_submit_button("Submit")  # Inside form
```

### Error 2: Session State Key Error

**Error:**
```
KeyError: 'my_key'
```

**Solution:**
```python
# Wrong
value = st.session_state.my_key  # Error if key doesn't exist

# Correct
if "my_key" not in st.session_state:
    st.session_state.my_key = None
value = st.session_state.my_key

# Or use get()
value = st.session_state.get("my_key", default_value)
```

### Error 3: File Not Found

**Error:**
```
FileNotFoundError: [Errno 2] No such file or directory
```

**Solution:**
```python
import os

file_path = "data.csv"
if os.path.exists(file_path):
    df = pd.read_csv(file_path)
else:
    st.error(f"File not found: {file_path}")
```

### Error 4: Type Errors

**Error:**
```
TypeError: unsupported operand type(s)
```

**Solution:**
```python
# Check types before operations
value = st.text_input("Enter number")
try:
    num_value = float(value)
    result = num_value * 2
except ValueError:
    st.error("Please enter a valid number")
```

## Testing Streamlit Apps

### Unit Testing

```python
import unittest
import streamlit as st

def process_data(data):
    """Function to test"""
    return data * 2

class TestApp(unittest.TestCase):
    def test_process_data(self):
        self.assertEqual(process_data(5), 10)
        self.assertEqual(process_data(0), 0)

if __name__ == "__main__":
    unittest.main()
```

### Testing with pytest

```python
import pytest
import streamlit as st

def add_numbers(a, b):
    return a + b

def test_add_numbers():
    assert add_numbers(2, 3) == 5
    assert add_numbers(0, 0) == 0
    assert add_numbers(-1, 1) == 0
```

### Integration Testing

```python
import streamlit as st
from streamlit.testing.v1 import AppTest

def test_app():
    at = AppTest.from_file("app.py")
    at.run()
    
    # Test widgets
    at.text_input("name").input("John").run()
    assert at.success[0].value == "Hello, John!"
```

## Debug Mode and Troubleshooting

### Enabling Debug Mode

```bash
# Run with debug logging
streamlit run app.py --logger.level=debug

# Run with show error details
streamlit run app.py --server.showErrorDetails=true
```

### Common Debugging Steps

1. **Check console output**: Look for error messages in terminal
2. **Use print statements**: Add print() to track execution
3. **Check session state**: Display session state values
4. **Validate inputs**: Check user input before processing
5. **Test incrementally**: Test small parts of code

### Debug Helper Function

```python
import streamlit as st

def debug_info():
    """Display debug information"""
    if st.sidebar.checkbox("Show Debug Info"):
        st.sidebar.write("### Session State")
        st.sidebar.json(dict(st.session_state))
        
        st.sidebar.write("### App Info")
        st.sidebar.write(f"Streamlit version: {st.__version__}")

# Use in app
debug_info()
```

## Practical Examples

### Example 1: Robust Data Loading

```python
import streamlit as st
import pandas as pd

def load_data_safely(file_path):
    """Load data with error handling"""
    try:
        if not os.path.exists(file_path):
            st.error(f"File not found: {file_path}")
            return None
        
        df = pd.read_csv(file_path)
        
        if df.empty:
            st.warning("File is empty")
            return None
        
        return df
    
    except pd.errors.EmptyDataError:
        st.error("File is empty or corrupted")
        return None
    except Exception as e:
        st.error(f"Error loading file: {str(e)}")
        st.exception(e)
        return None

df = load_data_safely("data.csv")
if df is not None:
    st.dataframe(df)
```

### Example 2: Error Handling in Forms

```python
import streamlit as st

with st.form("error_form"):
    name = st.text_input("Name")
    email = st.text_input("Email")
    age = st.number_input("Age", min_value=0, max_value=120)
    
    submitted = st.form_submit_button("Submit")
    
    if submitted:
        errors = []
        
        # Validate
        if not name:
            errors.append("Name is required")
        if not email:
            errors.append("Email is required")
        elif "@" not in email:
            errors.append("Invalid email format")
        if age < 18:
            errors.append("Must be 18 or older")
        
        # Display errors
        if errors:
            for error in errors:
                st.error(error)
        else:
            try:
                # Process form
                process_registration(name, email, age)
                st.success("Registration successful!")
            except Exception as e:
                st.error(f"Registration failed: {str(e)}")
                st.exception(e)
```

### Example 3: Debug Panel

```python
import streamlit as st

# Debug panel in sidebar
if st.sidebar.checkbox("Debug Mode"):
    st.sidebar.subheader("Debug Information")
    
    # Session state
    st.sidebar.write("### Session State")
    st.sidebar.json(dict(st.session_state))
    
    # Variables
    st.sidebar.write("### Variables")
    st.sidebar.write(f"Variable x: {x if 'x' in locals() else 'Not defined'}")
    
    # Clear cache button
    if st.sidebar.button("Clear Cache"):
        st.cache_data.clear()
        st.sidebar.success("Cache cleared!")
```

## Best Practices

1. **Always handle exceptions**: Use try-except blocks
2. **Provide user feedback**: Show clear error messages
3. **Log errors**: Log errors for debugging
4. **Validate inputs**: Check user input before processing
5. **Test thoroughly**: Test error cases

## Common Pitfalls

### Pitfall 1: Silent Failures

**Problem:**
```python
try:
    result = risky_operation()
except:
    pass  # Silent failure!
```

**Solution:**
```python
try:
    result = risky_operation()
except Exception as e:
    st.error(f"Operation failed: {str(e)}")
    logger.error(f"Error: {str(e)}", exc_info=True)
```

### Pitfall 2: Not Checking None

**Problem:**
```python
value = st.text_input("Enter value")
result = value.upper()  # Error if value is None!
```

**Solution:**
```python
value = st.text_input("Enter value")
if value:
    result = value.upper()
else:
    st.warning("Please enter a value")
```

## Next Steps

Now that you can handle errors:

- [Deployment](./17-deployment-production.md) - Deploy your app
- [Best Practices](./19-best-practices.md) - More error handling tips

## References

- [Error Handling](https://docs.streamlit.io/develop/api-reference/status/st.error)
- [Logging](https://docs.python.org/3/library/logging.html)
- [Testing](https://docs.streamlit.io/develop/api-reference/testing)

