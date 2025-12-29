"""
Streamlit Comprehensive Demo App
This app demonstrates most features covered in the Python + Streamlit course
with mock data and interactive examples.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from datetime import datetime, date, timedelta
import time
import json

# Page configuration
st.set_page_config(
    page_title="Streamlit Demo App",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if "counter" not in st.session_state:
    st.session_state.counter = 0
if "cart_items" not in st.session_state:
    st.session_state.cart_items = []
if "user_data" not in st.session_state:
    st.session_state.user_data = {}

# Generate mock data
@st.cache_data
def generate_sales_data():
    """Generate mock sales data"""
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
    np.random.seed(42)
    data = {
        'date': dates,
        'sales': np.random.normal(1000, 200, len(dates)),
        'quantity': np.random.randint(10, 100, len(dates)),
        'category': np.random.choice(['Electronics', 'Clothing', 'Food', 'Books'], len(dates)),
        'region': np.random.choice(['North', 'South', 'East', 'West'], len(dates))
    }
    df = pd.DataFrame(data)
    df['sales'] = df['sales'].abs()  # Ensure positive values
    return df

@st.cache_data
def generate_user_data():
    """Generate mock user data"""
    np.random.seed(42)
    data = {
        'user_id': range(1, 101),
        'name': [f'User {i}' for i in range(1, 101)],
        'age': np.random.randint(18, 65, 100),
        'city': np.random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'], 100),
        'score': np.random.normal(75, 15, 100),
        'active': np.random.choice([True, False], 100, p=[0.7, 0.3])
    }
    df = pd.DataFrame(data)
    df['score'] = df['score'].clip(0, 100)  # Keep scores between 0-100
    return df

# Load mock data
sales_df = generate_sales_data()
users_df = generate_user_data()

# Main App
st.title("🚀 Streamlit Comprehensive Demo App")
st.markdown("This app demonstrates various Streamlit features with mock data")

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select Demo",
    [
        "📊 Dashboard",
        "📝 Forms & Inputs",
        "📈 Data Visualization",
        "🔄 Session State",
        "⚡ Caching Demo",
        "📱 Layout Examples",
        "🎨 Advanced Features",
        "📁 File Operations"
    ]
)

# ============================================================================
# PAGE 1: DASHBOARD
# ============================================================================
if page == "📊 Dashboard":
    st.header("📊 Interactive Dashboard")
    
    # Filters in sidebar
    st.sidebar.subheader("Filters")
    selected_categories = st.sidebar.multiselect(
        "Categories",
        sales_df['category'].unique(),
        default=sales_df['category'].unique()
    )
    selected_regions = st.sidebar.multiselect(
        "Regions",
        sales_df['region'].unique(),
        default=sales_df['region'].unique()
    )
    date_range = st.sidebar.date_input(
        "Date Range",
        value=(sales_df['date'].min().date(), sales_df['date'].max().date()),
        min_value=sales_df['date'].min().date(),
        max_value=sales_df['date'].max().date()
    )
    
    # Apply filters
    filtered_df = sales_df[
        (sales_df['category'].isin(selected_categories)) &
        (sales_df['region'].isin(selected_regions))
    ]
    
    if isinstance(date_range, tuple) and len(date_range) == 2:
        filtered_df = filtered_df[
            (filtered_df['date'].dt.date >= date_range[0]) &
            (filtered_df['date'].dt.date <= date_range[1])
        ]
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Sales", f"${filtered_df['sales'].sum():,.0f}", 
                f"${filtered_df['sales'].sum() - sales_df['sales'].sum():,.0f}")
    col2.metric("Total Orders", f"{len(filtered_df):,}")
    col3.metric("Avg Order Value", f"${filtered_df['sales'].mean():,.2f}")
    col4.metric("Total Quantity", f"{filtered_df['quantity'].sum():,}")
    
    # Charts
    tab1, tab2, tab3 = st.tabs(["📈 Time Series", "📊 Category Analysis", "🗺️ Regional Analysis"])
    
    with tab1:
        st.subheader("Sales Over Time")
        daily_sales = filtered_df.groupby('date')['sales'].sum().reset_index()
        fig = px.line(daily_sales, x='date', y='sales', 
                     title="Daily Sales Trend")
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Sales by Category")
            category_sales = filtered_df.groupby('category')['sales'].sum().reset_index()
            fig = px.bar(category_sales, x='category', y='sales',
                        title="Total Sales by Category")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Category Distribution")
            fig = px.pie(filtered_df, names='category', values='sales',
                        title="Sales Distribution")
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("Regional Performance")
        regional_data = filtered_df.groupby('region').agg({
            'sales': 'sum',
            'quantity': 'sum'
        }).reset_index()
        fig = px.scatter(regional_data, x='quantity', y='sales', 
                        size='sales', color='region',
                        hover_data=['region'], title="Regional Sales vs Quantity")
        st.plotly_chart(fig, use_container_width=True)
    
    # Data table
    st.subheader("Filtered Data")
    st.dataframe(filtered_df.head(100), use_container_width=True)

# ============================================================================
# PAGE 2: FORMS & INPUTS
# ============================================================================
elif page == "📝 Forms & Inputs":
    st.header("📝 Forms and Input Widgets Demo")
    
    tab1, tab2, tab3 = st.tabs(["Basic Widgets", "Advanced Widgets", "Form Example"])
    
    with tab1:
        st.subheader("Basic Input Widgets")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Text Input**")
            name = st.text_input("Enter your name", placeholder="John Doe")
            if name:
                st.success(f"Hello, {name}!")
            
            st.write("**Text Area**")
            description = st.text_area("Description", placeholder="Enter description here...")
            
            st.write("**Number Input**")
            age = st.number_input("Age", min_value=0, max_value=120, value=25)
            
            st.write("**Slider**")
            price = st.slider("Price Range", 0.0, 1000.0, (100.0, 500.0))
            st.write(f"Selected range: ${price[0]:.2f} - ${price[1]:.2f}")
        
        with col2:
            st.write("**Date Input**")
            selected_date = st.date_input("Select a date", value=date.today())
            
            st.write("**Time Input**")
            selected_time = st.time_input("Select time", value=datetime.now().time())
            
            st.write("**Checkbox**")
            agree = st.checkbox("I agree to the terms", value=False)
            if agree:
                st.info("✓ Terms accepted")
            
            st.write("**Toggle**")
            dark_mode = st.toggle("Dark Mode", value=False)
            st.write(f"Dark mode: {'ON' if dark_mode else 'OFF'}")
    
    with tab2:
        st.subheader("Advanced Input Widgets")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Selectbox**")
            option = st.selectbox("Choose an option", ["Option 1", "Option 2", "Option 3"])
            st.write(f"Selected: {option}")
            
            st.write("**Multiselect**")
            colors = st.multiselect("Select colors", ["Red", "Green", "Blue", "Yellow"])
            if colors:
                st.write(f"Selected colors: {', '.join(colors)}")
            
            st.write("**Radio Buttons**")
            choice = st.radio("Choose one", ["Python", "JavaScript", "Java"])
            st.write(f"Favorite language: {choice}")
        
        with col2:
            st.write("**Color Picker**")
            color = st.color_picker("Pick a color", "#00f900")
            st.markdown(
                f'<div style="background-color: {color}; padding: 20px; border-radius: 5px; color: white;">'
                f'Selected Color: {color}</div>',
                unsafe_allow_html=True
            )
            
            st.write("**File Uploader**")
            uploaded_file = st.file_uploader("Upload a file", type=["csv", "txt"])
            if uploaded_file:
                st.success(f"File uploaded: {uploaded_file.name}")
                st.write(f"File size: {uploaded_file.size} bytes")
    
    with tab3:
        st.subheader("Form Example")
        
        with st.form("registration_form"):
            st.markdown("### Registration Form")
            
            col1, col2 = st.columns(2)
            with col1:
                first_name = st.text_input("First Name *")
                email = st.text_input("Email *")
                phone = st.text_input("Phone")
            
            with col2:
                last_name = st.text_input("Last Name *")
                birthday = st.date_input("Birthday", max_value=date.today())
                country = st.selectbox("Country", ["USA", "Canada", "UK", "Australia"])
            
            st.subheader("Preferences")
            newsletter = st.checkbox("Subscribe to newsletter")
            notifications = st.checkbox("Enable notifications")
            theme = st.selectbox("Theme", ["Light", "Dark", "Auto"])
            
            submitted = st.form_submit_button("Submit", type="primary")
            
            if submitted:
                errors = []
                if not first_name or not last_name:
                    errors.append("First and last name are required")
                if not email:
                    errors.append("Email is required")
                elif "@" not in email:
                    errors.append("Invalid email format")
                
                if errors:
                    for error in errors:
                        st.error(error)
                else:
                    st.success("✅ Registration successful!")
                    st.balloons()
                    st.json({
                        "first_name": first_name,
                        "last_name": last_name,
                        "email": email,
                        "phone": phone,
                        "birthday": str(birthday),
                        "country": country,
                        "newsletter": newsletter,
                        "notifications": notifications,
                        "theme": theme
                    })

# ============================================================================
# PAGE 3: DATA VISUALIZATION
# ============================================================================
elif page == "📈 Data Visualization":
    st.header("📈 Data Visualization Examples")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Native Charts", "Plotly", "Maps", "Custom"])
    
    with tab1:
        st.subheader("Streamlit Native Charts")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Line Chart**")
            chart_data = pd.DataFrame({
                'x': range(10),
                'y': np.random.randn(10)
            })
            st.line_chart(chart_data.set_index('x'))
        
        with col2:
            st.write("**Bar Chart**")
            bar_data = pd.DataFrame({
                'Category': ['A', 'B', 'C', 'D'],
                'Value': [10, 20, 30, 40]
            })
            st.bar_chart(bar_data.set_index('Category'))
        
        st.write("**Area Chart**")
        area_data = pd.DataFrame({
            'x': range(20),
            'Series A': np.random.randn(20).cumsum(),
            'Series B': np.random.randn(20).cumsum()
        })
        st.area_chart(area_data.set_index('x'))
    
    with tab2:
        st.subheader("Plotly Interactive Charts")
        
        chart_type = st.selectbox("Chart Type", ["Scatter", "Line", "Bar", "3D Scatter"])
        
        if chart_type == "Scatter":
            fig = px.scatter(users_df, x='age', y='score', color='active',
                           size='score', hover_data=['name', 'city'],
                           title="User Age vs Score")
            st.plotly_chart(fig, use_container_width=True)
        
        elif chart_type == "Line":
            daily_sales = sales_df.groupby('date')['sales'].sum().reset_index()
            fig = px.line(daily_sales, x='date', y='sales',
                         title="Sales Trend Over Time")
            st.plotly_chart(fig, use_container_width=True)
        
        elif chart_type == "Bar":
            category_sales = sales_df.groupby('category')['sales'].sum().reset_index()
            fig = px.bar(category_sales, x='category', y='sales',
                        title="Sales by Category")
            st.plotly_chart(fig, use_container_width=True)
        
        else:  # 3D Scatter
            fig = px.scatter_3d(users_df, x='age', y='score', z='user_id',
                               color='active', title="3D User Visualization")
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("Map Visualization")
        
        # Generate location data
        map_data = pd.DataFrame({
            'lat': [40.7128, 34.0522, 41.8781, 29.7604, 33.4484],
            'lon': [-74.0060, -118.2437, -87.6298, -95.3698, -112.0740],
            'city': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'],
            'sales': [1000, 800, 600, 500, 400]
        })
        
        st.map(map_data)
        st.dataframe(map_data)
    
    with tab4:
        st.subheader("Custom Visualizations")
        
        # Gauge chart
        st.write("**Gauge Chart**")
        value = st.slider("Gauge Value", 0, 100, 75)
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=value,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Performance"},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 100], 'color': "gray"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# PAGE 4: SESSION STATE
# ============================================================================
elif page == "🔄 Session State":
    st.header("🔄 Session State Demo")
    
    st.subheader("Counter Example")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Decrement"):
            st.session_state.counter -= 1
    
    with col2:
        st.metric("Counter", st.session_state.counter)
    
    with col3:
        if st.button("Increment"):
            st.session_state.counter += 1
    
    st.subheader("Shopping Cart Example")
    
    new_item = st.text_input("Add item to cart")
    col1, col2 = st.columns([3, 1])
    with col1:
        if st.button("Add to Cart"):
            if new_item:
                st.session_state.cart_items.append(new_item)
                st.success(f"Added: {new_item}")
                st.rerun()
    
    with col2:
        if st.button("Clear Cart"):
            st.session_state.cart_items = []
            st.rerun()
    
    if st.session_state.cart_items:
        st.write("**Cart Items:**")
        for i, item in enumerate(st.session_state.cart_items):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"{i+1}. {item}")
            with col2:
                if st.button("Remove", key=f"remove_{i}"):
                    st.session_state.cart_items.pop(i)
                    st.rerun()
    else:
        st.info("Cart is empty")
    
    st.subheader("User Data Storage")
    with st.form("user_data_form"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        submitted = st.form_submit_button("Save")
        
        if submitted:
            st.session_state.user_data = {
                "name": name,
                "email": email,
                "timestamp": datetime.now().isoformat()
            }
            st.success("Data saved to session state!")
    
    if st.session_state.user_data:
        st.write("**Stored Data:**")
        st.json(st.session_state.user_data)

# ============================================================================
# PAGE 5: CACHING DEMO
# ============================================================================
elif page == "⚡ Caching Demo":
    st.header("⚡ Caching Performance Demo")
    
    st.subheader("Data Caching (@st.cache_data)")
    
    @st.cache_data
    def expensive_operation(n):
        """Simulate expensive operation"""
        time.sleep(2)  # Simulate slow operation
        return sum(range(n))
    
    n = st.number_input("Enter a number", min_value=1, max_value=1000000, value=1000000)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Compute (Cached)"):
            start = time.time()
            result = expensive_operation(int(n))
            end = time.time()
            st.success(f"Result: {result}")
            st.info(f"Time taken: {end - start:.2f} seconds")
            st.caption("First run takes ~2 seconds, subsequent runs are instant!")
    
    with col2:
        if st.button("Clear Cache"):
            expensive_operation.clear()
            st.success("Cache cleared!")
    
    st.subheader("Resource Caching (@st.cache_resource)")
    
    @st.cache_resource
    def load_model():
        """Simulate loading a model"""
        time.sleep(1)
        return {"model_type": "ML Model", "version": "1.0"}
    
    if st.button("Load Model"):
        model = load_model()
        st.json(model)
        st.caption("Model is cached and reused across reruns")
    
    st.subheader("Cache Statistics")
    st.info("""
    **Cache Benefits:**
    - First call: Executes function and caches result
    - Subsequent calls: Returns cached result instantly
    - Use @st.cache_data for data (serializable)
    - Use @st.cache_resource for resources (non-serializable)
    """)

# ============================================================================
# PAGE 6: LAYOUT EXAMPLES
# ============================================================================
elif page == "📱 Layout Examples":
    st.header("📱 Layout and Container Examples")
    
    st.subheader("Columns")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Metric 1", "100", "10%")
    with col2:
        st.metric("Metric 2", "200", "5%")
    with col3:
        st.metric("Metric 3", "300", "-2%")
    
    st.subheader("Custom Column Widths")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.write("**Wide Column (2/3)**")
        st.dataframe(users_df.head(10))
    with col2:
        st.write("**Narrow Column (1/3)**")
        st.write("Additional content here")
    
    st.subheader("Expander")
    with st.expander("Click to expand"):
        st.write("This is hidden content that can be expanded.")
        st.dataframe(sales_df.head(5))
    
    st.subheader("Container")
    with st.container():
        st.write("Content in a container")
        st.bar_chart(pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]}))
    
    st.subheader("Tabs")
    tab1, tab2, tab3 = st.tabs(["Tab 1", "Tab 2", "Tab 3"])
    with tab1:
        st.write("Content in Tab 1")
    with tab2:
        st.write("Content in Tab 2")
    with tab3:
        st.write("Content in Tab 3")

# ============================================================================
# PAGE 7: ADVANCED FEATURES
# ============================================================================
elif page == "🎨 Advanced Features":
    st.header("🎨 Advanced Features Demo")
    
    tab1, tab2, tab3 = st.tabs(["Progress & Status", "Custom HTML/CSS", "Media"])
    
    with tab1:
        st.subheader("Progress Bar")
        progress_value = st.slider("Progress", 0, 100, 50)
        progress_bar = st.progress(progress_value / 100)
        st.write(f"Progress: {progress_value}%")
        
        st.subheader("Status Messages")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.success("Success message!")
        with col2:
            st.error("Error message!")
        with col3:
            st.warning("Warning message!")
        with col4:
            st.info("Info message!")
        
        st.subheader("Spinner")
        if st.button("Process Data"):
            with st.spinner("Processing..."):
                time.sleep(2)
            st.success("Done!")
        
        st.subheader("Balloons")
        if st.button("Celebrate!"):
            st.balloons()
    
    with tab2:
        st.subheader("Custom HTML/CSS")
        
        st.markdown("""
        <style>
        .custom-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            border-radius: 10px;
            color: white;
            margin: 10px 0;
        }
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="custom-box">
            <h2>Custom Styled Box</h2>
            <p>This is a custom HTML/CSS component</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.subheader("LaTeX Math")
        st.latex(r"E = mc^2")
        st.latex(r"\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}")
    
    with tab3:
        st.subheader("Image Display")
        # Generate a simple image using matplotlib
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3, 4], [1, 4, 2, 3])
        ax.set_xlabel("X Axis")
        ax.set_ylabel("Y Axis")
        ax.set_title("Sample Plot")
        st.pyplot(fig)
        plt.close(fig)  # Important: close figure to prevent memory issues
        
        st.subheader("Download Button")
        csv_data = users_df.to_csv(index=False)
        st.download_button(
            label="Download User Data as CSV",
            data=csv_data,
            file_name="users.csv",
            mime="text/csv"
        )

