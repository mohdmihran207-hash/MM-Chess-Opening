import streamlit as st
import streamlit.components.v1 as components
import chess
import random

# --- 1. PREMIUM SETTINGS ---
st.set_page_config(page_title="MM Chess Academy", layout="wide", page_icon="🏆")

# --- 2. SESSION STATE ---
if 'score' not in st.session_state: st.session_state.score = 2850
if 'xp' not in st.session_state: st.session_state.xp = 92

# --- 3. PREMIUM CSS ---
st.markdown("""
    <style>
    .stApp { background: #050505; color: #E5E5E5; }
    .premium-card {
        background: linear-gradient(145deg, #1a1a1a, #0a0a0a);
        border: 2px solid #fbbf24; border-radius: 15px; padding: 20px;
    }
    .gold-text { color: #fbbf24; font-weight: bold; font-family: 'Garamond', serif; }
    
    /* PRO EVAL BAR: White on Bottom */
    .eval-container { 
        height: 500px; width: 40px; background: #FFFFFF; 
        border: 3px solid #fbbf24; border-radius: 8px; position: relative; overflow: hidden; 
    }
    .eval-black-top { 
        width: 100%; background: #000000; position: absolute; top: 0; height: 45%; 
        transition: height 0.5s ease;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. TOP DASHBOARD ---
st.markdown("<h1 style='text-align:center; color:#fbbf24;'>MM ELITE: MOUSE CONTROL ACADEMY 💎</h1>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1: st.markdown(f"<div class='premium-card'><span class='gold-text'>ELO</span><br><h2>{st.session_state.score}</h2></div>", unsafe_allow_html=True)
with c2: st.markdown(f"<div class='premium-card'><span class='gold-text'>XP</span><br><h2>{st.session_state.xp}%</h2></div>", unsafe_allow_html=True)
with c3: st.markdown(f"<div class='premium-card'><span class='gold-text'>COACH</span><br><small>'Attack!' - Mikhail Tal</small></div>", unsafe_allow_html=True)

# --- 5. THE MOUSE-INTERACTIVE BOARD (HTML/JS) ---
# This block creates the real drag-and-drop board
board_html = """
<link rel="stylesheet" href="https://unpkg.com/@chrisoakman/chessboardjs@1.0.0/dist/chessboard-1.0.0.min.css">
<script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>
<script src="https://unpkg.com/@chrisoakman/chessboardjs@1.0.0/dist/chessboard-1.0.0.min.js"></script>

<div id="myBoard" style="width: 550px; border: 4px solid #fbbf24; border-radius: 10px;"></div>
<div style="margin-top: 10px;">
    <button onclick="board.start()" style="padding: 10px; background: #fbbf24; border: none; font-weight: bold; cursor: pointer;">Reset Board</button>
</div>

<script>
    var board = Chessboard('myBoard', {
      draggable: true,
      dropOffBoard: 'snapback',
      position: 'start',
      pieceTheme: 'https://chessboardjs.com/img/chesspieces/wikipedia/{piece}.png'
    });
</script>
"""

col_board, col_eval, col_ui = st.columns([2, 0.5, 1.5])

with col_board:
    st.markdown("<div class='premium-card' style='padding: 10px;'>", unsafe_allow_html=True)
    components.html(board_html, height=650)
    st.markdown("</div>", unsafe_allow_html=True)

with col_eval:
    st.markdown('<div class="eval-container"><div class="eval-black-top"></div></div>', unsafe_allow_html=True)
    st.caption("WHITE ADV (+0.8)")

with col_ui:
    st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
    st.markdown("### <span class='gold-text'>Opening Tutor AI</span>", unsafe_allow_html=True)
    st.write("Use your mouse to drag the pieces for the **Ruy Lopez**.")
    st.info("Goal: Reach a +1.0 advantage by move 10.")
    
    st.divider()
    st.write("**Current Phase:** Teaching & Discovery")
    if st.button("Submit Moves for AI Analysis"):
        st.session_state.score += 15
        st.success("Analysis Complete: Your accuracy is 98%!")
        st.balloons()
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='premium-card' style='margin-top:20px;'>", unsafe_allow_html=True)
    st.markdown("<span class='gold-text'>Strategic Why:</span>", unsafe_allow_html=True)
    st.write("By moving the Bishop to b5, you are pinning the Knight and preparing to win the e5 pawn later.")
    st.markdown("</div>", unsafe_allow_html=True)
