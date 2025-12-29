# Real-World Projects and Use Cases - Deep Dive

## Overview

This guide provides complete walkthroughs of real-world Streamlit projects including data science dashboards, ETL monitoring, ML model deployment, business intelligence dashboards, and more.

## Project 1: Data Science Dashboard

### Overview

A comprehensive dashboard for exploring and visualizing data science datasets.

### Implementation

```python
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Data Science Dashboard", layout="wide")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("data/sales.csv")

df = load_data()

# Sidebar filters
st.sidebar.header("Filters")
category = st.sidebar.multiselect("Category", df["category"].unique())
date_range = st.sidebar.date_input("Date Range", value=[df["date"].min(), df["date"].max()])

# Apply filters
filtered_df = df.copy()
if category:
    filtered_df = filtered_df[filtered_df["category"].isin(category)]

# Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Sales", f"${filtered_df['sales'].sum():,.0f}")
col2.metric("Orders", f"{len(filtered_df):,}")
col3.metric("Avg Order", f"${filtered_df['sales'].mean():,.2f}")
col4.metric("Growth", f"{filtered_df['sales'].pct_change().mean()*100:.1f}%")

# Charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("Sales Over Time")
    fig = px.line(filtered_df, x="date", y="sales", color="category")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Sales by Category")
    fig = px.bar(filtered_df.groupby("category")["sales"].sum().reset_index(), 
                 x="category", y="sales")
    st.plotly_chart(fig, use_container_width=True)

# Data table
st.subheader("Data Table")
st.dataframe(filtered_df, use_container_width=True)
```

## Project 2: ETL Pipeline Monitoring Dashboard

### Overview

Monitor ETL pipeline status, execution times, and data quality metrics.

### Implementation

```python
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

st.set_page_config(page_title="ETL Monitoring", layout="wide")

# Load pipeline runs
@st.cache_data(ttl=60)
def load_pipeline_runs():
    return pd.read_csv("data/pipeline_runs.csv")

df = load_pipeline_runs()

st.title("ETL Pipeline Monitoring")

# Status overview
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Runs", len(df))
col2.metric("Success Rate", f"{(df['status']=='success').sum()/len(df)*100:.1f}%")
col3.metric("Avg Duration", f"{df['duration'].mean():.2f}s")
col4.metric("Last Run", df['timestamp'].max())

# Status distribution
st.subheader("Status Distribution")
status_counts = df['status'].value_counts()
fig = px.pie(values=status_counts.values, names=status_counts.index)
st.plotly_chart(fig, use_container_width=True)

# Execution times
st.subheader("Execution Times")
fig = px.line(df, x="timestamp", y="duration", color="pipeline_name")
st.plotly_chart(fig, use_container_width=True)

# Recent runs
st.subheader("Recent Runs")
recent_runs = df.nlargest(10, "timestamp")
st.dataframe(recent_runs[["timestamp", "pipeline_name", "status", "duration"]])

# Pipeline selector
pipeline = st.selectbox("Select Pipeline", df["pipeline_name"].unique())
pipeline_data = df[df["pipeline_name"] == pipeline]

st.subheader(f"Pipeline: {pipeline}")
st.metric("Success Rate", f"{(pipeline_data['status']=='success').sum()/len(pipeline_data)*100:.1f}%")
st.metric("Avg Duration", f"{pipeline_data['duration'].mean():.2f}s")
```

## Project 3: Machine Learning Model Deployment

### Overview

Deploy and interact with machine learning models through a user-friendly interface.

### Implementation

```python
import streamlit as st
import pickle
import numpy as np
import pandas as pd

st.set_page_config(page_title="ML Model Deployment", layout="wide")

# Load model
@st.cache_resource
def load_model():
    with open("model.pkl", "rb") as f:
        return pickle.load(f)

model = load_model()

st.title("Machine Learning Model Deployment")

# Input form
st.subheader("Input Features")

col1, col2 = st.columns(2)

with col1:
    feature1 = st.number_input("Feature 1", value=0.0)
    feature2 = st.number_input("Feature 2", value=0.0)
    feature3 = st.number_input("Feature 3", value=0.0)

with col2:
    feature4 = st.number_input("Feature 4", value=0.0)
    feature5 = st.number_input("Feature 5", value=0.0)

# Prediction
if st.button("Predict", type="primary"):
    features = np.array([[feature1, feature2, feature3, feature4, feature5]])
    prediction = model.predict(features)
    probability = model.predict_proba(features)[0]
    
    st.subheader("Prediction")
    st.success(f"Predicted Class: {prediction[0]}")
    
    st.subheader("Probabilities")
    prob_df = pd.DataFrame({
        "Class": [f"Class {i}" for i in range(len(probability))],
        "Probability": probability
    })
    st.bar_chart(prob_df.set_index("Class"))

# Batch prediction
st.subheader("Batch Prediction")
uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    batch_df = pd.read_csv(uploaded_file)
    st.dataframe(batch_df)
    
    if st.button("Predict Batch"):
        predictions = model.predict(batch_df.values)
        batch_df["prediction"] = predictions
        st.dataframe(batch_df)
        
        st.download_button(
            label="Download Predictions",
            data=batch_df.to_csv(index=False),
            file_name="predictions.csv",
            mime="text/csv"
        )
```

