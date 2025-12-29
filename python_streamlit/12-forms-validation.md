# Forms and User Input Validation - Deep Dive

## Overview

Forms in Streamlit allow you to batch widget interactions and create structured data entry interfaces. This guide covers creating forms, form submission handling, input validation patterns, error handling, multi-step forms, and best practices.

## Creating Forms with st.form()

### Basic Form

```python
import streamlit as st

with st.form("my_form"):
    name = st.text_input("Name")
    email = st.text_input("Email")
    age = st.number_input("Age", min_value=0, max_value=120)
    
    submitted = st.form_submit_button("Submit")
    
    if submitted:
        st.write(f"Name: {name}")
        st.write(f"Email: {email}")
        st.write(f"Age: {age}")
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

## Form Submission Handling

### Basic Submission

```python
import streamlit as st

with st.form("registration_form"):
    st.subheader("Registration")
    
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    submitted = st.form_submit_button("Register")
    
    if submitted:
        if name and email and password:
            st.success("Registration successful!")
            # Process registration
        else:
            st.error("Please fill all fields")
```

### Processing Form Data

```python
import streamlit as st
import json

with st.form("data_form"):
    name = st.text_input("Name")
    email = st.text_input("Email")
    preferences = st.multiselect("Preferences", ["A", "B", "C"])
    
    submitted = st.form_submit_button("Submit")
    
    if submitted:
        form_data = {
            "name": name,
            "email": email,
            "preferences": preferences
        }
        
        # Store in session state
        if "submissions" not in st.session_state:
            st.session_state.submissions = []
        st.session_state.submissions.append(form_data)
        
        st.success("Form submitted!")
        st.json(form_data)
```

## Input Validation Patterns

### Required Field Validation

```python
import streamlit as st
import re

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

with st.form("validation_form"):
    name = st.text_input("Name *")
    email = st.text_input("Email *")
    phone = st.text_input("Phone")
    
    submitted = st.form_submit_button("Submit")
    
    if submitted:
        errors = []
        
        # Validate required fields
        if not name:
            errors.append("Name is required")
        
        if not email:
            errors.append("Email is required")
        elif not validate_email(email):
            errors.append("Invalid email format")
        
        if errors:
            for error in errors:
                st.error(error)
        else:
            st.success("Form is valid!")
```

### Range Validation

```python
import streamlit as st

with st.form("range_form"):
    age = st.number_input("Age", min_value=0, max_value=120)
    score = st.slider("Score", 0, 100)
    
    submitted = st.form_submit_button("Submit")
    
    if submitted:
        if age < 18:
            st.error("Must be 18 or older")
        elif score < 60:
            st.warning("Score is below passing")
        else:
            st.success("Validation passed!")
```

### Custom Validation Functions

```python
import streamlit as st

