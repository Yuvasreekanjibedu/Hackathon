import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, date
import json

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Finguard AI | Smart Finance Assistant",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── Global reset ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ── Dark gradient background ── */
.stApp {
    background: linear-gradient(135deg, #0a0e1a 0%, #0d1b2a 40%, #0f2440 100%);
    color: #e2e8f0;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1b2a 0%, #071220 100%);
    border-right: 1px solid rgba(99, 179, 237, 0.15);
}
[data-testid="stSidebar"] * {
    color: #cbd5e0 !important;
}

/* ── Metric cards ── */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
    border: 1px solid rgba(99,179,237,0.2);
    border-radius: 16px;
    padding: 1.2rem 1.5rem;
    backdrop-filter: blur(10px);
}
[data-testid="stMetricLabel"] { color: #90cdf4 !important; font-size: 0.8rem; font-weight: 600; letter-spacing: 0.05em; text-transform: uppercase; }
[data-testid="stMetricValue"] { color: #ffffff !important; font-size: 1.8rem; font-weight: 700; }
[data-testid="stMetricDelta"] svg { display: none; }

/* ── Buttons ── */
.stButton>button {
    background: linear-gradient(135deg, #3182ce, #2b6cb0);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 0.6rem 1.5rem;
    font-weight: 600;
    font-size: 0.95rem;
    transition: all 0.25s ease;
    box-shadow: 0 4px 15px rgba(49,130,206,0.3);
}
.stButton>button:hover {
    background: linear-gradient(135deg, #4299e1, #3182ce);
    box-shadow: 0 6px 25px rgba(49,130,206,0.5);
    transform: translateY(-1px);
}

/* ── Inputs ── */
.stNumberInput input, .stTextInput input, .stSelectbox select {
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(99,179,237,0.25) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
}

/* ── Sliders ── */
.stSlider [data-baseweb="slider"] {
    margin-top: 0.5rem;
}

/* ── Alert boxes ── */
.alert-success {
    background: linear-gradient(135deg, rgba(72,187,120,0.15), rgba(52,211,153,0.08));
    border: 1px solid rgba(72,187,120,0.4);
    border-left: 4px solid #48bb78;
    border-radius: 12px;
    padding: 1rem 1.5rem;
    margin: 0.8rem 0;
}
.alert-danger {
    background: linear-gradient(135deg, rgba(245,101,101,0.15), rgba(252,129,74,0.08));
    border: 1px solid rgba(245,101,101,0.4);
    border-left: 4px solid #f56565;
    border-radius: 12px;
    padding: 1rem 1.5rem;
    margin: 0.8rem 0;
}
.alert-warning {
    background: linear-gradient(135deg, rgba(246,173,85,0.15), rgba(251,211,141,0.08));
    border: 1px solid rgba(246,173,85,0.4);
    border-left: 4px solid #f6ad55;
    border-radius: 12px;
    padding: 1rem 1.5rem;
    margin: 0.8rem 0;
}
.alert-info {
    background: linear-gradient(135deg, rgba(99,179,237,0.12), rgba(118,169,250,0.06));
    border: 1px solid rgba(99,179,237,0.35);
    border-left: 4px solid #63b3ed;
    border-radius: 12px;
    padding: 1rem 1.5rem;
    margin: 0.8rem 0;
}

/* ── Section card ── */
.card {
    background: linear-gradient(135deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
    border: 1px solid rgba(99,179,237,0.15);
    border-radius: 20px;
    padding: 2rem;
    margin: 1rem 0;
    backdrop-filter: blur(8px);
}

/* ── Hero / brand header ── */
.hero {
    text-align: center;
    padding: 2.5rem 1rem 1rem;
}
.hero h1 {
    font-size: 3.2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #63b3ed, #b794f4, #76e4f7);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.3rem;
}
.hero p {
    color: #90cdf4;
    font-size: 1.15rem;
    font-weight: 400;
}

/* ── Feature pill badges ── */
.pill {
    display: inline-block;
    background: rgba(99,179,237,0.15);
    border: 1px solid rgba(99,179,237,0.3);
    color: #63b3ed;
    border-radius: 999px;
    padding: 0.3rem 0.9rem;
    font-size: 0.8rem;
    font-weight: 600;
    margin: 0.2rem;
}

/* ── Divider ── */
hr {
    border-color: rgba(99,179,237,0.15) !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.04);
    border-radius: 12px;
    padding: 4px;
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    color: #90cdf4;
    font-weight: 500;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #3182ce, #2b6cb0) !important;
    color: white !important;
}

/* ── Score gauge label ── */
.score-label {
    font-size: 3rem;
    font-weight: 800;
    text-align: center;
}

/* ── Expander ── */
[data-testid="stExpander"] {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(99,179,237,0.15);
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# SESSION STATE – in-memory expense log
# ─────────────────────────────────────────────────────────────
if "expenses" not in st.session_state:
    st.session_state.expenses = []
if "transactions" not in st.session_state:
    # Seed with realistic demo transactions for fraud demo
    st.session_state.transactions = [
        {"id": "TXN001", "amount": 1200, "merchant": "Amazon", "location": "Mumbai", "time": "10:30 AM", "type": "Online", "risk": "Low"},
        {"id": "TXN002", "amount": 85000, "merchant": "Unknown Vendor", "location": "International", "time": "3:47 AM", "type": "International", "risk": "High"},
        {"id": "TXN003", "amount": 450, "merchant": "Swiggy", "location": "Pune", "time": "12:15 PM", "type": "Food", "risk": "Low"},
    ]


# ─────────────────────────────────────────────────────────────
# SIDEBAR NAVIGATION
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 1rem 0 0.5rem;'>
        <div style='font-size:2.5rem;'>🛡️</div>
        <div style='font-size:1.3rem; font-weight:800; color:#63b3ed; letter-spacing:0.02em;'>FinGuard AI</div>
        <div style='font-size:0.75rem; color:#718096; margin-top:0.2rem;'>Smart Finance Assistant</div>
    </div>
    <hr/>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        ["🏠  Dashboard", "💰  Expense Tracker", "🛡️  Fraud Detection", "🏦  Loan Eligibility", "📊  Analytics"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("""
    <div style='font-size:0.75rem; color:#4a5568; text-align:center; padding:0.5rem;'>
        Built for <span style='color:#63b3ed; font-weight:600;'>FinTech Hackathon 2026</span><br/>
        Powered by AI & Streamlit
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────────────────────

def fraud_score(amount, location, hour, tx_type):
    """Simple rule-based fraud risk scorer (0-100)."""
    score = 0
    if amount > 50000:
        score += 40
    elif amount > 20000:
        score += 20
    elif amount > 10000:
        score += 10

    risky_locations = ["international", "unknown", "foreign", "overseas"]
    if any(loc in location.lower() for loc in risky_locations):
        score += 30

    if hour < 5 or hour > 23:
        score += 20

    if tx_type in ["International Wire", "Crypto Exchange", "Unknown Merchant"]:
        score += 25

    score = min(score, 100)
    return score


def loan_eligibility(income, credit_score, existing_emi, loan_amount, tenure):
    """Rule-based loan eligibility with detailed breakdown."""
    reasons = []
    score = 0

    # Income check
    monthly_income = income / 12
    if monthly_income >= 50000:
        score += 30
        reasons.append(("✅", "Strong monthly income", f"₹{monthly_income:,.0f}/month"))
    elif monthly_income >= 25000:
        score += 18
        reasons.append(("⚠️", "Moderate income", f"₹{monthly_income:,.0f}/month"))
    else:
        score += 5
        reasons.append(("❌", "Low income may limit eligibility", f"₹{monthly_income:,.0f}/month"))

    # Credit score
    if credit_score >= 750:
        score += 35
        reasons.append(("✅", "Excellent credit score", str(credit_score)))
    elif credit_score >= 650:
        score += 22
        reasons.append(("⚠️", "Fair credit score", str(credit_score)))
    elif credit_score >= 550:
        score += 10
        reasons.append(("❌", "Poor credit score", str(credit_score)))
    else:
        score += 0
        reasons.append(("❌", "Very poor credit score", str(credit_score)))

    # EMI burden
    emi_ratio = existing_emi / monthly_income if monthly_income > 0 else 1
    if emi_ratio < 0.3:
        score += 20
        reasons.append(("✅", "Low existing debt burden", f"{emi_ratio*100:.0f}% of income"))
    elif emi_ratio < 0.5:
        score += 10
        reasons.append(("⚠️", "Moderate debt burden", f"{emi_ratio*100:.0f}% of income"))
    else:
        score += 0
        reasons.append(("❌", "High existing EMI burden", f"{emi_ratio*100:.0f}% of income"))

    # Loan-to-income
    lti = loan_amount / income if income > 0 else 99
    if lti < 3:
        score += 15
        reasons.append(("✅", "Loan amount reasonable vs income", f"{lti:.1f}x annual income"))
    elif lti < 5:
        score += 8
        reasons.append(("⚠️", "Loan amount is high vs income", f"{lti:.1f}x annual income"))
    else:
        score += 0
        reasons.append(("❌", "Loan amount too high vs income", f"{lti:.1f}x annual income"))

    # Estimated EMI
    monthly_rate = 0.085 / 12  # 8.5% p.a. approx
    n = tenure * 12
    if n > 0 and monthly_rate > 0:
        emi = loan_amount * monthly_rate * (1 + monthly_rate)**n / ((1 + monthly_rate)**n - 1)
    else:
        emi = loan_amount / (n or 1)

    return score, reasons, emi


def spending_advice(categories):
    """Generate personalized spending advice."""
    advice = []
    total = sum(categories.values())
    if total == 0:
        return advice

    if categories.get("Entertainment", 0) / total > 0.15:
        advice.append(("🎮", "Entertainment spending is above 15% of total", "Consider reducing to under 10%"))
    if categories.get("Food", 0) / total > 0.35:
        advice.append(("🍔", "Food costs are high", "Meal planning could save ₹2,000-5,000/month"))
    if categories.get("Shopping", 0) / total > 0.20:
        advice.append(("🛍️", "Shopping is a large category", "Try a 24-hour cooling-off rule before purchases"))
    if len(advice) == 0:
        advice.append(("🌟", "Great spending balance!", "Keep maintaining this financial discipline"))
    return advice


# ─────────────────────────────────────────────────────────────
# PAGE: DASHBOARD
# ─────────────────────────────────────────────────────────────
if "Dashboard" in page:
    st.markdown("""
    <div class='hero'>
        <h1>🛡️ Finguard AI</h1>
        <p>Your AI-powered personal finance assistant — expenses, fraud, and loans in one place</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='text-align:center; margin-bottom:2rem;'>
        <span class='pill'>💡 Expense Intelligence</span>
        <span class='pill'>🛡️ Fraud Detection</span>
        <span class='pill'>🏦 Loan Predictor</span>
        <span class='pill'>📊 Real-time Analytics</span>
    </div>
    """, unsafe_allow_html=True)

    # Summary KPIs
    total_expenses = sum(e["amount"] for e in st.session_state.expenses)
    num_entries = len(st.session_state.expenses)
    high_risk_txns = sum(1 for t in st.session_state.transactions if t["risk"] == "High")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💸 Total Tracked Expenses", f"₹{total_expenses:,.0f}", f"{num_entries} entries")
    col2.metric("🛡️ Transactions Monitored", str(len(st.session_state.transactions)), "Live")
    col3.metric("⚠️ High Risk Alerts", str(high_risk_txns), "Requires review")
    col4.metric("📅 Today's Date", date.today().strftime("%d %b %Y"), "UTC+5:30")

    st.markdown("---")

    # Feature cards
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class='card'>
            <div style='font-size:2.5rem; margin-bottom:0.8rem;'>💰</div>
            <div style='font-size:1.15rem; font-weight:700; color:#63b3ed; margin-bottom:0.5rem;'>Expense Tracker</div>
            <p style='color:#90cdf4; font-size:0.9rem; line-height:1.6;'>
                Log daily expenses by category, visualize spending patterns, 
                track savings goals, and get personalized budget advice.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='card'>
            <div style='font-size:2.5rem; margin-bottom:0.8rem;'>🛡️</div>
            <div style='font-size:1.15rem; font-weight:700; color:#b794f4; margin-bottom:0.5rem;'>Fraud Detection</div>
            <p style='color:#90cdf4; font-size:0.9rem; line-height:1.6;'>
                Analyze transactions in real time using AI risk scoring. 
                Detect suspicious patterns by amount, location, time, and merchant type.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class='card'>
            <div style='font-size:2.5rem; margin-bottom:0.8rem;'>🏦</div>
            <div style='font-size:1.15rem; font-weight:700; color:#76e4f7; margin-bottom:0.5rem;'>Loan Eligibility</div>
            <p style='color:#90cdf4; font-size:0.9rem; line-height:1.6;'>
                Enter your financial profile and get instant loan eligibility assessment 
                with detailed factor breakdown and EMI calculator.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Recent transactions preview
    if st.session_state.transactions:
        st.markdown("### 📋 Recent Transaction Monitor")
        df = pd.DataFrame(st.session_state.transactions)
        def highlight_risk(row):
            color = "rgba(245,101,101,0.15)" if row["risk"] == "High" else "rgba(72,187,120,0.10)"
            return [f"background-color: {color}"] * len(row)
        st.dataframe(
            df[["id", "amount", "merchant", "location", "time", "risk"]].rename(columns={
                "id": "Transaction ID", "amount": "Amount (₹)", "merchant": "Merchant",
                "location": "Location", "time": "Time", "risk": "Risk Level"
            }),
            use_container_width=True,
            hide_index=True
        )


# ─────────────────────────────────────────────────────────────
# PAGE: EXPENSE TRACKER
# ─────────────────────────────────────────────────────────────
elif "Expense" in page:
    st.markdown("## 💰 Expense Tracker")
    st.markdown("Track your spending and get AI-powered budget insights.")

    tab1, tab2 = st.tabs(["➕ Log Expense", "📊 Analysis"])

    with tab1:
        with st.form("expense_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                monthly_income = st.number_input("Monthly Income (₹)", min_value=0, value=50000, step=1000)
                category = st.selectbox("Category", [
                    "Food", "Transport", "Shopping", "Entertainment",
                    "Healthcare", "Education", "Utilities", "Rent", "Other"
                ])
            with col2:
                amount = st.number_input("Expense Amount (₹)", min_value=1, value=500, step=50)
                description = st.text_input("Description", placeholder="e.g. Zomato dinner")

            submitted = st.form_submit_button("➕ Add Expense", use_container_width=True)
            if submitted:
                st.session_state.expenses.append({
                    "date": date.today().isoformat(),
                    "category": category,
                    "amount": amount,
                    "description": description,
                    "income": monthly_income
                })
                st.success(f"✅ Added ₹{amount:,.0f} under **{category}**")

        # Show expense list
        if st.session_state.expenses:
            st.markdown("#### 📋 Logged Expenses")
            df = pd.DataFrame(st.session_state.expenses)
            st.dataframe(
                df[["date", "category", "amount", "description"]].rename(columns={
                    "date": "Date", "category": "Category",
                    "amount": "Amount (₹)", "description": "Note"
                }),
                use_container_width=True, hide_index=True
            )

            total = df["amount"].sum()
            income = st.session_state.expenses[-1]["income"]
            savings = income - total
            savings_pct = (savings / income * 100) if income > 0 else 0

            col1, col2, col3 = st.columns(3)
            col1.metric("💸 Total Expenses", f"₹{total:,.0f}")
            col2.metric("💵 Estimated Savings", f"₹{max(savings,0):,.0f}")
            col3.metric("📈 Savings Rate", f"{max(savings_pct,0):.1f}%",
                        "🎯 Target: 20%" if savings_pct < 20 else "✅ Above target!")

            # Savings health bar
            st.markdown("#### 🎯 Savings Health")
            health_pct = min(savings_pct, 100)
            color = "#48bb78" if savings_pct >= 20 else ("#f6ad55" if savings_pct >= 10 else "#f56565")
            st.markdown(f"""
            <div style='background:rgba(255,255,255,0.05); border-radius:999px; height:14px; margin:0.5rem 0;'>
                <div style='background:{color}; width:{health_pct:.1f}%; height:100%; border-radius:999px; transition:width 0.5s;'></div>
            </div>
            <div style='text-align:right; color:{color}; font-size:0.85rem;'>{savings_pct:.1f}% saved</div>
            """, unsafe_allow_html=True)

    with tab2:
        if st.session_state.expenses:
            df = pd.DataFrame(st.session_state.expenses)
            cat_totals = df.groupby("category")["amount"].sum().to_dict()

            col1, col2 = st.columns(2)

            with col1:
                # Pie chart
                fig_pie = px.pie(
                    values=list(cat_totals.values()),
                    names=list(cat_totals.keys()),
                    title="Spending by Category",
                    color_discrete_sequence=px.colors.sequential.Blues_r,
                    hole=0.45
                )
                fig_pie.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font_color="#e2e8f0",
                    title_font_size=15,
                    showlegend=True
                )
                st.plotly_chart(fig_pie, use_container_width=True)

            with col2:
                # Bar chart
                fig_bar = px.bar(
                    x=list(cat_totals.keys()),
                    y=list(cat_totals.values()),
                    title="Expenses by Category (₹)",
                    color=list(cat_totals.values()),
                    color_continuous_scale="Blues",
                    labels={"x": "Category", "y": "Amount (₹)"}
                )
                fig_bar.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font_color="#e2e8f0",
                    title_font_size=15,
                    coloraxis_showscale=False
                )
                st.plotly_chart(fig_bar, use_container_width=True)

            # AI Advice
            st.markdown("#### 🤖 AI Budget Advice")
            advice = spending_advice(cat_totals)
            for icon, title, detail in advice:
                st.markdown(f"""
                <div class='alert-info'>
                    <span style='font-size:1.2rem;'>{icon}</span>
                    <strong style='color:#63b3ed;'> {title}</strong><br/>
                    <span style='color:#a0aec0; font-size:0.9rem;'>{detail}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class='alert-info'>
                <strong>No expenses logged yet.</strong> Use the "Log Expense" tab to get started!
            </div>
            """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# PAGE: FRAUD DETECTION
# ─────────────────────────────────────────────────────────────
elif "Fraud" in page:
    st.markdown("## 🛡️ AI Fraud Detection")
    st.markdown("Analyze transactions for suspicious activity using our intelligent risk scoring engine.")

    tab1, tab2 = st.tabs(["🔍 Analyze Transaction", "📋 Transaction Log"])

    with tab1:
        col1, col2 = st.columns([1.2, 1])

        with col1:
            st.markdown("#### Transaction Details")
            with st.form("fraud_form"):
                amount = st.number_input("Transaction Amount (₹)", min_value=1, value=5000, step=100)
                merchant = st.text_input("Merchant / Payee Name", value="Unknown Vendor")
                location = st.selectbox("Transaction Location", [
                    "Mumbai", "Delhi", "Bangalore", "Pune", "Chennai",
                    "International", "Unknown", "Foreign Country", "Overseas"
                ])
                tx_type = st.selectbox("Transaction Type", [
                    "UPI Transfer", "Card Payment", "Net Banking",
                    "International Wire", "Crypto Exchange", "Unknown Merchant"
                ])
                tx_time = st.slider("Transaction Hour (24h)", 0, 23, 14)
                analyze = st.form_submit_button("🔍 Analyze Risk", use_container_width=True)

            if analyze:
                score = fraud_score(amount, location, tx_time, tx_type)

                if score >= 60:
                    risk_level = "HIGH"
                    color = "#f56565"
                    css_class = "alert-danger"
                    icon = "🚨"
                    action = "Block this transaction immediately and contact your bank."
                elif score >= 30:
                    risk_level = "MEDIUM"
                    color = "#f6ad55"
                    css_class = "alert-warning"
                    icon = "⚠️"
                    action = "Verify the transaction with the merchant before proceeding."
                else:
                    risk_level = "LOW"
                    color = "#48bb78"
                    css_class = "alert-success"
                    icon = "✅"
                    action = "Transaction appears safe to proceed."

                # Gauge chart
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=score,
                    title={"text": "Fraud Risk Score", "font": {"color": "#e2e8f0", "size": 16}},
                    gauge={
                        "axis": {"range": [0, 100], "tickcolor": "#718096"},
                        "bar": {"color": color},
                        "bgcolor": "rgba(255,255,255,0.05)",
                        "steps": [
                            {"range": [0, 30], "color": "rgba(72,187,120,0.15)"},
                            {"range": [30, 60], "color": "rgba(246,173,85,0.15)"},
                            {"range": [60, 100], "color": "rgba(245,101,101,0.15)"},
                        ],
                        "threshold": {"line": {"color": color, "width": 3}, "value": score}
                    },
                    number={"font": {"color": color, "size": 42}, "suffix": "/100"}
                ))
                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    font_color="#e2e8f0",
                    height=280
                )
                st.plotly_chart(fig, use_container_width=True)

                st.markdown(f"""
                <div class='{css_class}'>
                    <div style='font-size:1.3rem; font-weight:700; color:{"#f56565" if risk_level=="HIGH" else ("#f6ad55" if risk_level=="MEDIUM" else "#48bb78")};'>
                        {icon} Risk Level: {risk_level}
                    </div>
                    <div style='color:#a0aec0; margin-top:0.4rem;'>{action}</div>
                </div>
                """, unsafe_allow_html=True)

                # Log transaction
                st.session_state.transactions.append({
                    "id": f"TXN{len(st.session_state.transactions)+1:03d}",
                    "amount": amount,
                    "merchant": merchant,
                    "location": location,
                    "time": f"{tx_time:02d}:00",
                    "type": tx_type,
                    "risk": risk_level.capitalize() if risk_level != "HIGH" else "High"
                })
                st.caption("✅ Transaction added to monitor log.")

        with col2:
            st.markdown("#### 📖 Risk Factor Guide")
            st.markdown("""
            <div class='card'>
                <div style='margin-bottom:0.8rem;'>
                    <span style='color:#f56565; font-weight:700;'>🚨 HIGH RISK indicators</span>
                    <ul style='color:#a0aec0; margin-top:0.4rem; font-size:0.88rem;'>
                        <li>Amount above ₹50,000</li>
                        <li>International / Unknown location</li>
                        <li>Transaction between midnight-5 AM</li>
                        <li>Crypto or unknown merchant type</li>
                    </ul>
                </div>
                <hr/>
                <div style='margin-top:0.8rem;'>
                    <span style='color:#f6ad55; font-weight:700;'>⚠️ MEDIUM RISK indicators</span>
                    <ul style='color:#a0aec0; margin-top:0.4rem; font-size:0.88rem;'>
                        <li>Amount ₹20,000–₹50,000</li>
                        <li>Unusual transaction hour</li>
                        <li>Unknown merchant name</li>
                    </ul>
                </div>
                <hr/>
                <div style='margin-top:0.8rem;'>
                    <span style='color:#48bb78; font-weight:700;'>✅ LOW RISK</span>
                    <ul style='color:#a0aec0; margin-top:0.4rem; font-size:0.88rem;'>
                        <li>Known domestic merchant</li>
                        <li>Reasonable amount</li>
                        <li>Normal business hours</li>
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with tab2:
        if st.session_state.transactions:
            df = pd.DataFrame(st.session_state.transactions)
            risk_counts = df["risk"].value_counts().to_dict()

            col1, col2, col3 = st.columns(3)
            col1.metric("🔴 High Risk", risk_counts.get("High", 0))
            col2.metric("🟡 Medium Risk", risk_counts.get("Medium", 0))
            col3.metric("🟢 Low Risk", risk_counts.get("Low", 0))

            st.dataframe(
                df[["id", "amount", "merchant", "location", "time", "type", "risk"]].rename(columns={
                    "id": "ID", "amount": "Amount (₹)", "merchant": "Merchant",
                    "location": "Location", "time": "Time", "type": "Type", "risk": "Risk"
                }),
                use_container_width=True, hide_index=True
            )

            # Risk distribution pie
            fig = px.pie(
                values=list(risk_counts.values()),
                names=list(risk_counts.keys()),
                title="Transaction Risk Distribution",
                color=list(risk_counts.keys()),
                color_discrete_map={"High": "#f56565", "Medium": "#f6ad55", "Low": "#48bb78"}
            )
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="#e2e8f0"
            )
            st.plotly_chart(fig, use_container_width=True)


# ─────────────────────────────────────────────────────────────
# PAGE: LOAN ELIGIBILITY
# ─────────────────────────────────────────────────────────────
elif "Loan" in page:
    st.markdown("## 🏦 Loan Eligibility Predictor")
    st.markdown("Get an instant, AI-powered loan eligibility assessment with detailed factor analysis.")

    col1, col2 = st.columns([1.2, 1])

    with col1:
        st.markdown("#### Your Financial Profile")
        with st.form("loan_form"):
            annual_income = st.number_input("Annual Income (₹)", min_value=0, value=600000, step=10000)
            credit_score_val = st.slider("Credit Score (300–900)", 300, 900, 720, step=5)
            existing_emi = st.number_input("Existing Monthly EMI (₹)", min_value=0, value=5000, step=500)
            loan_amount = st.number_input("Loan Amount Requested (₹)", min_value=10000, value=500000, step=10000)
            tenure = st.slider("Loan Tenure (Years)", 1, 30, 5)
            purpose = st.selectbox("Loan Purpose", [
                "Home Loan", "Personal Loan", "Car Loan",
                "Education Loan", "Business Loan", "Medical Emergency"
            ])
            check = st.form_submit_button("🔍 Check Eligibility", use_container_width=True)

        if check:
            score, reasons, emi = loan_eligibility(annual_income, credit_score_val, existing_emi, loan_amount, tenure)

            # Eligibility gauge
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=score,
                title={"text": "Eligibility Score", "font": {"color": "#e2e8f0", "size": 16}},
                gauge={
                    "axis": {"range": [0, 100], "tickcolor": "#718096"},
                    "bar": {"color": "#63b3ed" if score >= 70 else ("#f6ad55" if score >= 45 else "#f56565")},
                    "bgcolor": "rgba(255,255,255,0.05)",
                    "steps": [
                        {"range": [0, 45], "color": "rgba(245,101,101,0.12)"},
                        {"range": [45, 70], "color": "rgba(246,173,85,0.12)"},
                        {"range": [70, 100], "color": "rgba(99,179,237,0.12)"},
                    ],
                },
                number={"font": {"color": "#63b3ed", "size": 42}, "suffix": "/100"}
            ))
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="#e2e8f0",
                height=260
            )
            st.plotly_chart(fig, use_container_width=True)

            if score >= 70:
                verdict = ("alert-success", "✅", "Congratulations! You're likely ELIGIBLE", "#48bb78")
            elif score >= 45:
                verdict = ("alert-warning", "⚠️", "Conditional eligibility – Lender may require guarantor", "#f6ad55")
            else:
                verdict = ("alert-danger", "❌", "Currently NOT eligible – Improve your financial profile", "#f56565")

            css, icon, text, clr = verdict
            st.markdown(f"""
            <div class='{css}'>
                <div style='font-size:1.2rem; font-weight:700; color:{clr};'>{icon} {text}</div>
                <div style='color:#a0aec0; margin-top:0.4rem; font-size:0.9rem;'>
                    Purpose: <strong style='color:#63b3ed;'>{purpose}</strong> &nbsp;|&nbsp;
                    Estimated Monthly EMI: <strong style='color:#63b3ed;'>₹{emi:,.0f}</strong>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("#### 📋 Factor-by-Factor Breakdown")
            for icon, label, detail in reasons:
                color_map = {"✅": "#48bb78", "⚠️": "#f6ad55", "❌": "#f56565"}
                clr = color_map.get(icon, "#63b3ed")
                css_map = {"✅": "alert-success", "⚠️": "alert-warning", "❌": "alert-danger"}
                css = css_map.get(icon, "alert-info")
                st.markdown(f"""
                <div class='{css}' style='padding:0.6rem 1rem; margin:0.3rem 0;'>
                    <span style='font-weight:600; color:{clr};'>{icon} {label}</span>
                    <span style='color:#718096; font-size:0.85rem; float:right;'>{detail}</span>
                </div>
                """, unsafe_allow_html=True)

    with col2:
        st.markdown("#### 💡 Tips to Improve Eligibility")
        st.markdown("""
        <div class='card'>
            <div style='font-size:0.92rem; color:#a0aec0; line-height:1.9;'>
                <div><span style='color:#63b3ed;'>🎯</span> <strong style='color:#e2e8f0;'>Credit Score</strong> – Pay bills on time, reduce credit utilization below 30%</div>
                <div><span style='color:#63b3ed;'>💰</span> <strong style='color:#e2e8f0;'>Income</strong> – Show additional income sources like freelance, rent, or dividends</div>
                <div><span style='color:#63b3ed;'>📉</span> <strong style='color:#e2e8f0;'>Reduce EMI</strong> – Pay off existing loans before applying for a new one</div>
                <div><span style='color:#63b3ed;'>🏠</span> <strong style='color:#e2e8f0;'>Collateral</strong> – Secured loans have higher approval rates</div>
                <div><span style='color:#63b3ed;'>⏳</span> <strong style='color:#e2e8f0;'>Tenure</strong> – Longer tenure reduces EMI but increases total interest</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Credit score visual
        st.markdown("#### 📊 Credit Score Bands")
        bands = {"Poor\n(300-549)": 1, "Fair\n(550-649)": 1, "Good\n(650-749)": 1, "Excellent\n(750-900)": 1}
        colors = ["#f56565", "#f6ad55", "#63b3ed", "#48bb78"]
        fig_cs = go.Figure(go.Bar(
            x=list(bands.keys()),
            y=[1, 1, 1, 1],
            marker_color=colors,
            text=["Poor", "Fair", "Good", "Excellent"],
            textposition="inside"
        ))

        # Highlight current band
        if credit_score_val < 550:
            active = 0
        elif credit_score_val < 650:
            active = 1
        elif credit_score_val < 750:
            active = 2
        else:
            active = 3

        fig_cs.add_annotation(
            x=list(bands.keys())[active], y=1.05,
            text=f"▲ You: {credit_score_val}",
            showarrow=False, font=dict(color="#63b3ed", size=13)
        )
        fig_cs.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#e2e8f0",
            showlegend=False,
            yaxis=dict(visible=False),
            height=200,
            margin=dict(t=30, b=10)
        )
        st.plotly_chart(fig_cs, use_container_width=True)


# ─────────────────────────────────────────────────────────────
# PAGE: ANALYTICS
# ─────────────────────────────────────────────────────────────
elif "Analytics" in page:
    st.markdown("## 📊 Financial Analytics")
    st.markdown("Comprehensive overview of your financial data and trends.")

    # Demo data for analytics if no real data
    if not st.session_state.expenses:
        st.markdown("""
        <div class='alert-info'>
            <strong>Demo Mode</strong> – Add expenses in the Expense Tracker for personalized analytics. Showing sample data below.
        </div>
        """, unsafe_allow_html=True)
        demo_expenses = [
            {"date": "2026-06-01", "category": "Food", "amount": 3200},
            {"date": "2026-06-02", "category": "Transport", "amount": 800},
            {"date": "2026-06-03", "category": "Shopping", "amount": 4500},
            {"date": "2026-06-04", "category": "Entertainment", "amount": 1200},
            {"date": "2026-06-05", "category": "Food", "amount": 2800},
            {"date": "2026-06-05", "category": "Utilities", "amount": 1500},
            {"date": "2026-06-06", "category": "Healthcare", "amount": 600},
        ]
        df_exp = pd.DataFrame(demo_expenses)
    else:
        df_exp = pd.DataFrame(st.session_state.expenses)

    col1, col2 = st.columns(2)

    with col1:
        # Spending over time
        daily = df_exp.groupby("date")["amount"].sum().reset_index()
        fig_line = px.line(
            daily, x="date", y="amount",
            title="Daily Spending Trend (₹)",
            markers=True,
            color_discrete_sequence=["#63b3ed"]
        )
        fig_line.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#e2e8f0",
            xaxis=dict(gridcolor="rgba(99,179,237,0.1)"),
            yaxis=dict(gridcolor="rgba(99,179,237,0.1)")
        )
        st.plotly_chart(fig_line, use_container_width=True)

    with col2:
        # Category treemap
        cat_df = df_exp.groupby("category")["amount"].sum().reset_index()
        fig_tree = px.treemap(
            cat_df, path=["category"], values="amount",
            title="Spending Treemap",
            color="amount",
            color_continuous_scale="Blues"
        )
        fig_tree.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#e2e8f0"
        )
        st.plotly_chart(fig_tree, use_container_width=True)

    # Fraud analytics
    st.markdown("#### 🛡️ Transaction Risk Summary")
    df_txn = pd.DataFrame(st.session_state.transactions)
    risk_by_amount = df_txn.groupby("risk")["amount"].sum().reset_index()
    fig_risk = px.bar(
        risk_by_amount, x="risk", y="amount",
        title="Total Amount by Risk Level (₹)",
        color="risk",
        color_discrete_map={"High": "#f56565", "Medium": "#f6ad55", "Low": "#48bb78"}
    )
    fig_risk.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#e2e8f0",
        showlegend=False,
        yaxis=dict(gridcolor="rgba(99,179,237,0.1)")
    )
    st.plotly_chart(fig_risk, use_container_width=True)

    # Insights summary
    st.markdown("#### 🤖 Key Insights")
    col1, col2, col3 = st.columns(3)
    with col1:
        top_cat = df_exp.groupby("category")["amount"].sum().idxmax()
        top_amt = df_exp.groupby("category")["amount"].sum().max()
        st.markdown(f"""
        <div class='card' style='text-align:center;'>
            <div style='font-size:1.8rem;'>🏆</div>
            <div style='color:#63b3ed; font-weight:700;'>Top Spend Category</div>
            <div style='font-size:1.3rem; font-weight:800; color:#fff;'>{top_cat}</div>
            <div style='color:#718096;'>₹{top_amt:,.0f} total</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        avg_txn = df_txn["amount"].mean()
        st.markdown(f"""
        <div class='card' style='text-align:center;'>
            <div style='font-size:1.8rem;'>💳</div>
            <div style='color:#b794f4; font-weight:700;'>Avg Transaction</div>
            <div style='font-size:1.3rem; font-weight:800; color:#fff;'>₹{avg_txn:,.0f}</div>
            <div style='color:#718096;'>across {len(df_txn)} transactions</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        high_risk_pct = (df_txn["risk"] == "High").mean() * 100
        st.markdown(f"""
        <div class='card' style='text-align:center;'>
            <div style='font-size:1.8rem;'>⚠️</div>
            <div style='color:#f6ad55; font-weight:700;'>High Risk Rate</div>
            <div style='font-size:1.3rem; font-weight:800; color:#fff;'>{high_risk_pct:.0f}%</div>
            <div style='color:#718096;'>of all transactions</div>
        </div>
        """, unsafe_allow_html=True)
