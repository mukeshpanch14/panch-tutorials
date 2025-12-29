# Sample Streamlit Applications

This directory contains example Streamlit applications demonstrating various concepts and use cases covered in the tutorial.

## 🚀 Comprehensive Demo App

**Start here!** The main demo app showcases most features from the course:

```bash
streamlit run streamlit_demo_app.py
```

This comprehensive app includes:
- 📊 Interactive Dashboard with filters and multiple chart types
- 📝 Forms & Inputs (basic and advanced widgets)
- 📈 Data Visualization (native charts, Plotly, maps)
- 🔄 Session State examples (counter, shopping cart, data storage)
- ⚡ Caching Demo (performance optimization)
- 📱 Layout Examples (columns, tabs, containers, expanders)
- 🎨 Advanced Features (progress bars, custom HTML/CSS, media)
- 📁 File Operations (upload and download)

All examples use **mock data** - no external dependencies required!

## Structure

```
sample_apps/
├── README.md
├── streamlit_demo_app.py    # ⭐ Comprehensive demo app
├── basic_examples/
│   ├── hello_world.py
│   ├── widgets_demo.py
│   └── data_visualization.py
├── intermediate_examples/
│   ├── dashboard.py
│   ├── form_app.py
│   └── multi_page_app/
│       ├── app.py
│       └── pages/
│           ├── 1_Home.py
│           └── 2_Dashboard.py
└── advanced_examples/
    ├── ml_deployment.py
    ├── real_time_monitor.py
    └── data_explorer.py
```

## Getting Started

### Quick Start (Recommended)

Run the comprehensive demo app:

```bash
cd sample_apps
streamlit run streamlit_demo_app.py
```

### Individual Examples

1. **Navigate to a sample app directory**
   ```bash
   cd sample_apps/basic_examples
   ```

2. **Run the app**
   ```bash
   streamlit run hello_world.py
   ```

3. **View in browser**
   The app will open automatically at `http://localhost:8501`

## Examples by Category

### Basic Examples

- **hello_world.py**: Simple "Hello World" app
- **widgets_demo.py**: Demonstrates all basic widgets
- **data_visualization.py**: Basic charts and visualizations

### Intermediate Examples

- **dashboard.py**: Complete dashboard with filters and charts
- **form_app.py**: Multi-step form with validation
- **multi_page_app/**: Multi-page application structure

### Advanced Examples

- **ml_deployment.py**: Machine learning model deployment
- **real_time_monitor.py**: Real-time data monitoring
- **data_explorer.py**: Interactive data exploration tool

## Requirements

All examples require:
- Python 3.7+
- Streamlit
- Additional dependencies as specified in each example

Install dependencies:
```bash
pip install -r requirements.txt
```

## Contributing

Feel free to add your own examples! Follow these guidelines:

1. Add clear comments explaining the code
2. Include a brief description at the top
3. Use consistent naming conventions
4. Add to the appropriate category directory

## Notes

- These examples are for educational purposes
- Adapt them to your specific needs
- Some examples may require API keys or data files
- Check individual files for specific requirements

