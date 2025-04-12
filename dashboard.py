// Real Estate Call Dashboard - Web App (Streamlit)

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Load and clean data
@st.cache_data
def load_data():
    df = pd.read_csv("data.csv")
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['DayOfWeek'] = df['Date'].dt.day_name()

    cols_to_num = ['Total Dials', 'Conversations', 'Leads', 'Offer Made', 'Total Correct Numbers',
                   'Dead Number', 'Correct Initial Call', 'Correct Follow Up 1',
                   'Correct Follow Up 2', 'Correct Follow Up 3', 'Not Interested', 
                   'Wrong Number']
    for col in cols_to_num:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df['Connection Rate'] = df['Conversations'] / df['Total Dials']
    df['Offers per Convo'] = df.apply(lambda row: row['Offer Made'] / row['Conversations'] if row['Conversations'] and row['Conversations'] > 0 else None, axis=1)
    return df

# Load data
df = load_data()

st.title("📞 Real Estate Call Performance Dashboard")

# KPIs
st.header("📌 Key Metrics")
avg_metrics = df[['Total Dials', 'Conversations', 'Leads', 'Offer Made', 'Total Correct Numbers']].mean().round(2)
offer_efficiency = df['Offers per Convo'].dropna().mean().round(2) if not df['Offers per Convo'].dropna().empty else 0

col1, col2 = st.columns(2)
col1.metric("Avg. Conversations", f"{avg_metrics['Conversations']:.2f}")
col1.metric("Avg. Correct Numbers", f"{avg_metrics['Total Correct Numbers']:.2f}")
col2.metric("Avg. Offers Made", f"{avg_metrics['Offer Made']:.2f}")
col2.metric("Offer Efficiency", f"{offer_efficiency:.2%}")

# Connection Rate by Day
st.subheader("📅 Connection Rate by Day")
conn_rate_by_day = df.groupby('DayOfWeek')['Connection Rate'].mean().sort_values(ascending=False)
st.bar_chart(conn_rate_by_day)

# Call Quality Breakdown
st.subheader("📊 Call Quality Breakdown")
quality_metrics = df[['Wrong Number', 'Dead Number', 'Total Correct Numbers']].mean()
st.bar_chart(quality_metrics)

# Follow-Up Usage
st.subheader("📈 Follow-Up Call Totals")
follow_up_totals = df[['Correct Follow Up 1', 'Correct Follow Up 2', 'Correct Follow Up 3']].sum()
st.bar_chart(follow_up_totals)

# Automation Flow Recommendations
st.subheader("⚙️ Suggested Automations")
st.markdown("""
- 🔁 **Follow-Up Triggers**:
    - If *Correct Initial Call* but no *Offer Made* → schedule auto follow-up in 24h.
    - If *Follow Up 1* completed → auto-schedule Follow Up 2 in 3 days.

- 🚨 **Alerts**:
    - If *Connection Rate* drops below 10% → notify manager.
    - If *Wrong Number Rate* > 30% → flag list for review.

- 📨 **CRM Reminders**:
    - Push daily summaries to Slack or Email with key stats.
    - Track performance trends weekly.
""")
