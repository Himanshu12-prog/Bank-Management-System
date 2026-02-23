import streamlit as st
import sqlite3
import random
import string
import pandas as pd
from datetime import datetime, timedelta
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
import time

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="HDFC Bank",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -------------------- FINAL PRO CSS --------------------
st.markdown("""
<style>

/* GLOBAL FONT */
html, body, [class*="css"] {
    font-family: "Times New Roman", Times, serif !important;
}

/* MAIN BACKGROUND */
.stApp {
    background: linear-gradient(180deg, #f0f9ff 0%, #e0f2fe 100%);
    color: #0f172a;
}

/* CENTER CONTAINER */
.block-container {
    max-width: 1100px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #075985 0%, #0ea5e9 100%);
}
section[data-testid="stSidebar"] * {
    color: white !important;
}

/* CARD */
.glass-card {
    background: white;
    padding: 30px;
    border-radius: 18px;
    border: 1px solid #e0f2fe;
    box-shadow: 0 10px 30px rgba(2,132,199,0.08);
    margin-top: 12px;
}

/* BUTTON */
.stButton>button {
    background: linear-gradient(135deg, #075985, #0284c7);
    color: white !important;
    border-radius: 10px;
    height: 3em;
    font-weight: 600;
    border: none;
    transition: all 0.25s ease;
}
.stButton>button:hover {
    box-shadow: 0 6px 18px rgba(2,132,199,0.35);
    transform: translateY(-1px);
}

/* INPUTS */
.stTextInput input,
.stNumberInput input {
    background: white !important;
    border-radius: 10px !important;
    border: 1.5px solid #bae6fd !important;
    padding: 10px !important;
    color: #0f172a !important;
}

/* LABEL FIX */
label,
.stTextInput label,
.stNumberInput label {
    color: #0f172a !important;
    font-weight: 600 !important;
}

/* METRIC FIX */
[data-testid="stMetric"] {
    background: white !important;
    border: 1px solid #e0f2fe !important;
    padding: 16px !important;
    border-radius: 14px !important;
}
[data-testid="stMetricValue"] {
    color: #0f172a !important;
    font-weight: 800 !important;
    font-size: 30px !important;
}
[data-testid="stMetricLabel"] {
    color: #334155 !important;
    font-weight: 600 !important;
}

/* LOADER */
.custom-loader {
    width: 48px;
    height: 48px;
    border: 5px solid #bae6fd;
    border-top: 5px solid #0284c7;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
    margin: 10px auto;
}
@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

</style>
""", unsafe_allow_html=True)

# -------------------- TITLE --------------------
st.markdown("""
<h1 style='text-align:center;color:#075985;font-weight:700;letter-spacing:1px;'>
🏦 HDFC BANK
</h1>
<p style='text-align:center;color:#0369a1;'>
Digital Banking Dashboard
</p>
""", unsafe_allow_html=True)

# -------------------- TOP BANNER --------------------
st.markdown("""
<div style="
background: linear-gradient(135deg,#075985,#0284c7);
padding:18px 24px;
border-radius:14px;
color:white;
margin: 10px 0 25px 0;
box-shadow: 0 8px 20px rgba(2,132,199,0.25);
">
<b>Welcome to HDFC Bank</b><br>
Manage accounts, deposits, withdrawals and track your digital banking securely.
</div>
""", unsafe_allow_html=True)

