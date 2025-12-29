# Media and File Handling - Deep Dive

## Overview

This guide covers handling images, audio, video, file uploads, downloads, working with different file formats, and media optimization in Streamlit apps.

## Images: st.image()

### Basic Image Display

```python
import streamlit as st

# Display image from file
st.image("image.jpg")

# Display with caption
st.image("image.jpg", caption="My Image")

# Display with width
st.image("image.jpg", width=300)

# Display with use_container_width
st.image("image.jpg", use_container_width=True)
```

### Image from URL

```python
import streamlit as st

st.image("https://example.com/image.jpg", caption="Image from URL")
```

### Image from Bytes

```python
import streamlit as st
from PIL import Image
import io

# Create image
img = Image.new('RGB', (100, 100), color='red')

# Convert to bytes
img_bytes = io.BytesIO()
img.save(img_bytes, format='PNG')
img_bytes.seek(0)

st.image(img_bytes, caption="Image from bytes")
```

### Image Formats

```python
import streamlit as st

# Supported formats: JPEG, PNG, GIF, WebP, BMP
st.image("photo.jpg")  # JPEG
st.image("logo.png")  # PNG
st.image("animation.gif")  # GIF
st.image("image.webp")  # WebP
```

### Multiple Images

```python
import streamlit as st

col1, col2, col3 = st.columns(3)

with col1:
    st.image("image1.jpg", caption="Image 1")

with col2:
    st.image("image2.jpg", caption="Image 2")

with col3:
    st.image("image3.jpg", caption="Image 3")
```

## Audio: st.audio()

### Basic Audio

```python
import streamlit as st

# Play audio file
st.audio("audio.mp3")

# Play from URL
st.audio("https://example.com/audio.mp3")

# Play from bytes
with open("audio.mp3", "rb") as f:
    audio_bytes = f.read()
st.audio(audio_bytes, format="audio/mp3")
```

### Audio Formats

```python
import streamlit as st

# Supported formats: MP3, WAV, OGG, FLAC
st.audio("song.mp3", format="audio/mp3")
st.audio("sound.wav", format="audio/wav")
st.audio("music.ogg", format="audio/ogg")
```

### Audio Controls

```python
import streamlit as st

st.audio("audio.mp3", start_time=10)  # Start at 10 seconds
```

## Video: st.video()

### Basic Video

```python
import streamlit as st

# Play video file
st.video("video.mp4")

# Play from URL
st.video("https://example.com/video.mp4")

# Play from bytes
with open("video.mp4", "rb") as f:
    video_bytes = f.read()
st.video(video_bytes, format="video/mp4")
```

### Video Formats

```python
import streamlit as st

# Supported formats: MP4, WebM, OGG
st.video("movie.mp4", format="video/mp4")
st.video("clip.webm", format="video/webm")
```

### Video from YouTube

```python
import streamlit as st

# Embed YouTube video
st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
```

## File Uploads and Processing

### Basic File Upload

```python
import streamlit as st

uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None:
    st.write(f"File name: {uploaded_file.name}")
    st.write(f"File size: {uploaded_file.size} bytes")
    st.write(f"File type: {uploaded_file.type}")
```

### Image Upload and Display

```python
import streamlit as st
from PIL import Image

uploaded_image = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

if uploaded_image is not None:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image", use_container_width=True)
    
    # Process image
    st.write(f"Image size: {image.size}")
    st.write(f"Image mode: {image.mode}")
```

### Audio Upload and Playback

```python
import streamlit as st

uploaded_audio = st.file_uploader("Upload Audio", type=["mp3", "wav"])

if uploaded_audio is not None:
    audio_bytes = uploaded_audio.read()
    st.audio(audio_bytes, format="audio/mp3")
```

### Video Upload and Playback

```python
import streamlit as st

uploaded_video = st.file_uploader("Upload Video", type=["mp4", "webm"])

if uploaded_video is not None:
    video_bytes = uploaded_video.read()
    st.video(video_bytes, format="video/mp4")
```

### Multiple File Uploads

