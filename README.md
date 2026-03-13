# 🏙️ Cairo Real Estate Market Analysis Dashboard

A full interactive dashboard built with **Plotly Dash** + **Python** for analyzing Cairo's real estate market trends (2021–2024).

---

## Features

- 📊 **Price Trend Chart** — average listing price over time by property type
- 📍 **Interactive Map** — Cairo neighborhoods colored and sized by price & inventory
- 📦 **Inventory Tracker** — total active listings over time
- 🏠 **Property Type Breakdown** — compare Apartment, Villa, Duplex, Studio, Penthouse
- 🔽 **Filters** — filter by neighborhood and property type
- 📈 **KPI Cards** — avg price, price/sqm, total listings, YoY change

---

## Tech Stack

| Layer | Tech |
|---|---|
| Dashboard / Charts | Plotly Dash |
| Data Processing | Pandas + NumPy |
| Map | Mapbox (via Plotly) |
| Deployment | Render.com (Gunicorn) |

---

## Run Locally

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the app
python app.py

# 3. Open browser at:
http://localhost:8050
```

---

## Deploy to Render.com (Free)

1. Push this folder to a **GitHub repository**
2. Go to [render.com](https://render.com) → New → Web Service
3. Connect your GitHub repo
4. Render auto-detects `render.yaml` and deploys ✅
5. Your app will be live at `https://your-app.onrender.com`

---

## Project Structure

```
cairo-dashboard/
├── app.py            ← Main Dash app (layout + charts + callbacks)
├── data.py           ← Data generator (realistic Cairo market data)
├── requirements.txt  ← Python dependencies
├── render.yaml       ← Render.com deployment config
└── assets/
    └── style.css     ← Dark theme + font styling
```

---

## How It Works (Simple Explanation)

1. **`data.py`** generates a realistic dataset of Cairo real estate:
   - 15 neighborhoods (Zamalek, Maadi, New Cairo, etc.)
   - 5 property types (Apartment, Villa, Duplex, Studio, Penthouse)
   - Monthly data from Jan 2021 → Dec 2024
   - Prices follow real EGP inflation (~20%/year)

2. **`app.py`** is the full dashboard:
   - `app.layout` → defines what you see (filters, charts, map)
   - `@app.callback` → updates all charts when you change filters
   - Each chart is a Plotly figure (line, bar, area, scatter_mapbox)

3. **Render.com** hosts it online using Gunicorn as the web server
