import streamlit as st
import chess
import chess.svg

# 1. Premium Look (Custom CSS)
st.set_page_config(page_title="MM Chess Pro", page_icon="🏆", layout="wide")

st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
        color: #fafafa;
    }
    .stMetric {
        background-color: #1f2937;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #4b5563;
    }
    h1 {
        color: #fbbf24; /* Gold Color */
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("MM: Elite Chess Academy")

# 2. Motivation & Progress Header
col_a, col_b, col_c = st.columns(3)

with col_a:
    st.metric(label="Motivation", value="100%", delta="Keep Pushing!")
    st.write("*'Every master was once a beginner.'*")

with col_b:
    # We will make this dynamic later
    st.metric(label="Progress", value="15%", delta="3% today")

with col_c:
    st.metric(label="Completed Portions", value="2 / 40")

st.divider()

# 3. The Opening Library (Sidebar Navigation)
st.sidebar.title("📚 Opening Library")

category = st.sidebar.selectbox("Choose Your Level", ["Beginner (5)", "Intermediate (15)", "Advanced (5)"])
color_choice = st.sidebar.radio("Side", ["White", "Black"])

# This is where we will list your 20 + 20 openings
openings = {
    "Beginner (5)": ["Italian Game", "Ruy Lopez", "Sicilian Defense", "French Defense", "Queen's Gambit"],
    "Intermediate (15)": ["King's Indian", "Caro-Kann", "Scandinavian", "London System", "...and more"],
    "Advanced (5)": ["Grunfeld", "Najdorf Sicilian", "Berlin Defense", "...and more"]
}

selected_opening = st.sidebar.selectbox("Select Opening", openings[category])

# 4. The Board Area
col1, col2 = st.columns([2, 1])

if 'board' not in st.session_state:
    st.session_state.board = chess.Board()

with col1:
    st.subheader(f"Current Study: {selected_opening}")
    board_svg = chess.svg.board(st.session_state.board, size=450)
    st.image(board_svg)

with col2:
    st.write("### Variation Selector")
    # We will build the 6 variations per opening here
    variation = st.selectbox("Choose Variation", ["Main Line", "Exchange", "Attack", "Gambit", "Solid", "Modern"])
    
    st.info(f"Studying {selected_opening}: {variation}")
    
    if st.button("Reset Position"):
        st.session_state.board.reset()
        st.rerun()
