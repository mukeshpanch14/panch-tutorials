# Installation and Setup - Deep Dive

## Overview

This guide covers everything you need to set up Streamlit in your development environment, from installation to running your first application. We'll cover multiple installation methods, IDE configuration, and project structure best practices.

## Installing Streamlit

### Method 1: Using pip (Recommended)

The most common way to install Streamlit is using pip:

```bash
pip install streamlit
```

For Python 3, you might need to use `pip3`:

```bash
pip3 install streamlit
```

### Method 2: Using conda

If you're using Anaconda or Miniconda:

```bash
conda install -c conda-forge streamlit
```

Or using conda-forge channel:

```bash
conda install streamlit
```

### Method 3: Installing Specific Version

To install a specific version:

```bash
pip install streamlit==1.28.0
```

### Verifying Installation

After installation, verify it works:

```bash
streamlit --version
```

You should see the version number, e.g., `Streamlit, version 1.28.0`

## Virtual Environment Setup

### Why Use Virtual Environments?

Virtual environments isolate your project dependencies, preventing conflicts between different projects. This is a best practice for Python development.

### Creating a Virtual Environment

#### Using venv (Python 3.3+)

```bash
# Create virtual environment
python -m venv streamlit_env

# Activate on macOS/Linux
source streamlit_env/bin/activate

# Activate on Windows
streamlit_env\Scripts\activate
```

#### Using conda

```bash
# Create environment
conda create -n streamlit_env python=3.9

# Activate environment
conda activate streamlit_env
```

### Installing Streamlit in Virtual Environment

Once your virtual environment is activated:

```bash
pip install streamlit
```

### Creating requirements.txt

Create a `requirements.txt` file for your project:

```txt
streamlit==1.28.0
pandas==2.0.3
numpy==1.24.3
plotly==5.17.0
```

Install from requirements:

```bash
pip install -r requirements.txt
```

## Creating Your First Streamlit App

### Step 1: Create a Python File

Create a file named `app.py`:

```python
import streamlit as st

st.title("My First Streamlit App")
st.write("Hello, World!")
```

### Step 2: Run the App

```bash
streamlit run app.py
```

### Step 3: View Your App

Streamlit will:
- Start a local server (usually on `http://localhost:8501`)
- Automatically open your browser
- Display your app

### First Interactive App

Let's make it interactive:

```python
import streamlit as st

st.title("My First Streamlit App")

name = st.text_input("What's your name?")
if name:
    st.write(f"Hello, {name}!")
    
age = st.slider("How old are you?", 0, 100, 25)
st.write(f"You are {age} years old!")
```

## Running Apps Locally

### Basic Run Command

```bash
streamlit run app.py
```

### Running on Specific Port

```bash
streamlit run app.py --server.port 8502
```

### Running with Custom Server Address

```bash
streamlit run app.py --server.address 0.0.0.0
```

### Running in Headless Mode

For CI/CD or automated testing:

```bash
streamlit run app.py --server.headless true
```

### Command Line Options

Common options:

```bash
streamlit run app.py \
  --server.port 8501 \
  --server.address localhost \
  --server.headless false \
  --browser.gatherUsageStats false
```

## Project Structure Best Practices

### Recommended Structure

```
my_streamlit_app/
├── app.py                 # Main application file
├── pages/                 # Multi-page app pages
│   ├── 1_Home.py
│   ├── 2_Dashboard.py
│   └── 3_About.py
├── utils/                 # Utility functions
│   ├── __init__.py
│   ├── data_loader.py
│   └── helpers.py
├── data/                  # Data files
│   └── sample_data.csv
├── assets/                # Static assets
│   ├── images/
│   └── styles.css
├── requirements.txt       # Dependencies
├── README.md             # Project documentation
└── .streamlit/           # Streamlit config
    └── config.toml
```

### Example Project Structure

```python
# app.py - Main entry point
import streamlit as st
from utils.data_loader import load_data
from utils.helpers import process_data

def main():
    st.set_page_config(
        page_title="My App",
        page_icon="🚀",
        layout="wide"
    )
    
    st.title("My Streamlit App")
    data = load_data()
    processed = process_data(data)
    st.dataframe(processed)

if __name__ == "__main__":
    main()
```