```python
import streamlit as st

uploaded_files = st.file_uploader(
    "Upload multiple files",
    type=["jpg", "png", "pdf"],
    accept_multiple_files=True
)

if uploaded_files:
    for uploaded_file in uploaded_files:
        st.write(f"File: {uploaded_file.name}")
        if uploaded_file.type.startswith("image/"):
            st.image(uploaded_file)
```

## File Downloads

### Download Button

```python
import streamlit as st
import pandas as pd

# Download CSV
df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
csv = df.to_csv(index=False)

st.download_button(
    label="Download CSV",
    data=csv,
    file_name="data.csv",
    mime="text/csv"
)
```

### Download Different File Types

```python
import streamlit as st

# Download text file
text_data = "Hello, World!"
st.download_button(
    label="Download Text",
    data=text_data,
    file_name="hello.txt",
    mime="text/plain"
)

# Download JSON
import json
json_data = json.dumps({"key": "value"})
st.download_button(
    label="Download JSON",
    data=json_data,
    file_name="data.json",
    mime="application/json"
)

# Download image
with open("image.jpg", "rb") as f:
    image_data = f.read()
st.download_button(
    label="Download Image",
    data=image_data,
    file_name="image.jpg",
    mime="image/jpeg"
)
```

### Download Generated Content

```python
import streamlit as st
from PIL import Image
import io

# Generate image
img = Image.new('RGB', (200, 200), color='blue')

# Convert to bytes
img_bytes = io.BytesIO()
img.save(img_bytes, format='PNG')
img_bytes.seek(0)

st.download_button(
    label="Download Generated Image",
    data=img_bytes,
    file_name="generated.png",
    mime="image/png"
)
```

## Working with Different File Formats

### PDF Files

```python
import streamlit as st
import PyPDF2

uploaded_pdf = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded_pdf is not None:
    pdf_reader = PyPDF2.PdfReader(uploaded_pdf)
    st.write(f"Number of pages: {len(pdf_reader.pages)}")
    
    for i, page in enumerate(pdf_reader.pages):
        st.write(f"Page {i+1}:")
        st.write(page.extract_text())
```

### Excel Files

```python
import streamlit as st
import pandas as pd

uploaded_excel = st.file_uploader("Upload Excel", type=["xlsx", "xls"])

if uploaded_excel is not None:
    # Read all sheets
    excel_file = pd.ExcelFile(uploaded_excel)
    sheet_name = st.selectbox("Select Sheet", excel_file.sheet_names)
    
    df = pd.read_excel(uploaded_excel, sheet_name=sheet_name)
    st.dataframe(df)
```

### JSON Files

```python
import streamlit as st
import json

uploaded_json = st.file_uploader("Upload JSON", type=["json"])

if uploaded_json is not None:
    data = json.load(uploaded_json)
    st.json(data)
    
    # Convert to DataFrame if possible
    if isinstance(data, list):
        df = pd.DataFrame(data)
        st.dataframe(df)
```

## Media Optimization

### Image Optimization

```python
import streamlit as st
from PIL import Image
import io

def optimize_image(image, max_size=(800, 600), quality=85):
    """Resize and optimize image"""
    img = image.copy()
    img.thumbnail(max_size, Image.Resampling.LANCZOS)
    
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG', quality=quality, optimize=True)
    img_bytes.seek(0)
    return img_bytes

uploaded_image = st.file_uploader("Upload Image", type=["jpg", "png"])

if uploaded_image is not None:
    image = Image.open(uploaded_image)
    
    # Show original
    st.subheader("Original")
    st.image(image, caption=f"Size: {image.size}")
    
    # Show optimized
    st.subheader("Optimized")
    optimized = optimize_image(image)
    st.image(optimized, caption="Optimized version")
    
    # Download optimized
    st.download_button(
        label="Download Optimized",
        data=optimized,
        file_name="optimized.jpg",
        mime="image/jpeg"
    )
```

### Lazy Loading Images

```python
import streamlit as st

# Load images on demand
if st.button("Load Images"):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image("image1.jpg")
    with col2:
        st.image("image2.jpg")
    with col3:
        st.image("image3.jpg")
```

