
import streamlit as st
from validators import validate_username, validate_password_strength, validate_passwords_match
from auth import signup_user, login_user, update_user, delete_user, username_exists

st.set_page_config(page_title="User Management System", page_icon="🔐")

# ------------------------------------------------
# Session state initialize karna (login track karne ke liye)
# ------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "page" not in st.session_state:
    st.session_state.page = "Login"


# ------------------------------------------------
# SIGNUP PAGE
# ------------------------------------------------
def signup_page():
    st.title("📝 Signup")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Retype Password", type="password")

    if st.button("Sign Up"):
        # Step 1: Username validation
        valid, msg = validate_username(username)
        if not valid:
            st.error(msg)
            return

        # Step 2: Username uniqueness check
        if username_exists(username):
            st.error("⚠️ Ye username already liya gaya hai. Doosra try karo.")
            return

        # Step 3: Password strength validation
        valid, msg = validate_password_strength(password)
        if not valid:
            st.error(msg)
            return

        # Step 4: Password match validation
        valid, msg = validate_passwords_match(password, confirm_password)
        if not valid:
            st.error(msg)
            return

        # Sab validations pass ho gaye -> database mein save karo
        success, msg = signup_user(username, password)
        if success:
            st.success(msg)
            st.info("👉 Ab Login page par jaake login karo.")
        else:
            st.error(msg)

    st.markdown("---")
    if st.button("Already have an account? Login here"):
        st.session_state.page = "Login"
        st.rerun()


# ------------------------------------------------
# LOGIN PAGE
# ------------------------------------------------
def login_page():
    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        success, msg = login_user(username, password)
        if success:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.page = "Welcome"
            st.success(msg)
            st.rerun()
        else:
            st.error(msg)

    st.markdown("---")
    if st.button("New user? Sign up here"):
        st.session_state.page = "Signup"
        st.rerun()


# ------------------------------------------------
# WELCOME PAGE (Update / Delete Account)
# ------------------------------------------------
def welcome_page():
    st.title(f"👋 Welcome, {st.session_state.username}!")
    st.write("Apna account manage karne ke liye neeche se option choose karo.")

    tab1, tab2 = st.tabs(["✏️ Update Account", "🗑️ Delete Account"])

    # ---- UPDATE ACCOUNT TAB ----
    with tab1:
        st.subheader("Update Account Details")
        st.caption("Sirf wahi field bharo jise update karna hai. Baaki blank chhod do.")

        new_username = st.text_input("New Username (optional)")
        new_password = st.text_input("New Password (optional)", type="password")
        confirm_new_password = st.text_input("Confirm New Password", type="password")

        if st.button("Update Account"):
            # Agar naya username diya hai to validate karo
            if new_username:
                valid, msg = validate_username(new_username)
                if not valid:
                    st.error(msg)
                    return
                if username_exists(new_username):
                    st.error("⚠️ Ye username already liya gaya hai.")
                    return

            # Agar naya password diya hai to validate karo
            if new_password:
                valid, msg = validate_password_strength(new_password)
                if not valid:
                    st.error(msg)
                    return
                valid, msg = validate_passwords_match(new_password, confirm_new_password)
                if not valid:
                    st.error(msg)
                    return

            if not new_username and not new_password:
                st.warning("⚠️ Kam se kam ek field update karne ke liye bharo.")
                return

            success, msg = update_user(
                st.session_state.username,
                new_username if new_username else None,
                new_password if new_password else None
            )
            if success:
                st.success(msg)
                if new_username:
                    st.session_state.username = new_username
            else:
                st.error(msg)

    # ---- DELETE ACCOUNT TAB ----
    with tab2:
        st.subheader("Delete Account")
        st.warning("⚠️ Ye action permanent hai aur wapas nahi ho sakta!")

        confirm = st.checkbox("Haan, main apna account delete karna chahta/chahti hoon.")

        if st.button("Delete My Account", disabled=not confirm):
            success, msg = delete_user(st.session_state.username)
            if success:
                st.success(msg)
                st.session_state.logged_in = False
                st.session_state.username = ""
                st.session_state.page = "Login"
                st.rerun()
            else:
                st.error(msg)

    st.markdown("---")
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.page = "Login"
        st.rerun()


# ------------------------------------------------
# PAGE ROUTING
# ------------------------------------------------
if st.session_state.logged_in:
    welcome_page()
else:
    if st.session_state.page == "Signup":
        signup_page()
    else:
        login_page()
