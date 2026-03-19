import streamlit as st
import chess
import chess.svg
import random

# --- 1. PREMIUM CONFIG ---
st.set_page_config(page_title="MM Chess Academy", layout="wide", page_icon="🏆")

# --- 2. SESSION STATE ---
if 'score' not in st.session_state: st.session_state.score = 2450
if 'xp' not in st.session_state: st.session_state.xp = 85
if 'tutor_step' not in st.session_state: st.session_state.tutor_step = 0
if 'mode' not in st.session_state: st.session_state.mode = "Teaching"
if 'feedback' not in st.session_state: st.session_state.feedback = "neutral"

# --- 3. THE 50 OPENINGS & COMMENTARY ---
# (I have structured the first few perfectly; you can keep adding to the list)
DATABASE = {
    "Beginner (10)": {
        "Ruy Lopez": {
            "moves": ["e2e4", "e7e5", "g1f3", "b8c6", "f1b5"],
            "notes": ["Magnus: Control the center immediately.", "Kasparov: Black matches the challenge.", "Fischer: Develop the Knight toward the center.", "Tal: Support the center and prepare for war.", "MM Academy: The 'Spanish Torture' begins by attacking the defender."]
        },
        "Italian Game": {
            "moves": ["e2e4", "e7e5", "g1f3", "b8c6", "f1c4"],
            "notes": ["Magnus: The classic e4 start.", "Kasparov: Solid response from Black.", "Fischer: Aiming for the heart of the board.", "Tal: Developing toward the center.", "MM Academy: Aiming at the weak f7 pawn early!"]
        }
    },
    "Intermediate (30)": {
        "King's Gambit": {
            "moves": ["e2e4", "e7e5", "f2f4"],
            "notes": ["Magnus: A bold choice.", "Kasparov: Challenging the center with fire.", "Tal: This is where the deep dark forest begins!"]
        }
    },
    "Advanced (10)": {
        "Najdorf": {
            "moves": ["e2e4", "c7c5", "g1f3", "d7d6", "d4d4", "c5d4", "f3d4", "g8f6", "b1c3", "a7a6"],
            "notes": ["Fischer: My favorite weapon.", "Kasparov: The most complex battlefield in chess.", "Magnus: Precision is required here."]
        }
    }
}

# --- 4. PREMIUM CSS ---
st.markdown("""
    <style>
    .stApp { background: #0e1117; color: #E5E5E5; }
    .premium-card {
        background: rgba(255, 255, 255, 0.05); border: 1px solid #fbbf24;
        border-radius: 15px; padding: 20px; margin-bottom: 20px;
    }
    .gold-text { color: #fbbf24; font-weight: bold; }
    .commentary-box { background: rgba(251, 191, 36, 0.1); border-left: 5px solid #fbbf24; padding: 15px; border-radius: 5px; font-style: italic; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. TOP DASHBOARD ---
st.markdown("<h1 style='text-align:center; color:#fbbf24;'>MM CHESS ACADEMY 🚀</h1>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1: st.markdown(f"<div class='premium-card'><span class='gold-text'>ELO SCORE</span><br><h2>{st.session_state.score}</h2></div>", unsafe_allow_html=True)
with c2: st.markdown(f"<div class='premium-card'><span class='gold-text'>ACADEMY XP</span><br><h2>{st.session_state.xp}%</h2></div>", unsafe_allow_html=True)
with c3: st.markdown(f"<div class='premium-card'><span class='gold-text'>RANK</span><br><h2>Grandmaster Prep</h2></div>", unsafe_allow_html=True)

# --- 6. CORE LOGIC ---
tier = st.sidebar.selectbox("Skill Level", list(DATABASE.keys()))
opening_name = st.sidebar.selectbox("Select Opening", list(DATABASE[tier].keys()))
opening_data = DATABASE[tier][opening_name]
moves = opening_data["moves"]
notes = opening_data["notes"]

# SILENT BOARD ENGINE
board = chess.Board()
for i in range(st.session_state.tutor_step):
    try:
        board.push(chess.Move.from_uci(moves[i]))
    except: pass

col_board, col_ui = st.columns([1.8, 1])

with col_ui:
    st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
    st.markdown(f"### Mode: {st.session_state.mode}")
    
    if st.session_state.mode == "Teaching":
        st.write(f"Learning Step: {st.session_state.tutor_step} / {len(moves)}")
        if st.button("Learn Next Move ➡️"):
            if st.session_state.tutor_step < len(moves):
                st.session_state.tutor_step += 1
                st.session_state.feedback = "neutral"
                st.rerun()
        
        if st.button("Start Quiz 🧠"):
            st.session_state.mode = "Quiz"
            st.session_state.tutor_step = 0
            st.rerun()

    else: # QUIZ MODE
        st.write("### 🎯 Prove Your Knowledge")
        squares = [chess.square_name(s) for s in range(64)]
        from_sq = st.selectbox("From Square:", ["--"] + squares)
        to_sq = st.selectbox("To Square:", ["--"] + squares)
        
        if st.button("Submit Move"):
            if from_sq != "--" and to_sq != "--":
                try:
                    user_move = f"{from_sq}{to_sq}"
                    if user_move == moves[st.session_state.tutor_step]:
                        st.session_state.feedback = "correct"
                        st.session_state.tutor_step += 1
                        st.session_state.score += 25
                        if st.session_state.tutor_step == len(moves):
                            st.balloons()
                            st.session_state.mode = "Teaching"
                    else:
                        st.session_state.feedback = "wrong"
                except:
                    st.session_state.feedback = "wrong"
                st.rerun()

    if st.button("Reset Everything"):
        st.session_state.tutor_step = 0
        st.session_state.feedback = "neutral"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # LEGEND'S ANALYSIS BOX
    if st.session_state.tutor_step > 0:
        current_note = notes[min(st.session_state.tutor_step - 1, len(notes)-1)]
        st.markdown(f"<div class='commentary-box'>{current_note}</div>", unsafe_allow_html=True)

with col_board:
    # Set Feedback Colors
    l_col = "#90EE90" if st.session_state.feedback == "correct" else "#FFB6C1" if st.session_state.feedback == "wrong" else "#ead9b5"
    d_col = "#2E8B57" if st.session_state.feedback == "correct" else "#8B0000" if st.session_state.feedback == "wrong" else "#b58863"
    
    board_svg = chess.svg.board(
        board, 
        size=600,
        lastmove=board.peek() if board.move_stack else None,
        style=f".square.light {{fill: {l_col};}} .square.dark {{fill: {d_col};}} .lastmove {{fill: rgba(251, 191, 36, 0.4);}}"
    )
    st.image(board_svg)
