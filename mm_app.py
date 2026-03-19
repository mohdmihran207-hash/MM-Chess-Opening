import streamlit as st
from streamlit_chess import st_chess
import chess

# --- 1. PREMIUM PAGE CONFIG ---
st.set_page_config(page_title="MM Chess Academy", layout="wide", page_icon="🏆")

# --- 2. THE MASTER DATABASE (Simplified for Move Testing) ---
# We use UCI format (e.g., e2e4) because the interactive board tracks square-to-square
OPENINGS = {
    "White": {
        "Beginner (5)": {
            "Ruy Lopez": ["e2e4", "e7e5", "g1f3", "b8c6", "f1b5"],
            "Italian Game": ["e2e4", "e7e5", "g1f3", "b8c6", "f1c4"]
        }
    }
}

# --- 3. SESSION STATE (The Memory) ---
if 'score' not in st.session_state: st.session_state.score = 240
if 'quiz_step' not in st.session_state: st.session_state.quiz_step = 0
if 'fen' not in st.session_state: st.session_state.fen = chess.STARTING_FEN
if 'board_status' not in st.session_state: st.session_state.board_status = "normal"

# --- 4. PREMIUM DESIGN (CSS) ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), 
                    url('https://images.unsplash.com/photo-1529699211952-734e80c4d42b?q=80&w=2000');
        background-size: cover; background-attachment: fixed; color: #E5E5E5;
    }
    .premium-card {
        background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(12px);
        border: 1px solid rgba(251, 191, 36, 0.3); border-radius: 15px; padding: 20px;
    }
    .gold-text { color: #fbbf24; font-weight: bold; }
    h1, h2 { color: #fbbf24; margin-bottom: 0px; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. DASHBOARD ---
st.markdown("<h1>MM Chess Academy 🚀</h1>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1: st.markdown(f"<div class='premium-card'><span class='gold-text'>Score</span><br><h2>{st.session_state.score}</h2></div>", unsafe_allow_html=True)
with c2: 
    mode = st.sidebar.selectbox("Select Mode", ["Learning Mode", "Quiz Mode"])
    st.markdown(f"<div class='premium-card'><span class='gold-text'>Mode</span><br><h2>{mode}</h2></div>", unsafe_allow_html=True)
with c3: st.markdown(f"<div class='premium-card'><span class='gold-text'>Progress</span><br><h2>{st.session_state.quiz_step}/5</h2></div>", unsafe_allow_html=True)

st.divider()

# --- 6. INTERACTIVE BOARD ---
col_ui, col_board = st.columns([1, 2])

with col_ui:
    selected_op = st.selectbox("Select Opening", list(OPENINGS["White"]["Beginner (5)"].keys()))
    target_moves = OPENINGS["White"]["Beginner (5)"][selected_op]
    
    if mode == "Quiz Mode":
        st.write("### 🧠 Quiz Time!")
        st.write("Move the piece on the board to the correct square.")
    else:
        st.write("### 📖 Study the Moves")
        st.write(f"Goal moves: {', '.join(target_moves)}")

    if st.button("Reset Everything"):
        st.session_state.fen = chess.STARTING_FEN
        st.session_state.quiz_step = 0
        st.session_state.board_status = "normal"
        st.rerun()

with col_board:
    # Set Theme based on correctness
    if st.session_state.board_status == "correct":
        # Light Green Theme
        theme = {"light": "#90EE90", "dark": "#2E8B57"}
    elif st.session_state.board_status == "wrong":
        # Light Red Theme
        theme = {"light": "#FFB6C1", "dark": "#8B0000"}
    else:
        # Gold/Wood Theme
        theme = {"light": "#c5a059", "dark": "#8b4513"}

    # The Live Moveable Board
    board_output = st_chess(
        fen=st.session_state.fen,
        key="mm_chess_board",
        board_style=theme
    )

    # Move Validation Logic
    if board_output and board_output.get("move"):
        user_move = board_output["move"]
        
        if mode == "Quiz Mode":
            # Check if this move is next in the opening sequence
            if st.session_state.quiz_step < len(target_moves):
                expected_move = target_moves[st.session_state.quiz_step]
                
                if user_move == expected_move:
                    st.session_state.board_status = "correct"
                    st.session_state.quiz_step += 1
                    st.session_state.score += 20
                    st.session_state.fen = board_output["fen"]
                    if st.session_state.quiz_step == len(target_moves):
                        st.balloons()
                else:
                    st.session_state.board_status = "wrong"
                    st.warning("That's not the right move for this opening! Try again.")
                
                st.rerun()
        else:
            # Free play / Learning mode
            st.session_state.fen = board_output["fen"]
