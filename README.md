# 🧞 Genie — AI-Powered Data Assistant

Turn natural language questions into live SQL insights — no coding required.

Genie is a modern, Databricks Genie-inspired business intelligence platform that lets non-technical users query PostgreSQL databases using plain English. Built with FastAPI, React, Anthropic Claude, and Recharts.

[FastAPI](https://fastapi.tiangolo.com/) | [React](https://react.dev/) | [PostgreSQL](https://postgresql.org/) | [Anthropic](https://anthropic.com/) | [Vite](https://vitejs.dev/)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🗣️ Natural Language Queries | Ask questions in plain English — "Show me top 10 customers by revenue last quarter" |
| 🔒 Read-Only Security | Enforced SET TRANSACTION READ ONLY — zero risk of data modification |
| 📊 Auto-Generated Visualizations | Smart chart selection (Bar, Line, Pie) powered by Claude AI |
| 🧠 Business Insights | AI-generated contextual analysis alongside raw data |
| ⚡ Real-Time Schema Introspection | Live database schema discovery with intelligent caching |
| 🎨 Modern Chat Interface | Clean, responsive UI inspired by ChatGPT/Claude design patterns |
| 🔍 Transparent SQL | View, copy, and audit every generated query |

---

## 🏗️ Architecture

```mermaid
graph TD
    A[React Client<br>Vite + UI] --> B[FastAPI Backend<br>Python]
    B --> C[PostgreSQL<br>Read-Only]
    B --> D[Anthropic Claude<br>SQL + Viz]
    
    C -.-> B
    D -.-> A
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Node.js 18+
- PostgreSQL database
- Anthropic API key

### Backend Setup
cd backend

Create virtual environment
python -m venv .venv
source .venv/bin/activate # Windows: .venv\Scripts\activate

Install dependencies
pip install -r requirements.txt

Configure environment
cp .env.example .env


Edit `.env` with your credentials:
- DATABASE_URL=postgresql://user:pass@localhost:5432/dbname
- ANTHROPIC_API_KEY=sk-ant-...

Start the API server:
uvicorn main:app --reload --port 8000


API: http://localhost:8000
Swagger Docs: http://localhost:8000/docs

### Frontend Setup
cd frontend

Install dependencies
npm install

Configure environment (optional for local dev)
cp .env.example .env

Start development server
npm run dev


Frontend: http://localhost:5173
Vite auto-proxies /api/* to backend (no CORS issues)

---

## 💡 Usage Examples

| Question | Result |
|----------|--------|
| "What were our total sales by month in 2024?" | Line chart + monthly aggregation |
| "Top 5 products with lowest inventory" | Bar chart + inventory alerts |
| "Customer churn rate by region" | Pie chart + retention insights |
| "Average order value trend" | Time-series line + growth analysis |

---

## 🔒 Security Model
Backend enforces these protections:
SET TRANSACTION READ ONLY # PostgreSQL-level protection

Query whitelist: SELECT / WITH (CTE) only

SQL injection prevention via parameterized queries

API keys never exposed to frontend

---

## 🛠️ Tech Stack

**Backend**
- FastAPI (async Python web framework)
- asyncpg (high-performance PostgreSQL driver)
- Anthropic Claude 3 (LLM for SQL generation)
- Pydantic (data validation)

**Frontend**
- React 18 + Vite (modern build tool)
- Recharts (composable charting library)
- Axios (HTTP client)
- Tailwind CSS (utility-first styling)

---

## 🚢 Production Deployment
Build optimized frontend
cd frontend && npm run build

Serve with production ASGI server
cd backend && pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

Recommended: Use nginx/Caddy as reverse proxy serving frontend/dist as static files with API routes proxied to port 8000.

---

## 🎯 Roadmap

- [ ] Multi-database support (MySQL, SQL Server, BigQuery)
- [ ] User authentication & query history
- [ ] Export to CSV/Excel/PDF
- [ ] Scheduled reports & alerts
- [ ] Custom dashboard builder
- [ ] Slack/Teams integration

---

## 🤝 Contributing

Contributions welcome! Please read our Contributing Guide (coming soon).

---

## 📄 License

MIT License — see LICENSE file.

---

## 🙏 Acknowledgments

- Inspired by Databricks Genie
- Built with Anthropic Claude and FastAPI
- Made with ❤️ for data-driven teams

---

<div align="center">
⭐ Star this repository if you found it helpful! ⭐
</div>