```python
# utils/data_loader.py
import pandas as pd

def load_data():
    return pd.read_csv("data/sample_data.csv")
```

```python
# utils/helpers.py
def process_data(df):
    return df.head(10)
```

## IDE Configuration

### VS Code Setup

#### 1. Install Python Extension

Install the official Python extension from the VS Code marketplace.

#### 2. Install Streamlit Extension (Optional)

Search for "Streamlit" in VS Code extensions for syntax highlighting.

#### 3. Configure Launch Configuration

Create `.vscode/launch.json`:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Streamlit",
            "type": "python",
            "request": "launch",
            "module": "streamlit",
            "args": [
                "run",
                "app.py"
            ],
            "console": "integratedTerminal"
        }
    ]
}
```

#### 4. Recommended VS Code Settings

`.vscode/settings.json`:

```json
{
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black",
    "editor.formatOnSave": true
}
```

### PyCharm Setup

#### 1. Configure Python Interpreter

1. Go to File → Settings → Project → Python Interpreter
2. Select your virtual environment
3. Install Streamlit if not already installed

#### 2. Create Run Configuration

1. Go to Run → Edit Configurations
2. Click "+" → Python
3. Set:
   - Script path: `streamlit`
   - Parameters: `run app.py`
   - Working directory: Your project directory

#### 3. Recommended PyCharm Settings

- Enable code inspection
- Set up code formatting (Black or autopep8)
- Configure file watchers if needed

## Streamlit Configuration

### Config File Location

Create `.streamlit/config.toml` in your project root:

```toml
[server]
port = 8501
address = "localhost"
headless = false
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false
serverAddress = "localhost"
serverPort = 8501

[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"
```

### Environment Variables

You can also configure via environment variables:

```bash
export STREAMLIT_SERVER_PORT=8501
export STREAMLIT_SERVER_ADDRESS=localhost
export STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
```

## Troubleshooting Installation

### Common Issues

#### Issue 1: Command Not Found

**Problem:** `streamlit: command not found`

**Solution:**
- Ensure Streamlit is installed: `pip install streamlit`
- Check if Python/Scripts is in your PATH
- Use `python -m streamlit` instead

#### Issue 2: Port Already in Use

**Problem:** `Port 8501 is already in use`

**Solution:**
```bash
# Find process using port
lsof -i :8501  # macOS/Linux
netstat -ano | findstr :8501  # Windows

# Kill process or use different port
streamlit run app.py --server.port 8502
```

#### Issue 3: Import Errors

**Problem:** `ModuleNotFoundError: No module named 'streamlit'`

**Solution:**
- Activate your virtual environment
- Reinstall Streamlit: `pip install streamlit`
- Check Python version: `python --version` (should be 3.7+)

#### Issue 4: Browser Doesn't Open

**Problem:** Browser doesn't open automatically

**Solution:**
- Manually navigate to `http://localhost:8501`
- Check firewall settings
- Use `--server.headless true` if needed

## Testing Your Setup

### Quick Test Script

Create `test_setup.py`:

```python
import streamlit as st
import sys

st.title("Setup Test")

st.write("✅ Streamlit is installed and working!")
st.write(f"Python version: {sys.version}")
st.write(f"Streamlit version: {st.__version__}")

# Test widgets
name = st.text_input("Enter your name")
if name:
    st.success(f"Hello, {name}! Setup is complete.")
```

Run it:

```bash
streamlit run test_setup.py
```

## Next Steps

Now that you have Streamlit installed and configured:

1. **Create your first app** - Start with simple examples
2. **Explore widgets** - Try different input widgets
3. **Add visualizations** - Create charts and graphs
4. **Read Core Concepts** - [View detailed guide](./03-core-concepts.md)

## References

- [Streamlit Installation Guide](https://docs.streamlit.io/get-started/installation)
- [Streamlit Configuration](https://docs.streamlit.io/develop/api-reference/configuration)
- [VS Code Python Extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
- [PyCharm Documentation](https://www.jetbrains.com/help/pycharm/)