def validate_password(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    if not any(c.isupper() for c in password):
        return False, "Password must contain uppercase letter"
    if not any(c.islower() for c in password):
        return False, "Password must contain lowercase letter"
    if not any(c.isdigit() for c in password):
        return False, "Password must contain a digit"
    return True, ""

with st.form("password_form"):
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    
    submitted = st.form_submit_button("Submit")
    
    if submitted:
        is_valid, message = validate_password(password)
        if not is_valid:
            st.error(message)
        elif password != confirm_password:
            st.error("Passwords do not match")
        else:
            st.success("Password is valid!")
```

## Error Handling and User Feedback

### Error Messages

```python
import streamlit as st

with st.form("error_form"):
    value = st.number_input("Enter value", min_value=0)
    
    submitted = st.form_submit_button("Submit")
    
    if submitted:
        try:
            if value == 0:
                st.error("Value cannot be zero")
            else:
                result = 100 / value
                st.success(f"Result: {result}")
        except Exception as e:
            st.error(f"Error: {str(e)}")
```

### Success Messages

```python
import streamlit as st

with st.form("success_form"):
    name = st.text_input("Name")
    email = st.text_input("Email")
    
    submitted = st.form_submit_button("Submit")
    
    if submitted:
        if name and email:
            st.success("✅ Form submitted successfully!")
            st.balloons()  # Celebration!
        else:
            st.warning("⚠️ Please fill all fields")
```

### Validation Feedback

```python
import streamlit as st

with st.form("feedback_form"):
    email = st.text_input("Email")
    
    # Real-time validation feedback
    if email:
        if "@" in email and "." in email:
            st.success("✓ Valid email format")
        else:
            st.error("✗ Invalid email format")
    
    submitted = st.form_submit_button("Submit")
    
    if submitted:
        if email and "@" in email and "." in email:
            st.success("Email is valid!")
```

## Multi-step Forms

### Step-by-Step Form

```python
import streamlit as st

# Initialize form state
if "form_step" not in st.session_state:
    st.session_state.form_step = 1
    st.session_state.form_data = {}

# Step 1: Personal Information
if st.session_state.form_step == 1:
    st.subheader("Step 1: Personal Information")
    
    with st.form("step1_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        
        submitted = st.form_submit_button("Next")
        
        if submitted:
            if name and email:
                st.session_state.form_data.update({
                    "name": name,
                    "email": email,
                    "phone": phone
                })
                st.session_state.form_step = 2
                st.rerun()
            else:
                st.error("Name and email are required")

# Step 2: Preferences
elif st.session_state.form_step == 2:
    st.subheader("Step 2: Preferences")
    
    with st.form("step2_form"):
        theme = st.selectbox("Theme", ["Light", "Dark"])
        language = st.selectbox("Language", ["English", "Spanish"])
        notifications = st.checkbox("Enable notifications")
        
        col1, col2 = st.columns(2)
        with col1:
            back = st.form_submit_button("Back")
        with col2:
            next_step = st.form_submit_button("Next")
        
        if back:
            st.session_state.form_step = 1
            st.rerun()
        
        if next_step:
            st.session_state.form_data.update({
                "theme": theme,
                "language": language,
                "notifications": notifications
            })
            st.session_state.form_step = 3
            st.rerun()

# Step 3: Review and Submit
elif st.session_state.form_step == 3:
    st.subheader("Step 3: Review and Submit")
    
    st.json(st.session_state.form_data)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back"):
            st.session_state.form_step = 2
            st.rerun()
    with col2:
        if st.button("Submit"):
            st.success("Form submitted successfully!")
            # Process submission
            st.session_state.form_step = 1
            st.session_state.form_data = {}
            st.rerun()
```

## Form State Management

### Storing Form Data

```python
import streamlit as st

if "form_data" not in st.session_state:
    st.session_state.form_data = {}

with st.form("data_form"):
    name = st.text_input("Name")
    email = st.text_input("Email")
    
    submitted = st.form_submit_button("Save")
    
    if submitted:
        st.session_state.form_data = {
            "name": name,
            "email": email
        }
        st.success("Data saved!")

# Display stored data
if st.session_state.form_data:
    st.subheader("Stored Data")
    st.json(st.session_state.form_data)
```

### Form Reset

```python
import streamlit as st

with st.form("reset_form"):
    name = st.text_input("Name")
    email = st.text_input("Email")
    
    col1, col2 = st.columns(2)
    with col1:
        submitted = st.form_submit_button("Submit")
    with col2:
        reset = st.form_submit_button("Reset")
    
    if submitted:
        st.success("Form submitted!")
    
    if reset:
        st.session_state.form_data = {}
        st.info("Form reset")
```

## Best Practices for Form Design

### 1. Clear Labels and Help Text

```python
import streamlit as st

with st.form("clear_form"):
    name = st.text_input(
        "Full Name *",
        help="Enter your first and last name",
        placeholder="John Doe"
    )
    
    email = st.text_input(
        "Email Address *",
        help="We'll never share your email",
        placeholder="john@example.com"
    )
    
    submitted = st.form_submit_button("Submit")
```

### 2. Logical Grouping

```python
import streamlit as st

with st.form("grouped_form"):
    st.subheader("Personal Information")
    name = st.text_input("Name")
    email = st.text_input("Email")
    
    st.subheader("Preferences")
    theme = st.selectbox("Theme", ["Light", "Dark"])
    language = st.selectbox("Language", ["English", "Spanish"])
    
    submitted = st.form_submit_button("Submit")
```

### 3. Visual Feedback

```python
import streamlit as st

with st.form("visual_form"):
    name = st.text_input("Name")
    
    submitted = st.form_submit_button("Submit", type="primary")
    
    if submitted:
        if name:
            st.success("✅ Form submitted!")
            st.balloons()
        else:
            st.error("❌ Please enter a name")
```

## Practical Examples

### Example 1: Contact Form

```python
import streamlit as st
import re

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

st.title("Contact Us")

with st.form("contact_form"):
    name = st.text_input("Name *")
    email = st.text_input("Email *")
    subject = st.selectbox("Subject", ["General", "Support", "Sales"])
    message = st.text_area("Message *", height=150)
    
    submitted = st.form_submit_button("Send Message", type="primary")
    
    if submitted:
        errors = []
        
        if not name:
            errors.append("Name is required")
        if not email:
            errors.append("Email is required")
        elif not validate_email(email):
            errors.append("Invalid email format")
        if not message:
            errors.append("Message is required")
        
        if errors:
            for error in errors:
                st.error(error)
        else:
            st.success("Message sent successfully!")
            # Send email or save to database
```

### Example 2: Survey Form

```python
import streamlit as st

st.title("Customer Survey")

with st.form("survey_form"):
    st.subheader("About You")
    age_range = st.selectbox("Age Range", ["18-25", "26-35", "36-45", "46+"])
    location = st.text_input("Location")
    
    st.subheader("Your Experience")
    rating = st.slider("Overall Rating", 1, 5, 3)
    would_recommend = st.radio("Would you recommend us?", ["Yes", "No", "Maybe"])
    feedback = st.text_area("Additional Feedback")
    
    submitted = st.form_submit_button("Submit Survey")
    
    if submitted:
        survey_data = {
            "age_range": age_range,
            "location": location,
            "rating": rating,
            "would_recommend": would_recommend,
            "feedback": feedback
        }
        
        # Store survey data
        if "surveys" not in st.session_state:
            st.session_state.surveys = []
        st.session_state.surveys.append(survey_data)
        
        st.success("Thank you for your feedback!")
        st.balloons()
```

## Common Pitfalls

### Pitfall 1: Widgets Outside Form

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

### Pitfall 2: Not Validating Input

**Problem:**
```python
with st.form("my_form"):
    email = st.text_input("Email")
    submitted = st.form_submit_button("Submit")
    if submitted:
        send_email(email)  # No validation!
```

**Solution:**
```python
with st.form("my_form"):
    email = st.text_input("Email")
    submitted = st.form_submit_button("Submit")
    if submitted:
        if validate_email(email):
            send_email(email)
        else:
            st.error("Invalid email")
```

## Next Steps

Now that you can create forms:

- [Multi-page Apps](./13-multi-page-apps.md) - Organize forms across pages
- [Best Practices](./19-best-practices.md) - More form design tips

## References

- [Forms API](https://docs.streamlit.io/develop/api-reference/control-flow/st.form)
- [Form Submit Button](https://docs.streamlit.io/develop/api-reference/widgets/st.form_submit_button)

