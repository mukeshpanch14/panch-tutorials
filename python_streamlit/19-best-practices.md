# Best Practices and Design Patterns - Deep Dive

## Overview

This guide covers industry best practices for building maintainable, scalable, and production-ready Streamlit applications including code organization, component reusability, naming conventions, documentation, security, accessibility, and testing strategies.

## Code Organization and Structure

### Project Structure

```
my_streamlit_app/
├── app.py                 # Main application
├── pages/                 # Multi-page app pages
│   ├── 1_Home.py
│   └── 2_Dashboard.py
├── utils/                 # Utility functions
│   ├── __init__.py
│   ├── data_loader.py
│   ├── processors.py
│   └── visualizers.py
├── config/                # Configuration files
│   └── settings.py
├── data/                  # Data files
│   └── sample_data.csv
├── tests/                 # Test files
│   └── test_app.py
├── .streamlit/            # Streamlit config
│   └── config.toml
├── requirements.txt       # Dependencies
└── README.md             # Documentation
```

### Modular Code

```python
# app.py - Main entry point
import streamlit as st
from utils.data_loader import load_data
from utils.processors import process_data
from utils.visualizers import create_chart

def main():
    st.set_page_config(page_title="My App", layout="wide")
    st.title("My Streamlit App")
    
    data = load_data()
    processed = process_data(data)
    chart = create_chart(processed)
    st.plotly_chart(chart)

if __name__ == "__main__":
    main()
```

```python
# utils/data_loader.py
import pandas as pd
import streamlit as st

@st.cache_data
def load_data(file_path="data/sample.csv"):
    return pd.read_csv(file_path)
```

```python
# utils/processors.py
def process_data(df):
    return df.groupby("category").sum()
```

```python
# utils/visualizers.py
import plotly.express as px

def create_chart(df):
    return px.bar(df, x="category", y="value")
```

## Component Reusability

### Reusable Functions

```python
import streamlit as st

def metric_card(title, value, delta=None, delta_color="normal"):
    """Reusable metric card component"""
    st.metric(title, value, delta, delta_color)

# Use in app
col1, col2, col3 = st.columns(3)
with col1:
    metric_card("Revenue", "$100K", "+10%")
with col2:
    metric_card("Users", "1,234", "+5%")
with col3:
    metric_card("Growth", "5%", "-2%")
```

### Reusable Layout Components

```python
import streamlit as st

def sidebar_filters():
    """Reusable sidebar filter component"""
    st.sidebar.header("Filters")
    category = st.sidebar.selectbox("Category", ["All", "A", "B", "C"])
    date_range = st.sidebar.date_input("Date Range")
    return category, date_range

def dashboard_header(title):
    """Reusable dashboard header"""
    st.title(title)
    st.markdown("---")

# Use in app
dashboard_header("Sales Dashboard")
category, date_range = sidebar_filters()
```

### Class-Based Components

```python
import streamlit as st

class DataExplorer:
    def __init__(self, data):
        self.data = data
    
    def display_summary(self):
        st.subheader("Summary")
        st.write(f"Shape: {self.data.shape}")
        st.dataframe(self.data.describe())
    
    def display_chart(self, x_col, y_col):
        import plotly.express as px
        fig = px.scatter(self.data, x=x_col, y=y_col)
        st.plotly_chart(fig)

# Use in app
df = load_data()
explorer = DataExplorer(df)
explorer.display_summary()
explorer.display_chart("x", "y")
```

## Naming Conventions

### Functions and Variables

```python
# Good naming
def load_sales_data():
    pass

def calculate_total_revenue():
    pass

user_name = "John"
total_sales = 1000

# Bad naming
def load():
    pass

def calc():
    pass

n = "John"
x = 1000
```

### File Names

```
# Good
data_loader.py
sales_processor.py
dashboard_utils.py

# Bad
dl.py
sp.py
utils.py
```

### Constants

```python
# Good
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
DEFAULT_TIMEOUT = 30
API_BASE_URL = "https://api.example.com"

# Bad
maxFileSize = 10 * 1024 * 1024
default_timeout = 30
apiBaseUrl = "https://api.example.com"
```

## Documentation and Comments

### Docstrings

```python
def load_data(file_path, cache=True):
    """
    Load data from a CSV file.
    
    Parameters:
    -----------
    file_path : str
        Path to the CSV file
    cache : bool, optional
        Whether to cache the result (default: True)
    
    Returns:
    --------
    pandas.DataFrame
        Loaded data as a DataFrame
    
    Raises:
    -------
    FileNotFoundError
        If the file doesn't exist
    """
    import pandas as pd
    return pd.read_csv(file_path)
```

### Inline Comments

```python
# Calculate total revenue by summing all sales
total_revenue = sales_df['amount'].sum()

# Filter data for the last 30 days
recent_data = df[df['date'] >= (datetime.now() - timedelta(days=30))]
```

### README Documentation

```markdown
# My Streamlit App

## Description
A data visualization dashboard for sales analytics.

## Installation
```bash
pip install -r requirements.txt
```

## Usage
```bash
streamlit run app.py
```

## Features
- Sales dashboard
- Data filtering
- Interactive charts

## Configuration
Set environment variables in `.streamlit/secrets.toml`
```

## Version Control Best Practices

### .gitignore

```
# Python
__pycache__/
*.py[cod]
*.so
.Python
venv/
env/

# Streamlit
.streamlit/secrets.toml

# Data
*.csv
*.xlsx
data/

# IDE
.vscode/
.idea/
*.swp
```

