# Displaying Data and Text - Deep Dive

## Overview

Streamlit provides numerous ways to display text, data, and formatted content. This guide covers all text elements, data display methods, formatting options, and mathematical expressions.

## st.write() and Magic Commands

### st.write()

`st.write()` is Streamlit's Swiss Army knife - it can display almost anything:

```python
import streamlit as st

# Display text
st.write("Hello, World!")

# Display numbers
st.write(42)

# Display variables
name = "Alice"
st.write(f"Hello, {name}")

# Display multiple items
st.write("Name:", name, "Age:", 25)

# Display dataframes
import pandas as pd
df = pd.DataFrame({"A": [1, 2, 3]})
st.write(df)

# Display dictionaries
data = {"key": "value"}
st.write(data)
```

### Magic Commands

Streamlit's "magic" allows you to display values without explicitly calling `st.write()`:

```python
import streamlit as st
import pandas as pd

# These are equivalent:
st.write("Hello")
"Hello"  # Magic - automatically displayed

# Display variables
x = 42
x  # Automatically displayed

# Display dataframes
df = pd.DataFrame({"A": [1, 2, 3]})
df  # Automatically displayed as interactive dataframe

# Display dictionaries
{"key": "value"}  # Automatically displayed as JSON
```

**When to use magic:**
- Quick prototyping
- Simple displays
- Jupyter notebook-like experience

**When NOT to use magic:**
- Production code (less explicit)
- When you need specific formatting
- When you need to control display options

## Text Elements

### st.title()

Display a title (largest heading):

```python
import streamlit as st

st.title("My Application")
# Displays: # My Application
```

### st.header()

Display a header (section heading):

```python
import streamlit as st

st.header("Section 1")
# Displays: ## Section 1
```

### st.subheader()

Display a subheader (subsection heading):

```python
import streamlit as st

st.subheader("Subsection 1.1")
# Displays: ### Subsection 1.1
```

### st.text()

Display fixed-width text:

```python
import streamlit as st

st.text("This is fixed-width text")
st.text("Line 1\nLine 2\nLine 3")
```

### st.markdown()

Display Markdown-formatted text:

```python
import streamlit as st

# Basic markdown
st.markdown("# Heading 1")
st.markdown("## Heading 2")
st.markdown("**Bold text**")
st.markdown("*Italic text*")

# Lists
st.markdown("""
- Item 1
- Item 2
  - Subitem 2.1
  - Subitem 2.2
""")

# Links
st.markdown("[Streamlit](https://streamlit.io)")

# Code blocks
st.markdown("""
```python
def hello():
    print("Hello, World!")
```
""")

# Tables
st.markdown("""
| Column 1 | Column 2 |
|----------|----------|
| Value 1  | Value 2  |
""")
```

### st.caption()

Display small text (caption):

```python
import streamlit as st

st.caption("This is a caption")
```

### st.code()

Display code with syntax highlighting:

```python
import streamlit as st

# Python code
st.code("""
def hello():
    print("Hello, World!")
""", language="python")

# JavaScript code
st.code("""
function hello() {
    console.log("Hello, World!");
}
""", language="javascript")
```

## Displaying Data

### st.dataframe()

Display an interactive dataframe:

```python
import streamlit as st
import pandas as pd
import numpy as np

# Create dataframe
df = pd.DataFrame({
    "A": np.random.randn(10),
    "B": np.random.randn(10),
    "C": np.random.randn(10)
})

# Basic display
st.dataframe(df)

# With options
st.dataframe(
    df,
    width=700,
    height=300,
    use_container_width=True
)

# With column configuration
st.dataframe(
    df,
    column_config={
        "A": st.column_config.NumberColumn(
            "Column A",
            help="This is column A",
            format="%.2f"
        )
    }
)
```

### st.table()

Display a static table:

```python
import streamlit as st
import pandas as pd

df = pd.DataFrame({
    "A": [1, 2, 3],
    "B": [4, 5, 6]
})

st.table(df)  # Static, not sortable
```

**When to use st.table() vs st.dataframe():**
- `st.table()`: Small, simple tables
- `st.dataframe()`: Large tables, needs sorting/filtering

### st.json()

Display JSON data:

```python
import streamlit as st

data = {
    "name": "Alice",
    "age": 30,
    "city": "New York"
}

st.json(data)

# Expanded by default
st.json(data, expanded=True)
```

### st.metric()

Display a metric with optional delta:

```python
import streamlit as st

# Simple metric
st.metric("Temperature", "70 °F")

# With delta
st.metric(
    "Temperature",
    "70 °F",
    delta="2 °F",
    delta_color="normal"  # "normal", "inverse", "off"
)

# Multiple metrics
col1, col2, col3 = st.columns(3)
col1.metric("Revenue", "$100K", "$10K")
col2.metric("Users", "1,000", "100")
col3.metric("Growth", "5%", "-2%")
```

## Formatting and Styling Text

### Markdown Formatting

