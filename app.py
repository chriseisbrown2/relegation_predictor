"""
EPL 2025/26 Relegation Battle Dashboard
Run with: streamlit run app.py
"""

import random
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from collections import defaultdict

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="EPL Relegation Predictor 2025/26",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Source+Sans+3:wght@300;400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Source Sans 3', sans-serif;
    background-color: #0a0a0f;
    color: #e8e0d0;
}

.stApp {
    background: #0a0a0f;
}

/* Hide default streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 0 !important; max-width: 1200px; }

/* ── Hero header ── */
.hero {
    background: linear-gradient(135deg, #1a0a2e 0%, #0d1117 50%, #0a1a0a 100%);
    border-bottom: 2px solid #2a2a3a;
    padding: 32px 40px 24px;
    margin: -1rem -1rem 2rem -1rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    inset: 0;
    background: repeating-linear-gradient(45deg, transparent, transparent 40px,
        rgba(255,255,255,0.012) 40px, rgba(255,255,255,0.012) 41px);
    pointer-events: none;
}
.hero-eyebrow {
    font-size: 10px;
    letter-spacing: 4px;
    color: #555;
    text-transform: uppercase;
    margin-bottom: 6px;
    font-family: 'Source Sans 3', sans-serif;
}
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 36px;
    font-weight: 900;
    color: #f0e8d8;
    margin: 0 0 8px 0;
    letter-spacing: -0.5px;
}
.hero-sub {
    font-size: 13px;
    color: #666;
    font-style: italic;
}

/* ── Section labels ── */
.section-label {
    font-size: 10px;
    letter-spacing: 3px;
    color: #555;
    text-transform: uppercase;
    margin-bottom: 12px;
    font-family: 'Source Sans 3', sans-serif;
}

/* ── Standings table ── */
.standings-table {
    width: 100%;
    border-collapse: collapse;
    border-radius: 10px;
    overflow: hidden;
    border: 1px solid #1e1e2e;
    font-family: 'Source Sans 3', sans-serif;
}
.standings-table thead tr {
    background: #111118;
    font-size: 10px;
    letter-spacing: 2px;
    color: #555;
    text-transform: uppercase;
}
.standings-table thead th {
    padding: 10px 14px;
    text-align: left;
    font-weight: 400;
}
.standings-table thead th.right { text-align: right; }
.standings-table thead th.center { text-align: center; }

