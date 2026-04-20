"""
India Digital Payments — The Astral Terminal
A High-Velocity Performance Dashboard for UPI Financial Intelligence
Design System: The Astral Terminal (Cockpit-Class UI)
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="UPI Astral Terminal",
    layout="wide",
    page_icon="📡",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# THE ASTRAL TERMINAL DESIGN SYSTEM (CSS)
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

/* Base Styles */
html, body, [class*="css"] { 
    font-family: 'Inter', sans-serif; 
    color: #d6e3ff;
}

.stApp {
    background: #041329;
    background-image: radial-gradient(circle at 50% 0%, rgba(0, 229, 255, 0.05) 0%, transparent 50%),
                      radial-gradient(circle at 100% 100%, rgba(124, 77, 255, 0.05) 0%, transparent 50%);
    background-attachment: fixed;
}

/* ── Extreme Glassmorphism Container ── */
.glass-card {
    background: rgba(17, 32, 54, 0.45);
    backdrop-filter: blur(24px) saturate(150%);
    -webkit-backdrop-filter: blur(24px) saturate(150%);
    border-radius: 16px;
    border: 1px solid rgba(195, 245, 255, 0.12);
    padding: 24px;
    margin-bottom: 20px;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
}

/* ── HUD Header ── */
.hud-header {
    background: linear-gradient(135deg, rgba(4, 19, 41, 0.95) 0%, rgba(17, 32, 54, 0.8) 100%);
    padding: 40px 48px;
    border-radius: 0 0 40px 0;
    border-bottom: 2px solid #00e5ff;
    border-right: 2px solid #00e5ff;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
}
.hud-header::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background: repeating-linear-gradient(0deg, rgba(0,229,255,0.03) 0, rgba(0,229,255,0.03) 1px, transparent 1px, transparent 2px);
    pointer-events: none;
}
.hud-header h1 { 
    margin: 0; font-size: 34px; font-weight: 800; 
    letter-spacing: -1px; color: #fff;
    text-shadow: 0 0 15px rgba(0, 229, 255, 0.5);
}
.hud-header .status-line { 
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px; color: #00e5ff; 
    letter-spacing: 2px; text-transform: uppercase;
    margin-top: 8px; opacity: 0.8;
}

/* ── HUD KPI Displays ── */
.kpi-container {
    display: flex;
    flex-direction: column;
    position: relative;
    padding-left: 20px;
}
.kpi-power-bar {
    width: 3px; height: 40px; background: #7c4dff;
    position: absolute; left: 0; top: 5px;
    box-shadow: 0 0 10px #7c4dff;
}
.kpi-value { 
    font-size: 36px; font-weight: 800; color: #fff; 
    line-height: 1; letter-spacing: -1px;
    text-shadow: 0 0 12px rgba(195, 245, 255, 0.4);
}
.kpi-label { 
    font-size: 11px; color: #bac9cc; 
    text-transform: uppercase; font-weight: 600;
    letter-spacing: 1px; margin-top: 6px;
}
.kpi-delta-up { font-family: 'JetBrains Mono', monospace; font-size: 12px; color: #00ffaa; margin-top: 8px; }

/* ── Tab & UI Styling ── */
.stTabs [data-baseweb="tab-list"] { gap: 12px; background: transparent; }
.stTabs [data-baseweb="tab"] {
    background: rgba(17, 32, 54, 0.6);
    border-radius: 8px 8px 0 0; color: #bac9cc; padding: 10px 24px;
}
.stTabs [aria-selected="true"] {
    background: rgba(0, 229, 255, 0.1) !important;
    border-bottom: 2px solid #00e5ff !important;
    color: #fff !important;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}
.stMarkdown, .stPlotlyChart, .glass-card {
    animation: fadeIn 0.6s ease-out forwards;
}

[data-testid="stSidebar"] { background-color: #010e24; border-right: 1px solid rgba(0,229,255,0.1); }
</style>
""", unsafe_allow_html=True)

