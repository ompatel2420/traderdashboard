# 💳 Digital Payments India — Dashboard

**Subject:** CSIT922 — Information Visualisation and Decision Support

---

## 📁 Project Structure

```
digital_payments_india/
│
├── app.py                  ← Main Streamlit dashboard (run this)
├── requirements.txt        ← All libraries needed
│
└── data/
    ├── upi_growth.csv      ← Year & month wise UPI volume/value (2016-2025)
    ├── app_share.csv       ← App-wise market share (PhonePe, GPay, Paytm etc.)
    ├── state_wise.csv      ← State-wise UPI transactions across India
    ├── age_group.csv       ← Age group usage data
    └── time_heatmap.csv    ← Hour & day wise transaction heatmap data
```

---

## ▶️ How to Run

**Step 1 — Install libraries**
```bash
pip install -r requirements.txt
```

**Step 2 — Run the app**
```bash
streamlit run app.py
```

**Step 3 — Open in browser**
```
http://localhost:8501
```

---

## 📊 Dashboard Pages

| Tab | What it shows |
|-----|---------------|
| 📈 Growth Trend | How UPI grew from 2016 to 2025 year by year |
| 📱 App Battle | PhonePe vs Google Pay vs Paytm market share |
| 🗺️ Regional View | Which Indian states use UPI most |
| 👥 Age Group | Which age group uses digital payments more |
| ⏰ Time Patterns | At what time of day payments happen most |

---

## 📂 Data Sources

- **NPCI** — npci.org.in (UPI statistics)
- **RBI** — rbi.org.in (Digital payments master data)
- **dataful.in** — All datasets downloadable as CSV (updated to 2025-26)

Real dataset links:
- Growth: https://dataful.in/datasets/432/
- Apps: https://dataful.in/datasets/413/
- State: https://dataful.in/datasets/21563/
- Master: https://dataful.in/datasets/18061/

---

## 🛠️ Tech Stack

- Python
- Streamlit (web dashboard)
- Pandas (data handling)
- Plotly (charts)
