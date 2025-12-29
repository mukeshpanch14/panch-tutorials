# Caching and Performance Optimization - Deep Dive

## Overview

Streamlit's caching mechanism allows you to optimize app performance by storing the results of expensive operations. This guide covers data caching, resource caching, cache invalidation, and performance best practices.

## @st.cache_data

### Basic Usage

`@st.cache_data` caches the return value of a function:

```python
import streamlit as st
import pandas as pd
import time

@st.cache_data
def load_data():
    # Expensive operation
    time.sleep(2)  # Simulate slow operation
    return pd.read_csv("large_file.csv")

# First call: executes function and caches result
df = load_data()  # Takes 2 seconds

# Subsequent calls: returns cached result
df = load_data()  # Instant!
```

### When to Use st.cache_data

Use `@st.cache_data` for:
- Loading data from files (CSV, JSON, etc.)
- Fetching data from APIs
- Computing expensive transformations
- Any function that returns serializable data

```python
import streamlit as st
import pandas as pd
import requests

@st.cache_data
def fetch_api_data(url):
    response = requests.get(url)
    return response.json()

@st.cache_data
def process_data(df):
    # Expensive computation
    return df.groupby("category").sum()
```

### Cache Parameters

```python
import streamlit as st

@st.cache_data(
    ttl=3600,  # Time to live in seconds
    max_entries=10,  # Maximum cache entries
    show_spinner=True  # Show spinner while loading
)
def expensive_function():
    # Your code here
    return result
```

## @st.cache_resource

### Basic Usage

`@st.cache_resource` caches resources that shouldn't be copied (like ML models, database connections):

```python
import streamlit as st
import pickle

@st.cache_resource
def load_model():
    # Load ML model (shouldn't be copied)
    with open("model.pkl", "rb") as f:
        return pickle.load(f)

# Model is cached and reused
model = load_model()
```

### When to Use st.cache_resource

Use `@st.cache_resource` for:
- Machine learning models
- Database connections
- TensorFlow/PyTorch models
- Any non-serializable object

```python
import streamlit as st
import sqlite3

@st.cache_resource
def get_database_connection():
    return sqlite3.connect("database.db")

conn = get_database_connection()
```

## Cache Invalidation and TTL

### Time to Live (TTL)

```python
import streamlit as st

@st.cache_data(ttl=3600)  # Cache for 1 hour
def fetch_data():
    return fetch_from_api()

# Cache expires after 1 hour, then function runs again
```

### Manual Cache Clearing

```python
import streamlit as st

@st.cache_data
def load_data():
    return pd.read_csv("data.csv")

# Clear specific cache
load_data.clear()

# Clear all caches
st.cache_data.clear()
```

### Cache Invalidation on File Change

```python
import streamlit as st
import pandas as pd
from pathlib import Path

@st.cache_data
def load_data(file_path):
    return pd.read_csv(file_path)

# If file changes, cache is invalidated
file_path = "data.csv"
df = load_data(file_path)
```

## Performance Best Practices

### 1. Cache Expensive Operations

```python
import streamlit as st
import pandas as pd
import numpy as np

@st.cache_data
def load_and_process_data():
    # Load data
    df = pd.read_csv("large_file.csv")
    
    # Expensive processing
    df = df.groupby("category").agg({
        "sales": ["sum", "mean", "std"],
        "quantity": "sum"
    })
    
    return df

df = load_and_process_data()  # Cached!
```

### 2. Use Appropriate Cache Decorator

```python
import streamlit as st

# For data (serializable)
@st.cache_data
def get_data():
    return [1, 2, 3, 4, 5]

# For resources (non-serializable)
@st.cache_resource
def get_model():
    return load_ml_model()
```

### 3. Minimize Cache Dependencies

```python
import streamlit as st

# Good: Cache only what's needed
@st.cache_data
def process_data(df):
    return df.groupby("category").sum()

# Bad: Caching with too many dependencies
@st.cache_data
def process_data(df, filter1, filter2, filter3):
    # Too many parameters = more cache misses
    return df.groupby("category").sum()
```

## Handling Large Datasets

### Chunking Large Files

```python
import streamlit as st
import pandas as pd

@st.cache_data
def load_large_file(file_path, chunk_size=10000):
    chunks = []
    for chunk in pd.read_csv(file_path, chunksize=chunk_size):
        chunks.append(chunk)
    return pd.concat(chunks, ignore_index=True)

df = load_large_file("very_large_file.csv")
```

### Sampling for Display