## Project 4: Business Intelligence Dashboard

### Overview

A comprehensive BI dashboard with multiple views and interactive filters.

### Implementation

```python
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="BI Dashboard", layout="wide", initial_sidebar_state="expanded")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("data/business_data.csv")

df = load_data()

# Sidebar
st.sidebar.title("Filters")
date_range = st.sidebar.date_input("Date Range", value=[df["date"].min(), df["date"].max()])
region = st.sidebar.multiselect("Region", df["region"].unique())
product = st.sidebar.multiselect("Product", df["product"].unique())

# Apply filters
filtered_df = df.copy()
if region:
    filtered_df = filtered_df[filtered_df["region"].isin(region)]
if product:
    filtered_df = filtered_df[filtered_df["product"].isin(product)]

# Main dashboard
st.title("Business Intelligence Dashboard")

# KPI Row
col1, col2, col3, col4 = st.columns(4)
col1.metric("Revenue", f"${filtered_df['revenue'].sum():,.0f}", 
            f"${filtered_df['revenue'].sum() - df['revenue'].sum():,.0f}")
col2.metric("Orders", f"{len(filtered_df):,}")
col3.metric("Customers", f"{filtered_df['customer_id'].nunique():,}")
col4.metric("Avg Order Value", f"${filtered_df['revenue'].mean():,.2f}")

# Charts
tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Revenue", "Products", "Regions"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Revenue Trend")
        fig = px.line(filtered_df.groupby("date")["revenue"].sum().reset_index(),
                     x="date", y="revenue")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Orders by Region")
        fig = px.bar(filtered_df.groupby("region")["revenue"].sum().reset_index(),
                    x="region", y="revenue")
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Revenue Analysis")
    revenue_by_product = filtered_df.groupby("product")["revenue"].sum().sort_values(ascending=False)
    fig = px.bar(revenue_by_product.reset_index(), x="product", y="revenue")
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("Product Performance")
    product_metrics = filtered_df.groupby("product").agg({
        "revenue": "sum",
        "quantity": "sum"
    }).reset_index()
    st.dataframe(product_metrics)

with tab4:
    st.subheader("Regional Analysis")
    regional_data = filtered_df.groupby("region").agg({
        "revenue": "sum",
        "orders": "count"
    }).reset_index()
    fig = px.scatter(regional_data, x="orders", y="revenue", size="revenue",
                    hover_data=["region"])
    st.plotly_chart(fig, use_container_width=True)
```

## Project 5: Real-Time Monitoring App

### Overview

Monitor real-time data with auto-refresh and alerts.

### Implementation

```python
import streamlit as st
import pandas as pd
import plotly.express as px
import time
from datetime import datetime

st.set_page_config(page_title="Real-Time Monitor", layout="wide")

# Simulate real-time data
@st.cache_data(ttl=5)
def get_latest_data():
    # In production, this would fetch from API/database
    return pd.DataFrame({
        "timestamp": [datetime.now()],
        "value": [np.random.rand() * 100],
        "status": [np.random.choice(["OK", "Warning", "Error"])]
    })

st.title("Real-Time Monitoring")

# Auto-refresh toggle
auto_refresh = st.checkbox("Auto-refresh (5s)", value=False)

# Metrics
placeholder = st.empty()

if auto_refresh:
    while True:
        with placeholder.container():
            data = get_latest_data()
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Current Value", f"{data['value'].iloc[0]:.2f}")
            col2.metric("Status", data['status'].iloc[0])
            col3.metric("Last Update", data['timestamp'].iloc[0].strftime("%H:%M:%S"))
            
            # Status indicator
            status = data['status'].iloc[0]
            if status == "Error":
                st.error("⚠️ System Error Detected!")
            elif status == "Warning":
                st.warning("⚠️ Warning Condition")
            else:
                st.success("✓ System Normal")
        
        time.sleep(5)
        st.rerun()
else:
    data = get_latest_data()
    col1, col2, col3 = st.columns(3)
    col1.metric("Current Value", f"{data['value'].iloc[0]:.2f}")
    col2.metric("Status", data['status'].iloc[0])
    col3.metric("Last Update", data['timestamp'].iloc[0].strftime("%H:%M:%S"))
    
    if st.button("Refresh"):
        st.rerun()
```

