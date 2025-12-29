# Python + Streamlit Learning Plan

A structured, developer-focused guide to mastering **Python + Streamlit** for building interactive web applications and data science dashboards. Each section includes learning objectives, key concepts, practical examples, and official resources for deeper exploration.

## 1. Introduction to Streamlit

**Objective:**  
Understand what Streamlit is, why it's useful, and how it compares to other Python web frameworks.

**Key Concepts:**
- What is Streamlit: Python framework for building web apps
- Key features: rapid prototyping, data visualization, interactive widgets
- Streamlit vs Dash: differences and use cases
- Streamlit vs Flask/Django: when to use each
- Use cases: data science dashboards, web applications, ML model deployment
- Architecture: script-based execution, rerun model

**Example:**
```python
import streamlit as st

st.title("Hello Streamlit!")
st.write("This is my first Streamlit app")
```

**References:**
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Why Streamlit?](https://docs.streamlit.io/get-started)
- [Streamlit vs Other Frameworks](https://docs.streamlit.io/develop/tutorials)

**Deep Dive:** [View detailed guide](./01-introduction-streamlit.md)

---

## 2. Installation and Setup

**Objective:**  
Set up Streamlit in your development environment and create your first application.

**Key Concepts:**
- Installing Streamlit: pip and conda methods
- Creating your first Streamlit app
- Running apps locally: `streamlit run app.py`
- Project structure best practices
- Virtual environment setup
- IDE configuration: VS Code, PyCharm extensions

**Example:**
```bash
# Install Streamlit
pip install streamlit

# Run your app
streamlit run app.py
```

**References:**
- [Streamlit Installation](https://docs.streamlit.io/get-started/installation)
- [Quickstart Guide](https://docs.streamlit.io/get-started)

**Deep Dive:** [View detailed guide](./02-installation-setup.md)

---

## 3. Core Concepts and App Structure

**Objective:**  
Understand how Streamlit works internally and how to structure your applications effectively.

**Key Concepts:**
- How Streamlit works: rerun model and script execution
- Script execution model: top-to-bottom execution
- App lifecycle: initialization, reruns, cleanup
- Understanding state and reruns
- Basic app structure and organization
- Best practices for code organization

**Example:**
```python
import streamlit as st

# App runs from top to bottom on each interaction
st.title("My App")
name = st.text_input("Enter your name")
if name:
    st.write(f"Hello, {name}!")
```

**References:**
- [Streamlit Architecture](https://docs.streamlit.io/develop/concepts/architecture)
- [App Structure](https://docs.streamlit.io/develop/tutorials)

**Deep Dive:** [View detailed guide](./03-core-concepts.md)

---

## 4. Displaying Data and Text

**Objective:**  
Learn how to display text, data, and formatted content in your Streamlit apps.

**Key Concepts:**
- `st.write()` and magic commands
- Text elements: `st.title()`, `st.header()`, `st.subheader()`, `st.text()`, `st.markdown()`
- Displaying data: `st.dataframe()`, `st.table()`, `st.json()`
- Formatting and styling text with Markdown
- LaTeX and mathematical expressions

**Example:**
```python
import streamlit as st
import pandas as pd

st.title("Data Display")
st.header("Text Elements")
st.markdown("**Bold text** and *italic text*")

# Display data
df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
st.dataframe(df)
```

**References:**
- [Text Elements](https://docs.streamlit.io/develop/api-reference/text)
- [Data Display](https://docs.streamlit.io/develop/api-reference/data)

**Deep Dive:** [View detailed guide](./04-displaying-data.md)

---

## 5. User Input Widgets - Part 1

**Objective:**  
Master basic input widgets for collecting user data and interactions.

**Key Concepts:**
- Text input: `st.text_input()`, `st.text_area()`
- Numbers: `st.number_input()`, `st.slider()`
- Dates: `st.date_input()`, `st.time_input()`
- Buttons: `st.button()`, `st.download_button()`
- Checkbox and toggle: `st.checkbox()`, `st.toggle()`

**Example:**
```python
import streamlit as st

name = st.text_input("Enter your name")
age = st.slider("Select your age", 0, 100, 25)
birthday = st.date_input("Select your birthday")
if st.button("Submit"):
    st.write(f"Hello {name}, you are {age} years old!")
```

**References:**
- [Input Widgets](https://docs.streamlit.io/develop/api-reference/widgets)

**Deep Dive:** [View detailed guide](./05-input-widgets-basic.md)

---

## 6. User Input Widgets - Part 2

**Objective:**  
Learn advanced input widgets and form handling for complex user interactions.

**Key Concepts:**
- Selection widgets: `st.selectbox()`, `st.multiselect()`, `st.radio()`
- File uploader: `st.file_uploader()`
- Color picker: `st.color_picker()`
- Form handling: `st.form()` and form submission
- Widget behavior and callbacks

**Example:**
```python
import streamlit as st

option = st.selectbox("Choose an option", ["Option 1", "Option 2", "Option 3"])
colors = st.multiselect("Select colors", ["Red", "Green", "Blue"])
uploaded_file = st.file_uploader("Upload a file")
```

**References:**
- [Advanced Widgets](https://docs.streamlit.io/develop/api-reference/widgets)
- [Forms](https://docs.streamlit.io/develop/api-reference/control-flow/st.form)

**Deep Dive:** [View detailed guide](./06-input-widgets-advanced.md)

---

## 7. Layout and Containers

**Objective:**  
Organize your app's layout using sidebars, columns, containers, and tabs.

**Key Concepts:**
- Sidebar: `st.sidebar`
- Columns: `st.columns()`
- Containers: `st.container()`, `st.expander()`
- Tabs: `st.tabs()`
- Empty placeholders: `st.empty()`
- Layout best practices and responsive design

**Example:**
```python
import streamlit as st

# Sidebar
st.sidebar.title("Navigation")
st.sidebar.button("Home")

# Columns
col1, col2 = st.columns(2)
with col1:
    st.write("Column 1")
with col2:
    st.write("Column 2")

# Tabs
tab1, tab2 = st.tabs(["Tab 1", "Tab 2"])
```

**References:**
- [Layouts](https://docs.streamlit.io/develop/api-reference/layout)

**Deep Dive:** [View detailed guide](./07-layout-containers.md)

---

## 8. Data Visualization

**Objective:**  
Create interactive charts and visualizations using Streamlit's built-in and integrated plotting libraries.

**Key Concepts:**
- Charts: `st.line_chart()`, `st.bar_chart()`, `st.area_chart()`
- Plotly integration: `st.plotly_chart()`
- Matplotlib: `st.pyplot()`
- Altair: `st.altair_chart()`
- Vega-Lite: `st.vega_lite_chart()`
- Bokeh: `st.bokeh_chart()`
- Graphviz: `st.graphviz_chart()`
- Map visualization: `st.map()`
- Custom visualizations

**Example:**
```python
import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})
st.line_chart(df)
fig = px.scatter(df, x="x", y="y")
st.plotly_chart(fig)
```

**References:**
- [Charts](https://docs.streamlit.io/develop/api-reference/charts)
- [Plotly Integration](https://docs.streamlit.io/develop/api-reference/charts/st.plotly_chart)

**Deep Dive:** [View detailed guide](./08-data-visualization.md)

---

## 9. Session State and State Management

**Objective:**  
Manage application state across reruns to build interactive, stateful applications.

**Key Concepts:**
- Understanding `st.session_state`
- Initializing state
- Reading and writing state
- State persistence across reruns
- State management patterns
- Common state management pitfalls
- Building interactive apps with state

**Example:**
```python
import streamlit as st

# Initialize state
if "counter" not in st.session_state:
    st.session_state.counter = 0

# Use state
if st.button("Increment"):
    st.session_state.counter += 1

st.write(f"Counter: {st.session_state.counter}")
```

**References:**
- [Session State](https://docs.streamlit.io/develop/api-reference/execution-state/st.session_state)

**Deep Dive:** [View detailed guide](./09-session-state.md)

---

## 10. Caching and Performance Optimization

**Objective:**  
Optimize your Streamlit apps for performance using caching and best practices.

**Key Concepts:**
- `@st.cache_data` for data caching
- `@st.cache_resource` for resource caching
- Cache invalidation and TTL
- Performance best practices
- Handling large datasets
- Memory management
- Profiling and optimization

**Example:**
```python
import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    # Expensive operation
    return pd.read_csv("large_file.csv")

df = load_data()  # Cached after first run
```

**References:**
- [Caching](https://docs.streamlit.io/develop/api-reference/performance/st.cache_data)

**Deep Dive:** [View detailed guide](./10-caching-performance.md)

---

## 11. Working with Data

**Objective:**  
Load, manipulate, and work with various data sources in Streamlit applications.

**Key Concepts:**
- Loading data: CSV, Excel, JSON, databases
- Data manipulation with Pandas
- Data filtering and transformation
- Real-time data updates
- Data validation and error handling
- Working with APIs
- Database connections (SQLite, PostgreSQL, etc.)

**Example:**
```python
import streamlit as st
import pandas as pd

uploaded_file = st.file_uploader("Upload CSV", type="csv")
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.dataframe(df)
```

**References:**
- [Data Sources](https://docs.streamlit.io/develop/tutorials/databases)

**Deep Dive:** [View detailed guide](./11-working-with-data.md)

---

## 12. Forms and User Input Validation

**Objective:**  
Create forms with validation and proper error handling for user input.

**Key Concepts:**
- Creating forms with `st.form()`
- Form submission handling
- Input validation patterns
- Error handling and user feedback
- Multi-step forms
- Form state management
- Best practices for form design

**Example:**
```python
import streamlit as st

with st.form("my_form"):
    name = st.text_input("Name")
    email = st.text_input("Email")
    submitted = st.form_submit_button("Submit")
    
    if submitted:
        if name and email:
            st.success("Form submitted!")
        else:
            st.error("Please fill all fields")
```

**References:**
- [Forms](https://docs.streamlit.io/develop/api-reference/control-flow/st.form)

**Deep Dive:** [View detailed guide](./12-forms-validation.md)

---

## 13. Multi-page Apps

**Objective:**  
Build multi-page applications with navigation and shared state.

**Key Concepts:**
- Pages API: `st.set_page_config()`
- Creating multiple pages
- Navigation between pages
- Page routing and organization
- Sharing state across pages
- Building complex multi-page applications
- Navigation patterns

**Example:**
```python
# pages/1_Home.py
import streamlit as st
st.set_page_config(page_title="Home", page_icon="🏠")
st.title("Home Page")

# pages/2_About.py
import streamlit as st
st.set_page_config(page_title="About", page_icon="ℹ️")
st.title("About Page")
```

**References:**
- [Multi-page Apps](https://docs.streamlit.io/develop/api-reference/utilities/st.set_page_config)

**Deep Dive:** [View detailed guide](./13-multi-page-apps.md)

---

## 14. Advanced Features

**Objective:**  
Explore advanced Streamlit features for custom components and enhanced functionality.

**Key Concepts:**
- Custom components
- Streamlit Components API
- JavaScript integration
- Custom HTML/CSS
- Theming and customization
- Custom metrics and KPIs
- Progress bars and status indicators
- Spinners and loading states

**Example:**
```python
import streamlit as st
import time

with st.spinner("Loading..."):
    time.sleep(2)
st.success("Done!")

progress_bar = st.progress(0)
for i in range(100):
    progress_bar.progress(i + 1)
```

**References:**
- [Advanced Features](https://docs.streamlit.io/develop/api-reference/status)
- [Custom Components](https://docs.streamlit.io/develop/components)

**Deep Dive:** [View detailed guide](./14-advanced-features.md)

---

## 15. Media and File Handling

**Objective:**  
Handle images, audio, video, and file operations in your Streamlit apps.

**Key Concepts:**
- Images: `st.image()`
- Audio: `st.audio()`
- Video: `st.video()`
- File uploads and processing
- File downloads
- Working with different file formats
- Media optimization

**Example:**
```python
import streamlit as st

st.image("image.jpg", caption="My Image")
st.audio("audio.mp3")
st.video("video.mp4")

uploaded_file = st.file_uploader("Upload file")
if uploaded_file:
    st.download_button("Download", uploaded_file)
```

**References:**
- [Media Elements](https://docs.streamlit.io/develop/api-reference/media)

**Deep Dive:** [View detailed guide](./15-media-files.md)

---

## 16. Error Handling and Debugging

**Objective:**  
Implement proper error handling and debugging strategies for Streamlit applications.

**Key Concepts:**
- Exception handling in Streamlit
- Error messages and user feedback
- Debugging techniques
- Logging in Streamlit apps
- Common errors and solutions
- Testing Streamlit apps
- Debug mode and troubleshooting

**Example:**
```python
import streamlit as st

try:
    result = 10 / 0
except ZeroDivisionError:
    st.error("Division by zero error!")
    st.exception("Full error details")
```

**References:**
- [Error Handling](https://docs.streamlit.io/develop/api-reference/status/st.error)

**Deep Dive:** [View detailed guide](./16-error-handling-debugging.md)

---

## 17. Deployment and Production

**Objective:**  
Deploy Streamlit applications to production environments and cloud platforms.

**Key Concepts:**
- Streamlit Cloud deployment
- Deploying to Heroku
- Docker containerization
- AWS deployment (EC2, ECS, App Runner)
- Azure deployment
- Google Cloud deployment
- Environment variables and secrets
- Production best practices
- Monitoring and logging

**Example:**
```dockerfile
# Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "app.py", "--server.port=8501"]
```

**References:**
- [Deployment](https://docs.streamlit.io/cloud)
- [Docker Deployment](https://docs.streamlit.io/develop/deploy/docker)

**Deep Dive:** [View detailed guide](./17-deployment-production.md)

---

## 18. Integration with External Services

**Objective:**  
Integrate Streamlit apps with databases, APIs, authentication, and cloud services.

**Key Concepts:**
- Database connections
- API integrations
- Authentication and authorization
- OAuth integration
- Email and notifications
- Cloud storage (S3, GCS, Azure Blob)
- Message queues and background tasks

**Example:**
```python
import streamlit as st
import sqlite3

conn = sqlite3.connect("database.db")
df = pd.read_sql_query("SELECT * FROM users", conn)
st.dataframe(df)
```

**References:**
- [Database Connections](https://docs.streamlit.io/develop/tutorials/databases)
- [API Integration](https://docs.streamlit.io/develop/tutorials)

**Deep Dive:** [View detailed guide](./18-external-integrations.md)

---

## 19. Best Practices and Design Patterns

**Objective:**  
Apply industry best practices and design patterns for maintainable Streamlit applications.

**Key Concepts:**
- Code organization and structure
- Component reusability
- Naming conventions
- Documentation and comments
- Version control best practices
- Security considerations
- Accessibility
- Performance optimization patterns
- Testing strategies

**Example:**
```python
# Good structure
import streamlit as st
from utils import load_data, process_data

def main():
    st.title("My App")
    data = load_data()
    processed = process_data(data)
    st.dataframe(processed)

if __name__ == "__main__":
    main()
```

**References:**
- [Best Practices](https://docs.streamlit.io/develop/concepts/best-practices)

**Deep Dive:** [View detailed guide](./19-best-practices.md)

---

## 20. Real-World Projects and Use Cases

**Objective:**  
Apply all learned concepts through comprehensive real-world project examples.

**Examples:**
- Data science dashboard project
- ETL pipeline monitoring dashboard
- Machine learning model deployment
- Business intelligence dashboard
- Real-time monitoring app
- Interactive data exploration tool
- Form-based data collection app
- Complete project walkthroughs

**References:**
- [Streamlit Examples](https://docs.streamlit.io/develop/tutorials)
- [Community Examples](https://streamlit.io/gallery)

**Deep Dive:** [View detailed guide](./20-real-world-projects.md)

---

### Next Steps

You can use this guide as a self-paced learning roadmap or training material. For best results:
- Follow the order of topics progressively
- Practice each concept with hands-on exercises
- Build a portfolio of Streamlit projects
- Deploy your apps to share with others
- Contribute to the Streamlit community

---

**Author:** Developer Enablement  
**Version:** v1.0  
**Last Updated:** 2025