# ============================================================================
# PAGE 8: FILE OPERATIONS
# ============================================================================
elif page == "📁 File Operations":
    st.header("📁 File Operations Demo")
    
    tab1, tab2 = st.tabs(["Upload", "Download"])
    
    with tab1:
        st.subheader("File Upload")
        
        uploaded_file = st.file_uploader("Choose a file", type=["csv", "txt", "json"])
        
        if uploaded_file is not None:
            st.success(f"File uploaded: {uploaded_file.name}")
            st.write(f"File size: {uploaded_file.size} bytes")
            st.write(f"File type: {uploaded_file.type}")
            
            # Process based on file type
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
                st.dataframe(df)
                st.write(f"Shape: {df.shape}")
            
            elif uploaded_file.name.endswith('.txt'):
                text = uploaded_file.read().decode("utf-8")
                st.text_area("File Content", text, height=200)
            
            elif uploaded_file.name.endswith('.json'):
                data = json.load(uploaded_file)
                st.json(data)
    
    with tab2:
        st.subheader("File Download")
        
        # Download CSV
        st.write("**Download Sample Data**")
        csv_data = sales_df.to_csv(index=False)
        st.download_button(
            label="Download Sales Data (CSV)",
            data=csv_data,
            file_name="sales_data.csv",
            mime="text/csv"
        )
        
        # Download JSON
        json_data = users_df.head(10).to_json(orient='records', indent=2)
        st.download_button(
            label="Download User Data (JSON)",
            data=json_data,
            file_name="users.json",
            mime="application/json"
        )
        
        # Generate and download text
        text_data = "This is a sample text file.\nGenerated by Streamlit Demo App."
        st.download_button(
            label="Download Text File",
            data=text_data,
            file_name="sample.txt",
            mime="text/plain"
        )

# Footer
st.markdown("---")
st.markdown("**Streamlit Demo App** - Demonstrating comprehensive Streamlit features")
st.caption("This app showcases examples from the Python + Streamlit course")

