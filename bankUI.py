import streamlit as st
from pathlib import Path
import json
import random
import string

# -------------------- BANK CLASS --------------------
class Bank:
    database = "data.json"
    data = []

    # Load data
    if Path(database).exists():
        with open(database) as fs:
            data = json.loads(fs.read())

    @classmethod
    def update(cls):
        with open(cls.database, "w") as fs:
            fs.write(json.dumps(cls.data, indent=4))

    @staticmethod
    def generateAcc():
        digits = random.choices(string.digits, k=4)
        alpha = random.choices(string.ascii_letters, k=4)
        acc = digits + alpha
        random.shuffle(acc)
        return "".join(acc)

# -------------------- STREAMLIT UI --------------------

st.set_page_config(
    page_title="🏦 Himanshu Bank",
    page_icon="🏦",
    layout="centered"
)

st.title("🏦 Himanshu Bank Management System")
st.markdown("---")

menu = st.sidebar.selectbox(
    "📌 Select Option",
    [
        "Create Account",
        "Deposit Money",
        "Withdraw Money",
        "Check Details",
        "Update Details",
        "Delete Account",
    ],
)

bank = Bank()

# -------------------- CREATE ACCOUNT --------------------
if menu == "Create Account":
    st.subheader("🆕 Create New Account")

    with st.form("create_form"):
        name = st.text_input("Name")
        age = st.number_input("Age", step=1)
        phone = st.text_input("Phone Number")
        email = st.text_input("Email")
        pin = st.text_input("4 Digit PIN", type="password")

        submitted = st.form_submit_button("Create Account")

        if submitted:
            if (
                age > 18
                and len(pin) == 4
                and len(phone) == 10
            ):
                info = {
                    "name": name,
                    "age": age,
                    "Phonenumber": int(phone),
                    "Email": email,
                    "Pin": int(pin),
                    "Account.no": Bank.generateAcc(),
                    "Balance": 0,
                }

                Bank.data.append(info)
                Bank.update()

                st.success("✅ Account Created Successfully!")
                st.info(f"🆔 Your Account Number: {info['Account.no']}")
            else:
                st.error("❌ Invalid Details")

# -------------------- DEPOSIT --------------------
elif menu == "Deposit Money":
    st.subheader("💰 Deposit Money")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    amount = st.number_input("Amount", step=1)

    if st.button("Deposit"):
        user = [i for i in Bank.data if i["Account.no"] == acc and str(i["Pin"]) == pin]

        if not user:
            st.error("❌ User Not Found")
        else:
            if amount <= 0:
                st.error("Invalid Amount")
            else:
                user[0]["Balance"] += amount
                Bank.update()
                st.success("✅ Amount Credited")

# -------------------- WITHDRAW --------------------
elif menu == "Withdraw Money":
    st.subheader("🏧 Withdraw Money")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    amount = st.number_input("Amount", step=1)

    if st.button("Withdraw"):
        user = [i for i in Bank.data if i["Account.no"] == acc and str(i["Pin"]) == pin]

        if not user:
            st.error("❌ User Not Found")
        else:
            if user[0]["Balance"] < amount:
                st.error("❌ Insufficient Funds")
            else:
                user[0]["Balance"] -= amount
                Bank.update()
                st.success("✅ Amount Debited")

# -------------------- DETAILS --------------------
# -------------------- CHECK DETAILS --------------------
elif menu == "Check Details":
    st.subheader("📄 Account Details")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")

    if st.button("Show Details"):
        user = [i for i in Bank.data if i["Account.no"] == acc and str(i["Pin"]) == pin]

        if not user:
            st.error("❌ User Not Found")
        else:
            st.success("✅ Account Found")
            st.json(user[0])
            
# -------------------- UPDATE DETAILS --------------------
elif menu == "Update Details":
    st.subheader("✏️ Update Account Details")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")

    user = None
    if st.button("Fetch Details"):
        found = [i for i in Bank.data if i["Account.no"] == acc and str(i["Pin"]) == pin]
        if not found:
            st.error("❌ User Not Found")
        else:
            user = found[0]
            st.session_state["update_user"] = user
            st.success("✅ User Found")

    # ---------- show form after fetch ----------
    if "update_user" in st.session_state:
        user = st.session_state["update_user"]

        with st.form("update_form"):
            name = st.text_input("Name", value=user["name"])
            age = st.number_input("Age", value=int(user["age"]), step=1)
            phone = st.text_input("Phone", value=str(user["Phonenumber"]))
            email = st.text_input("Email", value=user["Email"])
            new_pin = st.text_input("New PIN", value=str(user["Pin"]), type="password")

            submitted = st.form_submit_button("Update Details")

            if submitted:
                if len(str(new_pin)) != 4 or len(phone) != 10:
                    st.error("❌ Invalid phone or PIN")
                else:
                    user["name"] = name
                    user["age"] = age
                    user["Phonenumber"] = int(phone)
                    user["Email"] = email
                    user["Pin"] = int(new_pin)

                    Bank.update()
                    st.success("✅ Details Updated Successfully")
                    del st.session_state["update_user"]

# -------------------- DELETE --------------------
elif menu == "Delete Account":
    st.subheader("🗑 Delete Account")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")

    if st.button("Delete"):
        user = [i for i in Bank.data if i["Account.no"] == acc and str(i["Pin"]) == pin]

        if not user:
            st.error("❌ User Not Found")
        else:
            Bank.data.remove(user[0])
            Bank.update()
            st.success("✅ Account Deleted")