import streamlit as st
import chess
import chess.svg
import random

# --- 1. PREMIUM PAGE CONFIG ---
st.set_page_config(page_title="MM Chess Academy", layout="wide", page_icon="🏆")

# --- 2. DEEP VARIATION DATABASE (To Advantage) ---
DATABASE = {
    "Beginner (10)": {
        "Ruy Lopez: Exchange Variation": {
            "moves": ["e2e4", "e7e5", "g1f3", "b8c6", "f1b5", "a7a6", "b5c6", "d7c6", "e1g1"],
            "depth": [
                "Center control.", "Black matches.", "Attack e5.", "Defend e5.", 
                "The Pin.", "Challenging the Bishop.", "The Exchange: Doubling Black's pawns.", 
                "Black recaptures.", "Castle: White is +0.6. Better pawn structure and King safety."
            ],
            "ai_coach": "Fischer: 'I like the Exchange Variation because it creates a permanent advantage in the endgame.'"
        }
    },
    "Intermediate (30)": {
        "Italian Game: Evans Gambit": {
            "moves": ["e2e4", "e7e5", "g1f3", "b8c6", "f1c4", "f1c5", "b2b4", "c5b4", "c2c3"],
            "depth": ["e4.", "e5.", "Nf3.", "Nc6.", "Bc4.", "Bc5.", "The Gambit! Offering a pawn for speed.", "Black accepts.", "Preparing d4. White has a massive center and attack +0.8."],
            "ai_coach": "Tal: 'The Evans Gambit is a gift from the gods of attack!'"
        }
    }
}

# --- 3. PREMIUM SESSION STATE ---
if 'score' not in st.session_state: st.session_state.score = 2850 
if 'xp' not in st.session_state: st.session_state.xp = 92
if 'tutor_step' not in st.session_state: st.session_state.tutor_step = 0
if 'mode' not in st.session_state: st.session_state.mode = "Teaching"
if 'feedback' not in st.session_state: st.session_state.feedback = "neutral"

# --- 4. THE "WHITE ON BOTTOM" PREMIUM CSS ---
st.markdown("""
    <style>
    .stApp { background: #050505; color: #E5E5E5; }
    .premium-card {
        background: linear-gradient(145deg, #1a1a1a, #0a0a0a);
        border: 2px solid #fbbf24; border-radius: 20px; padding: 25px;
    }
    .gold-text { color: #fbbf24; font-weight: bold; font-family: 'Garamond', serif; font-size: 22px; }
    
    /* PRO EVAL BAR: White is the Background, Black is the Fill from the TOP down */
    .eval-container { 
        height: 500px; width: 40px; 
        background: #FFFFFF; /* White advantage */
        border: 3px solid #fbbf24; border-radius: 8px; 
        position: relative; overflow: hidden; 
    }
    .eval-black-top { 
        width: 100%; 
        background: #000000; /* Black advantage */
        position: absolute; top: 0; 
        transition: height 0.8s ease-in-out; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- 5. DASHBOARD ---
st.markdown("<h1 style='text-align:center; color:#fbbf24;'>MM ELITE ACADEMY: WHITE ADVANTAGE 💎</h1>", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1: st.markdown(f"<div class='premium-card'><span class='gold-text'>ELO RATING</span><br><h2 style='color:#90EE90;'>{st.session_state.score}</h2></div>", unsafe_allow_html=True)
with c2: st.markdown(f"<div class='premium-card'><span class='gold-text'>MASTERY XP</span><br><h2>{st.session_state.xp}%</h2></div>", unsafe_allow_html=True)
with c3: st.markdown(f"<div class='premium-card'><span class='gold-text'>AI STATUS</span><br><h2>STOCKFISH 16 ON</h2></div>", unsafe_allow_html=True)

# --- 6. CORE LOGIC ---
tier = st.sidebar.selectbox("Category", list(DATABASE.keys()))
opening_name = st.sidebar.selectbox("Variation", list(DATABASE[tier].keys()))
data = DATABASE[tier][opening_name]
moves = data["moves"]

board = chess.Board()
for i in range(st.session_state.tutor_step):
    try: board.push(chess.Move.from_uci(moves[i]))
    except: pass

col_board, col_eval, col_ui = st.columns([2, 0.5, 1.5])

with col_ui:
    st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
    st.markdown(f"### <span class='gold-text'>{st.session_state.mode} Mode</span>", unsafe_allow_html=True)
    
    if st.session_state.mode == "Teaching":
        st.write(f"Deep Variation: **Step {st.session_state.tutor_step} / {len(moves)}**")
        if st.button("Analyze Next Move ➡️"):
            if st.session_state.tutor_step < len(moves):
                st.session_state.tutor_step += 1
                st.rerun()
        if st.button("Start Interactive Quiz 🧠"):
            st.session_state.mode = "Quiz"
            st.session_state.tutor_step = 0
            st.rerun()
    else: # QUIZ MODE
        st.info("🎯 Move the Piece by selecting squares:")
        squares = [chess.square_name(s) for s in range(64)]
        from_sq = st.selectbox("From:", ["--"] + squares)
        to_sq = st.selectbox("To:", ["--"] + squares)
        
        if st.button("Check with AI Coach"):
            if from_sq != "--" and to_sq != "--":
                user_move = f"{from_sq}{to_sq}"
                if user_move == moves[st.session_state.tutor_step]:
                    st.session_state.feedback = "correct"
                    st.session_state.tutor_step += 1
                    st.session_state.score += 50
                    if st.session_state.tutor_step == len(moves):
                        st.balloons()
                        st.session_state.mode = "Teaching"
                else:
                    st.session_state.feedback = "wrong"
                st.rerun()

    if st.button("Reset Academy"):
        st.session_state.tutor_step = 0
        st.session_state.feedback = "neutral"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.tutor_step > 0:
        st.markdown(f"<div style='background:rgba(251,191,36,0.1); padding:15px; border-left:4px solid #fbbf24;'><b>Tutor Analysis:</b><br>{data['depth'][st.session_state.tutor_step-1]}</div>", unsafe_allow_html=True)
        st.caption(data["ai_coach"])

with col_eval:
    # WHITE ON BOTTOM: The black section starts at the top and covers part of the white bar.
    # As White gets better (+ score), the black section (top) gets SHORTER.
    # If tutoring starts at 50/50, black is 50%. At the end (+1.5), black is only 30%.
    black_height = 50 - (st.session_state.tutor_step * 3) 
    st.markdown(f'<div class="eval-container"><div class="eval-black-top" style="height: {black_height}%;"></div></div>', unsafe_allow_html=True)
    st.caption("EVAL")

with col_board:
    l_c = "#90EE90" if st.session_state.feedback == "correct" else "#FFB6C1" if st.session_state.feedback == "wrong" else "#ead9b5"
    d_c = "#2E8B57" if st.session_state.feedback == "correct" else "#8B0000" if st.session_state.feedback == "wrong" else "#b58863"
    
    board_svg = chess.svg.board(
        board, size=600,
        lastmove=board.peek() if board.move_stack else None,
        style=f".square.light {{fill: {l_c};}} .square.dark {{fill: {d_c};}} .lastmove {{fill: rgba(251, 191, 36, 0.4);}}"
    )
    st.image(board_svg)
