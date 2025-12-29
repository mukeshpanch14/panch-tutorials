# Working with Data - Deep Dive

## Overview

This guide covers loading data from various sources, manipulating data with Pandas, filtering and transformation, real-time updates, data validation, API integration, and database connections in Streamlit apps.

## Loading Data

### CSV Files

```python
import streamlit as st
import pandas as pd

# Load from file
@st.cache_data
def load_csv(file_path):
    return pd.read_csv(file_path)

df = load_csv("data.csv")
st.dataframe(df)

# Load from uploaded file
uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.dataframe(df)
```

### Excel Files

```python
import streamlit as st
import pandas as pd

# Load Excel file
@st.cache_data
def load_excel(file_path, sheet_name=0):
    return pd.read_excel(file_path, sheet_name=sheet_name)

df = load_excel("data.xlsx", sheet_name="Sheet1")
st.dataframe(df)

# Load from uploaded file
uploaded_file = st.file_uploader("Upload Excel", type=["xlsx", "xls"])
if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.dataframe(df)
```

### JSON Files

```python
import streamlit as st
import pandas as pd
import json

# Load JSON file
@st.cache_data
def load_json(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

data = load_json("data.json")
st.json(data)

# Convert JSON to DataFrame
df = pd.json_normalize(data)
st.dataframe(df)
```

### Database Connections

#### SQLite

```python
import streamlit as st
import pandas as pd
import sqlite3

@st.cache_resource
def get_connection():
    return sqlite3.connect("database.db")

@st.cache_data
def load_from_db(query):
    conn = get_connection()
    return pd.read_sql_query(query, conn)

query = "SELECT * FROM users"
df = load_from_db(query)
st.dataframe(df)
```

#### PostgreSQL

```python
import streamlit as st
import pandas as pd
import psycopg2

@st.cache_resource
def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="mydb",
        user="user",
        password="password"
    )

@st.cache_data
def load_from_db(query):
    conn = get_connection()
    return pd.read_sql_query(query, conn)

df = load_from_db("SELECT * FROM users")
st.dataframe(df)
```

## Data Manipulation with Pandas

### Basic Operations

```python
import streamlit as st
import pandas as pd

df = pd.read_csv("data.csv")

# Display basic info
st.subheader("Data Info")
st.write(f"Shape: {df.shape}")
st.write(f"Columns: {list(df.columns)}")

# Display statistics
st.subheader("Statistics")
st.dataframe(df.describe())

# Display head/tail
col1, col2 = st.columns(2)
with col1:
    st.subheader("First 5 rows")
    st.dataframe(df.head())
with col2:
    st.subheader("Last 5 rows")
    st.dataframe(df.tail())
```

### Filtering Data

```python
import streamlit as st
import pandas as pd

df = pd.read_csv("data.csv")

# Filter by column value
category = st.selectbox("Category", df["category"].unique())
filtered_df = df[df["category"] == category]
st.dataframe(filtered_df)

# Multiple filters
min_value = st.slider("Min Value", 0, 100, 0)
max_value = st.slider("Max Value", 0, 100, 100)

filtered_df = df[
    (df["value"] >= min_value) & 
    (df["value"] <= max_value)
]
st.dataframe(filtered_df)
```

### Data Transformation

```python
import streamlit as st
import pandas as pd

df = pd.read_csv("data.csv")

# Group by
grouped = df.groupby("category").agg({
    "sales": "sum",
    "quantity": "mean"
})
st.dataframe(grouped)

# Pivot table
pivot = df.pivot_table(
    values="sales",
    index="category",
    columns="month",
    aggfunc="sum"
)
st.dataframe(pivot)

# Merge dataframes
df2 = pd.read_csv("data2.csv")
merged = pd.merge(df, df2, on="id")
st.dataframe(merged)
```

## Real-time Data Updates

### Auto-refresh

```python
import streamlit as st
import pandas as pd
import time

# Auto-refresh every 5 seconds
if st.button("Start Auto-refresh"):
    placeholder = st.empty()
    while True:
        # Fetch latest data
        df = pd.read_csv("data.csv")
        placeholder.dataframe(df)
        time.sleep(5)
```

### Manual Refresh

```python
import streamlit as st
import pandas as pd

if "last_refresh" not in st.session_state:
    st.session_state.last_refresh = None

if st.button("Refresh Data"):
    df = pd.read_csv("data.csv")
    st.session_state.data = df
    st.session_state.last_refresh = time.time()
    st.success("Data refreshed!")

if "data" in st.session_state:
    st.dataframe(st.session_state.data)
    if st.session_state.last_refresh:
        st.caption(f"Last refreshed: {st.session_state.last_refresh}")
```

## Data Validation and Error Handling

### Input Validation

```python
import streamlit as st
import pandas as pd

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        
        # Validate required columns
        required_columns = ["name", "email", "age"]
        missing = [col for col in required_columns if col not in df.columns]
        
        if missing:
            st.error(f"Missing required columns: {missing}")
        else:
            # Validate data types
            if not pd.api.types.is_numeric_dtype(df["age"]):
                st.error("Age must be numeric")
            else:
                st.success("Data is valid!")
                st.dataframe(df)
                
    except Exception as e:
        st.error(f"Error loading file: {str(e)}")
```

### Data Cleaning

