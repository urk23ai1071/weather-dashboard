# weather_dashboard.py
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# SQLAlchemy for cleaner connection (optional but recommended)
engine = create_engine("mysql+pymysql://root:root@127.0.0.1/customer_db")
df = pd.read_sql("SELECT * FROM weather_db", engine)

# Convert timestamp to datetime if needed
df['timestamp'] = pd.to_datetime(df['timestamp'])

# App Title & Description
st.set_page_config(page_title="Weather Dashboard 🌤️", layout="wide")
st.title("🌤️ Real-Time Weather Dashboard")
st.markdown("Get real-time insights into temperature and humidity across cities.")

# Add Filters
with st.sidebar:
    st.header("📍 Filters")
    cities = st.multiselect("Select Cities", options=df['city'].unique(), default=df['city'].unique())
    df = df[df['city'].isin(cities)]

    temp_range = st.slider("Temperature Range (°C)", 
                           int(df['temperature'].min()), 
                           int(df['temperature'].max()), 
                           (int(df['temperature'].min()), int(df['temperature'].max())))
    df = df[(df['temperature'] >= temp_range[0]) & (df['temperature'] <= temp_range[1])]

# Layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("🌡️ Temperature Over Time")
    st.line_chart(df.set_index('timestamp')['temperature'])

with col2:
    st.subheader("💧 Humidity by City")
    humidity_by_city = df.groupby('city')['humidity'].mean()
    st.bar_chart(humidity_by_city)

# KPIs
st.markdown("## 📊 Key Stats")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Avg Temp (°C)", f"{df['temperature'].mean():.2f}")
with col2:
    st.metric("Avg Humidity (%)", f"{df['humidity'].mean():.2f}")
with col3:
    st.metric("Cities Reporting", df['city'].nunique())

# Raw data table
with st.expander("📝 View Raw Data"):
    st.dataframe(df)

# Footer
st.markdown("""---  
Created with ❤️ using Streamlit | Data from `weather_db`  
""")
