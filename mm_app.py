import streamlit as st
import streamlit.components.v1 as components
import chess
import json

# --- 1. PREMIUM STYLING ---
st.set_page_config(page_title="MM_Chess_Opening", layout="wide", page_icon="👑")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&display=swap');
    .stApp { background: #010101; color: #e0e0e0; }
    .main-title {
        font-family: 'Orbitron', sans-serif;
        color: #fbbf24;
        text-align: center;
        font-size: 50px;
        text-shadow: 0 0 20px #fbbf24;
        padding: 20px;
    }
    .premium-card {
        background: #111;
        border: 2px solid #fbbf24;
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 20px;
    }
    .gold-text { color: #fbbf24; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. OPENING DATA WITH "WHY" ---
# Detailed 6-variation logic for the Ruy Lopez as an example
TEACHING_DATABASE = {
    "White: Ruy Lopez": [
        {"move": "e4", "why": "Controls the center and opens lines for the Queen and Bishop."},
        {"move": "e5", "why": "Black responds by claiming their own share of the center."},
        {"move": "Nf3", "why": "Attacks the e5 pawn and develops the Knight toward the center."},
        {"move": "Nc6", "why": "Black defends the e5 pawn while developing a piece."},
        {"move": "Bb5", "why": "The Ruy Lopez! This pins the Knight and puts pressure on the defender of e5."},
        {"move": "a6", "why": "Black 'asks the question' to the Bishop, forcing it to move or trade."}
    ]
}

# --- 3. SESSION STATE ---
if 'move_idx' not in st.session_state: st.session_state.move_idx = 0
if 'current_opening' not in st.session_state: st.session_state.current_opening = "White: Ruy Lopez"

# --- 4. LAYOUT ---
st.markdown("<h1 class='main-title'>MM_CHESS_OPENING</h1>", unsafe_allow_html=True)

col_board, col_ui = st.columns([2, 1])

with col_ui:
    st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
    st.markdown(f"### <span class='gold-text'>Teaching: {st.session_state.current_opening}</span>", unsafe_allow_html=True)
    
    current_moves = TEACHING_DATABASE[st.session_state.current_opening]
    
    if st.session_state.move_idx < len(current_moves):
        curr = current_moves[st.session_state.move_idx]
        st.write(f"**Current Move:** {curr['move']}")
        st.info(f"**AI Analysis:** {curr['why']}")
        
        if st.button("Play Next Move ♟️"):
            st.session_state.move_idx += 1
            st.rerun()
    else:
        st.success("Variation Complete! You are ready for the Quiz.")
        if st.button("Reset to Start"):
            st.session_state.move_idx = 0
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

with col_board:
    # We pass the moves into the Javascript board so it stays in sync
    past_moves = [m['move'] for m in current_moves[:st.session_state.move_idx]]
    moves_js = json.dumps(past_moves)

    board_html = f"""
    <link rel="stylesheet" href="https://unpkg.com/@chrisoakman/chessboardjs@1.0.0/dist/chessboard-1.0.0.min.css">
    <script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>
    <script src="https://unpkg.com/@chrisoakman/chessboardjs@1.0.0/dist/chessboard-1.0.0.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/chess.js/0.10.3/chess.min.js"></script>

    <div id="board" style="width: 550px; border: 3px solid #fbbf24; border-radius: 10px;"></div>

    <script>
        var game = new Chess();
        var board = Chessboard('board', {{
            position: 'start',
            draggable: true,
            pieceTheme: 'https://chessboardjs.com/img/chesspieces/wikipedia/{{piece}}.png'
        }});

        // SYNC PYTHON MOVES TO BOARD
        var moves = {moves_js};
        moves.forEach(function(m) {{
            game.move(m);
        }});
        board.position(game.fen());
    </script>
    """
    components.html(board_html, height=600)
