import streamlit as st
import streamlit.components.v1 as components
import json

# --- 1. CONFIG & GLOWING UI ---
st.set_page_config(page_title="MM_Chess_Opening", layout="wide", page_icon="👑")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Rajdhani:wght@500;700&display=swap');
    .stApp { background: #010101; color: #e0e0e0; font-family: 'Rajdhani', sans-serif; }
    .main-title {
        font-family: 'Orbitron', sans-serif; color: #fbbf24; text-align: center;
        font-size: 55px; text-shadow: 0 0 15px #fbbf24, 0 0 30px #d97706; padding: 25px;
    }
    .premium-card {
        background: rgba(15, 15, 15, 0.95); border: 2px solid #fbbf24; border-radius: 20px;
        padding: 20px; box-shadow: 0 0 25px rgba(251, 191, 36, 0.1); margin-bottom: 20px;
    }
    .gold-text { color: #fbbf24; font-weight: bold; text-transform: uppercase; }
    .eval-container { height: 500px; width: 45px; background: #FFF; border: 2px solid #fbbf24; border-radius: 10px; position: relative; overflow: hidden; }
    .eval-black-top { width: 100%; background: #000; position: absolute; top: 0; transition: height 1s; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. OPENING DATABASE (Example: Ruy Lopez) ---
OPENING_DATA = {
    "White: Ruy Lopez": {
        "variations": [
            {"moves": ["e4", "e5", "Nf3", "Nc6", "Bb5"], "desc": "The main line. Putting pressure on the defender of e5."},
            {"moves": ["e4", "e5", "Nf3", "Nc6", "Bb5", "a6", "Ba4"], "desc": "Morphy Defense: Black asks the bishop to move or capture."}
        ]
    }
}

# --- 3. SESSION STATE ---
if 'progress' not in st.session_state: st.session_state.progress = 0
if 'mode' not in st.session_state: st.session_state.mode = "TEACH"
if 'current_var' not in st.session_state: st.session_state.current_var = 0

st.markdown("<h1 class='main-title'>MM_CHESS_OPENING</h1>", unsafe_allow_html=True)
col_board, col_eval, col_side = st.columns([2, 0.4, 1.4])

# Data Extraction
opening_key = "White: Ruy Lopez"
variation = OPENING_DATA[opening_key]["variations"][st.session_state.current_var]

with col_side:
    st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
    st.markdown(f"### <span class='gold-text'>{st.session_state.mode} MODE</span>", unsafe_allow_html=True)
    st.progress(st.session_state.progress / 100)
    st.write(f"**Theory:** {variation['desc']}")
    
    if st.session_state.mode == "TEACH":
        st.info("AI: Watch the board. We will play the moves for you to memorize.")
        if st.button("Start Quiz 🎯"):
            st.session_state.mode = "QUIZ"
            st.rerun()
    else:
        st.warning("AI: Drag the pieces. If you make a mistake, they will snap back!")
        if st.button("Back to Study 📖"):
            st.session_state.mode = "TEACH"
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

with col_eval:
    h = 50 - (st.session_state.progress / 2)
    st.markdown(f"<div class='eval-container'><div class='eval-black-top' style='height:{h}%;'></div></div>", unsafe_allow_html=True)

with col_board:
    # BRIDGE: Passing moves and mode to Javascript
    moves_json = json.dumps(variation["moves"])
    
    board_html = f"""
    <link rel="stylesheet" href="https://unpkg.com/@chrisoakman/chessboardjs@1.0.0/dist/chessboard-1.0.0.min.css">
    <script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>
    <script src="https://unpkg.com/@chrisoakman/chessboardjs@1.0.0/dist/chessboard-1.0.0.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/chess.js/0.10.3/chess.min.js"></script>

    <div id="board" style="width: 580px; border: 4px solid #fbbf24; border-radius: 15px; box-shadow: 0 0 30px rgba(251, 191, 36, 0.3);"></div>
    <div id="msg" style="color: #fbbf24; font-weight: bold; margin-top: 15px; font-size: 1.2em;"></div>

    <script>
        var game = new Chess();
        var theory = {moves_json};
        var mode = "{st.session_state.mode}";
        var currentStep = 0;

        var board = Chessboard('board', {{
            draggable: true,
            position: 'start',
            onDrop: onMove,
            pieceTheme: 'https://chessboardjs.com/img/chesspieces/wikipedia/{{piece}}.png'
        }});

        function onMove(src, tgt) {{
            var move = game.move({{ from: src, to: tgt, promotion: 'q' }});
            if (move === null) return 'snapback';

            // Logic: Compare move to theory
            if (move.san === theory[currentStep]) {{
                currentStep++;
                document.getElementById('msg').innerHTML = "✅ EXCELLENT!";
                
                // In TEACH mode, auto-play the next theory move
                if (mode === "TEACH" && currentStep < theory.length) {{
                    setTimeout(() => {{
                        game.move(theory[currentStep]);
                        board.position(game.fen());
                        currentStep++;
                    }}, 600);
                }}
            }} else {{
                game.undo();
                document.getElementById('msg').innerHTML = "❌ WRONG THEORY! TRY AGAIN.";
                return 'snapback';
            }}
        }}

        // Initial trigger for TEACH mode
        if (mode === "TEACH") {{
            setTimeout(() => {{
                game.move(theory[0]);
                board.position(game.fen());
                currentStep = 1;
                document.getElementById('msg').innerHTML = "Study Move: " + theory[0];
            }}, 800);
        }}
    </script>
    """
    components.html(board_html, height=750)