```python
import streamlit as st
import pandas as pd

df = pd.read_csv("data.csv")

# Show data quality
st.subheader("Data Quality")
st.write(f"Missing values: {df.isnull().sum().sum()}")
st.write(f"Duplicate rows: {df.duplicated().sum()}")

# Clean data
if st.button("Clean Data"):
    # Remove duplicates
    df_clean = df.drop_duplicates()
    
    # Fill missing values
    df_clean = df_clean.fillna(0)
    
    # Remove outliers (example)
    Q1 = df_clean["value"].quantile(0.25)
    Q3 = df_clean["value"].quantile(0.75)
    IQR = Q3 - Q1
    df_clean = df_clean[
        (df_clean["value"] >= Q1 - 1.5*IQR) & 
        (df_clean["value"] <= Q3 + 1.5*IQR)
    ]
    
    st.success("Data cleaned!")
    st.dataframe(df_clean)
```

## Working with APIs

### Fetching API Data

```python
import streamlit as st
import requests
import pandas as pd

@st.cache_data(ttl=300)
def fetch_api_data(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

url = st.text_input("API URL")
if url:
    try:
        data = fetch_api_data(url)
        df = pd.json_normalize(data)
        st.dataframe(df)
    except Exception as e:
        st.error(f"Error fetching data: {str(e)}")
```

### REST API Integration

```python
import streamlit as st
import requests
import pandas as pd

API_BASE_URL = "https://api.example.com"

@st.cache_data(ttl=60)
def get_users():
    response = requests.get(f"{API_BASE_URL}/users")
    return response.json()

@st.cache_data(ttl=60)
def get_user(user_id):
    response = requests.get(f"{API_BASE_URL}/users/{user_id}")
    return response.json()

# Display users
users = get_users()
df = pd.DataFrame(users)
st.dataframe(df)

# Select user
selected_user = st.selectbox("Select User", df["id"])
if selected_user:
    user = get_user(selected_user)
    st.json(user)
```

## Database Connections

### SQLite Example

```python
import streamlit as st
import pandas as pd
import sqlite3

@st.cache_resource
def get_db_connection():
    return sqlite3.connect("app.db")

def execute_query(query, params=None):
    conn = get_db_connection()
    return pd.read_sql_query(query, conn, params=params)

# Query interface
query = st.text_area("SQL Query", "SELECT * FROM users LIMIT 10")

if st.button("Execute"):
    try:
        df = execute_query(query)
        st.dataframe(df)
    except Exception as e:
        st.error(f"Query error: {str(e)}")
```

### PostgreSQL Example

```python
import streamlit as st
import pandas as pd
import psycopg2
from sqlalchemy import create_engine

@st.cache_resource
def get_engine():
    return create_engine("postgresql://user:password@localhost/dbname")

def load_table(table_name):
    engine = get_engine()
    return pd.read_sql_table(table_name, engine)

table_name = st.selectbox("Table", ["users", "orders", "products"])
if table_name:
    df = load_table(table_name)
    st.dataframe(df)
```

## Practical Examples

### Example 1: Data Explorer

```python
import streamlit as st
import pandas as pd

st.title("Data Explorer")

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    # Filters
    st.sidebar.header("Filters")
    columns = st.sidebar.multiselect("Select Columns", df.columns)
    
    if columns:
        filtered_df = df[columns]
        
        # Operations
        operation = st.selectbox("Operation", ["View", "Statistics", "Group By"])
        
        if operation == "View":
            st.dataframe(filtered_df)
        elif operation == "Statistics":
            st.dataframe(filtered_df.describe())
        elif operation == "Group By":
            group_col = st.selectbox("Group By", filtered_df.columns)
            agg_col = st.selectbox("Aggregate", filtered_df.columns)
            grouped = filtered_df.groupby(group_col)[agg_col].sum()
            st.dataframe(grouped)
```

### Example 2: Database Query Interface

```python
import streamlit as st
import pandas as pd
import sqlite3

@st.cache_resource
def get_connection():
    return sqlite3.connect("database.db")

st.title("Database Query Interface")

# Table selector
conn = get_connection()
tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table'", conn)
table_name = st.selectbox("Table", tables["name"])

if table_name:
    # Show table data
    df = pd.read_sql(f"SELECT * FROM {table_name} LIMIT 100", conn)
    st.dataframe(df)
    
    # Custom query
    st.subheader("Custom Query")
    query = st.text_area("SQL Query")
    if st.button("Execute"):
        try:
            result = pd.read_sql(query, conn)
            st.dataframe(result)
        except Exception as e:
            st.error(f"Error: {str(e)}")
```

## Best Practices

1. **Cache data loading**: Use `@st.cache_data` for expensive operations
2. **Validate input**: Always validate user input and file uploads
3. **Handle errors**: Use try-except blocks for robust error handling
4. **Use connection pooling**: Cache database connections with `@st.cache_resource`
5. **Optimize queries**: Only fetch needed data

## Next Steps

Now that you can work with data:

- [Forms and Validation](./12-forms-validation.md) - Create data entry forms
- [Deployment](./17-deployment-production.md) - Deploy your data apps

## References

- [Pandas Documentation](https://pandas.pydata.org/)
- [SQLite Documentation](https://docs.python.org/3/library/sqlite3.html)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

