# Integration with External Services - Deep Dive

## Overview

This guide covers integrating Streamlit apps with databases, APIs, authentication systems, OAuth, email services, cloud storage, and message queues.

## Database Connections

### SQLite

```python
import streamlit as st
import sqlite3
import pandas as pd

@st.cache_resource
def get_connection():
    return sqlite3.connect("database.db")

@st.cache_data(ttl=60)
def load_data(query):
    conn = get_connection()
    return pd.read_sql_query(query, conn)

# Query interface
query = st.text_area("SQL Query", "SELECT * FROM users LIMIT 10")

if st.button("Execute"):
    try:
        df = load_data(query)
        st.dataframe(df)
    except Exception as e:
        st.error(f"Query error: {str(e)}")
```

### PostgreSQL

```python
import streamlit as st
import psycopg2
import pandas as pd
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

### MySQL

```python
import streamlit as st
import pymysql
import pandas as pd
from sqlalchemy import create_engine

@st.cache_resource
def get_engine():
    return create_engine("mysql+pymysql://user:password@localhost/dbname")

def query_database(query):
    engine = get_engine()
    return pd.read_sql_query(query, engine)

df = query_database("SELECT * FROM users")
st.dataframe(df)
```

## API Integrations

### REST API

```python
import streamlit as st
import requests

@st.cache_data(ttl=300)
def fetch_api_data(url, headers=None):
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

# API endpoint
url = st.text_input("API URL", "https://api.example.com/data")
api_key = st.text_input("API Key", type="password")

if st.button("Fetch Data"):
    try:
        headers = {"Authorization": f"Bearer {api_key}"} if api_key else None
        data = fetch_api_data(url, headers)
        st.json(data)
    except Exception as e:
        st.error(f"API Error: {str(e)}")
```

### POST Request

```python
import streamlit as st
import requests
import json

def post_data(url, data, headers=None):
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    return response.json()

# Form to submit data
with st.form("api_form"):
    name = st.text_input("Name")
    email = st.text_input("Email")
    
    submitted = st.form_submit_button("Submit")
    
    if submitted:
        data = {"name": name, "email": email}
        try:
            result = post_data("https://api.example.com/users", data)
            st.success("Data submitted successfully!")
            st.json(result)
        except Exception as e:
            st.error(f"Error: {str(e)}")
```

## Authentication and Authorization

### Basic Authentication

```python
import streamlit as st

def check_password():
    """Returns `True` if the user had the correct password."""
    
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == "mypassword":
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False
    
    if "password_correct" not in st.session_state:
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        st.error("Password incorrect")
        return False
    else:
        return True

if check_password():
    st.write("Welcome! You are authenticated.")
```

### Session-Based Auth

```python
import streamlit as st
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# User database (in production, use a real database)
users = {
    "admin": hash_password("admin123"),
    "user": hash_password("user123")
}

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("Login")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if username in users and hash_password(password) == users[username]:
            st.session_state.authenticated = True
            st.session_state.username = username
            st.rerun()
        else:
            st.error("Invalid credentials")
else:
    st.title(f"Welcome, {st.session_state.username}!")
    if st.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.username = None
        st.rerun()
```

## OAuth Integration

### Google OAuth

```python
import streamlit as st
from streamlit_oauth import OAuth

# Initialize OAuth
oauth = OAuth(
    provider="google",
    client_id=st.secrets["GOOGLE_CLIENT_ID"],
    client_secret=st.secrets["GOOGLE_CLIENT_SECRET"],
    redirect_uri="http://localhost:8501"
)

# Login button
if st.button("Login with Google"):
    auth_url = oauth.get_authorization_url()
    st.markdown(f"[Login]({auth_url})")
```

### GitHub OAuth

```python
import streamlit as st
import requests

CLIENT_ID = st.secrets["GITHUB_CLIENT_ID"]
CLIENT_SECRET = st.secrets["GITHUB_CLIENT_SECRET"]

if "github_token" not in st.session_state:
    st.session_state.github_token = None

if not st.session_state.github_token:
    st.markdown(f"[Login with GitHub](https://github.com/login/oauth/authorize?client_id={CLIENT_ID})")
else:
    # Use token to access GitHub API
    headers = {"Authorization": f"token {st.session_state.github_token}"}
    user = requests.get("https://api.github.com/user", headers=headers).json()
    st.write(f"Logged in as {user['login']}")
```

## Email and Notifications

### Sending Email

```python
import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(to_email, subject, body):
    smtp_server = st.secrets["SMTP_SERVER"]
    smtp_port = st.secrets["SMTP_PORT"]
    from_email = st.secrets["FROM_EMAIL"]
    password = st.secrets["EMAIL_PASSWORD"]
    
    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))
    
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(from_email, password)
    server.send_message(msg)
    server.quit()

# Email form
with st.form("email_form"):
    to_email = st.text_input("To")
    subject = st.text_input("Subject")
    body = st.text_area("Body")
    
    submitted = st.form_submit_button("Send Email")
    
    if submitted:
        try:
            send_email(to_email, subject, body)
            st.success("Email sent!")
        except Exception as e:
            st.error(f"Error: {str(e)}")
```

### SendGrid Integration

```python
import streamlit as st
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_email_sendgrid(to_email, subject, body):
    message = Mail(
        from_email=st.secrets["FROM_EMAIL"],
        to_emails=to_email,
        subject=subject,
        html_content=body
    )
    
    sg = SendGridAPIClient(st.secrets["SENDGRID_API_KEY"])
    response = sg.send(message)
    return response.status_code

# Use in app
if st.button("Send Notification"):
    send_email_sendgrid("user@example.com", "Notification", "Your data is ready!")
```

## Cloud Storage

### AWS S3

```python
import streamlit as st
import boto3
import pandas as pd

