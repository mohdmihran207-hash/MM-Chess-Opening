import streamlit as st
import chess
import chess.svg

# --- PAGE CONFIG & PREMIUM CSS ---
st.set_page_config(page_title="MM Chess Academy", layout="wide")
st.markdown("""
    <style>
    .stApp { background: #0a0a0a; color: #d4af37; } /* Black & Gold */
    .premium-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid #d4af37;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- THE OPENING DATABASE ---
# Format: "Opening Name": ["Variation 1 Moves", "Variation 2 Moves", ...]
WHITE_OPENINGS = {
    "Beginner": {
        "Italian Game": ["e4 e5 Nf3 Nc6 Bc4", "e4 e5 Nf3 Nc6 Bc4 Bc5", "e4 e5 Nf3 Nc6 Bc4 Nf6"],
        "Ruy Lopez": ["e4 e5 Nf3 Nc6 Bb5", "e4 e5 Nf3 Nc6 Bb5 a6", "e4 e5 Nf3 Nc6 Bb5 Nf6"],
        # Add 3 more for total 5 Beginner
    },
    "Intermediate": {
        "Sicilian: Alapin": ["e4 c5 c3", "e4 c5 c3 d5", "e4 c5 c3 Nf6"],
        "Queen's Gambit": ["d4 d5 c4", "d4 d5 c4 e6", "d4 d5 c4 dxc4"],
        # Add 13 more for total 15 Intermediate
    },
    "Advanced": {
        "Catalan": ["d4 Nf6 c4 e6 g3", "d4 d5 c4 e6 Nf3 Nf6 g3"],
        # Add 4 more for total 5 Advanced
    }
}

# --- APP LAYOUT ---
st.title("🏆 MM CHESS ACADEMY")

# Motivation & Progress Card
st.markdown(f"""
<div class="premium-card">
    <h3>Future Grandmaster Progress</h3>
    <p><b>Motivation:</b> 100% 🔥 | <b>Portions Completed:</b> 2 / 40</p>
</div>
""", unsafe_allow_html=True)

# Sidebar Selectors
st.sidebar.header("Select Your Path")
side = st.sidebar.radio("I want to learn for:", ["White", "Black"])
level = st.sidebar.selectbox("Difficulty", ["Beginner", "Intermediate", "Advanced"])

# Get the list of openings based on choice
current_db = WHITE_OPENINGS[level] # We'll add BLACK_OPENINGS next
opening_name = st.sidebar.selectbox("Select Opening", list(current_db.keys()))
variation_list = current_db[opening_name]
selected_var = st.sidebar.selectbox("Select Variation", variation_list)

# --- BOARD LOGIC ---
if 'board' not in st.session_state:
    st.session_state.board = chess.Board()

# Function to play the variation moves
def play_variation(move_string):
    temp_board = chess.Board()
    for move in move_string.split():
        temp_board.push_san(move)
    return temp_board

st.session_state.board = play_variation(selected_var)

# Display Board
col1, col2 = st.columns([2, 1])
with col1:
    st.image(chess.svg.board(st.session_state.board, size=450))
with col2:
    st.success(f"Studying: {opening_name}")
    st.write(f"**Moves:** {selected_var}")
    if st.button("Reset to Start"):
        st.session_state.board.reset()
        st.rerun()
