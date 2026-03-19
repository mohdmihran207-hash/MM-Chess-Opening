import streamlit as st
import streamlit.components.v1 as components
import json

# --- 1. PREMIUM NEON STYLING ---
st.set_page_config(page_title="MM_Chess_Opening", layout="wide", page_icon="👑")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Rajdhani:wght@500;700&display=swap');
    .stApp { background: #010101; color: #e0e0e0; font-family: 'Rajdhani', sans-serif; }
    .main-title {
        font-family: 'Orbitron', sans-serif; color: #fbbf24; text-align: center;
        font-size: 55px; text-shadow: 0 0 15px #fbbf24; padding: 20px;
    }
    .premium-card {
        background: #0a0a0a; border: 2px solid #fbbf24; border-radius: 20px;
        padding: 20px; box-shadow: 0 0 20px rgba(251, 191, 36, 0.1); margin-bottom: 20px;
    }
    .gold-text { color: #fbbf24; font-weight: bold; }
    .eval-container { height: 500px; width: 45px; background: #FFFFFF; border: 2px solid #fbbf24; border-radius: 10px; position: relative; overflow: hidden; }
    .eval-black-top { width: 100%; background: #000; position: absolute; top: 0; transition: height 1s; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE TEACHING DATABASE (Sample Data) ---
# In a real app, you would fill this with all 40 openings
OPENING_DATA = {
    "White: Ruy Lopez": {
        "variations": [
            {"moves": ["e4", "e5", "Nf3", "Nc6", "Bb5"], "why": "The Spanish Game: Pinning the knight to pressure the e5 pawn."},
            {"moves": ["e4", "e5", "Nf3", "Nc6", "Bb5", "a6", "Ba4"], "why": "Exchange Variation: Questioning the bishop immediately."}
        ]
    }
}

# --- 3. SESSION STATE ---
if 'progress' not in st.session_state: st.session_state.progress = 0
if 'mode' not in st.session_state: st.session_state.mode = "TEACH" # TEACH or QUIZ
if 'var_idx' not in st.session_state: st.session_state.var_idx = 0
if 'move_step' not in st.session_state: st.session_state.move_step = 0

# --- 4. LOGIC ---
st.markdown("<h1 class='main-title'>MM_CHESS_OPENING</h1>", unsafe_allow_html=True)
col_board, col_eval, col_side = st.columns([2, 0.4, 1.4])

# Get current data
current_opening = "White: Ruy Lopez" # This would be from your selectbox
var_data = OPENING_DATA[current_opening]["variations"][st.session_state.var_idx]
target_moves = var_data["moves"]

with col_side:
    st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
    st.markdown(f"### Mode: <span class='gold-text'>{st.session_state.mode}</span>", unsafe_allow_html=True)
    st.write(f"Variation {st.session_state.var_idx + 1} of 6")
    st.progress(st.session_state.progress / 100)
    
    if st.session_state.mode == "TEACH":
        st.info("💡 Study the moves below. The board will guide you.")
        st.write(f"**Strategic Goal:** {var_data['why']}")
        if st.button("I'm Ready for the Quiz ➡️"):
            st.session_state.mode = "QUIZ"
            st.session_state.move_step = 0
            st.rerun()
    else:
        st.warning("🎯 QUIZ: Play the variation from memory!")
        st.write(f"Move {st.session_state.move_step + 1} of {len(target_moves)}")
        if st.button("Back to Teaching"):
            st.session_state.mode = "TEACH"
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

with col_eval:
    h = 50 - (st.session_state.progress / 2)
    st.markdown(f"<div class='eval-container'><div class='eval-black-top' style='height:{h}%;'></div></div>", unsafe_allow_html=True)

with col_board:
    # Pass Python data to Javascript
    moves_json = json.dumps(target_moves)
    mode_js = st.session_state.mode
    
    board_html = f"""
    <link rel="stylesheet" href="https://unpkg.com/@chrisoakman/chessboardjs@1.0.0/dist/chessboard-1.0.0.min.css">
    <script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>
    <script src="https://unpkg.com/@chrisoakman/chessboardjs@1.0.0/dist/chessboard-1.0.0.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/chess.js/0.10.3/chess.min.js"></script>

    <div id="board" style="width: 580px; border: 4px solid #fbbf24; border-radius: 15px;"></div>
    <div id="status" style="color: #fbbf24; margin-top: 10px; font-weight: bold;"></div>

    <script>
        var game = new Chess();
        var targetMoves = {moves_json};
        var mode = "{mode_js}";
        var step = 0;

        var board = Chessboard('board', {{
            draggable: true,
            position: 'start',
            onDrop: handleMove,
            pieceTheme: 'https://chessboardjs.com/img/chesspieces/wikipedia/{{piece}}.png'
        }});

        function handleMove(source, target) {{
            var move = game.move({{ from: source, to: target, promotion: 'q' }});
            
            if (move === null) return 'snapback';

            // Check if move matches theory
            if (move.san === targetMoves[step]) {{
                step++;
                document.getElementById('status').innerText = "✅ Correct!";
                if (step < targetMoves.length && mode === "TEACH") {{
                    setTimeout(() => {{ 
                        game.move(targetMoves[step]); 
                        board.position(game.fen());
                        step++;
                    }}, 500);
                }}
            }} else {{
                game.undo();
                document.getElementById('status').innerText = "❌ Wrong Move! Try again.";
                return 'snapback';
            }}
        }}

        // If in TEACH mode, show first move
        if (mode === "TEACH") {{
            setTimeout(() => {{ 
                game.move(targetMoves[0]); 
                board.position(game.fen());
                step = 1;
            }}, 500);
        }}
    </script>
    """
    components.html(board_html, height=700)
