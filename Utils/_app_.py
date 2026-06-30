import os
import sys
from dotenv import load_dotenv
import streamlit as st

# =========================
# LOAD ENV
# =========================

load_dotenv()

# =========================
# PROJECT PATH
# =========================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="Cricbuzz LiveStats Dashboard",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# IMPORT PAGES
# =========================

from pages import _home as home
from pages import _live_matches as live
from pages import _top_stats as stats
from pages import _sql_queries as sql
from pages import _crud_operations as crud

# =========================
# CUSTOM CSS
# =========================

st.markdown("""
<style>

/* Main App */
.stApp {
    background-color: #f8fafc;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #020c2b;
}

/* Sidebar Text */
section[data-testid="stSidebar"] * {
    color: white;
}

/* Remove Streamlit default pages */
[data-testid="stSidebarNav"] {
    display: none;
}

/* Radio Labels */
.stRadio label {
    font-size: 18px !important;
    font-weight: 500 !important;
}

/* Buttons */
.stButton > button {
    background-color: #16a34a;
    color: white;
    border-radius: 10px;
    border: none;
}

.stButton > button:hover {
    background-color: #15803d;
    color: white;
}

</style>
""", unsafe_allow_html=True)



# =========================
# CUSTOM NAVIGATION
# =========================

page = st.sidebar.radio(
    "📂 Go To",
    [
        "Home",
        "Live Matches",
        "Top Player Stats",
        "SQL Analytics",
        "CRUD Operations"
    ]
)

st.sidebar.markdown("---")

st.sidebar.success(
    "📊 Real-Time Cricket Analytics Dashboard"
)

# =========================
# PAGE ROUTING
# =========================

if page == "Home":
    home.show()

elif page == "Live Matches":
    live.show()

elif page == "Top Player Stats":
    stats.show()

elif page == "SQL Analytics":
    sql.show()

elif page == "CRUD Operations":
    crud.show()