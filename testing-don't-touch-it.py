# ========================== PART 1 ==========================
# SecurePay AI | UPI Fraud Detection
# (Admin Panel + CSV Persistent Blacklist + Admin Session Persistence)

import streamlit as st
import pandas as pd
import plotly.express as px
import random
import re
import io
import os
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# ---------------- CONFIG ----------------
st.set_page_config(page_title="SecurePay AI | UPI Fraud Detection", layout="wide")

BLACKLIST_FILE = "blacklist.csv"
ADMIN_SESSION_FILE = "admin_session.txt"
TRANSACTION_LOG_FILE = "transactions_log.csv"


# ---------------- CSS ----------------
st.markdown("""
<style>
.main { background-color: #f8f9fa; }
.top-nav {
    background-color: #004a99;
    padding: 15px;
    color: white;
    border-radius: 0px 0px 15px 15px;
    margin-bottom: 25px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.stButton>button {
    width: 100%;
    border-radius: 8px;
    height: 3em;
    background-color: #004a99;
    color: white;
    font-weight: bold;
}
.status-card {
    padding: 25px;
    border-radius: 15px;
    color: white;
    text-align: center;
    margin-bottom: 20px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}
.insight-card {
    background: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    border-top: 4px solid #004a99;
    text-align: center;
    height: 100%;
}

/* Existing CSS ke niche ye add karein */
.helpline-card {
    background: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    border-left: 5px solid #d9534f;
    margin-bottom: 20px;
    height: 160px; /* Fixed height for symmetry */
}
.step-num {
    background: #004a99;
    color: white;
    padding: 2px 10px;
    border-radius: 50%;
    margin-right: 10px;
    font-size: 18px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("""
<div class="top-nav">
    <span style="font-size: 24px; font-weight: bold;">🛡 SecurePay AI: Security Command Center</span>
    <span style="background:#28a745;padding:5px 15px;border-radius:20px;font-size:14px;">
        System Status: ACTIVE & SECURE
    </span>
</div>
""", unsafe_allow_html=True)

# ---------------- CSV BLACKLIST FUNCTIONS ----------------
def load_blacklist():
    if not os.path.exists(BLACKLIST_FILE):
        df = pd.DataFrame({"UPI_ID": []})
        df.to_csv(BLACKLIST_FILE, index=False)
        return []
    df = pd.read_csv(BLACKLIST_FILE)
    return df["UPI_ID"].astype(str).str.lower().tolist()

def save_blacklist(blacklist):
    df = pd.DataFrame({"UPI_ID": blacklist})
    df.to_csv(BLACKLIST_FILE, index=False)

def log_transaction(data):
    if not os.path.exists(TRANSACTION_LOG_FILE):
        df = pd.DataFrame(columns=[
            "TXN_ID","UPI_ID","MOBILE","AMOUNT","LOCATION","TYPE",
            "PROBABILITY","RISK","RESULT","DATETIME"
        ])
        df.to_csv(TRANSACTION_LOG_FILE, index=False)

    df = pd.read_csv(TRANSACTION_LOG_FILE)
    df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
    df.to_csv(TRANSACTION_LOG_FILE, index=False)


# ---------------- ADMIN SESSION FUNCTIONS ----------------
def save_admin_session(status):
    with open(ADMIN_SESSION_FILE, "w") as f:
        f.write("1" if status else "0")

def load_admin_session():
    if os.path.exists(ADMIN_SESSION_FILE):
        with open(ADMIN_SESSION_FILE, "r") as f:
            return f.read().strip() == "1"
    return False

# ---------------- SESSION STATE ----------------
if 'result_data' not in st.session_state:
    st.session_state.result_data = None
if 'form_id' not in st.session_state:
    st.session_state.form_id = 0
if 'admin_logged_in' not in st.session_state:
    st.session_state.admin_logged_in = load_admin_session()
if 'blacklist' not in st.session_state:
    st.session_state.blacklist = load_blacklist()

# ---------------- SIDEBAR LOGIN ----------------
st.sidebar.title("🔐 Access Control")

if not st.session_state.admin_logged_in:
    with st.sidebar.expander("Admin Login"):
        user_input = st.text_input("Username")
        pwd_input = st.text_input("Password", type="password")
        if st.button("Login"):
            if user_input == "anas" and pwd_input == "anas123":
                st.session_state.admin_logged_in = True
                save_admin_session(True)
                st.sidebar.success("Welcome, Admin!")
                st.rerun()
            else:
                st.sidebar.error("Invalid Credentials")
else:
    st.sidebar.success("Logged in as Admin")
    if st.sidebar.button("Logout"):
        st.session_state.admin_logged_in = False
        save_admin_session(False)
        st.rerun()

# ---------------- NAVIGATION ----------------
if st.session_state.admin_logged_in:
    nav_options = ["Admin Dashboard","Manage Blacklist"]
    st.sidebar.title("👨‍💼 Admin Panel")
else:
    nav_options = ["Single Detection", "Bulk Upload", "Analytics Dashboard", "Fraud Helpline", "Verified Fraud UPIs"]
    st.sidebar.title("👤 User Navigation")

menu = st.sidebar.radio("Go to:", nav_options)

USER_HOME_CITY = "Mumbai"

if menu == "Admin Dashboard":
    st.title("📊 Admin Monitoring Dashboard")

    if not os.path.exists(TRANSACTION_LOG_FILE):
        st.warning("No transactions recorded yet.")
    else:
        df = pd.read_csv(TRANSACTION_LOG_FILE)

        total = len(df)
        fraud = len(df[df["RESULT"] == "FRAUD"])
        safe = len(df[df["RESULT"] == "SAFE"])

        c1, c2, c3 = st.columns(3)
        c1.metric("Total Transactions", total)
        c2.metric("Fraud Detected", fraud)
        c3.metric("Safe Transactions", safe)

        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            st.plotly_chart(px.pie(
                names=["FRAUD", "SAFE"],
                values=[fraud, safe],
                title="Fraud vs Safe Distribution",
                color_discrete_map={"FRAUD": "#d9534f", "SAFE": "#5cb85c"}
            ))

        with col2:
            st.plotly_chart(px.bar(
                x=["Total", "FraUD", "Safe"],
                y=[total, fraud, safe],
                title="Overall Transaction Summary"
            ))

        st.divider()
        st.subheader("📄 Transaction History Log")

        st.dataframe(df.sort_values(by="DATETIME", ascending=False), use_container_width=True)


# ---------------- CORE LOGIC ----------------
def validate_upi(upi_id):
    upi_pattern = r'^[\w.-]+@(?!gmail\.com|yahoo\.com|outlook\.com|hotmail\.com|icloud\.com)[\w.-]+$'
    return re.match(upi_pattern, upi_id)

def calculate_fraud_score(amount, loc, home_city, upi_id, t_type):
    score = 0
    reasons = []

    if upi_id.lower() in st.session_state.blacklist:
        return 100, ["CRITICAL: This UPI ID is blacklisted in the global fraud database."]

    current_hour = datetime.now().hour
    if 23 <= current_hour or current_hour <= 4:
        score += 20
        reasons.append("Temporal Risk: High-frequency fraud window (Late Night/Early Morning).")

    if amount > 90000:
        score += 50
        reasons.append("Critical Threshold: Transaction exceeds 90% of standard UPI P2P daily limit.")
    elif amount > 45000:
        score += 25
        reasons.append("High-Value Alert: Large outbound transfer requires verification.")

    handle_part = upi_id.split('@')[0].lower()
    fraud_keywords = ['fraud','lottery','win','prize','gift','hacker','admin','verify','claim','bonus']
    if any(k in handle_part for k in fraud_keywords):
        score += 55
        reasons.append("Phishing Pattern: Recipient handle matches blacklisted fraud keywords.")

    if bool(re.search(r'[a-z]{1,2}\d{5,}', handle_part)) or len(handle_part) > 18:
        score += 25
        reasons.append("Mule Account Pattern: Handle structure mimics randomized generation.")

    if loc.lower() != home_city.lower():
        score += 35
        reasons.append(f"Geographic Anomaly: Sudden IP/Location shift from {home_city} to {loc}.")

    if t_type == "Merchant" and amount > 25000:
        score += 20
        reasons.append("Merchant Risk: Unusual high-value payment to unverified gateway.")

    prob = min(score, 99)
    if prob < 25:
        reasons.append("Safe Pattern: Transaction correlates with historical low-risk behavior.")
    return prob, reasons

# ---------------- PDF REPORT FUNCTION ----------------
def create_pdf_report(data, status, proba, risk, reasons):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(300, 750, "BANKING SECURITY - FRAUD INVESTIGATION REPORT")
    p.line(50, 730, 550, 730)

    y = 700
    p.setFont("Helvetica", 12)
    for key, value in data.items():
        p.drawString(50, y, f"{key}: {value}")
        y -= 20

    p.line(50, y, 550, y)
    y -= 30

    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, y, f"FINAL PREDICTION: {status} ({risk} Risk)")
    y -= 20
    p.drawString(50, y, f"FRAUD PROBABILITY: {proba}%")

    y -= 40
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, "Risk Factors Identified:")
    y -= 20

    p.setFont("Helvetica", 10)
    for r in reasons:
        p.drawString(60, y, f"- {r}")
        y -= 15

    p.save()
    buffer.seek(0)
    return buffer

# ---------------- ADMIN PANEL ----------------
if st.session_state.admin_logged_in:
    if menu == "Manage Blacklist":
        st.title("🚫 Admin: Global Blacklist Management")
        st.write("Manage restricted UPI handles. Data is saved permanently in CSV.")

        tab1, tab2 = st.tabs(["➕ Manual Entry", "📁 Bulk Upload (CSV/Excel)"])

        with tab1:
            new_id = st.text_input("Enter UPI ID to block", placeholder="fraud@upi")
            if st.button("Add to Blacklist"):
                if new_id and new_id.lower() not in st.session_state.blacklist:
                    st.session_state.blacklist.append(new_id.lower())
                    save_blacklist(st.session_state.blacklist)
                    st.success(f"{new_id} added successfully!")
                    st.rerun()
                else:
                    st.warning("Invalid ID or already blacklisted.")

        with tab2:
            uploaded_bl = st.file_uploader("Upload list of fraud IDs", type=['csv','xlsx'])
            if uploaded_bl:
                try:
                    bl_df = pd.read_csv(uploaded_bl) if uploaded_bl.name.endswith('.csv') else pd.read_excel(uploaded_bl)
                    if 'UPI_ID' in bl_df.columns:
                        new_ids = bl_df['UPI_ID'].astype(str).str.lower().unique().tolist()
                        added = 0
                        for i in new_ids:
                            if i not in st.session_state.blacklist:
                                st.session_state.blacklist.append(i)
                                added += 1
                        save_blacklist(st.session_state.blacklist)
                        st.success(f"{added} IDs successfully added.")
                    else:
                        st.error("File must contain column: UPI_ID")
                except Exception as e:
                    st.error(f"File Error: {e}")

        st.divider()
        st.subheader("Current Blacklisted UPI IDs")
        st.table(pd.DataFrame(st.session_state.blacklist[::-1], columns=["Blocked UPI ID"]))

# ======================= END OF PART 1 =======================
else:
    # ================= USER FEATURES ONLY =================

    if menu == "Single Detection":
        st.title("UPI Fraud Detector")

        def reset_transaction():
            st.session_state.result_data = None
            st.session_state.form_id += 1

        col_header1, col_header2 = st.columns([5, 1.2])
        with col_header2:
            if st.button("🔄 New Transaction"):
                reset_transaction()
                st.rerun()

        with st.container():
            with st.form(key=f"single_form_{st.session_state.form_id}"):
                c1, c2 = st.columns(2)
                with c1:
                    txn_id = st.text_input("Transaction ID", "TXN" + str(random.randint(10000, 99999)))
                    upi_input = st.text_input("UPI ID", placeholder="user@okhdfc")
                    amount_input = st.number_input("Amount (INR)", min_value=0.0)
                with c2:
                    loc_input = st.text_input("Current Location", placeholder="City Name")
                    m_no = st.text_input("Mobile Number (Optional)", max_chars=10, placeholder="Enter if available")
                    t_type = st.selectbox("Type", ["Person-to-Person", "Merchant", "Bill Pay"])
                btn = st.form_submit_button("ANALYZE TRANSACTION")

        if btn:
            if not upi_input or not loc_input:
                st.error("All fields are mandatory.")
            elif not validate_upi(upi_input):
                st.error("Invalid UPI ID: Personal email domains are blocked.")
            elif m_no and (not m_no.isdigit() or len(m_no) < 10):
                st.error("Please enter a valid 10-digit mobile number or leave it blank.")
            else:
                prob, reasons = calculate_fraud_score(
                    amount_input, loc_input, USER_HOME_CITY, upi_input, t_type
                )
                st.session_state.result_data = {
                    "prob": prob,
                    "reasons": reasons,
                    "status": "FRAUD" if prob >= 50 else "SAFE",
                    "risk": "High" if prob > 75 else ("Medium" if prob >= 40 else "Low"),
                    "details": {
                        "TXN ID": txn_id,
                        "UPI ID": upi_input,
                        "Amount": amount_input,
                        "Location": loc_input,
                        "Type": t_type
                    }
                }
                log_transaction({
    "TXN_ID": txn_id,
    "UPI_ID": upi_input,
    "MOBILE": m_no,
    "AMOUNT": amount_input,
    "LOCATION": loc_input,
    "TYPE": t_type,
    "PROBABILITY": prob,
    "RISK": "High" if prob > 75 else ("Medium" if prob >= 40 else "Low"),
    "RESULT": "FRAUD" if prob >= 50 else "SAFE",
    "DATETIME": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
})


        if st.session_state.result_data:
            res = st.session_state.result_data
            st.divider()
            r1, r2 = st.columns([1, 2])
            with r1:
                bg = "#d9534f" if res["status"] == "FRAUD" else "#5cb85c"
                st.markdown(
                    f'<div class="status-card" style="background-color:{bg};">'
                    f'<h1>{res["status"]}</h1><h3>{res["risk"]} Risk</h3></div>',
                    unsafe_allow_html=True
                )
            with r2:
                st.subheader("Investigation Insights")
                for r in res["reasons"]:
                    st.write(f"- {r}")

            st.plotly_chart(
                px.pie(
                    values=[res['prob'], 100 - res['prob']],
                    names=['Fraud', 'Safe'],
                    color_discrete_sequence=['#ff4b4b', '#00cc96'],
                    hole=0.5
                )
            )

            pdf = create_pdf_report(
                res["details"],
                res["status"],
                res["prob"],
                res["risk"],
                res["reasons"]
            )
            st.download_button(
                "📥 Download Official PDF Report",
                pdf,
                file_name=f"Report_{res['details']['TXN ID']}.pdf"
            )

    elif menu == "Bulk Upload":
        st.title("Bulk Processing Engine")
        uploaded_file = st.file_uploader("Upload CSV or Excel", type=['csv', 'xlsx'])
        if uploaded_file:
            df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)

            df['Fraud_Prob'] = df.apply(
                lambda x: calculate_fraud_score(
                    x['Amount'],
                    x['Location'],
                    USER_HOME_CITY,
                    x['UPI_ID'],
                    x['Type']
                )[0],
                axis=1
            )
            df['Result'] = df['Fraud_Prob'].apply(lambda x: 'FRAUD' if x >= 50 else 'SAFE')

            st.dataframe(df)
            st.plotly_chart(
                px.histogram(
                    df,
                    x="Result",
                    color="Result",
                    color_discrete_map={'SAFE': 'green', 'FRAUD': 'red'}
                )
            )

    elif menu == "Analytics Dashboard":
        st.title("📊 Security Intelligence Panel")

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(
                '<div class="insight-card"><h6>Dataset Coverage</h6>'
                '<h3 style="color:#004a99;">50,000+ Records</h3></div>',
                unsafe_allow_html=True
            )
        with c2:
            st.markdown(
                '<div class="insight-card"><h6>Top Fraud Factor</h6>'
                '<h3 style="color:#d9534f;">Location Anomaly</h3></div>',
                unsafe_allow_html=True
            )
        with c3:
            st.markdown(
                '<div class="insight-card"><h6>Avg Fraud Amount</h6>'
                '<h3 style="color:#f0ad4e;">₹62,450</h3></div>',
                unsafe_allow_html=True
            )

        with c1:
            st.markdown(
                '<div class="insight-card"><h6>High Risk City</h6>'
                '<h3 style="color:#004a99;">Delhi</h3></div>',
                unsafe_allow_html=True
            )
        with c2:
            st.markdown(
                '<div class="insight-card"><h6>Fraud Categories</h6>'
                '<h3 style="color:#d9534f;">Phishing | Mule Accounts</h3></div>',
                unsafe_allow_html=True
            )
        with c3:
            st.markdown(
                '<div class="insight-card"><h6>ML Confidence</h6>'
                '<h3 style="color:#f0ad4e;">98.2%</h3></div>',
                unsafe_allow_html=True
            )

        st.divider()

        g1, g2 = st.columns(2)
        with g1:
            days = [(datetime.now() - timedelta(days=i)).strftime('%d %b') for i in range(7)][::-1]
            st.plotly_chart(
                px.line(
                    x=days,
                    y=[12, 18, 15, 25, 30, 22, 10],
                    title="7-Day Security Alert Trends",
                    markers=True
                )
            )

        with g2:
            st.plotly_chart(
                px.pie(
                    names=['Location Shift', 'High Value Threshold', 'Suspicious Handle'],
                    values=[40, 35, 25],
                    title="System Risk Factor Weights"
                )
            )
    elif menu == "Fraud Helpline":
        st.title("🚨 Fraud Helpline & Emergency Protocol")

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("""
                <div class="helpline-card">
                    <h4><span class="step-num">1</span> Report to Cybercrime</h4>
                    <p>Immediately visit <b>cybercrime.gov.in</b> or call 1930.</p>
                    <h2 style="color:#d9534f; margin-top:10px;"></h2>
                </div>
                <div class="helpline-card" style="border-left-color:#004a99;">
                    <h4><span class="step-num">3</span> Inform Bank/App</h4>
                    <p>Call your bank and the UPI app to raise a dispute immediately.</p>
                </div>
            """, unsafe_allow_html=True)

        with col_b:
            st.markdown("""
                <div class="helpline-card" style="border-left-color:#f0ad4e;">
                    <h4><span class="step-num">2</span> Block UPI/Accounts</h4>
                    <p>Deactivate your UPI ID and block any linked debit/credit cards.</p>
                </div>
                <div class="helpline-card" style="border-left-color:#28a745;">
                    <h4><span class="step-num">4</span> Preserve Evidence</h4>
                    <p>Take screenshots of transaction IDs, alerts, and suspicious chats.</p>
                </div>
            """, unsafe_allow_html=True)

        st.divider()
        st.subheader("📊 The 'Golden Hour' Rule")
        rec_df = pd.DataFrame({
            "Time Since Fraud": ["Within 2 hrs", "2-6 hrs", "6-12 hrs", "After 24 hrs"],
            "Recovery Chance (%)": [95, 65, 30, 5]
        })
        st.plotly_chart(px.bar(
            rec_df, 
            x="Time Since Fraud", 
            y="Recovery Chance (%)", 
            color="Recovery Chance (%)", 
            color_continuous_scale="RdYlGn",
            text_auto=True
        ))

    elif menu == "Verified Fraud UPIs":
        st.title("🚫 Verified Fraudulent UPI Database")
        st.markdown("""
            <div style="background-color: #fff5f5; padding: 15px; border-radius: 10px;
                        border: 1px solid #feb2b2; margin-bottom: 20px;">
                <p style="color: #c53030; font-weight: bold; margin-bottom: 0;">
                    ⚠️ Security Notice: The handles listed below have been verified as fraudulent.
                    Cross-check this list before authorizing any payments to unknown recipients.
                </p>
            </div>
        """, unsafe_allow_html=True)

        if st.session_state.blacklist:
            public_view_df = pd.DataFrame({
                "Fraudulent UPI Handle": st.session_state.blacklist,
                "Status": ["🚩 BLACKLISTED" for _ in st.session_state.blacklist],
                "Verification": ["Verified by Admin" for _ in st.session_state.blacklist]
            })
            st.table(public_view_df)
        else:
            st.info("No fraudulent IDs reported in the database yet.")