@st.cache_resource
def get_s3_client():
    return boto3.client(
        's3',
        aws_access_key_id=st.secrets["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=st.secrets["AWS_SECRET_ACCESS_KEY"]
    )

def upload_to_s3(file, bucket, key):
    s3_client = get_s3_client()
    s3_client.upload_fileobj(file, bucket, key)

def download_from_s3(bucket, key):
    s3_client = get_s3_client()
    obj = s3_client.get_object(Bucket=bucket, Key=key)
    return obj['Body'].read()

# Upload file
uploaded_file = st.file_uploader("Upload to S3")
if uploaded_file:
    if st.button("Upload"):
        upload_to_s3(uploaded_file, "my-bucket", uploaded_file.name)
        st.success("File uploaded!")
```

### Google Cloud Storage

```python
import streamlit as st
from google.cloud import storage

@st.cache_resource
def get_gcs_client():
    return storage.Client.from_service_account_json("credentials.json")

def upload_to_gcs(file, bucket_name, blob_name):
    client = get_gcs_client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_file(file)

# Use in app
uploaded_file = st.file_uploader("Upload to GCS")
if uploaded_file:
    upload_to_gcs(uploaded_file, "my-bucket", uploaded_file.name)
```

### Azure Blob Storage

```python
import streamlit as st
from azure.storage.blob import BlobServiceClient

@st.cache_resource
def get_blob_client():
    return BlobServiceClient.from_connection_string(
        st.secrets["AZURE_STORAGE_CONNECTION_STRING"]
    )

def upload_to_azure(file, container_name, blob_name):
    blob_service = get_blob_client()
    blob_client = blob_service.get_blob_client(container=container_name, blob=blob_name)
    blob_client.upload_blob(file)

# Use in app
uploaded_file = st.file_uploader("Upload to Azure")
if uploaded_file:
    upload_to_azure(uploaded_file, "my-container", uploaded_file.name)
```

## Message Queues and Background Tasks

### Redis Queue

```python
import streamlit as st
import redis
from rq import Queue

@st.cache_resource
def get_redis_connection():
    return redis.Redis(host='localhost', port=6379, db=0)

@st.cache_resource
def get_queue():
    redis_conn = get_redis_connection()
    return Queue('tasks', connection=redis_conn)

def process_task(data):
    # Long-running task
    import time
    time.sleep(10)
    return f"Processed: {data}"

# Add task to queue
if st.button("Process Task"):
    queue = get_queue()
    job = queue.enqueue(process_task, "task_data")
    st.success(f"Task queued: {job.id}")
```

### Celery Integration

```python
import streamlit as st
from celery import Celery

app = Celery('tasks', broker='redis://localhost:6379')

@app.task
def process_data(data):
    # Long-running task
    return f"Processed: {data}"

# Trigger task
if st.button("Process"):
    result = process_data.delay("task_data")
    st.success(f"Task started: {result.id}")
```

## Practical Examples

### Example 1: Database Dashboard

```python
import streamlit as st
import pandas as pd
import sqlite3

@st.cache_resource
def get_db():
    return sqlite3.connect("sales.db")

st.title("Sales Dashboard")

# Query options
query_type = st.selectbox("Query Type", ["Daily", "Monthly", "Yearly"])

if query_type == "Daily":
    query = "SELECT date, SUM(amount) as total FROM sales GROUP BY date"
elif query_type == "Monthly":
    query = "SELECT strftime('%Y-%m', date) as month, SUM(amount) as total FROM sales GROUP BY month"
else:
    query = "SELECT strftime('%Y', date) as year, SUM(amount) as total FROM sales GROUP BY year"

df = pd.read_sql_query(query, get_db())
st.dataframe(df)
st.line_chart(df.set_index(df.columns[0]))
```

### Example 2: API Integration Dashboard

```python
import streamlit as st
import requests
import pandas as pd

@st.cache_data(ttl=300)
def fetch_weather_data(city, api_key):
    url = f"https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key, "units": "metric"}
    response = requests.get(url, params=params)
    return response.json()

city = st.text_input("City", "London")
api_key = st.text_input("API Key", type="password")

if st.button("Get Weather"):
    try:
        data = fetch_weather_data(city, api_key)
        st.write(f"Temperature: {data['main']['temp']}°C")
        st.write(f"Description: {data['weather'][0]['description']}")
    except Exception as e:
        st.error(f"Error: {str(e)}")
```

## Best Practices

1. **Cache connections**: Use `@st.cache_resource` for database/API clients
2. **Handle errors**: Always wrap API calls in try-except
3. **Secure secrets**: Use Streamlit secrets or environment variables
4. **Rate limiting**: Be mindful of API rate limits
5. **Connection pooling**: Reuse connections when possible

## Common Pitfalls

### Pitfall 1: Not Caching Connections

**Problem:**
```python
def get_db():
    return sqlite3.connect("db.sqlite")  # New connection every time!
```

**Solution:**
```python
@st.cache_resource
def get_db():
    return sqlite3.connect("db.sqlite")  # Cached connection
```

### Pitfall 2: Exposing API Keys

**Problem:**
```python
api_key = "my-secret-key"  # Hardcoded!
```

**Solution:**
```python
api_key = st.secrets["API_KEY"]  # From secrets
```

## Next Steps

Now that you can integrate external services:

- [Best Practices](./19-best-practices.md) - More integration tips
- [Real-World Projects](./20-real-world-projects.md) - Complete examples

## References

- [Streamlit Secrets](https://docs.streamlit.io/develop/api-reference/utilities/st.secrets)
- [SQLAlchemy Documentation](https://www.sqlalchemy.org/)
- [Requests Documentation](https://requests.readthedocs.io/)