# -------------------- DATABASE --------------------
conn = sqlite3.connect("bank.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS accounts(
account_no TEXT PRIMARY KEY,
name TEXT,
age INTEGER,
phone TEXT,
email TEXT,
pin TEXT,
balance REAL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions(
id INTEGER PRIMARY KEY AUTOINCREMENT,
account_no TEXT,
type TEXT,
amount REAL,
time TEXT
)
""")
conn.commit()

# -------------------- HELPERS --------------------
def generate_acc():
    return "".join(random.choices(string.digits + string.ascii_letters, k=8))

def show_loader(msg="Processing..."):
    with st.spinner(msg):
        st.markdown('<div class="custom-loader"></div>', unsafe_allow_html=True)
        time.sleep(1)

def get_balance(acc):
    cursor.execute("SELECT balance FROM accounts WHERE account_no=?", (acc,))
    row = cursor.fetchone()
    return row[0] if row else 0.0

def fraud_check(acc, amount):
    cursor.execute(
        "SELECT amount, time FROM transactions WHERE account_no=? ORDER BY id DESC LIMIT 5",
        (acc,),
    )
    rows = cursor.fetchall()

    # large transaction warning
    if amount >= 50000:
        return "⚠️ Large transaction detected"

    # rapid transactions warning
    if len(rows) >= 3:
        try:
            t1 = datetime.strptime(rows[0][1], "%Y-%m-%d %H:%M:%S")
            t3 = datetime.strptime(rows[-1][1], "%Y-%m-%d %H:%M:%S")
            if (t1 - t3) < timedelta(minutes=2):
                return "⚠️ Too many transactions quickly"
        except:
            pass

    return None

def log_transaction(acc, ttype, amount):
    cursor.execute(
        "INSERT INTO transactions(account_no, type, amount, time) VALUES (?, ?, ?, ?)",
        (
            acc,
            ttype,
            float(amount),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        ),
    )
    conn.commit()

# -------------------- LOGIN --------------------
st.sidebar.markdown("## 🔐 Login")
login_acc = st.sidebar.text_input("Account No")
login_pin = st.sidebar.text_input("PIN", type="password")

if st.sidebar.button("Login"):
    show_loader("Authenticating...")
    cursor.execute("SELECT * FROM accounts WHERE account_no=? AND pin=?",
                   (login_acc, login_pin))
    if cursor.fetchone():
        st.session_state["user"] = login_acc
        st.sidebar.success("✅ Logged in")
    else:
        st.sidebar.error("❌ Invalid")

# -------------------- MENU --------------------
menu = st.sidebar.selectbox(
    "📌 Select Option",
    ["Create Account","Deposit Money","Withdraw Money",
     "Check Details","Update Details","Delete Account","Admin Panel"]
)

# -------------------- CREATE --------------------
if menu == "Create Account":
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("🆕 Create Account")

    with st.form("create"):
        name = st.text_input("Name")
        age = st.number_input("Age", step=1)
        phone = st.text_input("Phone")
        email = st.text_input("Email")
        pin = st.text_input("PIN", type="password")
        sub = st.form_submit_button("Create")

        if sub:
            show_loader("Creating account...")
            if age > 18 and len(pin) == 4 and len(phone) == 10:
                acc = generate_acc()
                cursor.execute(
                    "INSERT INTO accounts VALUES(?,?,?,?,?,?,?)",
                    (acc, name, age, phone, email, pin, 0),
                )
                conn.commit()
                st.success("✅ Account Created")
                st.info(f"Account No: {acc}")
            else:
                st.error("❌ Invalid details")

    st.markdown("</div>", unsafe_allow_html=True)

# -------------------- DEPOSIT --------------------
elif menu == "Deposit Money":
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("💰 Deposit Money")

    acc = st.text_input("Account")
    pin = st.text_input("PIN", type="password")
    amount = st.number_input("Amount", step=1)

    if st.button("Deposit"):
        cursor.execute(
            "SELECT * FROM accounts WHERE account_no=? AND pin=?",
            (acc, pin),
        )
        user = cursor.fetchone()

        if not user:
            st.error("❌ User not found")
        else:
            warning = fraud_check(acc, amount)
            if warning:
                st.warning(warning)

            new_bal = user[-1] + amount
            cursor.execute(
                "UPDATE accounts SET balance=? WHERE account_no=?",
                (new_bal, acc),
            )
            conn.commit()
            log_transaction(acc, "DEPOSIT", amount)
            st.success("✅ Amount Credited")

    st.markdown("</div>", unsafe_allow_html=True)

# -------------------- WITHDRAW --------------------
elif menu == "Withdraw Money":
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("🏧 Withdraw Money")

    acc = st.text_input("Account")
    pin = st.text_input("PIN", type="password")
    amount = st.number_input("Amount", step=1)

    if st.button("Withdraw"):
        cursor.execute(
            "SELECT * FROM accounts WHERE account_no=? AND pin=?",
            (acc, pin),
        )
        user = cursor.fetchone()

        if not user:
            st.error("❌ User not found")
        elif user[-1] < amount:
            st.error("❌ Insufficient funds")
        else:
            warning = fraud_check(acc, amount)
            if warning:
                st.warning(warning)

            new_bal = user[-1] - amount
            cursor.execute(
                "UPDATE accounts SET balance=? WHERE account_no=?",
                (new_bal, acc),
            )
            conn.commit()
            log_transaction(acc, "WITHDRAW", amount)
            st.success("✅ Amount Debited")

    st.markdown("</div>", unsafe_allow_html=True)

# -------------------- CHECK --------------------
elif menu == "Check Details":
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("📄 Account Details")

    acc = st.text_input("Account")
    pin = st.text_input("PIN", type="password")

    if st.button("Show"):
        df = pd.read_sql_query(
            "SELECT * FROM accounts WHERE account_no=? AND pin=?",
            conn,
            params=(acc, pin),
        )
        if df.empty:
            st.error("❌ User not found")
        else:
            st.dataframe(df)

    st.markdown("</div>", unsafe_allow_html=True)

# -------------------- UPDATE --------------------
elif menu == "Update Details":
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("✏️ Update Details")

    acc = st.text_input("Account")
    pin = st.text_input("PIN", type="password")

    if st.button("Fetch"):
        df = pd.read_sql_query(
            "SELECT * FROM accounts WHERE account_no=? AND pin=?",
            conn,
            params=(acc, pin),
        )
        if df.empty:
            st.error("❌ User not found")
        else:
            st.session_state["edit"] = df.iloc[0]

    if "edit" in st.session_state:
        u = st.session_state["edit"]
        name = st.text_input("Name", u["name"])
        age = st.number_input("Age", value=int(u["age"]))
        phone = st.text_input("Phone", u["phone"])
        email = st.text_input("Email", u["email"])
        new_pin = st.text_input("New PIN", u["pin"], type="password")

        if st.button("Update"):
            cursor.execute(
                """UPDATE accounts
                   SET name=?, age=?, phone=?, email=?, pin=?
                   WHERE account_no=?""",
                (name, age, phone, email, new_pin, acc),
            )
            conn.commit()
            st.success("✅ Updated")
            del st.session_state["edit"]

    st.markdown("</div>", unsafe_allow_html=True)

# -------------------- DELETE --------------------
elif menu == "Delete Account":
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("🗑 Delete Account")

    acc = st.text_input("Account")
    pin = st.text_input("PIN", type="password")

    if st.button("Delete"):
        cursor.execute(
            "DELETE FROM accounts WHERE account_no=? AND pin=?",
            (acc, pin),
        )
        conn.commit()
        st.success("✅ Account Deleted")

    st.markdown("</div>", unsafe_allow_html=True)

# -------------------- ADMIN --------------------
elif menu == "Admin Panel":
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("👨‍💼 Admin Panel")

    df1 = pd.read_sql_query("SELECT * FROM accounts", conn)
    df2 = pd.read_sql_query("SELECT * FROM transactions", conn)

    c1, c2 = st.columns(2)
    with c1:
        st.metric("👥 Accounts", len(df1))
    with c2:
        st.metric("💰 Bank Money", df1["balance"].sum() if not df1.empty else 0)

    st.dataframe(df1, use_container_width=True)
    st.dataframe(df2, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)