```python
import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    return pd.read_csv("large_file.csv")

df = load_data()

# Show sample for display
st.dataframe(df.head(1000))  # Show first 1000 rows

# Process full dataset when needed
if st.button("Process Full Dataset"):
    with st.spinner("Processing..."):
        result = process_full_dataset(df)
```

## Memory Management

### Clearing Unused Caches

```python
import streamlit as st

# Clear specific cache
@st.cache_data
def load_data():
    return pd.read_csv("data.csv")

# When done with data
load_data.clear()

# Clear all caches
st.cache_data.clear()
```

### Monitoring Cache Usage

```python
import streamlit as st

@st.cache_data
def load_data():
    return pd.read_csv("data.csv")

# Check cache info (in Streamlit's cache management UI)
# Go to Settings > Clear cache
```

## Profiling and Optimization

### Measuring Performance

```python
import streamlit as st
import time

@st.cache_data
def slow_function():
    time.sleep(2)
    return "result"

start = time.time()
result = slow_function()
end = time.time()

st.write(f"Time taken: {end - start:.2f} seconds")
# First call: ~2 seconds
# Subsequent calls: ~0 seconds (cached)
```

### Identifying Bottlenecks

```python
import streamlit as st
import cProfile
import pstats

def profile_function(func):
    profiler = cProfile.Profile()
    profiler.enable()
    result = func()
    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(10)  # Top 10 slowest functions
    return result

# Use in development to find slow functions
```

## Practical Examples

### Example 1: Data Loading with Caching

```python
import streamlit as st
import pandas as pd

@st.cache_data(ttl=3600)
def load_sales_data():
    return pd.read_csv("sales_data.csv")

@st.cache_data
def process_sales_data(df):
    return df.groupby("category").agg({
        "sales": "sum",
        "quantity": "sum"
    })

# Load and process (cached)
df = load_sales_data()
processed = process_sales_data(df)

st.dataframe(processed)
```

### Example 2: API Data with TTL

```python
import streamlit as st
import requests

@st.cache_data(ttl=300)  # Cache for 5 minutes
def fetch_weather_data(city):
    api_key = "your_api_key"
    url = f"https://api.weather.com/v1/{city}?key={api_key}"
    response = requests.get(url)
    return response.json()

city = st.selectbox("City", ["New York", "London", "Tokyo"])
weather = fetch_weather_data(city)
st.json(weather)
```

### Example 3: ML Model Caching

```python
import streamlit as st
import pickle
import numpy as np

@st.cache_resource
def load_model():
    with open("model.pkl", "rb") as f:
        return pickle.load(f)

@st.cache_data
def preprocess_data(input_data):
    # Expensive preprocessing
    return np.array(input_data).reshape(1, -1)

model = load_model()  # Cached model

input_data = st.text_input("Enter features (comma-separated)")
if input_data:
    features = [float(x) for x in input_data.split(",")]
    processed = preprocess_data(features)
    prediction = model.predict(processed)
    st.write(f"Prediction: {prediction[0]}")
```

## Best Practices

1. **Cache expensive operations**: Use caching for slow operations
2. **Choose right decorator**: Use `cache_data` for data, `cache_resource` for resources
3. **Set appropriate TTL**: Balance freshness vs performance
4. **Clear caches when needed**: Provide cache clearing options
5. **Monitor memory**: Be aware of memory usage with large caches

## Common Pitfalls

### Pitfall 1: Caching Functions with Side Effects

**Problem:**
```python
@st.cache_data
def write_to_file(data):
    with open("output.txt", "w") as f:
        f.write(data)  # Only writes once due to caching!
```

**Solution:**
```python
def write_to_file(data):
    with open("output.txt", "w") as f:
        f.write(data)  # Don't cache functions with side effects
```

### Pitfall 2: Caching Non-Hashable Arguments

**Problem:**
```python
@st.cache_data
def process_data(df, config):  # config is a dict (mutable)
    return df.groupby(config["group_by"]).sum()
```

**Solution:**
```python
@st.cache_data
def process_data(df, group_by):  # Use immutable arguments
    return df.groupby(group_by).sum()
```

## Next Steps

Now that you understand caching:

- [Working with Data](./11-working-with-data.md) - Load and process data efficiently
- [Best Practices](./19-best-practices.md) - More optimization tips

## References

- [Caching API](https://docs.streamlit.io/develop/api-reference/performance/st.cache_data)
- [Performance Optimization](https://docs.streamlit.io/develop/concepts/architecture)

