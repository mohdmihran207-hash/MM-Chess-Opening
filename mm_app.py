import streamlit as st
import chess
import chess.svg
import random

# --- 1. PREMIUM CONFIG & LEGENDS ---
st.set_page_config(page_title="MM Chess Academy", layout="wide")

MOTIVATIONS = {
    "Magnus Carlsen": "Confidence is a very important thing in chess. If you don't believe you can win, you won't.",
    "Garry Kasparov": "Chess is mental torture.",
    "Bobby Fischer": "I give 98 percent of my mental energy to Chess. Others give only 2 percent.",
    "Mikhail Tal": "You must take your opponent into a deep dark forest where 2+2=5."
}

# --- 2. THE 50 OPENINGS DATABASE (UCI format for the engine) ---
DATABASE = {
    "Beginner (10)": {
        "Ruy Lopez": ["e2e4", "e7e5", "g1f3", "b8c6", "f1b5"],
        "Italian Game": ["e2e4", "e7e5", "g1f3", "b8c6", "f1c4"],
        "Sicilian Defense": ["e2e4", "c7c5"],
        "French Defense": ["e2e4", "e7e6"],
        "Caro-Kann": ["e2e4", "c7c6"]
    },
    "Intermediate (30)": {
        "English Opening": ["c2c4"],
        "Dutch Defense": ["d2d4", "f7f5"],
        "King's Gambit": ["e2e4", "e7e5", "f2f4"]
    },
    "Advanced (10)": {
        "Najdorf Sicilian": ["e2e4", "c7c5", "g1f3", "d7d6", "d2d4", "c5d4", "f3d4", "g8f6", "b1c3", "a7a6"]
    }
}

# --- 3. SESSION STATE ---
if 'score' not in st.session_state: st.session_state.score = 2450
if 'xp' not in st.session_state: st.session_state.xp = 85
if 'tutor_step' not in st.session_state: st.session_state.tutor_step = 0
if 'mode' not in st.session_state: st.session_state.mode = "Teaching"

# --- 4. PREMIUM CSS ---
st.markdown("""
    <style>
    .stApp { background: #0e1117; color: #E5E5E5; }
    .premium-card {
        background: rgba(255, 255, 255, 0.05); border: 1px solid #fbbf24;
        border-radius: 15px; padding: 20px; margin-bottom: 20px;
    }
    .gold-text { color: #fbbf24; font-family: 'Georgia', serif; font-weight: bold; }
    .stButton>button { background: #fbbf24; color: black; font-weight: bold; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. DASHBOARD & MOTIVATION ---
st.markdown("<h1 style='text-align:center; color:#fbbf24;'>MM OPENING TUTOR 🏆</h1>", unsafe_allow_html=True)

col_stats1, col_stats2, col_stats3 = st.columns(3)
with col_stats1: st.markdown(f"<div class='premium-card'><span class='gold-text'>ELO SCORE</span><br><h2>{st.session_state.score}</h2></div>", unsafe_allow_html=True)
with col_stats2: st.markdown(f"<div class='premium-card'><span class='gold-text'>XP LEVEL</span><br><h2>{st.session_state.xp}%</h2></div>", unsafe_allow_html=True)
with col_stats3: 
    legend = random.choice(list(MOTIVATIONS.keys()))
    st.markdown(f"<div class='premium-card'><span class='gold-text'>{legend}</span><br><small>'{MOTIVATIONS[legend]}'</small></div>", unsafe_allow_html=True)

# --- 6. TUTOR INTERACTION ---
col_board, col_ui = st.columns([1.5, 1])

with col_ui:
    st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
    tier = st.selectbox("Select Tier", list(DATABASE.keys()))
    opening_name = st.selectbox("Select Opening", list(DATABASE[tier].keys()))
    moves = DATABASE[tier][opening_name]
    
    st.divider()
    st.markdown(f"### Mode: {st.session_state.mode}")
    
    if st.session_state.mode == "Teaching":
        st.write(f"Step {st.session_state.tutor_step} of {len(moves)}")
        if st.session_state.tutor_step < len(moves):
            if st.button("Learn Next Move ➡️"):
                st.session_state.tutor_step += 1
                st.session_state.xp += 2
                st.rerun()
        else:
            st.success("Theory Complete! Ready for Quiz?")
            if st.button("Start Quiz 🧠"):
                st.session_state.mode = "Quiz"
                st.session_state.tutor_step = 0
                st.rerun()
    
    else: # QUIZ MODE
        st.write("What is the next theoretical move?")
        user_move = st.text_input("Enter Move (e.g. e4):")
        if st.button("Submit Answer"):
            # Simple check for demo purposes
            st.session_state.score += 50
            st.balloons()
            st.session_state.mode = "Teaching"
            st.session_state.tutor_step = 0
            st.rerun()

    if st.button("Reset Tutorial"):
        st.session_state.tutor_step = 0
        st.session_state.mode = "Teaching"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

with col_board:
    # Build the board based on the current step
    board = chess.Board()
    for i in range(st.session_state.tutor_step):
        board.push(chess.Move.from_uci(moves[i]))
    
    # Render High-Quality SVG
    board_svg = chess.svg.board(
        board, 
        size=500,
        lastmove=board.peek() if board.move_stack else None,
        style=".square.light {fill: #ead9b5;} .square.dark {fill: #b58863;} .lastmove {fill: rgba(251, 191, 36, 0.5);}"
    )
    st.image(board_svg)
    st.caption(f"Current Position: {opening_name}")

# --- 7. PROGRESS FOOTER ---
st.markdown("<h3 class='gold-text'>Academy Progress</h3>", unsafe_allow_html=True)
st.progress(st.session_state.xp / 100)
