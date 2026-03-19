import streamlit as st
import chess
import chess.svg

# --- PREMIUM STYLING ---
st.set_page_config(page_title="MM Chess Academy", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: #050505; /* Deep Black */
        color: #E5E5E5;
    }
    .opening-card {
        background: rgba(255, 215, 0, 0.05);
        border: 1px solid #D4AF37; /* Gold Border */
        border-radius: 12px;
        padding: 20px;
        transition: 0.3s;
        text-align: center;
        margin-bottom: 15px;
    }
    .opening-card:hover {
        background: rgba(255, 215, 0, 0.1);
        border-color: #FFD700;
        transform: translateY(-5px);
    }
    .gold-title { color: #D4AF37; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- APP HEADER ---
st.markdown("<h1 style='text-align: center; color: #D4AF37;'>MM CHESS ACADEMY</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Master the 40 Most Essential Openings</p>", unsafe_allow_html=True)

# --- SIDEBAR: NAV & PROGRESS ---
with st.sidebar:
    st.markdown("<h2 class='gold-title'>Your Stats</h2>", unsafe_allow_html=True)
    st.metric("Progress", "15%", "+2% Today")
    st.progress(0.15)
    
    st.divider()
    side = st.radio("Choose Side:", ["White (20 Openings)", "Black (20 Openings)"])
    level = st.selectbox("Difficulty:", ["Beginner", "Intermediate", "Advanced"])

# --- OPENING GRID ---
st.subheader(f"Top {level} Openings for {side}")

# Example logic for 1 of the 20 cards
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div class="opening-card">
            <h3 class="gold-title">The Ruy Lopez</h3>
            <p>6 Variations Available</p>
            <small>Success Rate: 54%</small>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Start Training: Ruy Lopez"):
        st.session_state.current_opening = "Ruy Lopez"

# --- THE TRAINING BOARD ---
st.divider()
col_board, col_info = st.columns([2, 1])

if 'board' not in st.session_state:
    st.session_state.board = chess.Board()

with col_board:
    # Customizable board colors (Gold/Dark theme)
    board_svg = chess.svg.board(st.session_state.board, size=450, style="""
        .square.light { fill: #2d2d2d; }
        .square.dark { fill: #1a1a1a; }
        .piece { filter: drop-shadow(2px 2px 2px black); }
    """)
    st.image(board_svg)

with col_info:
    st.markdown("<h3 class='gold-title'>Training Mode</h3>", unsafe_allow_html=True)
    st.info("Follow the 'Main Line' variation to continue.")
    move = st.text_input("Enter Move:")
    if st.button("Submit Move"):
        # Logic to check against the 6 variations
        pass
