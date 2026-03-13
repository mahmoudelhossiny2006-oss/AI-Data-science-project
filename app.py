import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from data import generate_cairo_data

# ── Load data ──────────────────────────────────────────────────────────────────
df = generate_cairo_data()
neighborhoods = sorted(df["neighborhood"].unique())
property_types = sorted(df["property_type"].unique())

# ── App init ───────────────────────────────────────────────────────────────────
app = dash.Dash(
    __name__,
    title="Cairo Real Estate Dashboard",
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}]
)
server = app.server  # for Render/Gunicorn

# ── Color palette ──────────────────────────────────────────────────────────────
GOLD   = "#C9A84C"
DARK   = "#0F0F0F"
CARD   = "#1A1A1A"
BORDER = "#2A2A2A"
TEXT   = "#E8E8E0"
MUTED  = "#888880"

# ── Layout ─────────────────────────────────────────────────────────────────────
app.layout = html.Div(style={"backgroundColor": DARK, "minHeight": "100vh", "fontFamily": "'IBM Plex Mono', monospace", "color": TEXT}, children=[

    # ── Header ────────────────────────────────────────────────────────────────
    html.Div(style={"borderBottom": f"1px solid {BORDER}", "padding": "24px 40px", "display": "flex", "alignItems": "center", "justifyContent": "space-between"}, children=[
        html.Div([
            html.Span("🏙️ ", style={"fontSize": "28px"}),
            html.Span("CAIRO", style={"fontSize": "26px", "fontWeight": "700", "color": GOLD, "letterSpacing": "6px"}),
            html.Span("  REAL ESTATE INTEL", style={"fontSize": "14px", "color": MUTED, "letterSpacing": "3px"}),
        ]),
        html.Div("2021 – 2024 MARKET DATA", style={"fontSize": "11px", "color": MUTED, "letterSpacing": "2px"}),
    ]),

    # ── Filters ───────────────────────────────────────────────────────────────
    html.Div(style={"padding": "20px 40px", "display": "flex", "gap": "24px", "flexWrap": "wrap", "borderBottom": f"1px solid {BORDER}", "backgroundColor": "#111"}, children=[
        html.Div([
            html.Label("NEIGHBORHOOD", style={"fontSize": "10px", "color": MUTED, "letterSpacing": "2px", "display": "block", "marginBottom": "8px"}),
            dcc.Dropdown(
                id="filter-neighborhood",
                options=[{"label": n, "value": n} for n in neighborhoods],
                value=neighborhoods,
                multi=True,
                placeholder="All neighborhoods...",
                style={"width": "360px", "backgroundColor": CARD},
                className="dark-dropdown"
            ),
        ]),
        html.Div([
            html.Label("PROPERTY TYPE", style={"fontSize": "10px", "color": MUTED, "letterSpacing": "2px", "display": "block", "marginBottom": "8px"}),
            dcc.Dropdown(
                id="filter-type",
                options=[{"label": t, "value": t} for t in property_types],
                value=property_types,
                multi=True,
                placeholder="All types...",
                style={"width": "300px"},
                className="dark-dropdown"
            ),
        ]),
    ]),

    # ── KPI Row ───────────────────────────────────────────────────────────────
    html.Div(id="kpi-row", style={"display": "flex", "gap": "1px", "backgroundColor": BORDER, "borderBottom": f"1px solid {BORDER}"}),

    # ── Charts grid ───────────────────────────────────────────────────────────
    html.Div(style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "1px", "backgroundColor": BORDER}, children=[
        html.Div(style={"backgroundColor": DARK, "padding": "28px"}, children=[
            html.Div("AVG PRICE TREND OVER TIME", style={"fontSize": "11px", "color": MUTED, "letterSpacing": "2px", "marginBottom": "16px"}),
            dcc.Graph(id="chart-trend", config={"displayModeBar": False})
        ]),
        html.Div(style={"backgroundColor": DARK, "padding": "28px"}, children=[
            html.Div("PRICE PER SQM BY NEIGHBORHOOD", style={"fontSize": "11px", "color": MUTED, "letterSpacing": "2px", "marginBottom": "16px"}),
            dcc.Graph(id="chart-sqm", config={"displayModeBar": False})
        ]),
        html.Div(style={"backgroundColor": DARK, "padding": "28px"}, children=[
            html.Div("INVENTORY (ACTIVE LISTINGS)", style={"fontSize": "11px", "color": MUTED, "letterSpacing": "2px", "marginBottom": "16px"}),
            dcc.Graph(id="chart-inventory", config={"displayModeBar": False})
        ]),
        html.Div(style={"backgroundColor": DARK, "padding": "28px"}, children=[
            html.Div("PROPERTY TYPE PRICE BREAKDOWN", style={"fontSize": "11px", "color": MUTED, "letterSpacing": "2px", "marginBottom": "16px"}),
            dcc.Graph(id="chart-type", config={"displayModeBar": False})
        ]),
    ]),

    # ── Map ───────────────────────────────────────────────────────────────────
    html.Div(style={"backgroundColor": DARK, "padding": "28px", "borderTop": f"1px solid {BORDER}"}, children=[
        html.Div("CAIRO NEIGHBORHOOD PRICE MAP", style={"fontSize": "11px", "color": MUTED, "letterSpacing": "2px", "marginBottom": "16px"}),
        dcc.Graph(id="chart-map", config={"displayModeBar": False}, style={"height": "500px"})
    ]),

    # ── Footer ────────────────────────────────────────────────────────────────
    html.Div(style={"borderTop": f"1px solid {BORDER}", "padding": "16px 40px", "textAlign": "center", "color": MUTED, "fontSize": "11px", "letterSpacing": "1px"}, children=[
        "CAIRO REAL ESTATE MARKET ANALYSIS DASHBOARD  ·  DATA: 2021–2024  ·  BUILT WITH PLOTLY DASH"
    ])
])

