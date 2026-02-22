import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Broadband Dashboard", layout="wide")

st.title("🌐 Broadband Operations Web App")

# โหลดข้อมูล (ดึงไฟล์จากในโฟลเดอร์เดียวกัน)
@st.cache_data
def load_data():
    df = pd.read_excel("Test.xlsx", header=1) # ชื่อไฟล์ต้องตรงกับบน GitHub
    df.columns = df.columns.str.strip()
    df = df.dropna(subset=['Region', 'Solution Type', 'Overall Status'])
    return df

try:
    df = load_data()
    
    # ตัวกรองที่แถบข้าง
    st.sidebar.header("ตัวกรอง")
    region = st.sidebar.multiselect("เลือกภูมิภาค", options=df['Region'].unique(), default=df['Region'].unique())
    
    filtered_df = df[df['Region'].isin(region)]

    # แสดงผล
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(px.bar(filtered_df.groupby('Solution Type').size().reset_index(name='Counts'), 
                               x='Solution Type', y='Counts', title="จำนวนตาม Solution"), use_container_width=True)
    with c2:
        st.plotly_chart(px.pie(filtered_df, names='Overall Status', title="สถานะโครงการ"), use_container_width=True)

    st.dataframe(filtered_df, use_container_width=True)

except Exception as e:
    st.error(f"กรุณาตรวจสอบว่ามีไฟล์ Test.xlsx หรือยัง? (Error: {e})")