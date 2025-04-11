import os
import streamlit as st
import pandas as pd
import pymysql
import matplotlib.pyplot as plt
import matplotlib.style as style
import seaborn as sns
import plotly.express as px
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# ✅ Use a valid matplotlib style
try:
    style.use('ggplot')
except OSError:
    style.use('default')

# ✅ DB Connection using Railway Env Variables
def get_connection():
    return pymysql.connect(
        host=os.getenv("MYSQLHOST", "mysql"),
        user=os.getenv("MYSQLUSER", "root"),
        password=os.getenv("MYSQLPASSWORD", ""),
        db=os.getenv("MYSQLDATABASE", "railway"),
        port=int(os.getenv("MYSQLPORT", 3306))
    )

# ✅ Fetch Data
def fetch_data():
    try:
        conn = get_connection()
        df = pd.read_sql("SELECT * FROM customer_db", conn)
        conn.close()
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
        return df.dropna(subset=['timestamp'])
    except Exception as e:
        st.error(f"❌ Error fetching data: {e}")
        return pd.DataFrame()

# ✅ App Config
st.set_page_config(page_title="🌤️ Weather Dashboard", layout="wide")
st.title("🌦️ Real-Time Weather Monitoring Dashboard")

# ✅ Auto Refresh
st_autorefresh(interval=10 * 1000, key="datarefresh")  # every 10 seconds

# ✅ Load and filter data
df = fetch_data()
if df.empty:
    st.warning("⚠️ No data available.")
    st.stop()

city_options = df['city'].unique().tolist()
selected_city = st.sidebar.selectbox("🏙️ Select City", city_options)

# ✅ Date filter
min_timestamp = df['timestamp'].min().date()
max_timestamp = df['timestamp'].max().date()
if min_timestamp < max_timestamp:
    date_range = st.slider("📆 Select Date Range", 
                           min_value=min_timestamp,
                           max_value=max_timestamp,
                           value=(min_timestamp, max_timestamp))
    start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
else:
    start_date = end_date = pd.to_datetime(min_timestamp)
    st.info("Only one date available. Showing that day.")

# ✅ Filtered data
city_df = df[(df['city'] == selected_city) & 
             (df['timestamp'] >= start_date) & 
             (df['timestamp'] <= end_date)]

st.header(f"📍 City Dashboard: {selected_city}")

# ✅ Alerts
alert_placeholder = st.empty()
if not city_df.empty:
    max_temp = city_df['temperature'].max()
    max_humidity = city_df['humidity'].max()

    if max_temp > 40:
        alert_placeholder.warning(f"🔥 Extreme Heat Alert! Max Temp: {max_temp}°C")
    elif max_temp < 5:
        alert_placeholder.warning(f"❄️ Cold Weather Alert! Min Temp: {max_temp}°C")
    else:
        alert_placeholder.success(f"✅ Normal Temperature Conditions ({max_temp}°C)")

    if max_humidity > 80:
        st.error(f"💦 High Humidity Alert! Humidity: {max_humidity:.2f}%")

    avg_temp = city_df['temperature'].mean()
    avg_humidity = city_df['humidity'].mean()

    st.markdown("### 📊 Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("🌡️ Avg Temp (°C)", f"{avg_temp:.2f}")
    col2.metric("💧 Avg Humidity (%)", f"{avg_humidity:.2f}")
    col3.metric("📍 Cities Reporting", df['city'].nunique())

    # ✅ Visualizations
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Line Chart", "📊 Humidity Chart", "🔥 Heatmap", "📽️ Animation"])

    with tab1:
        st.subheader("📈 Temperature Over Time")
        fig1, ax1 = plt.subplots()
        city_df.sort_values('timestamp').plot(x='timestamp', y='temperature', ax=ax1, color='tomato')
        ax1.set_xlabel("Timestamp")
        ax1.set_ylabel("Temperature (°C)")
        ax1.set_title(f"🌡️ Temperature Trend in {selected_city}")
        plt.xticks(rotation=45)
        st.pyplot(fig1)

    with tab2:
        st.subheader("📊 Average Humidity by City")
        fig2, ax2 = plt.subplots()
        df.groupby('city')['humidity'].mean().plot(kind='bar', ax=ax2, color='skyblue')
        ax2.set_ylabel("Humidity (%)")
        ax2.set_title("💧 Humidity Levels by City")
        st.pyplot(fig2)

    with tab3:
        st.subheader("🔥 Heatmap of Temperature")
        heatmap_df = df.pivot_table(index='timestamp', columns='city', values='temperature')
        fig3, ax3 = plt.subplots(figsize=(12, 6))
        sns.heatmap(heatmap_df.T, cmap="coolwarm", ax=ax3, cbar_kws={'label': 'Temperature (°C)'})
        plt.xlabel("Time")
        plt.ylabel("City")
        st.pyplot(fig3)

    with tab4:
        st.subheader("📽️ Animated Temperature Trend (Plotly)")
        fig4 = px.line(city_df.sort_values('timestamp'),
                       x='timestamp', y='temperature', color='city',
                       animation_frame=city_df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S'),
                       title="🌡️ Temperature Trend Over Time")
        st.plotly_chart(fig4, use_container_width=True)

    with st.expander("🧾 Show Data Table"):
        st.dataframe(city_df)

    csv = city_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name=f"weather_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime='text/csv',
    )
else:
    st.warning("⚠️ No data available for selected city.")

# ✅ Footer
st.markdown("---")
st.markdown("Made with ❤️ using **Streamlit** | Data from `weather_db` 📦")
