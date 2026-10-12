import html
from zoneinfo import ZoneInfo

import psycopg
import streamlit as st

st.set_page_config(page_title="MY CAMPUS", page_icon="🏫", layout="wide")

st.html("""
<style>
  html { scroll-behavior: smooth; }
  body { background: #f7f9fc; }
  [data-testid="stHeader"], [data-testid="stSidebar"] { display: none; }
  .block-container { max-width: 1120px; padding-top: 2rem; padding-bottom: 5rem; }
  .campus-nav { background: #21649d; border-radius: 15px; min-height: 88px;
    display: flex; align-items: center; justify-content: space-between; gap: 1.5rem;
    padding: 1rem 2.2rem; color: white; }
  .campus-brand { color: white; font-size: 1.7rem; font-weight: 800;
    line-height: 1; text-decoration: none; letter-spacing: .01em; flex: 0 0 auto; }
  .campus-links { display: flex; flex-wrap: wrap; justify-content: flex-end; gap: .25rem; }
  .campus-links a { color: white; text-decoration: none; font-size: 1.08rem;
    padding: .7rem .85rem; border-radius: 8px; transition: color .15s, background-color .15s; }
  .campus-links a:hover { color: #ffe27b; background: #164e81; }
  .campus-links a:focus-visible { outline: 3px solid #ffe27b; outline-offset: 2px; }
  .campus-section { scroll-margin-top: 24px; padding: 3rem 1rem 1rem; }
  .campus-section h1, .campus-section h2 { color: #163e68; margin: 0 0 1rem; }
  .campus-section h1 { font-size: clamp(2rem, 5vw, 3.4rem); }
  .campus-section h2 { font-size: 1.8rem; }
  .campus-section p { color: #334155; font-size: 1.05rem; line-height: 1.75; }
  .campus-hero { min-height: 300px; display: flex; flex-direction: column; justify-content: center; }
  .campus-news { background: white; border: 1px solid #dce6ef; border-radius: 16px;
    padding: 1.5rem; margin: 1rem 0; }
  .campus-news h3 { color: #173f68; margin: 0 0 .5rem; font-size: 1.35rem; }
  .campus-news p { margin: 0 0 .75rem; white-space: pre-wrap; overflow-wrap: anywhere; }
  .campus-news time { color: #64748b; font-size: .9rem; }
  .campus-muted { background: #eaf1f7; border-radius: 16px; padding: 1.5rem; }
  @media (max-width: 720px) {
    .campus-nav { align-items: flex-start; flex-direction: column; padding: 1.1rem; }
    .campus-links { justify-content: flex-start; gap: .1rem; }
    .campus-links a { padding: .45rem .55rem; font-size: .95rem; }
    .campus-section { padding: 2.5rem .25rem 1rem; }
  }
  @media (prefers-reduced-motion: reduce) {
    html { scroll-behavior: auto; }
    .campus-links a { transition: none; }
  }
</style>
<nav class="campus-nav" aria-label="主要導覽">
  <a class="campus-brand" href="#home">MY<br>CAMPUS</a>
  <div class="campus-links">
    <a href="#home">首頁</a>
    <a href="#news">最新消息</a>
    <a href="#courses">課程資訊</a>
    <a href="#life">校園生活</a>
    <a href="#contact">聯絡我們</a>
  </div>
</nav>
<section class="campus-section campus-hero" id="home">
  <h1>MY CAMPUS</h1>
  <p>校園消息與課程資訊，都在這裡。</p>
</section>
<section class="campus-section" id="news">
  <h2>最新消息</h2>
  <p>查看校園公告與最新動態。</p>
</section>
""")

try:
    database_url = st.secrets["DATABASE_URL"]
except (KeyError, FileNotFoundError):
    st.error("尚未設定資料庫連線。請在 Streamlit Cloud 的 Secrets 設定 DATABASE_URL。")
    st.stop()

try:
    with psycopg.connect(database_url, connect_timeout=10) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT title, content, created_at FROM announcements_announcement ORDER BY created_at DESC"
            )
            announcements = cursor.fetchall()
except psycopg.Error:
    st.error("目前無法讀取公告資料，請稍後再試。")
    st.stop()

if announcements:
    cards = []
    for title, content, created_at in announcements:
        local_time = created_at.astimezone(ZoneInfo("Asia/Taipei"))
        cards.append(
            '<article class="campus-news">'
            f"<h3>{html.escape(title)}</h3>"
            f"<p>{html.escape(content)}</p>"
            f'<time datetime="{created_at.isoformat()}">發布時間：{local_time:%Y-%m-%d %H:%M}（台灣時間）</time>'
            "</article>"
        )
    st.html("".join(cards))
else:
    st.info("目前沒有公告")

st.html("""
<section class="campus-section" id="courses">
  <h2>課程資訊</h2>
  <div class="campus-muted"><p>課程資訊將於此區公布。</p></div>
</section>
<section class="campus-section" id="life">
  <h2>校園生活</h2>
  <div class="campus-muted"><p>校園活動與生活資訊將於此區公布。</p></div>
</section>
<section class="campus-section" id="contact">
  <h2>聯絡我們</h2>
  <div class="campus-muted"><p>聯絡方式將於此區公布。</p></div>
</section>
""")