### Commit Messages

```
# Good
feat: Add data filtering functionality
fix: Resolve session state initialization bug
docs: Update README with installation instructions

# Bad
update
fix
changes
```

## Security Considerations

### Secrets Management

```python
import streamlit as st
import os

# Good: Use secrets
api_key = st.secrets.get("API_KEY")
database_url = st.secrets.get("DATABASE_URL")

# Bad: Hardcoded
api_key = "my-secret-key"  # Never do this!
```

### Input Validation

```python
import streamlit as st
import re

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

email = st.text_input("Email")
if email and not validate_email(email):
    st.error("Invalid email format")
```

### SQL Injection Prevention

```python
import streamlit as st
import sqlite3

# Good: Use parameterized queries
def get_user(user_id):
    conn = sqlite3.connect("db.sqlite")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

# Bad: String concatenation (vulnerable to SQL injection)
def get_user_bad(user_id):
    conn = sqlite3.connect("db.sqlite")
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")  # Dangerous!
    return cursor.fetchone()
```

## Accessibility

### Alt Text for Images

```python
import streamlit as st

# Good: Provide alt text
st.image("chart.png", caption="Sales chart showing monthly revenue")

# Better: Use markdown with alt text
st.markdown('![Sales Chart](chart.png "Monthly revenue chart")')
```

### Color Contrast

```python
import streamlit as st

# Good: High contrast
st.markdown("""
<style>
.high-contrast {
    color: #000000;
    background-color: #FFFFFF;
}
</style>
""", unsafe_allow_html=True)

# Bad: Low contrast
st.markdown("""
<style>
.low-contrast {
    color: #CCCCCC;
    background-color: #DDDDDD;
}
</style>
""", unsafe_allow_html=True)
```

### Keyboard Navigation

```python
import streamlit as st

# Use standard widgets that support keyboard navigation
name = st.text_input("Name")  # Keyboard accessible
option = st.selectbox("Option", ["A", "B", "C"])  # Keyboard accessible
```

## Performance Optimization Patterns

### Caching Strategy

```python
import streamlit as st

# Cache expensive operations
@st.cache_data(ttl=3600)
def load_large_dataset():
    return pd.read_csv("large_file.csv")

# Cache resources
@st.cache_resource
def load_ml_model():
    return pickle.load(open("model.pkl", "rb"))

# Don't cache functions with side effects
def save_data(data):
    # Don't cache this!
    with open("output.csv", "w") as f:
        f.write(data)
```

### Lazy Loading

```python
import streamlit as st

# Load data only when needed
if st.checkbox("Load Data"):
    df = load_data()  # Only loads when checkbox is checked
    st.dataframe(df)
```

### Efficient Data Processing

```python
import streamlit as st
import pandas as pd

# Process data in chunks for large datasets
def process_large_data(df, chunk_size=10000):
    results = []
    for chunk in pd.read_csv("large_file.csv", chunksize=chunk_size):
        processed = process_chunk(chunk)
        results.append(processed)
    return pd.concat(results, ignore_index=True)
```

## Testing Strategies

### Unit Testing

```python
import unittest
from utils.processors import process_data
import pandas as pd

class TestProcessors(unittest.TestCase):
    def test_process_data(self):
        df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
        result = process_data(df)
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 1)

if __name__ == "__main__":
    unittest.main()
```

### Integration Testing

```python
import pytest
from streamlit.testing.v1 import AppTest

def test_app():
    at = AppTest.from_file("app.py")
    at.run()
    
    # Test widget interactions
    at.text_input("name").input("John").run()
    assert "John" in str(at)
```

### Test Coverage

```bash
# Install coverage
pip install coverage

# Run tests with coverage
coverage run -m pytest tests/
coverage report
coverage html
```

## Code Review Checklist

- [ ] Code follows PEP 8 style guide
- [ ] Functions have docstrings
- [ ] No hardcoded secrets
- [ ] Error handling implemented
- [ ] Caching used appropriately
- [ ] Tests written for new features
- [ ] README updated
- [ ] No commented-out code
- [ ] Variable names are descriptive

## Common Anti-Patterns to Avoid

### Anti-Pattern 1: Global State

```python
# Bad: Global variables
counter = 0

def increment():
    global counter
    counter += 1

# Good: Session state
if "counter" not in st.session_state:
    st.session_state.counter = 0

def increment():
    st.session_state.counter += 1
```

### Anti-Pattern 2: Not Caching Expensive Operations

```python
# Bad: Runs every rerun
def load_data():
    return pd.read_csv("large_file.csv")  # Slow!

# Good: Cached
@st.cache_data
def load_data():
    return pd.read_csv("large_file.csv")  # Cached!
```

### Anti-Pattern 3: Too Much Logic in Main

```python
# Bad: Everything in main
def main():
    # 200 lines of code here
    pass

# Good: Modular
def main():
    data = load_data()
    processed = process_data(data)
    display_results(processed)
```

## Next Steps

Now that you know best practices:

- [Real-World Projects](./20-real-world-projects.md) - Apply these practices
- Review your code: Refactor using these patterns

## References

- [PEP 8 Style Guide](https://pep8.org/)
- [Python Best Practices](https://docs.python-guide.org/writing/style/)
- [Streamlit Best Practices](https://docs.streamlit.io/develop/concepts/best-practices)

