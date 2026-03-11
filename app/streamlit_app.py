"""
NidDouillet — Observatoire du marché immobilier toulonnais
Dashboard principal Streamlit
"""

import streamlit as st
import pandas as pd
import numpy as np
import sys
import os
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Ajouter le répertoire racine au path
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from analysis.stats import (
    mean, median, variance, standard_deviation,
    correlation
)
from analysis.regression import least_squares_fit, predict, r_squared
from analysis.scoring import opportunity_score

# ─── Config page ────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="NidDouillet · Observatoire Toulonnais",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS personnalisé ────────────────────────────────────────────────────────

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,400&family=Syne:wght@400;600;700&display=swap');

  html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
    background-color: #0a0f1a;
    color: #e8e0d0;
  }

  h1, h2, h3 {
    font-family: 'Playfair Display', serif !important;
    color: #f5e6c8 !important;
  }

  /* ── SIDEBAR NOIR ── */
  [data-testid="stSidebar"] {
    background: #080c14 !important;
    border-right: 1px solid rgba(255,180,60,0.15) !important;
  }
  [data-testid="stSidebar"] * {
    color: #c8bfad !important;
  }
  [data-testid="stSidebar"] .stRadio label {
    color: #c8bfad !important;
    font-size: 0.9rem;
    padding: 6px 0;
  }
  [data-testid="stSidebar"] .stRadio [data-baseweb="radio"] {
    background: transparent;
  }
  [data-testid="stSidebar"] [data-baseweb="select"] > div,
  [data-testid="stSidebar"] [data-baseweb="input"] > div {
    background: #111827 !important;
    border-color: rgba(255,180,60,0.2) !important;
    color: #e8e0d0 !important;
  }
  [data-testid="stSidebar"] .stSlider [data-testid="stTickBar"] {
    color: #6b7a8d !important;
  }
  [data-testid="stSidebar"] hr {
    border-color: rgba(255,180,60,0.15) !important;
  }
  [data-testid="stSidebar"] .stSelectbox label,
  [data-testid="stSidebar"] .stSlider label {
    color: #8fa0b0 !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
  }

  /* Sidebar logo zone */
  .sidebar-brand {
    padding: 1rem 0 0.5rem 0;
    border-bottom: 1px solid rgba(255,180,60,0.2);
    margin-bottom: 1.2rem;
  }
  .sidebar-brand .logo-text {
    font-family: 'Playfair Display', serif;
    font-size: 1.3rem;
    color: #f5e6c8 !important;
    font-weight: 700;
  }
  .sidebar-brand .logo-sub {
    font-size: 0.72rem;
    color: #ffb43c !important;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-top: 2px;
  }

  /* Nav items custom */
  .nav-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px 12px;
    border-radius: 8px;
    margin: 3px 0;
    cursor: pointer;
    transition: background 0.2s;
  }
  .nav-item:hover { background: rgba(255,180,60,0.08); }
  .nav-item.active { background: rgba(255,180,60,0.15); border-left: 2px solid #ffb43c; }

  /* ── MAIN BACKGROUND ── */
  .main .block-container {
    background: #0a0f1a;
    padding-top: 1.5rem;
  }

  /* ── HERO ── */
  .hero {
    background: linear-gradient(135deg, #0d1b2a 0%, #0a1520 50%, #111827 100%);
    border: 1px solid rgba(255,180,60,0.2);
    border-radius: 20px;
    padding: 2.8rem 3.2rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
  }
  .hero::before {
    content: '';
    position: absolute;
    top: -80px; right: -80px;
    width: 350px; height: 350px;
    background: radial-gradient(circle, rgba(255,180,60,0.12) 0%, transparent 65%);
    border-radius: 50%;
    pointer-events: none;
  }
  .hero::after {
    content: '';
    position: absolute;
    bottom: -60px; left: -40px;
    width: 250px; height: 250px;
    background: radial-gradient(circle, rgba(26,143,160,0.1) 0%, transparent 65%);
    border-radius: 50%;
    pointer-events: none;
  }
  .hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(255,180,60,0.12);
    color: #ffb43c;
    border: 1px solid rgba(255,180,60,0.3);
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    margin-bottom: 1rem;
    text-transform: uppercase;
  }
  .hero-badge::before {
    content: '';
    width: 7px; height: 7px;
    background: #ffb43c;
    border-radius: 50%;
    animation: pulse 1.8s ease-in-out infinite;
  }
  @keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.4; transform: scale(0.7); }
  }
  .hero h1 {
    font-size: 2.6rem !important;
    margin: 0 0 0.4rem 0 !important;
    line-height: 1.15 !important;
    background: linear-gradient(135deg, #f5e6c8, #ffb43c 60%, #e8c88a);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }
  .hero p {
    color: rgba(200,191,173,0.7);
    font-size: 0.98rem;
    margin: 0;
    line-height: 1.6;
  }

  /* ── KPI CARDS ── */
  .kpi-card {
    background: linear-gradient(145deg, #111827, #0d1520);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 1.5rem 1.6rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s, transform 0.2s;
  }
  .kpi-card:hover {
    border-color: rgba(255,180,60,0.3);
    transform: translateY(-2px);
  }
  .kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #ffb43c, transparent);
  }
  .kpi-label {
    color: #6b7a8d;
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 0.6rem;
  }
  .kpi-value {
    color: #f5e6c8;
    font-size: 2.1rem;
    font-weight: 700;
    font-family: 'Playfair Display', serif;
    line-height: 1;
  }
  .kpi-sub {
    color: #4a5a6a;
    font-size: 0.75rem;
    margin-top: 0.4rem;
  }
  .kpi-icon {
    position: absolute;
    top: 1.2rem; right: 1.2rem;
    font-size: 1.6rem;
    opacity: 0.2;
  }

  /* ── SCORE BADGES ── */
  .score-high   { background: rgba(34,197,94,0.15); color: #4ade80; border: 1px solid rgba(34,197,94,0.3); border-radius: 8px; padding: 4px 12px; font-weight: 700; font-size: 0.85rem; }
  .score-medium { background: rgba(234,179,8,0.15);  color: #fbbf24; border: 1px solid rgba(234,179,8,0.3);  border-radius: 8px; padding: 4px 12px; font-weight: 700; font-size: 0.85rem; }
  .score-low    { background: rgba(239,68,68,0.15);  color: #f87171; border: 1px solid rgba(239,68,68,0.3);  border-radius: 8px; padding: 4px 12px; font-weight: 700; font-size: 0.85rem; }

  /* ── SECTION TITLES ── */
  .section-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.35rem;
    color: #f5e6c8 !important;
    margin: 2.2rem 0 1.2rem 0;
    padding-bottom: 0.6rem;
    border-bottom: 1px solid rgba(255,180,60,0.2);
    display: flex;
    align-items: center;
    gap: 10px;
  }

  /* ── DATAFRAME ── */
  [data-testid="stDataFrame"] {
    background: #111827 !important;
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.06) !important;
  }

  /* ── METRICS ── */
  [data-testid="metric-container"] {
    background: #111827;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 1rem;
  }
  [data-testid="metric-container"] label {
    color: #6b7a8d !important;
    font-size: 0.75rem !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
  }
  [data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #f5e6c8 !important;
    font-family: 'Playfair Display', serif !important;
  }

  /* ── INFO BOX ── */
  [data-testid="stInfo"] {
    background: rgba(26,143,160,0.12) !important;
    border: 1px solid rgba(26,143,160,0.3) !important;
    color: #a8d8e0 !important;
    border-radius: 10px;
  }

  /* ── SUCCESS BOX ── */
  [data-testid="stSuccess"] {
    background: rgba(34,197,94,0.1) !important;
    border: 1px solid rgba(34,197,94,0.25) !important;
    color: #86efac !important;
    border-radius: 10px;
  }

  /* ── TABLE HTML custom ── */
  table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.88rem;
    color: #c8bfad;
  }
  th {
    background: #111827;
    color: #6b7a8d;
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    padding: 10px 14px;
    border-bottom: 1px solid rgba(255,255,255,0.07);
    font-weight: 700;
  }
  td {
    padding: 10px 14px;
    border-bottom: 1px solid rgba(255,255,255,0.04);
  }
  tr:hover td { background: rgba(255,180,60,0.04); }

  /* ── FOOTER ── */
  .footer {
    text-align: center;
    color: #2a3545;
    font-size: 0.72rem;
    margin-top: 4rem;
    padding-top: 1.5rem;
    border-top: 1px solid rgba(255,255,255,0.05);
    letter-spacing: 0.05em;
  }

  /* ── SCROLLBAR ── */
  ::-webkit-scrollbar { width: 5px; }
  ::-webkit-scrollbar-track { background: #080c14; }
  ::-webkit-scrollbar-thumb { background: #1e2d3d; border-radius: 3px; }

</style>
""", unsafe_allow_html=True)

# ─── Chargement des données ──────────────────────────────────────────────────

def _no_data_screen(message: str):
    """Affiche un écran d'attente élégant quand les données sont manquantes."""
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #0d1b2a, #111827);
        border: 1px solid rgba(255,180,60,0.2);
        border-radius: 20px;
        padding: 3.5rem 2rem;
        text-align: center;
        margin: 2rem 0;
    ">
      <div style="font-size: 3rem; margin-bottom: 1rem;">⏳</div>
      <div style="
        font-family: 'Playfair Display', serif;
        font-size: 1.5rem;
        color: #f5e6c8;
        margin-bottom: 0.8rem;
      ">Données en cours de collecte</div>
      <div style="color: #6b7a8d; font-size: 0.9rem; max-width: 400px; margin: 0 auto; line-height: 1.7;">
        {message}
      </div>
      <div style="
        display: inline-block;
        margin-top: 1.5rem;
        background: rgba(255,180,60,0.1);
        border: 1px solid rgba(255,180,60,0.25);
        color: #ffb43c;
        border-radius: 20px;
        padding: 5px 16px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
      ">En attente · Pipeline de données</div>
    </div>
    """, unsafe_allow_html=True)


@st.cache_data(show_spinner="Chargement des données DVF…")
def load_dvf():
    dvf_path = ROOT / "data" / "dvf_toulon_clean.csv"
    if not dvf_path.exists():
        dvf_path = ROOT / "data" / "dvf_toulon.csv"
    if not dvf_path.exists():
        return None  # Pas de données disponibles

    df = pd.read_csv(dvf_path, low_memory=False)
    col_map = {}
    for col in df.columns:
        lc = col.lower().replace(" ", "_")
        if "prix" in lc or "valeur" in lc:
            col_map[col] = "prix"
        elif "surface" in lc and "bati" in lc:
            col_map[col] = "surface"
        elif "commune" in lc or "nom_commune" in lc:
            col_map[col] = "commune"
        elif "code_postal" in lc or "cp" in lc:
            col_map[col] = "code_postal"
        elif "type_local" in lc or "nature" in lc:
            col_map[col] = "type_bien"
        elif "date" in lc and "mutation" in lc:
            col_map[col] = "date"
    df = df.rename(columns=col_map)
    if "commune" in df.columns:
        df = df[df["commune"].str.upper().str.contains("TOULON", na=False)]
    elif "code_postal" in df.columns:
        df["code_postal"] = pd.to_numeric(df["code_postal"], errors="coerce")
        df = df[(df["code_postal"] >= 83000) & (df["code_postal"] <= 83100)]
    for col in ["prix", "surface"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    if "prix" in df.columns and "surface" in df.columns:
        df = df[(df["prix"] > 10_000) & (df["surface"] > 5) & (df["surface"] < 500)]
        df["prix_m2"] = df["prix"] / df["surface"]
    return df


@st.cache_data(show_spinner="Chargement des annonces…")
def load_annonces():
    ann_path = ROOT / "data" / "annonces.csv"
    if not ann_path.exists():
        return None  # Pas de données disponibles
    return pd.read_csv(ann_path, low_memory=False)


# ─── Sidebar ─────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
      <div class="logo-text">🏠 NidDouillet</div>
      <div class="logo-sub">Observatoire Toulonnais</div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        ["📊 Tableau de bord", "🗺️ Carte des prix", "📈 Tendances",
         "🔍 Scoring Opportunités", "⚙️ Stats avancées"],
        label_visibility="collapsed",
    )

    st.divider()
    st.markdown("<span style='color:#6b7a8d;font-size:0.72rem;font-weight:700;text-transform:uppercase;letter-spacing:0.1em'>FILTRES</span>", unsafe_allow_html=True)
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    df_dvf_raw = load_dvf()
    df_ann_raw = load_annonces()

    dvf_ok = df_dvf_raw is not None
    ann_ok = df_ann_raw is not None

    type_options = ["Tous"] + sorted(df_dvf_raw["type_bien"].dropna().unique().tolist()) \
        if dvf_ok and "type_bien" in df_dvf_raw.columns else ["Tous"]
    type_filter = st.selectbox("Type de bien", type_options)

    prix_max = int(df_dvf_raw["prix"].quantile(0.99)) \
        if dvf_ok and "prix" in df_dvf_raw.columns else 900_000
    budget = st.slider("Budget max (€)", 100_000, prix_max, 450_000, step=10_000)

    surface_min = st.slider("Surface min (m²)", 10, 150, 30)

    st.divider()
    dvf_label = f"<b style='color:#6b7a8d'>{len(df_dvf_raw):,}</b>" if dvf_ok else "<b style='color:#e05c5c'>—</b>"
    ann_label  = f"<b style='color:#6b7a8d'>{len(df_ann_raw):,}</b>" if ann_ok  else "<b style='color:#e05c5c'>—</b>"
    st.markdown(
        f"<small style='color:#3a4a5a'>DVF · {dvf_label} transactions<br>"
        f"Annonces · {ann_label} biens</small>",
        unsafe_allow_html=True
    )


# ─── Filtrage ─────────────────────────────────────────────────────────────────

def apply_filters(df):
    if df is None:
        return None
    d = df.copy()
    if type_filter != "Tous" and "type_bien" in d.columns:
        d = d[d["type_bien"] == type_filter]
    if "prix" in d.columns:
        d = d[d["prix"] <= budget]
    if "surface" in d.columns:
        d = d[d["surface"] >= surface_min]
    return d

df_dvf = apply_filters(df_dvf_raw)
df_ann = apply_filters(df_ann_raw)

# Palette dark
NAVY   = "#0d2233"
GOLD   = "#ffb43c"
TEAL   = "#1a8fa0"
DARK_BG = "#111827"
COLORS = [TEAL, GOLD, "#e05c5c", "#5cb85c", "#7a6cf0", "#f08c3c", "#3ca8f0", "#c87aa8"]

PLOTLY_DARK = dict(
    template="plotly_dark",
    paper_bgcolor="#111827",
    plot_bgcolor="#111827",
    font=dict(color="#c8bfad", family="Syne"),
    margin=dict(l=0, r=0, t=10, b=0),
)

# ─── PAGE : TABLEAU DE BORD ───────────────────────────────────────────────────

if page == "📊 Tableau de bord":

    st.markdown("""
    <div class="hero">
      <div class="hero-badge">Live · Marché Toulonnais</div>
      <h1>Observatoire NidDouillet</h1>
      <p>Analyse statistique du marché immobilier de Toulon<br>Données DVF data.gouv.fr · Algorithmes from scratch</p>
    </div>
    """, unsafe_allow_html=True)

    if df_dvf is None:
        _no_data_screen("Les données DVF Toulon n'ont pas encore été intégrées.<br>En attente du pipeline de collecte de votre équipe.")
        st.stop()

    pm2_vals  = df_dvf["prix_m2"].dropna().tolist() if "prix_m2" in df_dvf.columns else []
    pm2_mean  = mean(pm2_vals)  if pm2_vals else 0
    pm2_med   = median(pm2_vals) if pm2_vals else 0
    pm2_std   = standard_deviation(pm2_vals) if pm2_vals else 0
    n_trans   = len(df_dvf)

    col1, col2, col3, col4 = st.columns(4)
    kpis = [
        ("Prix moyen / m²", f"{pm2_mean:,.0f} €", f"Médiane : {pm2_med:,.0f} €/m²", "📐"),
        ("Transactions", f"{n_trans:,}", f"sur {len(df_dvf_raw):,} au total", "📋"),
        ("Budget / m²", f"{budget / surface_min:,.0f} €", f"Pour {surface_min} m² min", "💰"),
        ("Volatilité", f"{pm2_std:,.0f} €", "Écart-type €/m²", "📊"),
    ]
    for col, (label, value, sub, icon) in zip([col1, col2, col3, col4], kpis):
        with col:
            st.markdown(f"""
            <div class="kpi-card">
              <div class="kpi-icon">{icon}</div>
              <div class="kpi-label">{label}</div>
              <div class="kpi-value">{value}</div>
              <div class="kpi-sub">{sub}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown('<div class="section-title">📉 Distribution des prix au m²</div>', unsafe_allow_html=True)

    col_a, col_b = st.columns([3, 2])
    with col_a:
        if pm2_vals:
            fig = go.Figure()
            fig.add_trace(go.Histogram(x=pm2_vals, nbinsx=50,
                                       marker_color=TEAL, opacity=0.85, name="DVF"))
            if "prix_m2" in df_ann.columns:
                fig.add_trace(go.Histogram(
                    x=df_ann["prix_m2"].dropna().tolist(),
                    nbinsx=40, marker_color=GOLD, opacity=0.65, name="Annonces"))
            fig.add_vline(x=pm2_mean, line_dash="dash", line_color="#e05c5c",
                          annotation_text=f"Moy. {pm2_mean:,.0f}€",
                          annotation_font_color="#e05c5c")
            fig.add_vline(x=pm2_med, line_dash="dot", line_color="#7a6cf0",
                          annotation_text=f"Méd. {pm2_med:,.0f}€",
                          annotation_font_color="#7a6cf0")
            fig.update_layout(**PLOTLY_DARK, height=320, barmode="overlay",
                               legend=dict(orientation="h", y=1.02),
                               xaxis_title="€/m²", yaxis_title="Fréquence",
                               xaxis=dict(gridcolor="rgba(255,255,255,0.04)"),
                               yaxis=dict(gridcolor="rgba(255,255,255,0.04)"))
            st.plotly_chart(fig, use_container_width=True)

    with col_b:
        if pm2_vals and len(pm2_vals) >= 4:
            stats = describe(pm2_vals)
            rows = {
                "Minimum":       f"{stats.get('min', min(pm2_vals)):,.0f} €/m²",
                "P25":           f"{percentile(pm2_vals, 25):,.0f} €/m²",
                "Médiane":       f"{pm2_med:,.0f} €/m²",
                "Moyenne":       f"{pm2_mean:,.0f} €/m²",
                "P75":           f"{percentile(pm2_vals, 75):,.0f} €/m²",
                "Maximum":       f"{stats.get('max', max(pm2_vals)):,.0f} €/m²",
                "Écart-type":    f"{pm2_std:,.0f} €/m²",
                "Transactions":  f"{n_trans:,}",
            }
            st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
            for k, v in rows.items():
                c1, c2 = st.columns([1.3, 1])
                c1.markdown(f"<small style='color:#4a5a6a;font-weight:700;text-transform:uppercase;letter-spacing:0.05em;font-size:0.7rem'>{k}</small>", unsafe_allow_html=True)
                c2.markdown(f"<small style='color:#c8bfad;font-weight:600'>{v}</small>", unsafe_allow_html=True)

    if "quartier" in df_dvf.columns and "prix_m2" in df_dvf.columns:
        st.markdown('<div class="section-title">🏘️ Prix moyen par quartier</div>', unsafe_allow_html=True)
        q_stats = (df_dvf.groupby("quartier")["prix_m2"]
                   .agg(["mean", "count"])
                   .sort_values("mean", ascending=True)
                   .reset_index())
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            y=q_stats["quartier"], x=q_stats["mean"], orientation="h",
            marker=dict(
                color=q_stats["mean"],
                colorscale=[[0, "#1a3a4a"], [0.5, TEAL], [1, GOLD]],
                showscale=False,
            ),
            name="Moyenne €/m²",
            text=q_stats["mean"].apply(lambda v: f"{v:,.0f} €"),
            textposition="outside",
            textfont=dict(color="#c8bfad", size=11),
        ))
        fig2.update_layout(**PLOTLY_DARK, height=320,
                            xaxis_title="€/m²",
                            xaxis=dict(gridcolor="rgba(255,255,255,0.04)"),
                            yaxis=dict(gridcolor="rgba(0,0,0,0)"))
        st.plotly_chart(fig2, use_container_width=True)


# ─── PAGE : CARTE ─────────────────────────────────────────────────────────────

elif page == "🗺️ Carte des prix":
    st.markdown('<div class="section-title">🗺️ Carte des prix par quartier</div>', unsafe_allow_html=True)
    if df_dvf is None:
        _no_data_screen("Les données DVF sont nécessaires pour afficher la carte.<br>En attente du pipeline de collecte.")
        st.stop()

    COORDS = {
        "Centre":        (43.1242, 5.9280),
        "Le Mourillon":  (43.1168, 5.9450),
        "Le Jonquet":    (43.1350, 5.9100),
        "La Serinette":  (43.1450, 5.9200),
        "Sainte-Musse":  (43.1300, 5.9600),
        "Cap Brun":      (43.1050, 5.9550),
        "La Rode":       (43.1380, 5.9400),
        "Pont du Las":   (43.1480, 5.9350),
    }

    if "quartier" in df_dvf.columns and "prix_m2" in df_dvf.columns:
        q_agg = df_dvf.groupby("quartier")["prix_m2"].mean().reset_index()
        q_agg["lat"] = q_agg["quartier"].map(lambda q: COORDS.get(q, (43.125, 5.93))[0])
        q_agg["lon"] = q_agg["quartier"].map(lambda q: COORDS.get(q, (43.125, 5.93))[1])
        q_agg.columns = ["quartier", "prix_m2_moyen", "lat", "lon"]

        fig_map = px.scatter_mapbox(
            q_agg, lat="lat", lon="lon",
            size="prix_m2_moyen", color="prix_m2_moyen",
            color_continuous_scale=[[0, "#0d2233"], [0.5, TEAL], [1, GOLD]],
            hover_name="quartier",
            hover_data={"prix_m2_moyen": ":.0f", "lat": False, "lon": False},
            zoom=12, height=520, size_max=50,
        )
        fig_map.update_layout(
            mapbox_style="carto-darkmatter",
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor="#111827",
            coloraxis_colorbar=dict(title="€/m²", tickfont=dict(color="#c8bfad"), title_font=dict(color="#c8bfad")),
        )
        st.plotly_chart(fig_map, use_container_width=True)
        st.dataframe(
            q_agg[["quartier", "prix_m2_moyen"]].rename(
                columns={"quartier": "Quartier", "prix_m2_moyen": "€/m² moyen"}),
            use_container_width=True, hide_index=True)
    else:
        st.info("Données quartier non disponibles.")


# ─── PAGE : TENDANCES ─────────────────────────────────────────────────────────

elif page == "📈 Tendances":
    st.markdown('<div class="section-title">📈 Évolution temporelle des prix</div>', unsafe_allow_html=True)
    if df_dvf is None:
        _no_data_screen("Les données DVF sont nécessaires pour afficher les tendances.<br>En attente du pipeline de collecte.")
        st.stop()

    if "date" in df_dvf.columns and "prix_m2" in df_dvf.columns:
        df_t = df_dvf.copy()
        df_t["date"] = pd.to_datetime(df_t["date"], errors="coerce")
        df_t = df_t.dropna(subset=["date", "prix_m2"])
        df_t["mois"] = df_t["date"].dt.to_period("M").astype(str)
        monthly = (df_t.groupby("mois")["prix_m2"]
                   .agg(["mean", "count"])
                   .reset_index())
        monthly.columns = ["Mois", "Moyenne", "Transactions"]
        monthly = monthly[monthly["Transactions"] >= 3]

        if len(monthly) >= 3:
            xs = list(range(len(monthly)))
            ys = monthly["Moyenne"].tolist()
            alpha, beta = least_squares_fit(xs, ys)
            trend = [predict(alpha, beta, x) for x in xs]

            fig_trend = go.Figure()
            fig_trend.add_trace(go.Scatter(
                x=monthly["Mois"], y=monthly["Moyenne"],
                mode="lines+markers", name="Prix moyen mensuel",
                line=dict(color=TEAL, width=2.5),
                marker=dict(size=6, color=TEAL, line=dict(color="#0a0f1a", width=1.5))))
            fig_trend.add_trace(go.Scatter(
                x=monthly["Mois"], y=trend, mode="lines",
                name=f"Tendance (β={beta:+.1f} €/mois)",
                line=dict(color=GOLD, width=2, dash="dash")))
            fig_trend.update_layout(
                **PLOTLY_DARK, height=380,
                legend=dict(orientation="h", y=1.05),
                xaxis_title="Mois", yaxis_title="Prix moyen €/m²",
                xaxis=dict(tickangle=45, gridcolor="rgba(255,255,255,0.04)"),
                yaxis=dict(gridcolor="rgba(255,255,255,0.04)"))
            st.plotly_chart(fig_trend, use_container_width=True)
            st.metric("Tendance mensuelle", f"{beta:+.1f} €/m²/mois")

    if "type_bien" in df_dvf.columns and "prix_m2" in df_dvf.columns:
        st.markdown('<div class="section-title">📦 Distribution par type de bien</div>', unsafe_allow_html=True)
        fig_box = px.box(
            df_dvf.dropna(subset=["type_bien", "prix_m2"]),
            x="type_bien", y="prix_m2",
            color="type_bien", color_discrete_sequence=COLORS,
            template="plotly_dark", height=340)
        fig_box.update_layout(
            paper_bgcolor="#111827", plot_bgcolor="#111827",
            font=dict(color="#c8bfad"),
            margin=dict(l=0, r=0, t=10, b=0),
            showlegend=False,
            xaxis_title="Type de bien", yaxis_title="€/m²",
            xaxis=dict(gridcolor="rgba(255,255,255,0.04)"),
            yaxis=dict(gridcolor="rgba(255,255,255,0.04)"))
        st.plotly_chart(fig_box, use_container_width=True)


# ─── PAGE : SCORING ───────────────────────────────────────────────────────────

elif page == "🔍 Scoring Opportunités":
    st.markdown('<div class="section-title">🔍 Score d\'opportunité par bien</div>', unsafe_allow_html=True)
    st.markdown("<p style='color:#6b7a8d;font-size:0.9rem'>Les biens dont le prix est inférieur à la médiane du marché obtiennent un meilleur score.</p>", unsafe_allow_html=True)
    if df_dvf is None or df_ann is None:
        _no_data_screen("Les données DVF et les annonces sont nécessaires pour le scoring.<br>En attente du pipeline de collecte.")
        st.stop()

    if "prix_m2" in df_ann.columns and len(df_ann) > 0 and "prix_m2" in df_dvf.columns:
        market_pm2 = df_dvf["prix_m2"].dropna().tolist()
        scored = df_ann.copy()
        scored["score"] = scored["prix_m2"].apply(
            lambda p: opportunity_score(p, market_pm2) if not np.isnan(p) else 0)
        scored = scored.sort_values("score", ascending=False)

        def fmt_score(s):
            if s >= 70:
                return f'<span class="score-high">⭐ {s:.0f}/100</span>'
            elif s >= 45:
                return f'<span class="score-medium">🟡 {s:.0f}/100</span>'
            else:
                return f'<span class="score-low">🔴 {s:.0f}/100</span>'

        top = scored.head(10).copy()
        top["Score"]   = top["score"].apply(fmt_score)
        top["Prix"]    = top["prix"].apply(lambda v: f"{v:,.0f} €")
        top["€/m²"]    = top["prix_m2"].apply(lambda v: f"{v:,.0f}")
        top["Surface"] = top["surface"].apply(lambda v: f"{v:.0f} m²")

        cols_show = [c for c in ["quartier", "type_bien", "Surface", "Prix", "€/m²", "Score"]
                     if c in top.columns]
        st.markdown(top[cols_show].to_html(escape=False, index=False), unsafe_allow_html=True)

        st.markdown('<div class="section-title">💹 Prix vs Score</div>', unsafe_allow_html=True)
        fig_sc = px.scatter(
            scored.dropna(subset=["prix", "score"]),
            x="prix", y="score", color="score",
            color_continuous_scale=[[0, "#ef4444"], [0.45, "#eab308"], [1, "#22c55e"]],
            size="surface" if "surface" in scored.columns else None,
            template="plotly_dark", height=380)
        fig_sc.add_hline(y=70, line_dash="dot", line_color="#22c55e",
                         annotation_text="Seuil bonne opportunité",
                         annotation_font_color="#22c55e")
        fig_sc.update_layout(
            paper_bgcolor="#111827", plot_bgcolor="#111827",
            font=dict(color="#c8bfad"),
            margin=dict(l=0, r=0, t=10, b=0),
            xaxis_title="Prix (€)", yaxis_title="Score opportunité",
            xaxis=dict(gridcolor="rgba(255,255,255,0.04)"),
            yaxis=dict(gridcolor="rgba(255,255,255,0.04)"))
        st.plotly_chart(fig_sc, use_container_width=True)


# ─── PAGE : STATS AVANCÉES ────────────────────────────────────────────────────

elif page == "⚙️ Stats avancées":
    st.markdown('<div class="section-title">⚙️ Statistiques avancées (from scratch)</div>', unsafe_allow_html=True)
    if df_dvf is None:
        _no_data_screen("Les données DVF sont nécessaires pour les statistiques avancées.<br>En attente du pipeline de collecte.")
        st.stop()

    if "prix_m2" in df_dvf.columns and "surface" in df_dvf.columns:
        pm2  = df_dvf["prix_m2"].dropna().tolist()
        surf = df_dvf["surface"].dropna().tolist()

        if pm2 and surf:
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Prix au m²")
                for k, v in describe(pm2).items():
                    st.metric(k.capitalize(), f"{v:,.2f}")
            with col2:
                st.subheader("Surface")
                for k, v in describe(surf[:len(pm2)]).items():
                    st.metric(k.capitalize(), f"{v:,.2f}")

            n_min = min(len(pm2), len(surf))
            if n_min >= 5:
                corr = correlation(pm2[:n_min], surf[:n_min])
                st.divider()
                st.metric("Corrélation surface ↔ prix/m²", f"{corr:.4f}")

            st.markdown('<div class="section-title">📐 Régression : surface → prix total</div>', unsafe_allow_html=True)
            prix_list = df_dvf["prix"].dropna().tolist()
            surf_list = df_dvf["surface"].dropna().tolist()
            n_min2 = min(len(prix_list), len(surf_list))
            if n_min2 >= 10:
                alpha, beta = least_squares_fit(surf_list[:n_min2], prix_list[:n_min2])
                r2 = r_squared(alpha, beta, surf_list[:n_min2], prix_list[:n_min2])
                st.info(f"**Modèle** : Prix = {alpha:,.0f} + {beta:,.0f} × Surface  —  R² = {r2:.3f}")

                xs_plot = sorted(surf_list[:n_min2])
                ys_pred = [predict(alpha, beta, x) for x in xs_plot]
                fig_reg = go.Figure()
                fig_reg.add_trace(go.Scatter(
                    x=surf_list[:n_min2], y=prix_list[:n_min2],
                    mode="markers",
                    marker=dict(color=TEAL, opacity=0.45, size=5), name="Transactions"))
                fig_reg.add_trace(go.Scatter(
                    x=xs_plot, y=ys_pred, mode="lines",
                    line=dict(color=GOLD, width=2.5),
                    name=f"Régression (β={beta:,.0f}€/m²)"))
                fig_reg.update_layout(
                    **PLOTLY_DARK, height=370,
                    xaxis_title="Surface (m²)", yaxis_title="Prix (€)",
                    xaxis=dict(gridcolor="rgba(255,255,255,0.04)"),
                    yaxis=dict(gridcolor="rgba(255,255,255,0.04)"))
                st.plotly_chart(fig_reg, use_container_width=True)

                st.markdown("**🧮 Simulateur de prix**")
                sim_surf = st.slider("Surface (m²)", 20, 200, 65)
                sim_prix = predict(alpha, beta, sim_surf)
                st.success(
                    f"Surface de **{sim_surf} m²** → "
                    f"Prix estimé : **{sim_prix:,.0f} €** "
                    f"({sim_prix/sim_surf:,.0f} €/m²)")

# ─── Footer ──────────────────────────────────────────────────────────────────

st.markdown(f"""
<div class="footer">
  NIDDOUILLET · OBSERVATOIRE TOULONNAIS · DONNÉES DVF DATA.GOUV.FR ·
  {datetime.now().strftime("%d/%m/%Y")}
</div>
""", unsafe_allow_html=True)