## Practical Examples

### Example 1: Image Gallery

```python
import streamlit as st
from PIL import Image
import os

st.title("Image Gallery")

# Get images from directory
image_dir = "images"
if os.path.exists(image_dir):
    images = [f for f in os.listdir(image_dir) if f.endswith(('.jpg', 'png', 'jpeg'))]
    
    selected_image = st.selectbox("Select Image", images)
    
    if selected_image:
        image_path = os.path.join(image_dir, selected_image)
        image = Image.open(image_path)
        st.image(image, use_container_width=True)
        
        # Image info
        st.write(f"Size: {image.size}")
        st.write(f"Mode: {image.mode}")
```

### Example 2: Media Player

```python
import streamlit as st

st.title("Media Player")

media_type = st.selectbox("Media Type", ["Image", "Audio", "Video"])

if media_type == "Image":
    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png"])
    if uploaded_file:
        st.image(uploaded_file)

elif media_type == "Audio":
    uploaded_file = st.file_uploader("Upload Audio", type=["mp3", "wav"])
    if uploaded_file:
        st.audio(uploaded_file)

elif media_type == "Video":
    uploaded_file = st.file_uploader("Upload Video", type=["mp4"])
    if uploaded_file:
        st.video(uploaded_file)
```

### Example 3: File Converter

```python
import streamlit as st
from PIL import Image
import io

st.title("Image Converter")

uploaded_image = st.file_uploader("Upload Image", type=["jpg", "png"])

if uploaded_image:
    image = Image.open(uploaded_image)
    st.image(image, caption="Original")
    
    target_format = st.selectbox("Convert to", ["JPEG", "PNG", "WebP"])
    
    if st.button("Convert"):
        img_bytes = io.BytesIO()
        
        if target_format == "JPEG":
            image.convert("RGB").save(img_bytes, format="JPEG")
            mime = "image/jpeg"
            ext = "jpg"
        elif target_format == "PNG":
            image.save(img_bytes, format="PNG")
            mime = "image/png"
            ext = "png"
        else:
            image.save(img_bytes, format="WebP")
            mime = "image/webp"
            ext = "webp"
        
        img_bytes.seek(0)
        
        st.image(img_bytes, caption=f"Converted to {target_format}")
        
        st.download_button(
            label=f"Download {target_format}",
            data=img_bytes,
            file_name=f"converted.{ext}",
            mime=mime
        )
```

## Best Practices

1. **Optimize media**: Resize and compress images/videos
2. **Use appropriate formats**: Choose formats based on use case
3. **Handle errors**: Check file types and sizes
4. **Provide feedback**: Show upload progress and status
5. **Cache media**: Use caching for frequently accessed media

## Common Pitfalls

### Pitfall 1: Large File Uploads

**Problem:**
```python
uploaded_file = st.file_uploader("Upload file")
data = uploaded_file.read()  # May be too large!
```

**Solution:**
```python
uploaded_file = st.file_uploader("Upload file", type=["csv"])
if uploaded_file:
    if uploaded_file.size > 10 * 1024 * 1024:  # 10MB
        st.error("File too large!")
    else:
        data = uploaded_file.read()
```

### Pitfall 2: Not Checking File Type

**Problem:**
```python
uploaded_file = st.file_uploader("Upload image")
image = Image.open(uploaded_file)  # Error if not image!
```

**Solution:**
```python
uploaded_file = st.file_uploader("Upload image", type=["jpg", "png"])
if uploaded_file and uploaded_file.type.startswith("image/"):
    image = Image.open(uploaded_file)
```

## Next Steps

Now that you can handle media:

- [Error Handling](./16-error-handling-debugging.md) - Handle errors gracefully
- [Deployment](./17-deployment-production.md) - Deploy your app

## References

- [Media API](https://docs.streamlit.io/develop/api-reference/media)
- [File Uploader](https://docs.streamlit.io/develop/api-reference/widgets/st.file_uploader)
- [Download Button](https://docs.streamlit.io/develop/api-reference/widgets/st.download_button)