# ── Helpers ───────────────────────────────────────────────────────────────────
CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="IBM Plex Mono", color=TEXT, size=11),
    margin=dict(l=10, r=10, t=10, b=10),
    xaxis=dict(gridcolor=BORDER, zeroline=False),
    yaxis=dict(gridcolor=BORDER, zeroline=False),
    legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor=BORDER),
    colorway=[GOLD, "#E8834A", "#6CA6CD", "#A8D8A8", "#C98BBF"],
)

def fmt_egp(val):
    if val >= 1_000_000:
        return f"EGP {val/1_000_000:.1f}M"
    return f"EGP {val/1_000:.0f}K"

# ── Callbacks ─────────────────────────────────────────────────────────────────
@app.callback(
    Output("kpi-row", "children"),
    Output("chart-trend", "figure"),
    Output("chart-sqm", "figure"),
    Output("chart-inventory", "figure"),
    Output("chart-type", "figure"),
    Output("chart-map", "figure"),
    Input("filter-neighborhood", "value"),
    Input("filter-type", "value"),
)
def update_all(selected_neighborhoods, selected_types):
    # Guard
    if not selected_neighborhoods or not selected_types:
        empty = go.Figure()
        empty.update_layout(**CHART_LAYOUT)
        return [], empty, empty, empty, empty, empty

    filtered = df[
        df["neighborhood"].isin(selected_neighborhoods) &
        df["property_type"].isin(selected_types)
    ]

    # ── KPIs ──────────────────────────────────────────────────────────────────
    latest = filtered[filtered["date"] == filtered["date"].max()]
    prev_year = filtered[filtered["date"] == filtered["date"].max() - pd.DateOffset(years=1)]

    avg_price = latest["avg_price_egp"].mean()
    avg_sqm   = latest["price_per_sqm"].mean()
    total_inv = latest["listings"].sum()
    n_hoods   = latest["neighborhood"].nunique()

    prev_price = prev_year["avg_price_egp"].mean() if len(prev_year) else avg_price
    yoy = ((avg_price - prev_price) / prev_price * 100) if prev_price else 0

    def kpi_card(label, value, sub=None):
        return html.Div(style={"flex": "1", "backgroundColor": CARD, "padding": "20px 28px", "borderRight": f"1px solid {BORDER}"}, children=[
            html.Div(label, style={"fontSize": "10px", "color": MUTED, "letterSpacing": "2px", "marginBottom": "8px"}),
            html.Div(value, style={"fontSize": "22px", "fontWeight": "700", "color": GOLD}),
            html.Div(sub or "", style={"fontSize": "11px", "color": "#5A8A5A" if yoy >= 0 else "#C05050", "marginTop": "4px"}),
        ])

    kpis = [
        kpi_card("AVG LISTING PRICE", fmt_egp(avg_price), f"{'▲' if yoy>=0 else '▼'} {abs(yoy):.1f}% YoY"),
        kpi_card("AVG PRICE / SQM", fmt_egp(avg_sqm)),
        kpi_card("ACTIVE LISTINGS", f"{total_inv:,}"),
        kpi_card("NEIGHBORHOODS", str(n_hoods)),
    ]

    # ── Trend chart ───────────────────────────────────────────────────────────
    trend = filtered.groupby(["date", "property_type"])["avg_price_egp"].mean().reset_index()
    fig_trend = px.line(trend, x="date", y="avg_price_egp", color="property_type", labels={"avg_price_egp": "Avg Price (EGP)", "date": "", "property_type": ""})
    fig_trend.update_traces(line_width=2)
    fig_trend.update_layout(**CHART_LAYOUT)

    # ── Price per sqm bar ─────────────────────────────────────────────────────
    sqm = filtered.groupby("neighborhood")["price_per_sqm"].mean().reset_index().sort_values("price_per_sqm", ascending=True)
    fig_sqm = px.bar(sqm, x="price_per_sqm", y="neighborhood", orientation="h", labels={"price_per_sqm": "EGP / sqm", "neighborhood": ""})
    fig_sqm.update_traces(marker_color=GOLD)
    fig_sqm.update_layout(**CHART_LAYOUT)

    # ── Inventory area chart ──────────────────────────────────────────────────
    inv = filtered.groupby("date")["listings"].sum().reset_index()
    fig_inv = px.area(inv, x="date", y="listings", labels={"listings": "Total Listings", "date": ""})
    fig_inv.update_traces(line_color=GOLD, fillcolor="rgba(201,168,76,0.15)")
    fig_inv.update_layout(**CHART_LAYOUT)

    # ── Property type breakdown ───────────────────────────────────────────────
    type_data = filtered.groupby("property_type")["avg_price_egp"].mean().reset_index().sort_values("avg_price_egp")
    fig_type = px.bar(type_data, x="property_type", y="avg_price_egp", labels={"avg_price_egp": "Avg Price (EGP)", "property_type": ""})
    fig_type.update_traces(marker_color=[GOLD, "#E8834A", "#6CA6CD", "#A8D8A8", "#C98BBF"][:len(type_data)])
    fig_type.update_layout(**CHART_LAYOUT)

    # ── Map ───────────────────────────────────────────────────────────────────
    map_data = filtered.groupby(["neighborhood", "lat", "lon"]).agg(
        avg_price=("avg_price_egp", "mean"),
        listings=("listings", "sum")
    ).reset_index()

    fig_map = px.scatter_mapbox(
        map_data,
        lat="lat", lon="lon",
        size="listings",
        color="avg_price",
        hover_name="neighborhood",
        hover_data={"avg_price": ":,.0f", "listings": True, "lat": False, "lon": False},
        color_continuous_scale=[[0, "#1A3A2A"], [0.5, GOLD], [1, "#FF6B35"]],
        size_max=40,
        zoom=10,
        center={"lat": 30.044, "lon": 31.235},
        mapbox_style="carto-darkmatter",
        labels={"avg_price": "Avg Price (EGP)"}
    )
    fig_map.update_layout(paper_bgcolor="rgba(0,0,0,0)", font=dict(family="IBM Plex Mono", color=TEXT), margin=dict(l=0,r=0,t=0,b=0), coloraxis_colorbar=dict(title="Avg Price", tickfont=dict(color=TEXT), titlefont=dict(color=TEXT)))

    return kpis, fig_trend, fig_sqm, fig_inv, fig_type, fig_map


if __name__ == "__main__":
    app.run(debug=True, port=8050)
