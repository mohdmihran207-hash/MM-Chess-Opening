import streamlit as st
import chess
import chess.svg
import random

# --- 1. PREMIUM CONFIG ---
st.set_page_config(page_title="MM Chess Academy", layout="wide", page_icon="🏆")

# --- 2. DEEP THEORY DATABASE (The "Why") ---
DATABASE = {
    "Beginner (10)": {
        "Ruy Lopez": {
            "moves": ["e2e4", "e7e5", "g1f3", "b8c6", "f1b5"],
            "logic": [
                "Control the center and open lines for the Queen and Bishop.",
                "Black claims their share of the center, staying symmetrical.",
                "Developing the Knight to attack e5 and prepare kingside castling.",
                "Defending the e5 pawn while developing a piece. Standard response.",
                "The 'Spanish' move. Putting pressure on the defender of e5 to control the game."
            ],
            "legend": "Magnus Carlsen: 'The Ruy Lopez is a test of your deep understanding of chess.'"
        },
        "Italian Game": {
            "moves": ["e2e4", "e7e5", "g1f3", "b8c6", "f1c4"],
            "logic": [
                "Classic King's Pawn opening.",
                "Symmetrical response.",
                "Pressure on e5.",
                "Standard defense.",
                "Targeting the weak f7 square—the only square defended only by the King!"
            ],
            "legend": "Garry Kasparov: 'The Italian Game is full of tactical traps if you aren't careful.'"
        }
    }
}

# --- 3. SESSION STATE ---
if 'score' not in st.session_state: st.session_state.score = 2450
if 'xp' not in st.session_state: st.session_state.xp = 85
if 'tutor_step' not in st.session_state: st.session_state.tutor_step = 0
if 'mode' not in st.session_state: st.session_state.mode = "Teaching"
if 'feedback' not in st.session_state: st.session_state.feedback = "neutral"

# --- 4. PREMIUM CSS ---
st.markdown("""
    <style>
    .stApp { background: #0e1117; color: #E5E5E5; }
    .premium-card {
        background: rgba(255, 255, 255, 0.05); border: 1px solid #fbbf24;
        border-radius: 15px; padding: 20px; margin-bottom: 20px;
    }
    .gold-text { color: #fbbf24; font-weight: bold; font-family: 'Georgia', serif; }
    .strategy-box { background: rgba(251, 191, 36, 0.1); border-left: 5px solid #fbbf24; padding: 15px; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. TOP PANEL ---
st.markdown("<h1 style='text-align:center; color:#fbbf24;'>MM ACADEMY: STRATEGY TUTOR 🚀</h1>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1: st.markdown(f"<div class='premium-card'><span class='gold-text'>ELO SCORE</span><br><h2>{st.session_state.score}</h2></div>", unsafe_allow_html=True)
with c2: st.markdown(f"<div class='premium-card'><span class='gold-text'>ACADEMY XP</span><br><h2>{st.session_state.xp}%</h2></div>", unsafe_allow_html=True)
with c3: st.markdown(f"<div class='premium-card'><span class='gold-text'>ENGINE</span><br><h2>STOCKFISH 16</h2></div>", unsafe_allow_html=True)

# --- 6. CORE LOGIC ---
tier = st.sidebar.selectbox("Skill Tier", list(DATABASE.keys()))
opening_name = st.sidebar.selectbox("Opening", list(DATABASE[tier].keys()))
data = DATABASE[tier][opening_name]
moves = data["moves"]
logics = data["logic"]

# Build board up to current step
board = chess.Board()
for i in range(st.session_state.tutor_step):
    try: board.push(chess.Move.from_uci(moves[i]))
    except: pass

col_board, col_ui = st.columns([1.8, 1])

with col_ui:
    st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
    st.markdown(f"### Mode: {st.session_state.mode}")
    
    if st.session_state.mode == "Teaching":
        st.write(f"Step: {st.session_state.tutor_step} / {len(moves)}")
        if st.button("Learn Next Move ➡️"):
            if st.session_state.tutor_step < len(moves):
                st.session_state.tutor_step += 1
                st.session_state.feedback = "neutral"
                st.rerun()
        
        if st.button("Switch to Quiz Mode 🧠"):
            st.session_state.mode = "Quiz"
            st.session_state.tutor_step = 0
            st.rerun()

    else: # QUIZ MODE
        st.info("🎯 Move the Piece by selecting squares:")
        squares = [chess.square_name(s) for s in range(64)]
        from_sq = st.selectbox("From:", ["--"] + squares)
        to_sq = st.selectbox("To:", ["--"] + squares)
        
        if st.button("Confirm Move"):
            if from_sq != "--" and to_sq != "--":
                user_move = f"{from_sq}{to_sq}"
                if user_move == moves[st.session_state.tutor_step]:
                    st.session_state.feedback = "correct"
                    st.session_state.tutor_step += 1
                    st.session_state.score += 20
                    if st.session_state.tutor_step == len(moves):
                        st.balloons()
                        st.session_state.mode = "Teaching"
                else:
                    st.session_state.feedback = "wrong"
                st.rerun()

    if st.button("Reset Opening"):
        st.session_state.tutor_step = 0
        st.session_state.feedback = "neutral"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # DEEP WHY ANALYSIS
    if st.session_state.tutor_step > 0:
        st.markdown("<div class='strategy-box'>", unsafe_allow_html=True)
        st.markdown(f"<span class='gold-text'>Why this move?</span><br>{logics[st.session_state.tutor_step-1]}", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        st.caption(data["legend"])

with col_board:
    # Set Dynamic Colors
    l_col = "#90EE90" if st.session_state.feedback == "correct" else "#FFB6C1" if st.session_state.feedback == "wrong" else "#ead9b5"
    d_col = "#2E8B57" if st.session_state.feedback == "correct" else "#8B0000" if st.session_state.feedback == "wrong" else "#b58863"
    
    board_svg = chess.svg.board(
        board, 
        size=600,
        lastmove=board.peek() if board.move_stack else None,
        style=f".square.light {{fill: {l_col};}} .square.dark {{fill: {d_col};}} .lastmove {{fill: rgba(251, 191, 36, 0.4);}}"
    )
    st.image(board_svg)
