import streamlit as st
import chess
import chess.svg
import random

# --- 1. PREMIUM CONFIG & LEGENDS ---
st.set_page_config(page_title="MM Chess Academy", layout="wide", page_icon="🏆")

LEGENDS = {
    "Magnus Carlsen": "Confidence is a very important thing in chess. If you don't believe you can win, you won't.",
    "Garry Kasparov": "Chess is mental torture.",
    "Bobby Fischer": "I don't believe in psychology. I believe in good moves.",
    "Mikhail Tal": "You must take your opponent into a deep dark forest where 2+2=5."
}

# --- 2. DEEP STRATEGY DATABASE (The "Why") ---
DATABASE = {
    "Beginner (10)": {
        "Ruy Lopez": {
            "moves": ["e2e4", "e7e5", "g1f3", "b8c6", "f1b5"],
            "depth": ["Control center/open lines.", "Symmetrical claim of space.", "Attacking e5/preparing castle.", "Defending e5/developing.", "Applying pressure to the defender of e5."],
            "tip": "The 'Spanish Torture' is a test of long-term planning."
        },
        "Italian Game": {
            "moves": ["e2e4", "e7e5", "g1f3", "b8c6", "f1c4"],
            "depth": ["King's Pawn opening.", "Matches the center.", "Develops and attacks.", "Standard development.", "Targeting the weak f7 pawn early!"],
            "tip": "Classic development that leads to sharp tactical battles."
        }
    },
    "Intermediate (30)": {
        "Sicilian Defense": {
            "moves": ["e2e4", "c7c5", "g1f3", "d7d6", "d4d4"],
            "depth": ["Standard start.", "Asymmetrical fight for the center.", "Developing toward center.", "Opening lines for the Bishop.", "Challenging the c5 pawn directly."],
            "tip": "Black's most aggressive response to e4."
        }
    },
    "Advanced (10)": {
        "Najdorf Sicilian": {
            "moves": ["e2e4", "c7c5", "g1f3", "d7d6", "d4d4", "c5d4", "f3d4", "g8f6", "b1c3", "a7a6"],
            "depth": ["Start.", "C-pawn thrust.", "Nf3.", "d6.", "d4.", "Trading pawns.", "Center knight.", "Pressure.", "Nc3.", "The Najdorf move—preventing Bb5!"],
            "tip": "The favorite weapon of Kasparov and Fischer."
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
    .strategy-box { background: rgba(251, 191, 36, 0.1); border-left: 5px solid #fbbf24; padding: 15px; border-radius: 5px; margin-top: 10px; }
    .eval-bar { height: 450px; width: 35px; background: white; border: 2px solid #fbbf24; border-radius: 5px; position: relative; }
    .eval-fill { width: 100%; position: absolute; bottom: 0; background: #222; transition: all 0.6s ease; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. DASHBOARD ---
st.markdown("<h1 style='text-align:center; color:#fbbf24;'>MM CHESS OPENING ACADEMY 🚀</h1>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1: st.markdown(f"<div class='premium-card'><span class='gold-text'>ELO SCORE</span><br><h2>{st.session_state.score}</h2></div>", unsafe_allow_html=True)
with c2: st.markdown(f"<div class='premium-card'><span class='gold-text'>ACADEMY XP</span><br><h2>{st.session_state.xp}%</h2></div>", unsafe_allow_html=True)
with c3: 
    l_name, l_quote = random.choice(list(LEGENDS.items()))
    st.markdown(f"<div class='premium-card'><span class='gold-text'>{l_name}</span><br><small>'{l_quote}'</small></div>", unsafe_allow_html=True)

# --- 6. CORE LOGIC ---
tier = st.sidebar.selectbox("Skill Level", list(DATABASE.keys()))
opening_name = st.sidebar.selectbox("Select Opening", list(DATABASE[tier].keys()))
opening_data = DATABASE[tier][opening_name]
moves = opening_data["moves"]

# Silent Board Build
board = chess.Board()
for i in range(st.session_state.tutor_step):
    try: board.push(chess.Move.from_uci(moves[i]))
    except: pass

col_board, col_eval, col_ui = st.columns([2, 0.4, 1.5])

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
        st.write("### 🎯 Your Move")
        squares = [chess.square_name(s) for s in range(64)]
        from_sq = st.selectbox("From:", ["--"] + squares)
        to_sq = st.selectbox("To:", ["--"] + squares)
        
        if st.button("Confirm Move"):
            if from_sq != "--" and to_sq != "--":
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
                st.rerun()

    if st.button("Reset Everything"):
        st.session_state.tutor_step = 0
        st.session_state.feedback = "neutral"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # DEEP WHY ANALYSIS
    if st.session_state.tutor_step > 0:
        st.markdown("<div class='strategy-box'>", unsafe_allow_html=True)
        st.markdown(f"<span class='gold-text'>Strategic Why:</span><br>{opening_data['depth'][st.session_state.tutor_step-1]}", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        st.caption(f"💡 {opening_data['tip']}")

with col_eval:
    # Stockfish Style Eval Bar
    eval_val = 50 + (st.session_state.tutor_step * 2.5)
    st.markdown(f'<div class="eval-bar"><div class="eval-fill" style="height: {eval_val}%;"></div></div>', unsafe_allow_html=True)
    st.caption("EVAL")

with col_board:
    # Feedback Colors
    l_c = "#90EE90" if st.session_state.feedback == "correct" else "#FFB6C1" if st.session_state.feedback == "wrong" else "#ead9b5"
    d_c = "#2E8B57" if st.session_state.feedback == "correct" else "#8B0000" if st.session_state.feedback == "wrong" else "#b58863"
    
    board_svg = chess.svg.board(
        board, 
        size=600,
        lastmove=board.peek() if board.move_stack else None,
        style=f".square.light {{fill: {l_c};}} .square.dark {{fill: {d_c};}} .lastmove {{fill: rgba(251, 191, 36, 0.4);}}"
    )
    st.image(board_svg)