.standings-table tbody tr {
    border-bottom: 1px solid #1a1a24;
    cursor: pointer;
    transition: background 0.15s;
}
.standings-table tbody tr:nth-child(odd)  { background: #0d0d14; }
.standings-table tbody tr:nth-child(even) { background: #0f0f18; }
.standings-table tbody tr:hover { background: #1a1a2a; }

.standings-table td {
    padding: 11px 14px;
    font-size: 13px;
    color: #ccc;
}
.standings-table td.pts  { font-weight: 700; font-size: 15px; color: #f0e8d8; text-align: center; }
.standings-table td.gd   { text-align: center; font-size: 12px; }
.standings-table td.num  { text-align: center; }
.standings-table td.right{ text-align: right; }

.dot {
    display: inline-block;
    width: 10px; height: 10px;
    border-radius: 50%;
    margin-right: 8px;
    vertical-align: middle;
    flex-shrink: 0;
}

/* ── Risk badge ── */
.risk-badge {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.5px;
}

/* ── Metric cards ── */
.metric-card {
    background: #111118;
    border: 1px solid #1e1e2e;
    border-radius: 10px;
    padding: 16px 20px;
    text-align: center;
}
.metric-label {
    font-size: 10px;
    letter-spacing: 2px;
    color: #555;
    text-transform: uppercase;
    margin-bottom: 6px;
}
.metric-value {
    font-family: 'Playfair Display', serif;
    font-size: 28px;
    font-weight: 700;
    line-height: 1;
}

/* ── Detail panel ── */
.detail-header {
    padding: 18px 20px;
    border-bottom: 1px solid #1e1e2e;
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    border-radius: 12px 12px 0 0;
}
.detail-body { padding: 16px 0; }
.fixture-row {
    display: grid;
    grid-template-columns: 28px 80px 60px 1fr 70px;
    gap: 10px;
    align-items: center;
    padding: 8px 12px;
    border-radius: 6px;
    font-size: 13px;
    font-family: 'Source Sans 3', sans-serif;
}
.fixture-row:nth-child(odd) { background: #111118; }

/* ── Methodology box ── */
.method-box {
    background: #0a0a10;
    border: 1px solid #1a1a24;
    border-radius: 8px;
    padding: 16px 20px;
    font-size: 11px;
    color: #444;
    line-height: 1.8;
    margin-top: 24px;
}
.method-box strong { color: #666; letter-spacing: 1px; }

/* ── Legend row ── */
.legend-row {
    display: flex;
    gap: 24px;
    margin-bottom: 16px;
}
.legend-item {
    font-size: 11px;
    color: #555;
    display: flex;
    align-items: center;
    gap: 6px;
}
.legend-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    display: inline-block;
}
</style>
""", unsafe_allow_html=True)

# ── Data ──────────────────────────────────────────────────────────────────────

HISTORICAL = {
    "TOT": {"w": 0.42, "d": 0.22, "l": 0.36},
    "LEE": {"w": 0.31, "d": 0.22, "l": 0.47},
    "NFO": {"w": 0.30, "d": 0.25, "l": 0.45},
    "WHU": {"w": 0.39, "d": 0.22, "l": 0.39},
    "BUR": {"w": 0.22, "d": 0.22, "l": 0.56},
    "WOL": {"w": 0.30, "d": 0.24, "l": 0.46},
}

RECENT_FORM = {
    "TOT": {"w": 0, "d": 3, "l": 7},
    "LEE": {"w": 3, "d": 3, "l": 4},
    "NFO": {"w": 3, "d": 2, "l": 5},
    "WHU": {"w": 4, "d": 1, "l": 5},
    "BUR": {"w": 2, "d": 2, "l": 6},
    "WOL": {"w": 3, "d": 3, "l": 4},
}

OPP_STRENGTH = {
    "ARS": 0.20, "MCI": 0.18, "LFC": 0.16, "MUN": 0.10,
    "AVL": 0.08, "CFC": 0.07, "NEW": 0.05, "BRE": 0.04,
    "BRI": 0.03, "EVE": 0.02, "BOU": 0.01, "FUL": 0.01,
    "SUN": -0.01, "CRY": 0.00, "LEE": -0.04, "TOT": -0.05,
    "NFO": -0.06, "WHU": -0.06, "BUR": -0.10, "WOL": -0.11,
}

HOME_BOOST = 0.07

TEAMS = [
    {"id": "LEE", "name": "Leeds United",       "pts": 31, "gd": -12,
     "remaining": [("CRY",False),("BRE",True),("MUN",False),("WOL",True),("BOU",False),("BUR",True),("TOT",False),("BRI",True),("WHU",False)]},
    {"id": "TOT", "name": "Tottenham Hotspur",  "pts": 29, "gd": -14,
     "remaining": [("LFC",False),("NFO",True),("SUN",False),("BRI",True),("WOL",False),("AVL",False),("LEE",True),("CFC",False),("EVE",True)]},
    {"id": "NFO", "name": "Nottingham Forest",  "pts": 28, "gd": -16,
     "remaining": [("FUL",True),("TOT",False),("AVL",True),("BUR",True),("SUN",False),("CFC",False),("NEW",True),("MUN",False),("BOU",True)]},
    {"id": "WHU", "name": "West Ham United",    "pts": 28, "gd": -18,
     "remaining": [("MCI",True),("AVL",False),("WOL",True),("CRY",False),("EVE",True),("BRE",False),("ARS",True),("NEW",False),("LEE",True)]},
    {"id": "BUR", "name": "Burnley FC",         "pts": 19, "gd": -28,
     "remaining": [("BOU",True),("FUL",False),("BRI",True),("NFO",False),("MCI",True),("LEE",False),("AVL",True),("ARS",False),("WOL",True)]},
    {"id": "WOL", "name": "Wolverhampton W.",   "pts": 16, "gd": -24,
     "remaining": [("BRE",False),("WHU",False),("LEE",False),("TOT",True),("SUN",False),("BRI",False),("BUR",False),("FUL",True),("BUR",False)]},
]

COLORS = {
    "TOT": {"primary": "#132257", "accent": "#FFFFFF"},
    "LEE": {"primary": "#FFCD00", "accent": "#1A1A1A"},
    "NFO": {"primary": "#DD0000", "accent": "#FFFFFF"},
    "WHU": {"primary": "#7A263A", "accent": "#F0B323"},
    "BUR": {"primary": "#6C1D45", "accent": "#99D6EA"},
    "WOL": {"primary": "#FDB913", "accent": "#231F20"},
}

# ── Model ─────────────────────────────────────────────────────────────────────

def calc_win_prob(team_id, is_home, opp_id):
    hist   = HISTORICAL[team_id]
    recent = RECENT_FORM[team_id]
    rw = recent["w"] / 10.0
    rd = recent["d"] / 10.0
    blended_w = 0.6 * hist["w"] + 0.4 * rw
    blended_d = 0.6 * hist["d"] + 0.4 * rd
    opp_mod  = OPP_STRENGTH.get(opp_id, 0.0)
    home_mod = HOME_BOOST if is_home else -HOME_BOOST * 0.5
    w = max(0.05, min(0.75, blended_w - opp_mod + home_mod))
    d = max(0.05, min(0.35, blended_d * 0.85))
    l = max(0.05, 1.0 - w - d)
    total = w + d + l
    return w/total, d/total, l/total


@st.cache_data(show_spinner=False)
def run_monte_carlo(iterations=100_000, _seed=42):
    random.seed(_seed)
    relegation_counts = defaultdict(int)
    points_tally      = defaultdict(list)

    for _ in range(iterations):
        final_pts = {t["id"]: t["pts"] for t in TEAMS}
        for team in TEAMS:
            for opp, is_home in team["remaining"]:
                w, d, _ = calc_win_prob(team["id"], is_home, opp)
                r = random.random()
                if   r < w:     final_pts[team["id"]] += 3
                elif r < w + d: final_pts[team["id"]] += 1

        ranked = sorted(final_pts.items(), key=lambda x: x[1])
        for tid, _ in ranked[:3]:
            relegation_counts[tid] += 1
        for tid, pts in final_pts.items():
            points_tally[tid].append(pts)

    stats = {}
    for team in TEAMS:
        tid = team["id"]
        pl  = sorted(points_tally[tid])
        n   = len(pl)
        stats[tid] = {
            "rel_pct":    round(relegation_counts[tid] / iterations * 100, 1),
            "median_pts": pl[n // 2],
            "p10_pts":    pl[int(n * 0.10)],
            "p90_pts":    pl[int(n * 0.90)],
            "min_pts":    pl[0],
            "max_pts":    pl[-1],
            "dist":       pl,
        }
    return stats


def danger_color(pct):
    if pct >= 75: return "#ef4444"
    if pct >= 50: return "#f97316"
    if pct >= 25: return "#eab308"
    return "#22c55e"


def risk_label(pct):
    if pct >= 75: return ("🔴 ALMOST CERTAIN", "#ef4444")
    if pct >= 50: return ("🟠 HIGH RISK",       "#f97316")
    if pct >= 25: return ("🟡 MODERATE",         "#eab308")
    if pct >= 10: return ("🟢 LOW",              "#22c55e")
    return          ("✅ VERY LOW",               "#22c55e")

# ── Run simulation ────────────────────────────────────────────────────────────

with st.spinner("Running 100,000 Monte Carlo simulations…"):
    stats = run_monte_carlo(100_000)

sorted_teams = sorted(TEAMS, key=lambda t: -t["pts"])

# ── Hero ──────────────────────────────────────────────────────────────────────

st.markdown("""
<div class="hero">
  <div class="hero-eyebrow">Premier League 2025/26 · Statistical Analysis</div>
  <div class="hero-title">Relegation Battle Predictor</div>
  <div class="hero-sub">Monte Carlo simulation · 100,000 iterations · Based on 5-season historical EPL data · All points integer-valued</div>
</div>
""", unsafe_allow_html=True)

# ── Standings table ───────────────────────────────────────────────────────────

st.markdown('<div class="section-label">Current Standings & Projected Final Points</div>', unsafe_allow_html=True)

rows_html = ""
for i, team in enumerate(sorted_teams):
    tid   = team["id"]
    s     = stats[tid]
    c     = COLORS[tid]
    label, lcolor = risk_label(s["rel_pct"])
    gd_color = "#f87171" if team["gd"] < 0 else "#86efac"
    marker = "▼" if i >= 3 else "&nbsp;"
    rows_html += f"""
    <tr>
      <td style="color:#ef4444;font-weight:700">{marker}</td>
      <td style="font-size:12px;color:#555">{i+1}</td>
      <td>
        <span class="dot" style="background:{c['primary']};border:2px solid {c['accent']}"></span>
        <strong style="color:#f0e8d8">{team['name']}</strong>
      </td>
      <td class="pts">{team['pts']}</td>
      <td class="gd" style="color:{gd_color}">{team['gd']}</td>
      <td class="num" style="color:#a5b4fc;font-weight:600">{s['median_pts']}</td>
      <td class="num" style="color:#666;font-size:11px">{s['p10_pts']}–{s['p90_pts']}</td>
      <td class="right">
        <span class="risk-badge" style="background:{lcolor}22;color:{lcolor}">{label}</span>
      </td>
      <td class="right" style="font-weight:700;color:{danger_color(s['rel_pct'])};font-size:15px">{s['rel_pct']}%</td>
    </tr>"""

st.markdown(f"""
<table class="standings-table">
  <thead>
    <tr>
      <th></th><th>#</th><th>Club</th>
      <th class="center">Pts</th><th class="center">GD</th>
      <th class="center">Median</th><th class="center">P10–P90</th>
      <th class="right">Risk</th><th class="right">Rel %</th>
    </tr>
  </thead>
  <tbody>{rows_html}</tbody>
</table>
<div style="font-size:11px;color:#444;margin-top:8px;font-style:italic">
  Median = most likely final points · P10 = pessimistic · P90 = optimistic
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Bar chart ─────────────────────────────────────────────────────────────────

st.markdown('<div class="section-label">Relegation Probability</div>', unsafe_allow_html=True)

bar_teams = sorted_teams[:]
fig_bar = go.Figure()

for team in bar_teams:
    tid = team["id"]
    pct = stats[tid]["rel_pct"]
    fig_bar.add_trace(go.Bar(
        x=[pct],
        y=[team["name"]],
        orientation="h",
        marker=dict(
            color=danger_color(pct),
            opacity=0.85,
            line=dict(width=0),
        ),
        text=f"  {pct}%",
        textposition="outside",
        textfont=dict(color=danger_color(pct), size=13, family="Source Sans 3"),
        hovertemplate=f"<b>{team['name']}</b><br>Relegation: {pct}%<extra></extra>",
        showlegend=False,
    ))

fig_bar.update_layout(
    paper_bgcolor="#0a0a0f",
    plot_bgcolor="#0d0d14",
    height=280,
    margin=dict(l=0, r=80, t=10, b=10),
    xaxis=dict(
        range=[0, 115],
        showgrid=True, gridcolor="#1e1e2e", gridwidth=1,
        zeroline=False,
        tickfont=dict(color="#555", size=10),
        title=dict(text="Relegation Probability (%)", font=dict(color="#555", size=10)),
    ),
    yaxis=dict(
        autorange="reversed",
        tickfont=dict(color="#ccc", size=13, family="Source Sans 3"),
        showgrid=False,
    ),
    bargap=0.35,
)
st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})

# ── Two-column layout: selector + detail ─────────────────────────────────────

st.markdown('<div class="section-label">Fixture-by-Fixture Breakdown</div>', unsafe_allow_html=True)

col_sel, col_detail = st.columns([1, 2.6], gap="large")

with col_sel:
    team_options = {t["name"]: t["id"] for t in sorted_teams}
    selected_name = st.radio(
        "Select a club",
        options=list(team_options.keys()),
        index=1,   # default: Tottenham
        label_visibility="collapsed",
    )
    selected_id = team_options[selected_name]
    selected_team = next(t for t in TEAMS if t["id"] == selected_id)
    s = stats[selected_id]
    c = COLORS[selected_id]

    # Metric cards
    st.markdown("<br>", unsafe_allow_html=True)
    rel_color = danger_color(s["rel_pct"])
    st.markdown(f"""
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:10px">
      <div class="metric-card">
        <div class="metric-label">Current Pts</div>
        <div class="metric-value" style="color:#f0e8d8">{selected_team['pts']}</div>
      </div>
      <div class="metric-card">
        <div class="metric-label">Median Finish</div>
        <div class="metric-value" style="color:#a5b4fc">{s['median_pts']}</div>
      </div>
      <div class="metric-card">
        <div class="metric-label">Pessimistic (P10)</div>
        <div class="metric-value" style="color:#f87171">{s['p10_pts']}</div>
      </div>
      <div class="metric-card">
        <div class="metric-label">Optimistic (P90)</div>
        <div class="metric-value" style="color:#86efac">{s['p90_pts']}</div>
      </div>
    </div>
    <div class="metric-card" style="margin-bottom:10px">
      <div class="metric-label">Relegation Risk</div>
      <div class="metric-value" style="color:{rel_color};font-size:36px">{s['rel_pct']}%</div>
      <div style="font-size:12px;color:{rel_color};margin-top:4px">{risk_label(s['rel_pct'])[0]}</div>
    </div>
    """, unsafe_allow_html=True)

with col_detail:
    # Fixture breakdown table
    fix_rows = ""
    for i, (opp, is_home) in enumerate(selected_team["remaining"]):
        w, d, l = calc_win_prob(selected_id, is_home, opp)
        w_pct, d_pct, l_pct = int(w*100), int(d*100), int(l*100)
        exp_pts = w*3 + d*1
        venue   = "🏠 HOME" if is_home else "✈️  AWAY"
        # mini bar segments
        bar_html = f"""
        <div style="display:flex;height:6px;border-radius:3px;overflow:hidden;background:#1a1a2a;width:100%">
          <div style="width:{w_pct}%;background:#22c55e"></div>
          <div style="width:{d_pct}%;background:#eab308"></div>
          <div style="width:{l_pct}%;background:#ef4444"></div>
        </div>
        <div style="display:flex;gap:8px;margin-top:3px;font-size:10px">
          <span style="color:#22c55e">{w_pct}%W</span>
          <span style="color:#eab308">{d_pct}%D</span>
          <span style="color:#ef4444">{l_pct}%L</span>
        </div>"""

        exp_color = "#86efac" if exp_pts >= 2 else "#fde68a" if exp_pts >= 1 else "#fca5a5"
        bg = "#111118" if i % 2 == 0 else "transparent"
        fix_rows += f"""
        <tr style="background:{bg}">
          <td style="color:#555;font-size:11px;padding:8px 10px">{i+1}</td>
          <td style="font-size:11px;color:#777;padding:8px 6px;white-space:nowrap">{venue}</td>
          <td style="font-size:13px;color:#ccc;padding:8px 10px">vs <strong style="color:#e8e0d0">{opp}</strong></td>
          <td style="padding:8px 10px;min-width:160px">{bar_html}</td>
          <td style="font-weight:700;color:{exp_color};font-size:12px;padding:8px 10px;text-align:right;white-space:nowrap">{exp_pts:.2f} pts</td>
        </tr>"""

    st.markdown(f"""
    <div style="background:#0d0d14;border:1px solid #1e1e2e;border-radius:12px;overflow:hidden">
      <div style="padding:16px 20px;background:linear-gradient(135deg,{c['primary']}33 0%,#111118 100%);border-bottom:1px solid #1e1e2e">
        <div style="font-size:11px;letter-spacing:3px;color:#555;text-transform:uppercase;margin-bottom:4px">Remaining Fixtures</div>
        <div style="font-size:18px;font-family:'Playfair Display',serif;color:#f0e8d8;font-weight:700">{selected_name}</div>
        <div style="font-size:12px;color:#888;margin-top:2px">{len(selected_team['remaining'])} games left · Range: {s['min_pts']}–{s['max_pts']} pts possible</div>
      </div>
      <table style="width:100%;border-collapse:collapse">
        <thead>
          <tr style="background:#111118;font-size:10px;letter-spacing:2px;color:#555;text-transform:uppercase">
            <th style="padding:8px 10px;text-align:left;font-weight:400">#</th>
            <th style="padding:8px 6px;text-align:left;font-weight:400">Venue</th>
            <th style="padding:8px 10px;text-align:left;font-weight:400">Opponent</th>
            <th style="padding:8px 10px;text-align:left;font-weight:400">Win / Draw / Loss</th>
            <th style="padding:8px 10px;text-align:right;font-weight:400">Exp Pts</th>
          </tr>
        </thead>
        <tbody>{fix_rows}</tbody>
      </table>
    </div>
    """, unsafe_allow_html=True)

# ── Points distribution histogram ─────────────────────────────────────────────

st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="section-label">Simulated Points Distribution (all 6 clubs)</div>', unsafe_allow_html=True)

fig_hist = go.Figure()
for team in sorted_teams:
    tid  = team["id"]
    dist = stats[tid]["dist"]
    c    = COLORS[tid]
    fig_hist.add_trace(go.Histogram(
        x=dist,
        name=team["name"],
        opacity=0.65,
        nbinsx=28,
        marker_color=c["primary"] if c["primary"] != "#FFCD00" else "#d4aa00",
        hovertemplate=f"<b>{team['name']}</b><br>Points: %{{x}}<br>Count: %{{y}}<extra></extra>",
    ))

# Relegation line (approximate safe point ~36 pts)
fig_hist.add_vline(x=36, line_dash="dash", line_color="#ef4444", line_width=1.5,
                   annotation_text="~Safe zone", annotation_font_color="#ef4444",
                   annotation_font_size=10)

fig_hist.update_layout(
    barmode="overlay",
    paper_bgcolor="#0a0a0f",
    plot_bgcolor="#0d0d14",
    height=300,
    margin=dict(l=0, r=0, t=10, b=10),
    legend=dict(
        font=dict(color="#aaa", size=11, family="Source Sans 3"),
        bgcolor="rgba(0,0,0,0)",
        orientation="h",
        y=-0.18,
    ),
    xaxis=dict(
        title=dict(text="Final Points", font=dict(color="#555", size=10)),
        tickfont=dict(color="#555", size=10),
        showgrid=True, gridcolor="#1e1e2e",
        zeroline=False,
    ),
    yaxis=dict(
        title=dict(text="Simulated Seasons", font=dict(color="#555", size=10)),
        tickfont=dict(color="#555", size=10),
        showgrid=True, gridcolor="#1e1e2e",
    ),
)
st.plotly_chart(fig_hist, use_container_width=True, config={"displayModeBar": False})

# ── Head-to-head relegation race scatter ─────────────────────────────────────

st.markdown('<div class="section-label">Survival Probability by Projected Points</div>', unsafe_allow_html=True)

scatter_x, scatter_y, scatter_text, scatter_colors, scatter_sizes = [], [], [], [], []
for team in sorted_teams:
    tid = team["id"]
    s   = stats[tid]
    scatter_x.append(s["median_pts"])
    scatter_y.append(100 - s["rel_pct"])
    scatter_text.append(team["name"])
    c = COLORS[tid]
    scatter_colors.append(c["primary"] if c["primary"] != "#FFCD00" else "#d4aa00")
    scatter_sizes.append(20)

fig_scatter = go.Figure()
fig_scatter.add_trace(go.Scatter(
    x=scatter_x, y=scatter_y,
    mode="markers+text",
    text=scatter_text,
    textposition="top center",
    textfont=dict(color="#aaa", size=11, family="Source Sans 3"),
    marker=dict(size=16, color=scatter_colors, line=dict(width=1.5, color="#333")),
    hovertemplate="<b>%{text}</b><br>Median pts: %{x}<br>Survival: %{y:.1f}%<extra></extra>",
))
fig_scatter.add_hline(y=50, line_dash="dot", line_color="#555", line_width=1)
fig_scatter.update_layout(
    paper_bgcolor="#0a0a0f",
    plot_bgcolor="#0d0d14",
    height=300,
    margin=dict(l=0, r=0, t=10, b=10),
    xaxis=dict(
        title=dict(text="Median Final Points", font=dict(color="#555", size=10)),
        tickfont=dict(color="#555", size=10),
        showgrid=True, gridcolor="#1e1e2e", zeroline=False,
    ),
    yaxis=dict(
        title=dict(text="Survival Probability (%)", font=dict(color="#555", size=10)),
        tickfont=dict(color="#555", size=10),
        showgrid=True, gridcolor="#1e1e2e",
        range=[0, 105],
    ),
    showlegend=False,
)
st.plotly_chart(fig_scatter, use_container_width=True, config={"displayModeBar": False})

# ── Methodology ───────────────────────────────────────────────────────────────

st.markdown("""
<div class="method-box">
  <strong>METHODOLOGY</strong> &nbsp;·&nbsp;
  Win/draw/loss probabilities are a weighted blend of
  <em>60% five-season historical EPL record (2020/21–2024/25)</em> and
  <em>40% current-season form (last 10 league games)</em>.
  A +7% home advantage modifier is applied per fixture alongside an opponent-strength adjustment.
  100,000 Monte Carlo iterations simulate each remaining fixture by sampling W/D/L
  using Python's <code>random.random()</code>.
  Points awarded as integers only: Win = 3, Draw = 1, Loss = 0.
  The bottom 3 in each iteration are counted as relegated.
  P10/P90 percentiles reflect the full integer-point distribution across all simulated seasons.
</div>
""", unsafe_allow_html=True)
