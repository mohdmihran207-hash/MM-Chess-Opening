import streamlit as st
import chess
import chess.svg
import random

# --- 1. PREMIUM CONFIG & LEGENDS ---
st.set_page_config(page_title="MM Chess Academy", layout="wide")

LEGENDS = {
    "Magnus Carlsen": "Confidence is a very important thing in chess. If you don't believe you can win, you won't.",
    "Garry Kasparov": "Chess is mental torture.",
    "Bobby Fischer": "I don't believe in psychology. I believe in good moves.",
    "Mikhail Tal": "You must take your opponent into a deep dark forest where 2+2=5."
}

# --- 2. THE 50 OPENINGS DATABASE (Sample Structure) ---
DATABASE = {
    "Beginner (10)": {
        "Ruy Lopez": ["e2e4", "e7e5", "g1f3", "b8c6", "f1b5"],
        "Italian Game": ["e2e4", "e7e5", "g1f3", "b8c6", "f1c4"],
        "Sicilian Defense": ["e2e4", "c7c5", "g1f3", "d7d6", "d4d4"]
    },
    "Intermediate (30)": {
        "King's Gambit": ["e4", "e5", "f4"],
        "Dutch Defense": ["d4", "f5"]
    },
    "Advanced (10)": {
        "Najdorf": ["e4", "c5", "Nf3", "d6", "d4", "cxd4", "Nxd4", "Nf6", "Nc3", "a6"]
    }
}

# --- 3. SESSION STATE ---
if 'score' not in st.session_state: st.session_state.score = 2450
if 'xp' not in st.session_state: st.session_state.xp = 85
if 'tutor_step' not in st.session_state: st.session_state.tutor_step = 0
if 'mode' not in st.session_state: st.session_state.mode = "Teaching"
if 'move_from' not in st.session_state: st.session_state.move_from = None
if 'feedback' not in st.session_state: st.session_state.feedback = "neutral"

# --- 4. PREMIUM CSS ---
st.markdown("""
    <style>
    .stApp { background: #0e1117; color: #E5E5E5; }
    .premium-card {
        background: rgba(255, 255, 255, 0.05); border: 1px solid #fbbf24;
        border-radius: 15px; padding: 20px; margin-bottom: 20px;
    }
    .gold-text { color: #fbbf24; font-weight: bold; }
    .stButton>button { background: #fbbf24; color: black; font-weight: bold; border-radius: 10px; }
    .eval-bar { height: 400px; width: 30px; background: white; border: 2px solid #fbbf24; border-radius: 5px; position: relative; }
    .eval-fill { width: 100%; position: absolute; bottom: 0; background: black; transition: height 0.5s; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. DASHBOARD ---
st.markdown("<h1 style='text-align:center; color:#fbbf24;'>MM ACADEMY: OPENING TUTOR 🏆</h1>", unsafe_allow_html=True)

c1, c2, c3 = st.columns([1, 1, 2])
with c1: st.markdown(f"<div class='premium-card'><span class='gold-text'>ELO SCORE</span><br><h2>{st.session_state.score}</h2></div>", unsafe_allow_html=True)
with c2: st.markdown(f"<div class='premium-card'><span class='gold-text'>XP LEVEL</span><br><h2>{st.session_state.xp}%</h2></div>", unsafe_allow_html=True)
with c3: 
    l_name, l_quote = random.choice(list(LEGENDS.items()))
    st.markdown(f"<div class='premium-card'><span class='gold-text'>{l_name}</span><br><small>'{l_quote}'</small></div>", unsafe_allow_html=True)

# --- 6. INTERACTIVE TUTOR LOGIC ---
col_board, col_eval, col_ui = st.columns([2, 0.3, 1.5])

# Determine current opening and moves
tier = st.sidebar.selectbox("Skill Tier", list(DATABASE.keys()))
opening_name = st.sidebar.selectbox("Opening", list(DATABASE[tier].keys()))
moves = DATABASE[tier][opening_name]

# Teaching Board Construction
board = chess.Board()
for i in range(st.session_state.tutor_step):
    try:
        m = moves[i]
        board.push_san(m) if len(m) < 5 else board.push_uci(m)
    except: pass

with col_ui:
    st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
    st.markdown(f"### Mode: {st.session_state.mode}")
    
    if st.session_state.mode == "Teaching":
        st.write(f"Learning Step: {st.session_state.tutor_step} / {len(moves)}")
        if st.button("Learn Next Move ➡️"):
            if st.session_state.tutor_step < len(moves):
                st.session_state.tutor_step += 1
                st.session_state.xp = min(100, st.session_state.xp + 2)
            else:
                st.success("Theory Mastered!")
            st.rerun()
        
        if st.button("Switch to Quiz 🧠"):
            st.session_state.mode = "Quiz"
            st.session_state.tutor_step = 0
            st.rerun()

    else: # QUIZ MODE
        st.write("### 🎯 Your Turn to Move")
        st.info("Click the 'From' square, then the 'To' square.")
        
        squares = [chess.square_name(s) for s in range(64)]
        from_sq = st.selectbox("From:", ["--"] + squares)
        to_sq = st.selectbox("To:", ["--"] + squares)
        
        if st.button("Execute Move"):
            if from_sq != "--" and to_sq != "--":
                try:
                    move_uci = f"{from_sq}{to_sq}"
                    move_obj = board.parse_uci(move_uci)
                    correct_move_san = moves[st.session_state.tutor_step]
                    
                    if board.san(move_obj) == correct_move_san:
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

    if st.button("Reset Session"):
        st.session_state.tutor_step = 0
        st.session_state.feedback = "neutral"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

with col_eval:
    # Simulated Stockfish Eval Bar (50% is equal)
    eval_height = 50 + (st.session_state.tutor_step * 2) 
    st.markdown(f'<div class="eval-bar"><div class="eval-fill" style="height: {eval_height}%;"></div></div>', unsafe_allow_html=True)

with col_board:
    # Board Colors based on Accuracy
    l_color = "#90EE90" if st.session_state.feedback == "correct" else "#FFB6C1" if st.session_state.feedback == "wrong" else "#ead9b5"
    d_color = "#2E8B57" if st.session_state.feedback == "correct" else "#8B0000" if st.session_state.feedback == "wrong" else "#b58863"
    
    board_svg = chess.svg.board(
        board, 
        size=500,
        style=f".square.light {{fill: {l_color};}} .square.dark {{fill: {d_color};}}"
    )
    st.image(board_svg)