## Project 6: Interactive Data Exploration Tool

### Overview

An interactive tool for exploring datasets with dynamic filtering and visualization.

### Implementation

```python
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Data Explorer", layout="wide")

st.title("Interactive Data Explorer")

# File upload
uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    # Data info
    st.subheader("Data Overview")
    col1, col2, col3 = st.columns(3)
    col1.metric("Rows", len(df))
    col2.metric("Columns", len(df.columns))
    col3.metric("Memory", f"{df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    
    # Column selector
    st.subheader("Column Analysis")
    selected_column = st.selectbox("Select Column", df.columns)
    
    if selected_column:
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("Statistics")
            st.dataframe(df[selected_column].describe())
        
        with col2:
            st.write("Value Counts")
            st.dataframe(df[selected_column].value_counts().head(10))
    
    # Visualization
    st.subheader("Visualization")
    
    chart_type = st.selectbox("Chart Type", ["Scatter", "Line", "Bar", "Histogram"])
    x_col = st.selectbox("X Axis", df.columns)
    y_col = st.selectbox("Y Axis", df.columns) if chart_type != "Histogram" else None
    
    if chart_type == "Scatter":
        fig = px.scatter(df, x=x_col, y=y_col)
    elif chart_type == "Line":
        fig = px.line(df, x=x_col, y=y_col)
    elif chart_type == "Bar":
        fig = px.bar(df, x=x_col, y=y_col)
    else:
        fig = px.histogram(df, x=x_col)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Data table
    st.subheader("Data Table")
    st.dataframe(df, use_container_width=True)
```

## Project 7: Form-Based Data Collection App

### Overview

A multi-step form for collecting and storing user data.

### Implementation

```python
import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="Data Collection", layout="centered")

# Initialize form state
if "form_step" not in st.session_state:
    st.session_state.form_step = 1
    st.session_state.form_data = {}

st.title("Data Collection Form")

# Step 1: Personal Information
if st.session_state.form_step == 1:
    st.subheader("Step 1: Personal Information")
    
    with st.form("step1"):
        name = st.text_input("Full Name *")
        email = st.text_input("Email *")
        phone = st.text_input("Phone")
        birthday = st.date_input("Birthday", max_value=date.today())
        
        submitted = st.form_submit_button("Next")
        
        if submitted:
            if name and email:
                st.session_state.form_data.update({
                    "name": name,
                    "email": email,
                    "phone": phone,
                    "birthday": str(birthday)
                })
                st.session_state.form_step = 2
                st.rerun()
            else:
                st.error("Name and email are required")

# Step 2: Additional Information
elif st.session_state.form_step == 2:
    st.subheader("Step 2: Additional Information")
    
    with st.form("step2"):
        occupation = st.text_input("Occupation")
        experience = st.slider("Years of Experience", 0, 50, 0)
        skills = st.multiselect("Skills", ["Python", "SQL", "Excel", "Statistics"])
        
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
                "occupation": occupation,
                "experience": experience,
                "skills": ", ".join(skills)
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
            # Save to CSV
            df = pd.DataFrame([st.session_state.form_data])
            df.to_csv("submissions.csv", mode="a", header=not pd.io.common.file_exists("submissions.csv"), index=False)
            
            st.success("Form submitted successfully!")
            st.balloons()
            
            # Reset
            st.session_state.form_step = 1
            st.session_state.form_data = {}
            st.rerun()
```

## Best Practices for Real-World Projects

1. **Modular code**: Break projects into reusable components
2. **Error handling**: Always handle errors gracefully
3. **Caching**: Cache expensive operations
4. **Documentation**: Document your code and provide README
5. **Testing**: Write tests for critical functionality
6. **Performance**: Optimize for large datasets
7. **Security**: Protect sensitive data and APIs

## Next Steps

- Implement these projects: Start with simple ones and progress
- Customize: Adapt projects to your needs
- Deploy: Share your projects with others
- Contribute: Share your projects with the community

## References

- [Streamlit Gallery](https://streamlit.io/gallery) - More project examples
- [Streamlit Community](https://discuss.streamlit.io/) - Get help and share projects

