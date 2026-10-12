# 雲端公告範例

依照課堂簡報建立：Django Admin 在 Render，資料存在 Neon PostgreSQL，Streamlit Community Cloud 顯示公告。

## 本機檢查

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
Copy-Item .env.example .env
.\.venv\Scripts\python manage.py migrate
.\.venv\Scripts\python manage.py createsuperuser
.\.venv\Scripts\python manage.py runserver
```

開啟 `http://127.0.0.1:8000/admin/`，新增 Announcement。未填 `DATABASE_URL` 時，本機使用 SQLite；部署時必須在 Render 設定 Neon 的完整連線字串。

## 雲端部署

1. 在 Neon 建立 PostgreSQL 專案，複製含密碼的 Connection String。不要把它寫入 GitHub。
2. 將本專案推到 GitHub。`render.yaml` 定義 Render 的免費 Web Service。在 Render 用 Blueprint 連結此倉庫，設定 `DATABASE_URL`。`SECRET_KEY` 會由 Render 產生。
3. 部署成功後前往 `https://服務網域/admin/`。若本機先用 SQLite 建立管理員，需改連 Neon 後再執行 `createsuperuser`；若本機已連 Neon，原帳號可沿用。
4. 在 Streamlit Community Cloud 從同一 GitHub 倉庫建立 App，Main file path 選 `frontend/app.py`。在 App Settings → Secrets 加入：

   ```toml
   DATABASE_URL = "postgresql://user:password@host/database?sslmode=require"
   ```

5. 在 Django Admin 新增公告，重新整理 Streamlit 網頁確認顯示。

Render 的建置會執行 `collectstatic` 和 `migrate`。Streamlit 只讀取公告，不顯示資料庫錯誤細節。
