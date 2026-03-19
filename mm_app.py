import streamlit as st
import chess
import chess.svg

# --- 1. PREMIUM PAGE CONFIG ---
st.set_page_config(page_title="MM Chess Academy", layout="wide", page_icon="🏆")

# --- 2. SESSION STATE (The Memory) ---
if 'board' not in st.session_state: st.session_state.board = chess.Board()
if 'score' not in st.session_state: st.session_state.score = 240
if 'quiz_step' not in st.session_state: st.session_state.quiz_step = 0
if 'feedback' not in st.session_state: st.session_state.feedback = "normal"

# --- 3. THE MASTER DATABASE (Realistic Openings) ---
OPENINGS = {
    "Ruy Lopez": ["e4", "e5", "Nf3", "Nc6", "Bb5"],
    "Italian Game": ["e4", "e5", "Nf3", "Nc6", "Bc4"],
    "Sicilian Defense": ["e4", "c5", "Nf3", "d6", "d4"]
}

# --- 4. PREMIUM DESIGN (CSS) ---
st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.9), rgba(0,0,0,0.9)), 
                    url('https://images.unsplash.com/photo-1529699211952-734e80c4d42b?q=80&w=2000');
        background-size: cover; background-attachment: fixed; color: #E5E5E5;
    }}
    .premium-card {{
        background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(15px);
        border: 2px solid {'#90EE90' if st.session_state.feedback == 'correct' else '#FFB6C1' if st.session_state.feedback == 'wrong' else '#fbbf24'};
        border-radius: 15px; padding: 20px; text-align: center;
    }}
    .gold-text {{ color: #fbbf24; font-weight: bold; font-family: 'Georgia', serif; }}
    </style>
    """, unsafe_allow_html=True)

# --- 5. DASHBOARD ---
st.markdown("<h1 style='text-align:center; color:#fbbf24;'>MM CHESS ACADEMY 🚀</h1>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1: st.markdown(f"<div class='premium-card'><span class='gold-text'>SCORE</span><br><h2>{st.session_state.score}</h2></div>", unsafe_allow_html=True)
with c2: 
    mode = st.sidebar.selectbox("Training Mode", ["Learning Mode", "Quiz Mode"])
    st.markdown(f"<div class='premium-card'><span class='gold-text'>MODE</span><br><h2>{mode}</h2></div>", unsafe_allow_html=True)
with c3: st.markdown(f"<div class='premium-card'><span class='gold-text'>PROGRESS</span><br><h2>{st.session_state.quiz_step}/5</h2></div>", unsafe_allow_html=True)

# --- 6. INTERACTIVE TRAINING LOGIC ---
col_ui, col_board = st.columns([1, 2])

with col_ui:
    selected_op = st.selectbox("Choose Opening", list(OPENINGS.keys()))
    target_moves = OPENINGS[selected_op]
    
    st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
    if mode == "Quiz Mode":
        st.write("### 🧠 Move Piece")
        # Creating a grid of buttons to act as the board controller
        from_sq = st.selectbox("From Square:", ["--"] + [chess.square_name(i) for i in range(64)])
        to_sq = st.selectbox("To Square:", ["--"] + [chess.square_name(i) for i in range(64)])
        
        if st.button("Confirm Move"):
            if from_sq != "--" and to_sq != "--":
                try:
                    move = st.session_state.board.find_move(chess.parse_square(from_sq), chess.parse_square(to_sq))
                    san_move = st.session_state.board.san(move)
                    
                    if san_move == target_moves[st.session_state.quiz_step]:
                        st.session_state.board.push(move)
                        st.session_state.quiz_step += 1
                        st.session_state.score += 25
                        st.session_state.feedback = "correct"
                        if st.session_state.quiz_step == len(target_moves): st.balloons()
                    else:
                        st.session_state.feedback = "wrong"
                except:
                    st.session_state.feedback = "wrong"
                st.rerun()
    else:
        st.write("### 📖 Learning")
        st.write(f"Moves: {' '.join(target_moves)}")
    
    if st.button("Reset Training"):
        st.session_state.board.reset()
        st.session_state.quiz_step = 0
        st.session_state.feedback = "normal"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

with col_board:
    # Set dynamic board colors for Green/Red feedback
    l_color = "#90EE90" if st.session_state.feedback == "correct" else "#FFB6C1" if st.session_state.feedback == "wrong" else "#d18b47"
    d_color = "#2E8B57" if st.session_state.feedback == "correct" else "#8B0000" if st.session_state.feedback == "wrong" else "#ffce9e"
    
    board_svg = chess.svg.board(
        st.session_state.board,
        size=550,
        style=f".square.light {{fill: {l_color};}} .square.dark {{fill: {d_color};}}"
    )
    st.image(board_svg)