```python
import streamlit as st

# Bold and italic
st.markdown("**Bold text** and *italic text*")

# Strikethrough
st.markdown("~~Strikethrough text~~")

# Inline code
st.markdown("Use `st.write()` to display text")

# Blockquotes
st.markdown("> This is a quote")

# Horizontal rule
st.markdown("---")
```

### HTML Formatting

You can use HTML in markdown (with `unsafe_allow_html=True`):

```python
import streamlit as st

st.markdown(
    "<h1 style='color: red;'>Red Heading</h1>",
    unsafe_allow_html=True
)

st.markdown(
    """
    <div style='background-color: #f0f0f0; padding: 10px; border-radius: 5px;'>
        <p>Styled content</p>
    </div>
    """,
    unsafe_allow_html=True
)
```

### Custom CSS

For more advanced styling:

```python
import streamlit as st

st.markdown("""
<style>
.custom-text {
    font-size: 20px;
    color: #FF6B6B;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="custom-text">Custom styled text</p>', unsafe_allow_html=True)
```

## LaTeX and Mathematical Expressions

### Inline Math

```python
import streamlit as st

st.latex(r"E = mc^2")
st.latex(r"\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}")
```

### Block Math

```python
import streamlit as st

st.markdown(r"""
$$
\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}
$$
""")
```

### Complex Equations

```python
import streamlit as st

st.latex(r"""
\begin{align}
\nabla \times \vec{\mathbf{B}} -\, \frac1c\, \frac{\partial\vec{\mathbf{E}}}{\partial t} &= \frac{4\pi}{c}\vec{\mathbf{j}} \\
\nabla \cdot \vec{\mathbf{E}} &= 4 \pi \rho \\
\nabla \times \vec{\mathbf{E}}\, +\, \frac1c\, \frac{\partial\vec{\mathbf{B}}}{\partial t} &= \vec{\mathbf{0}} \\
\nabla \cdot \vec{\mathbf{B}} &= 0
\end{align}
""")
```

### Math in Markdown

```python
import streamlit as st

st.markdown(r"""
Inline math: $E = mc^2$

Block math:
$$
\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}
$$
""")
```

## Practical Examples

### Example 1: Data Summary

```python
import streamlit as st
import pandas as pd

st.title("Data Summary")

df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [25, 30, 35],
    "Score": [85, 90, 88]
})

st.dataframe(df)

st.subheader("Statistics")
st.metric("Average Age", f"{df['Age'].mean():.1f}")
st.metric("Average Score", f"{df['Score'].mean():.1f}")
```

### Example 2: Formatted Report

```python
import streamlit as st

st.title("Monthly Report")

st.markdown("""
## Executive Summary

This month we achieved:
- **Revenue**: $100K (↑ 10%)
- **Users**: 1,000 (↑ 5%)
- **Growth**: 5% (↓ 2%)

### Key Metrics

| Metric | Value | Change |
|--------|-------|--------|
| Revenue | $100K | +10% |
| Users | 1,000 | +5% |
| Growth | 5% | -2% |
""")
```

### Example 3: Code Documentation

```python
import streamlit as st

st.title("API Documentation")

st.markdown("""
### Function: `calculate_total`

Calculates the total of a list of numbers.

**Parameters:**
- `numbers` (list): List of numbers to sum

**Returns:**
- `float`: Sum of all numbers

**Example:**
```python
result = calculate_total([1, 2, 3, 4])
# Returns: 10
```
""")

st.code("""
def calculate_total(numbers):
    return sum(numbers)
""", language="python")
```

## Best Practices

1. **Use appropriate elements**: Choose the right element for your content
2. **Format consistently**: Use consistent formatting throughout your app
3. **Keep it readable**: Don't overuse formatting
4. **Use markdown**: Prefer markdown over HTML when possible
5. **Test display**: Test how content looks on different screen sizes

## Common Pitfalls

### Pitfall 1: Overusing Magic

**Problem:**
```python
# Hard to debug
df
x
y
```

**Solution:**
```python
# More explicit
st.dataframe(df)
st.write(f"X: {x}")
st.write(f"Y: {y}")
```

### Pitfall 2: Not Formatting Numbers

**Problem:**
```python
st.write(f"Price: {price}")  # Shows: Price: 99.9999999
```

**Solution:**
```python
st.write(f"Price: ${price:.2f}")  # Shows: Price: $100.00
```

### Pitfall 3: Large Dataframes

**Problem:**
```python
st.dataframe(huge_df)  # Slow rendering
```

**Solution:**
```python
st.dataframe(df.head(100))  # Show first 100 rows
# Or use pagination
```

## Next Steps

Now that you can display data and text:

- [Input Widgets - Part 1](./05-input-widgets-basic.md) - Learn basic input widgets
- [Input Widgets - Part 2](./06-input-widgets-advanced.md) - Learn advanced input widgets

## References

- [Text Elements API](https://docs.streamlit.io/develop/api-reference/text)
- [Data Display API](https://docs.streamlit.io/develop/api-reference/data)
- [Markdown Guide](https://www.markdownguide.org/)

