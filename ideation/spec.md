# LLM Stock Prediction MVP Specification

## Overview
A minimalist web app that uses an LLM with a super-analyst persona to predict stock prices. Users can upload their own CSV stock data and instructions, or use provided samples. The app outputs a 1-year monthly prediction for the top 10 most profitable stocks, with explanations, and allows CSV download. Built with Django (Python), Postgres, and HTMX templates.

---

## 1. User Flow
- User lands on a minimalist login/signup page (Django auth, HTMX).
- After login, user sees:
  - Option to use sample stock data and instructions, or upload their own CSV and instructions.md.
  - View default instructions and upload their own if desired.
- User submits data and triggers prediction.
- App displays:
  - Top 10 predicted profitable price movements (table + explanations).
  - Combined line chart of predicted prices for top 10 stocks (12 months).
  - Download link for prediction.csv (1 year, monthly, 10 stocks = 120 rows).

---

## 2. Tech Stack
- Backend: Python, Django (minimal setup), Postgres (for auth only)
- Frontend: HTMX templates, minimalist UI
- LLM: Flexible API key, uses Langchain for LLM API interaction (supports web-enabled LLMs: GPT-4o, Perplexity, Gemini Pro, etc.)
- File storage: Temporary (local, not in DB)

---

## 3. Inputs
- **Stock Data:** CSV only, 3 years of monthly data, any stock symbols (US or international)
  - Format: `symbol,date,open,high,low,close,volume` (one row per stock per month)
- **Instructions:**
  - Default instructions provided (see below)
  - User can view and upload their own instructions.md

---

## 4. LLM Persona Prompt (Default)
You are “The Oracle,” a world-class stock market analyst with a reputation for uncanny accuracy and deep insight. Your tone is confident, concise, and professional, but approachable. You analyze data with scientific rigor, explain your reasoning clearly, and always back up your predictions with evidence from the data. You avoid hype and speculation, focusing on actionable, data-driven insights. When presenting predictions, you rank them by expected profitability and explain the logic behind each one in plain language.

Use state of the art analysis techniques. Take into consideration:
- Technical analysis
- Fundamental analysis
- Geopolitical analysis
- News analysis

Use any data you have access to. The `data.csv` input file is a set of Stock data for an x amount of years. Use that as a baseline. Then use whatever data you have access to about current news events, geopolitical understanding, and the best fundamental & technical analysis expertise you have.

---

## 5. LLM Model
- Uses a web-enabled LLM (e.g., GPT-4o with browsing, Perplexity, Gemini Pro)
- Prompt assumes model can access the internet for real-time data
- API key is pluggable/configurable

---

## 6. Outputs
- **prediction.csv:** 1-year (12 months) prediction for the top 10 most profitable stocks (selected by LLM), 1 row per stock per month (120 rows total)
  - Columns: `symbol,month,predicted_price`
- **UI Table:** Top 10 profitable price movements (with explanations)
- **UI Chart:** Combined line chart for all 10 stocks’ predicted prices over 12 months
- **Download:** Button to download prediction.csv

---

## 7. Minimalist Features
- Minimalist Django auth (login/signup)
- Minimalist HTMX UI (upload, view, download, chart)
- No admin dashboard, logging, or advanced user management
- English only
- Temporary file storage (no DB for uploads/results)

---

## 8. Out of Scope
- Real-time fetching of external data (handled by LLM’s web access)
- Multi-language support
- Persistent storage of user files/results
- Admin/monitoring dashboard

---

## 9. Quick Deployment
- Designed for fast setup and deployment
- Minimal dependencies and configuration

---

## 10. Future Considerations
- Add persistent storage for user files/results
- Add admin dashboard and analytics
- Add multi-language support
- Support for more file formats (e.g., Excel)

---