# ── Tech Theme Helper ──
def apply_hud_theme(fig):
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#bac9cc', family='Inter'),
        margin=dict(t=50, b=40, l=40, r=40),
        xaxis=dict(gridcolor='rgba(255,255,255,0.05)', zeroline=False, showline=False),
        yaxis=dict(gridcolor='rgba(255,255,255,0.05)', zeroline=False, showline=False),
        legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(size=10)),
        hoverlabel=dict(bgcolor='#112036', font_size=12, font_family='JetBrains Mono')
    )
    return fig

# ─────────────────────────────────────────────
# DATA ENGINE
# ─────────────────────────────────────────────
import os

@st.cache_data
def load_data():
    base_path = os.path.dirname(__file__)
    
    def get_path(filename):
        return os.path.join(base_path, "data", filename)

    try:
        growth  = pd.read_csv(get_path("upi_growth.csv"))
        apps    = pd.read_csv(get_path("app_share.csv"))
        states  = pd.read_csv(get_path("state_wise.csv"))
        age     = pd.read_csv(get_path("age_group.csv"))
        timemap = pd.read_csv(get_path("time_heatmap.csv"))
    except FileNotFoundError as e:
        st.error(f"📡 CRITICAL_ERROR: Data Subsystem Offline. {e}")
        st.info(f"Directory Content Check: {os.listdir(os.path.join(base_path, 'data'))}")
        st.stop()

    month_order = {"Apr":1,"May":2,"Jun":3,"Jul":4,"Aug":5,"Sep":6,"Oct":7,"Nov":8,"Dec":9,"Jan":10,"Feb":11,"Mar":12}
    growth["month_num"] = growth["month"].map(month_order)
    growth = growth.sort_values(["year","month_num"]).reset_index(drop=True)
    yearly = growth.groupby("year").agg(total_volume=("volume_millions","sum"), total_value=("value_crore","sum")).reset_index()
    yearly["vol_yoy_pct"] = yearly["total_volume"].pct_change()*100
    yearly["val_yoy_pct"] = yearly["total_value"].pct_change()*100
    return growth, apps, states, age, timemap, yearly

growth_df, apps_df, states_df, age_df, time_df, yearly_df = load_data()
latest_year = yearly_df.iloc[-1]["year"]
ly = yearly_df[yearly_df["year"] == latest_year].iloc[0]

# ─────────────────────────────────────────────
# SIDEBAR & HEADER
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("<h2 style='color:#00e5ff; font-weight:800; letter-spacing:-1px;'>ASTRAL TERMINAL</h2>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:10px; color:#bac9cc; opacity:0.6;'>SYSTEM V3.4 // UPI FINANCIAL CORE</p>", unsafe_allow_html=True)
    st.markdown("---")
    selected_years = st.multiselect("SECTOR_YEAR_FILTER", options=yearly_df["year"].unique(), default=yearly_df["year"].unique()[-3:])
    st.markdown("---")
    sel_apps = st.multiselect("SUBSYSTEM_FILTER", sorted(apps_df["app"].unique()), default=sorted(apps_df["app"].unique())[:6])

