import psycopg
import streamlit as st

st.set_page_config(page_title="最新公告", page_icon="📢")
st.title("📢 最新公告")
try:
    database_url = st.secrets["DATABASE_URL"]
except (KeyError, FileNotFoundError):
    st.error("尚未設定資料庫連線。請在 Streamlit Cloud 的 Secrets 設定 DATABASE_URL。")
    st.stop()
try:
    with psycopg.connect(database_url, connect_timeout=10) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT title, content, created_at FROM announcements_announcement ORDER BY created_at DESC")
            announcements = cursor.fetchall()
except psycopg.Error:
    st.error("目前無法讀取公告資料，請稍後再試。")
    st.stop()
if announcements:
    for title, content, created_at in announcements:
        st.subheader(title)
        st.write(content)
        st.caption(f"發布時間：{created_at:%Y-%m-%d %H:%M}")
        st.divider()
else:
    st.info("目前沒有公告")
