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
        font-size: 55px; text-shadow: 0 0 20px #fbbf24, 0 0 40px #d97706; padding: 25px;
    }
    .premium-card {
        background: rgba(10, 10, 10, 0.9); border: 2px solid #fbbf24; border-radius: 20px;
        padding: 20px; box-shadow: 0 0 25px rgba(251, 191, 36, 0.15); margin-bottom: 20px;
    }
    .gold-text { color: #fbbf24; font-weight: bold; text-transform: uppercase; }
    
    /* White Advantage on Bottom */
    .eval-container { 
        height: 520px; width: 50px; background: #FFFFFF; 
        border: 3px solid #fbbf24; border-radius: 12px; position: relative; overflow: hidden;
    }
    .eval-black-top { 
        width: 100%; background: #000; position: absolute; top: 0; 
        transition: height 0.8s cubic-bezier(0.4, 0, 0.2, 1);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE OPENING BRAIN (Sample Structure) ---
# You can keep adding to this list to reach your 40 openings goal!
OPENING_DATABASE = {
    "Beginner (White)": {
        "Ruy Lopez": ["e4", "e5", "Nf3", "Nc6", "Bb5"],
        "Italian Game": ["e4", "e5", "Nf3", "Nc6", "Bc4"],
        "London System": ["d4", "Nf6", "Bf4"]
    },
    "Beginner (Black)": {
        "Sicilian Defense": ["e4", "c5"],
        "French Defense": ["e4", "e6"]
    }
}

# --- 3. SESSION STATE ---
if 'progress' not in st.session_state: st.session_state.progress = 0
if 'mode' not in st.session_state: st.session_state.mode = "STUDY" # STUDY or QUIZ
if 'eval_val' not in st.session_state: st.session_state.eval_val = 50

# --- 4. UI LAYOUT ---
st.markdown("<h1 class='main-title'>MM_CHESS_OPENING</h1>", unsafe_allow_html=True)
col_board, col_eval, col_side = st.columns([2, 0.4, 1.4])

with col_side:
    st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
    st.markdown(f"### <span class='gold-text'>MODE: {st.session_state.mode}</span>", unsafe_allow_html=True)
    
    tier = st.selectbox("Select Tier", list(OPENING_DATABASE.keys()))
    opening = st.selectbox("Select Opening", list(OPENING_DATABASE[tier].keys()))
    
    theory_moves = OPENING_DATABASE[tier][opening]
    
    st.divider()
    st.write(f"**Progress:** {st.session_state.progress}%")
    st.progress(st.session_state.progress / 100)

    if st.session_state.mode == "STUDY":
        st.info("📖 Drag the pieces. The AI will guide you through the theory.")
        if st.button("Start Quiz 🎯"):
            st.session_state.mode = "QUIZ"
            st.rerun()
    else:
        st.warning("🎯 QUIZ: Play the opening from memory. Errors will snap back!")
        if st.button("Back to Study"):
            st.session_state.mode = "STUDY"
            st.rerun()
    
    if st.button("Reset Opening"):
        st.session_state.progress = 0
        st.session_state.eval_val = 50
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

with col_eval:
    st.markdown(f"""
        <div class='eval-container'>
            <div class='eval-black-top' style='height: {st.session_state.eval_val}%;'></div>
        </div>
    """, unsafe_allow_html=True)
    st.caption("WHITE")

with col_board:
    # Passing the moves to Javascript
    moves_json = json.dumps(theory_moves)
    
    board_html = f"""
    <link rel="stylesheet" href="https://unpkg.com/@chrisoakman/chessboardjs@1.0.0/dist/chessboard-1.0.0.min.css">
    <script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>
    <script src="https://unpkg.com/@chrisoakman/chessboardjs@1.0.0/dist/chessboard-1.0.0.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/chess.js/0.10.3/chess.min.js"></script>

    <div id="board" style="width: 580px; border: 4px solid #fbbf24; border-radius: 15px; box-shadow: 0 0 30px rgba(251, 191, 36, 0.3);"></div>
    <div id="status" style="color: #fbbf24; margin-top: 15px; font-weight: bold; font-size: 1.2em;"></div>

    <script>
        var game = new Chess();
        var theory = {moves_json};
        var mode = "{st.session_state.mode}";
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

            // Verify against theory
            if (move.san === theory[step]) {{
                step++;
                document.getElementById('status').innerText = "✅ CORRECT";
                
                // If Studying, auto-play the response
                if (mode === "STUDY" && step < theory.length) {{
                    setTimeout(() => {{
                        game.move(theory[step]);
                        board.position(game.fen());
                        step++;
                    }}, 600);
                }}
            }} else {{
                game.undo();
                document.getElementById('status').innerText = "❌ WRONG! NOT THE THEORY.";
                return 'snapback';
            }}
        }}
    </script>
    """
    st.markdown("<div class='premium-card' style='display:flex; justify-content:center;'>", unsafe_allow_html=True)
    components.html(board_html, height=750)
    st.markdown("</div>", unsafe_allow_html=True)