st.markdown(f"""
<div class="hud-header">
    <div class="status-line">System Status: Active // Network Flux: Stable</div>
    <h1>💳 UPI_FINANCIAL_MISSION_CONTROL</h1>
    <div style="font-size:13px; color:#bac9cc; margin-top:4px; opacity:0.7;">
        Sovereign Cockpit for Unified Payments Intelligence · {latest_year} Report Cycle
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TAB INTERFACE
# ─────────────────────────────────────────────
tabs = st.tabs(["🏛️ EXEC_SUMMARY", "📈 GROWTH_VECTORS", "📱 APP_INTEL", "🗺️ REGIONAL_HUB", "👥 SEGMENTATION", "⏰ PULSE_HEATMAP", "🔮 PREDICTOR"])

# ── EXEC_SUMMARY ──
with tabs[0]:
    st.markdown("""<div class="glass-card"><p style="font-family:'JetBrains Mono'; color:#00e5ff; font-size:11px; margin-bottom:12px;">// SECTOR_BRIEF_V2.0</p>
    <p style="font-size:15px; line-height:1.7; color:#d6e3ff;">Global-scale digital liquidity detected. Aggregate flux has passed the <b>{(ly['total_volume']/1000):.1f}B</b> threshold. System integrity confirmed.</p></div>""", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    metrics = [(c1, f"{ly['total_volume']/1000:.1f}B", "Aggregate Volume", f"▲ {ly['vol_yoy_pct']:.1f}%"), (c2, f"₹{ly['total_value']/100000:.1f}L Cr", "Asset Flux Value", f"▲ {ly['val_yoy_pct']:.1f}%"), (c3, f"₹{(ly['total_value']*10/ly['total_volume']):.0f}", "Avg Ticket Size", "STABLE"), (c4, f"{(growth_df.iloc[-1]['volume_millions']/1000):.1f}B", "Peak Monthly Flux", "PEAK_REACHED")]
    for col, val, label, delta in metrics:
        with col:
            st.markdown(f'<div class="glass-card kpi-container"><div class="kpi-power-bar"></div><div class="kpi-value">{val}</div><div class="kpi-label">{label}</div><div class="kpi-delta-up">{delta}</div></div>', unsafe_allow_html=True)
    colA, colB = st.columns(2)
    with colA:
        st.markdown('<p style="font-family:Inter; font-weight:700; color:#fff; border-left:3px solid #00e5ff; padding-left:12px; font-size:12px;">VOLUME_EXPANSION_CURVE</p>', unsafe_allow_html=True)
        st.plotly_chart(apply_hud_theme(px.bar(yearly_df[yearly_df['year'].isin(selected_years)], x="year", y="total_volume", color_discrete_sequence=["#00e5ff"])), width='stretch')
    with colB:
        st.markdown('<p style="font-family:Inter; font-weight:700; color:#fff; border-left:3 solid #7c4dff; padding-left:12px; font-size:12px;">VALUE_FLUX_TRAJECTORY</p>', unsafe_allow_html=True)
        st.plotly_chart(apply_hud_theme(px.line(yearly_df[yearly_df['year'].isin(selected_years)], x="year", y="total_value", markers=True, color_discrete_sequence=["#7c4dff"])), width='stretch')

# ── GROWTH_VECTORS ──
with tabs[1]:
    st.markdown('<p style="font-family:JetBrains Mono; color:#00e5ff; font-size:11px;">// HISTORICAL_FLUX_OVERLAY</p>', unsafe_allow_html=True)
    fig_full = go.Figure()
    fig_full.add_trace(go.Bar(x=growth_df['year']+"-"+growth_df['month'], y=growth_df['volume_millions'], name='Flux Volume', marker_color='#00e5ff', opacity=0.7))
    fig_full.add_trace(go.Scatter(x=growth_df['year']+"-"+growth_df['month'], y=growth_df['volume_millions'], mode='lines', name='Trendline', line=dict(color='#7c4dff', width=3)))
    st.plotly_chart(apply_hud_theme(fig_full), width='stretch')

# ── APP_INTEL ──
with tabs[2]:
    app_colors = {"PhonePe":"#00e5ff","Google Pay":"#7c4dff","Paytm":"#f97316","BHIM":"#16a34a","Amazon Pay":"#ff9900","CRED":"#fff","Navi":"#00ffaa","WhatsApp Pay":"#25D366","Others":"#64748b"}
    c1, c2 = st.columns([1, 1])
    with c1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        snap = apps_df[apps_df['year'] == apps_df['year'].max()].groupby('app')['volume_millions'].sum().reset_index()
        st.plotly_chart(apply_hud_theme(px.pie(snap, names='app', values='volume_millions', color='app', color_discrete_map=app_colors, hole=0.6, title="MARKET_SHARE_SNAPSHOT")), width='stretch')
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        app_t = apps_df[apps_df['app'].isin(sel_apps)].groupby(['year', 'app'])['volume_millions'].sum().reset_index()
        st.plotly_chart(apply_hud_theme(px.line(app_t, x='year', y='volume_millions', color='app', color_discrete_map=app_colors, markers=True, title="SUBSYSTEM_TRAJECTORY")), width='stretch')
        st.markdown('</div>', unsafe_allow_html=True)

# ── REGIONAL_HUB ──
with tabs[3]:
    curr = states_df[states_df['year'] == states_df['year'].max()].sort_values('volume_millions', ascending=False)
    st.plotly_chart(apply_hud_theme(px.bar(curr.head(15), x='volume_millions', y='state', orientation='h', color='volume_millions', color_continuous_scale='GnBu', title="TOP_SECTOR_DENSITY")), width='stretch')
    st.markdown('<p style="font-family:JetBrains Mono; color:#7c4dff; font-size:11px;">// QUADRANT_DEPLOYMENT_MATRIX</p>', unsafe_allow_html=True)
    fig_q = px.scatter(curr, x='volume_contribution_pct', y='value_contribution_pct', text='state', size='volume_millions', color='volume_contribution_pct', color_continuous_scale='Turbo')
    fig_q.add_hline(y=curr['value_contribution_pct'].mean(), line_dash="dash", line_color="#7c4dff")
    fig_q.add_vline(x=curr['volume_contribution_pct'].mean(), line_dash="dash", line_color="#00e5ff")
    st.plotly_chart(apply_hud_theme(fig_q), width='stretch')

# ── SEGMENTATION ──
with tabs[4]:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.plotly_chart(apply_hud_theme(px.bar(age_df, x='age_group', y='user_pct', color_discrete_sequence=['#00e5ff'], title="COHORT_DENSITY")), width='stretch')
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.plotly_chart(apply_hud_theme(px.bar(age_df, x='age_group', y='avg_ticket_size', color_discrete_sequence=['#7c4dff'], title="VALUATION_BY_AGE")), width='stretch')
        st.markdown('</div>', unsafe_allow_html=True)

# ── PULSE_HEATMAP ──
with tabs[5]:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    hp = time_df.pivot(index="hour", columns="day", values="transactions_millions")[["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]]
    st.plotly_chart(apply_hud_theme(px.imshow(hp, color_continuous_scale='GnBu', title="NETWORK_FLUX_PULSE")), width='stretch')
    st.markdown('</div>', unsafe_allow_html=True)

# ── PREDICTOR ──
with tabs[6]:
    st.markdown('<p style="font-family:JetBrains Mono; color:#00e5ff; font-size:11px;">// ALGORITHMIC_PROJECTION_V1.0</p>', unsafe_allow_html=True)
    X = np.array(list(range(len(yearly_df['year'].unique())))).reshape(-1, 1)
    y = yearly_df['total_volume'].values
    model = LinearRegression().fit(X, y)
    f_y = model.predict(np.array([len(X), len(X)+1, len(X)+2]).reshape(-1, 1))
    fig_f = go.Figure()
    fig_f.add_trace(go.Scatter(x=yearly_df['year'], y=yearly_df['total_volume'], name='Historical', line=dict(color='#00e5ff', width=4)))
    fig_f.add_trace(go.Scatter(x=["2026-27", "2027-28", "2028-29"], y=f_y, name='Algorithm Forecast', line=dict(color='#7c4dff', dash='dash', width=4)))
    st.plotly_chart(apply_hud_theme(fig_f), width='stretch')
    st.markdown(f'<div class="glass-card" style="border-left: 4px solid #7c4dff;"><p style="font-family:JetBrains Mono; color:#7c4dff; font-size:11px;">// PREDICTIVE_REPORT</p><p style="font-size:14px;">Liquidity surge of <b>{(f_y[0]/y[-1]*100-100):.1f}%</b> projected for next sector cycle.</p></div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown('<div style="text-align:center; color:#bac9cc; font-size:10px; opacity:0.4; font-family:JetBrains Mono;">ASTRAL_TERMINAL_SESSION // END_OF_LINE // DATA_STREAM_STABLE</div>', unsafe_allow_html=True)
