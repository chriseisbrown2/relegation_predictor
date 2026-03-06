# EPL 2025/26 Relegation Battle Dashboard

Interactive Streamlit dashboard with Monte Carlo simulation.

## Setup & Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Launch the dashboard
streamlit run app.py
```

The app will open at http://localhost:8501

## Features
- 100,000 Monte Carlo simulations (integer points only: W=3, D=1, L=0)
- Interactive club selector with fixture-by-fixture win/draw/loss breakdown
- Relegation probability bar chart
- Simulated points distribution histogram (all 6 clubs overlaid)
- Survival probability scatter plot
- Based on 5-season historical EPL data (2020/21–2024/25) blended with current form
