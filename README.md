# Genie — AI Data Assistant

A Databricks Genie-style AI assistant with a **FastAPI backend** and **React (Vite) frontend**.  
Ask questions in plain English → get live SQL results from your PostgreSQL database.

```
genie-app/
├── backend/          # FastAPI + asyncpg + Anthropic
│   ├── main.py
│   ├── requirements.txt
│   ├── .env.example
│   └── .gitignore
└── frontend/         # React + Vite + Recharts
    ├── src/
    │   ├── App.jsx
    │   ├── api.js
    │   ├── index.css
    │   ├── main.jsx
    │   └── components/
    │       ├── ChartView.jsx
    │       ├── DataTable.jsx
    │       ├── Message.jsx
    │       └── SqlBlock.jsx
    ├── index.html
    ├── package.json
    ├── vite.config.js
    └── .env.example
```

---

## 1 · Backend Setup

```bash
cd backend

# Create & activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy and fill in your secrets
cp .env.example .env
```

Edit `backend/.env`:

```env
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/yourdbname
ANTHROPIC_API_KEY=sk-ant-...
FRONTEND_URL=http://localhost:5173
```

Start the server:

```bash
uvicorn main:app --reload --port 8000
```

API will be live at **http://localhost:8000**  
Swagger docs at **http://localhost:8000/docs**

---

## 2 · Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Copy env file (no changes needed for local dev)
cp .env.example .env
```

Start the dev server:

```bash
npm run dev
```

Frontend will be live at **http://localhost:5173**

> Vite proxies all `/api/*` requests to `http://localhost:8000` automatically — no CORS issues during development.

---

## 3 · How It Works

```
User types question
      │
      ▼
Frontend (React/Vite)
  POST /api/query  { message, history }
      │
      ▼
Backend (FastAPI)
  1. Introspects live DB schema (cached)
  2. Sends schema + question to Claude
  3. Claude returns { sql, explanation, chartType, insight }
  4. Backend executes SQL on PostgreSQL (read-only)
  5. Returns results as JSON
      │
      ▼
Frontend renders
  • Bar / Line / Pie chart  (Recharts)
  • Data table
  • SQL panel (collapsible, with copy button)
  • Business insight card
```

---

## 4 · Security Notes

- The backend enforces **`SET TRANSACTION READ ONLY`** before executing any SQL — no writes possible.
- Only `SELECT` and `WITH` (CTE) statements are allowed; anything else is rejected with HTTP 400.
- Your `ANTHROPIC_API_KEY` and `DATABASE_URL` never leave the backend.

---

## 5 · Production Build

```bash
# Build frontend static files
cd frontend && npm run build

# Serve with a production ASGI server
cd backend && uvicorn main:app --host 0.0.0.0 --port 8000
```

Point your reverse proxy (nginx / Caddy) at port 8000 and serve `frontend/dist` as static files.