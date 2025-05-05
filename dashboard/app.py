import streamlit as st
from azure.storage.blob import ContainerClient
import json, os
from dotenv import load_dotenv
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Factory Hot Alerts Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load connection string from .env
def load_conn():
    load_dotenv()
    return os.getenv('STORAGE_CONNECTION_STRING')

conn_str = load_conn()
if not conn_str:
    st.error("❌ No STORAGE_CONNECTION_STRING found in environment. Please add it to your .env file.")
    st.stop()

# Connect to Azure Blob Storage container
try:
    container = ContainerClient.from_connection_string(conn_str, 'hot-alerts')
except Exception as e:
    st.error(f"❌ Error connecting to Azure Blob Storage: {e}!")
    st.stop()

# Load all alerts into a DataFrame
alerts = []
for blob in container.list_blobs():
    data = container.download_blob(blob.name).readall()
    record = json.loads(data)
    alerts.append(record)

if alerts:
    df = pd.DataFrame(alerts)
    # Convert time to datetime for sorting and charting
    df['time'] = pd.to_datetime(df['time'], format='%H:%M:%S')
    df = df.sort_values('time')

    # Title and overall chart
    st.markdown("# 🔥 Factory Hot Alerts")
    st.line_chart(
        data=df.set_index('time')['temperature'],
        width=0, height=300,
        use_container_width=True
    )

    st.markdown("---")
    st.markdown("## Detailed Alerts")

    # Display each alert in columns
    for _, row in df.iterrows():
        col1, col2, col3, spacer = st.columns([1, 1, 1, 6])
        col1.metric("Machine", row.get('machine', 'Unknown'))
        col2.metric("Time", row['time'].strftime('%H:%M:%S'))
        col3.metric(
            "Temperature (°C)",
            value=row.get('temperature', 'N/A'),
            delta=round(row.get('temperature', 0) - df['temperature'].mean(), 2)
        )
        st.markdown("---")
else:
    st.markdown("# 🔔 No hot alerts yet. Everything is cool! 😊")