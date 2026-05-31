import streamlit as st
from pathlib import Path
import json
import os

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="File Management System",
    page_icon="📂",
    layout="wide"
)

# ---------------- Styling ----------------
st.markdown(
    """
    <style>
    .main {background-color: #f5f7fb;}
    h1 {color: #4f46e5;}
    h2 {color: #16a34a;}
    .stButton>button {
        background-color: #4f46e5;
        color: white;
        border-radius: 8px;
        height: 45px;
        width: 100%;
        font-size: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- Data ----------------
DB_FILE = "data.json"
if Path(DB_FILE).exists():
    users = json.loads(Path(DB_FILE).read_text())
else:
    users = []

# ---------------- Helper ----------------
def save_users():
    Path(DB_FILE).write_text(json.dumps(users, indent=4))

# ---------------- Session ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None

# ---------------- Login / Register ----------------
st.title("📁 File Management System")

if not st.session_state.logged_in:
    st.subheader("🔐 Login or Create Account")
    tab1, tab2 = st.tabs(["Existing User", "New User"])

    with tab1:
        email = st.text_input("Email")
        pin = st.text_input("4-digit PIN", type="password")
        if st.button("Login"):
            user = next((u for u in users if u["email"] == email and u["pin"] == pin), None)
            if user:
                st.session_state.logged_in = True
                st.session_state.user = user
                st.balloons()
                st.rerun()
            else:
                st.error("Invalid credentials")

    with tab2:
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=1)
        phone = st.text_input("Phone Number")
        email_n = st.text_input("Email", key="new_email")
        pin_n = st.text_input("Create 4-digit PIN", type="password")

        if st.button("Create Account"):
            if len(pin_n) == 4 and len(phone) == 10:
                users.append({
                    "name": name,
                    "age": age,
                    "phoneno": phone,
                    "email": email_n,
                    "pin": pin_n
                })
                save_users()
                st.success("Account created successfully 🎉")
                st.balloons()
            else:
                st.error("Invalid phone number or PIN")

# ---------------- Main App ----------------
else:
    user = st.session_state.user
    st.success(f"👋 Hello {user['name']}! Welcome back")

    menu = st.sidebar.radio("Choose Action", [
        "Create Folder", "List Files & Folders", "Rename Folder",
        "Delete Folder", "Create File", "Read File",
        "Update File", "Delete File"
    ])

    base = Path(".")

    if menu == "Create Folder":
        fname = st.text_input("Folder Name")
        if st.button("Create Folder"):
            p = Path(fname)
            if not p.exists():
                p.mkdir()
                st.success("Folder created 🎉")
                st.balloons()
            else:
                st.error("Folder already exists")

    elif menu == "List Files & Folders":
        st.subheader("📄 Files & Folders")
        for i, item in enumerate(base.rglob("*")):
            if ".git" not in str(item):
                st.write(f"{i+1}. {item}")

    elif menu == "Rename Folder":
        old = st.text_input("Old Folder Name")
        new = st.text_input("New Folder Name")
        if st.button("Rename"):
            if Path(old).exists() and not Path(new).exists():
                Path(old).rename(new)
                st.success("Folder renamed 🎉")
            else:
                st.error("Invalid folder name")

    elif menu == "Delete Folder":
        dname = st.text_input("Folder Name")
        if st.button("Delete"):
            p = Path(dname)
            if p.exists() and p.is_dir():
                try:
                    p.rmdir()
                    st.success("Folder deleted 🗑️")
                except:
                    st.error("Folder not empty")

    elif menu == "Create File":
        fname = st.text_input("File Name")
        content = st.text_area("File Content")
        if st.button("Create File"):
            if not Path(fname).exists():
                Path(fname).write_text(content)
                st.success("File created 🎉")
                st.balloons()

    elif menu == "Read File":
        fname = st.text_input("File Name")
        if st.button("Read"):
            if Path(fname).exists():
                st.text_area("Content", Path(fname).read_text(), height=200)

    elif menu == "Update File":
        fname = st.text_input("File Name")
        newdata = st.text_area("New Content")
        if st.button("Overwrite"):
            if Path(fname).exists():
                Path(fname).write_text(newdata)
                st.success("File updated")

    elif menu == "Delete File":
        fname = st.text_input("File Name")
        if st.button("Delete"):
            if Path(fname).exists():
                os.remove(fname)
                st.success("File deleted 🗑️")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.rerun()