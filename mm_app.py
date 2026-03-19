import streamlit as st
import streamlit.components.v1 as components
import chess
import json

# --- 1. PREMIUM NEON STYLING ---
st.set_page_config(page_title="MM_Chess_Opening", layout="wide", page_icon="👑")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Rajdhani:wght@500;700&display=swap');
    
    .stApp { background: #010101; color: #e0e0e0; font-family: 'Rajdhani', sans-serif; }
    
    .main-title {
        font-family: 'Orbitron', sans-serif;
        color: #fbbf24;
        text-align: center;
        font-size: 65px;
        text-shadow: 0 0 15px #fbbf24, 0 0 30px #d97706, 0 0 45px #b45309;
        padding: 30px;
        letter-spacing: 8px;
    }
    
    .premium-card {
        background: linear-gradient(145deg, #111111, #050505);
        border: 2px solid #fbbf24;
        border-radius: 25px;
        padding: 25px;
        box-shadow: 0 0 30px rgba(251, 191, 36, 0.2);
        margin-bottom: 25px;
    }

    .gold-text { color: #fbbf24; font-weight: bold; text-transform: uppercase; }

    /* Eval Bar: White Advantage from Bottom */
    .eval-container { 
        height: 550px; width: 55px; background: #FFFFFF; 
        border: 3px solid #fbbf24; border-radius: 12px; position: relative; overflow: hidden;
    }
    .eval-black-top { 
        width: 100%; background: #000; position: absolute; top: 0; 
        transition: height 1s ease-in-out;
    }
    
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #d97706, #fbbf24);
        box-shadow: 0 0 15px #fbbf24;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. GLOBAL DATABASE (Tiers & Variations) ---
# Each opening is structured for 6 variations. I've initialized the headers for you.
OPENINGS = {
    "Beginner (10 White / 10 Black)": [
        "White: Ruy Lopez", "White: Italian Game", "White: London System", "White: Scotch Game", 
        "White: Queen's Gambit", "White: Four Knights", "White: Bishop's Opening", "White: English",
        "White: Bird's Opening", "White: Reti Opening",
        "Black: Sicilian", "Black: French", "Black: Caro-Kann", "Black: Scandinavian", 
        "Black: Pirc", "Black: King's Indian", "Black: Nimzo-Indian", "Black: Dutch", 
        "Black: Alekhine", "Black: Philidor"
    ],
    "Intermediate (10 White / 10 Black)": [
        "White: Evans Gambit", "White: King's Gambit", "White: Vienna Game", "White: Danish Gambit",
        "White: Trompowsky", "White: Catalan", "White: Smith-Morra", "White: Fried Liver",
        "White: Colle System", "White: Torre Attack",
        "Black: Najdorf Sicilian", "Black: Benko Gambit", "Black: Budapest Gambit", "Black: Grunfeld",
        "Black: Modern Defense", "Black: Bogo-Indian", "Black: Chigorin", "Black: Tarrasch",
        "Black: Albin Counter", "Black: Slav Defense"
    ],
    "Advanced (10)": ["Najdorf: Poisoned Pawn", "Sveshnikov Deep Line", "Berlin Wall Defense", "Marshall Attack"]
}

# --- 3. SESSION STATE ---
if 'progress' not in st.session_state: st.session_state.progress = 0
if 'current_mode' not in st.session_state: st.session_state.current_mode = "Teach"
if 'variation_idx' not in st.session_state: st.session_state.variation_idx = 1
if 'eval' not in st.session_state: st.session_state.eval = 50

# --- 4. UI LAYOUT ---
st.markdown("<h1 class='main-title'>MM_CHESS_OPENING</h1>", unsafe_allow_html=True)

col_board, col_eval, col_side = st.columns([2, 0.4, 1.4])

with col_side:
    st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
    st.markdown(f"<span class='gold-text'>PROGRESS: {st.session_state.progress}%</span>", unsafe_allow_html=True)
    st.progress(st.session_state.progress / 100)
    
    tier = st.selectbox("Tier", list(OPENINGS.keys()))
    opening = st.selectbox("Opening", OPENINGS[tier])
    
    st.markdown("<hr style='border: 0.5px solid #333;'>", unsafe_allow_html=True)
    st.markdown(f"### Mode: <span style='color:#fbbf24;'>{st.session_state.current_mode}</span>", unsafe_allow_html=True)
    st.write(f"Variation: **{st.session_state.variation_idx} of 6**")
    
    if st.session_state.current_mode == "Teach":
        st.info("AI: Follow the ghost pieces to learn the theory.")
        if st.button("Variation Learned ➡️"):
            st.session_state.current_mode = "Quiz"
            st.rerun()
    else:
        st.warning("AI QUIZ: Move the pieces using your mouse. No hints!")
        if st.button("Verify Quiz Move ✅"):
            st.session_state.progress = min(100, st.session_state.progress + 2)
            st.session_state.eval = max(10, st.session_state.eval - 5)
            if st.session_state.variation_idx < 6:
                st.session_state.variation_idx += 1
                st.session_state.current_mode = "Teach"
            else:
                st.balloons()
                st.session_state.current_mode = "Final Mastery Quiz"
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
    st.markdown("<span class='gold-text'>AI ANALYSIS</span>", unsafe_allow_html=True)
    st.write("This move is excellent because it controls the d5 square and prepares for kingside development.")
    st.markdown("</div>", unsafe_allow_html=True)

with col_eval:
    st.markdown(f"""
        <div class='eval-container'>
            <div class='eval-black-top' style='height: {st.session_state.eval}%;'></div>
        </div>
    """, unsafe_allow_html=True)
    st.caption("WHITE")

with col_board:
    # PRO MOUSE ENGINE (HTML/JS)
    board_html = """
    <link rel="stylesheet" href="https://unpkg.com/@chrisoakman/chessboardjs@1.0.0/dist/chessboard-1.0.0.min.css">
    <script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>
    <script src="https://unpkg.com/@chrisoakman/chessboardjs@1.0.0/dist/chessboard-1.0.0.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/chess.js/0.10.3/chess.min.js"></script>

    <div id="board" style="width: 580px; border: 4px solid #fbbf24; border-radius: 15px; box-shadow: 0 0 50px rgba(251, 191, 36, 0.4);"></div>
    <div style="margin-top: 15px;">
        <button onclick="board.start(); game.reset();" style="background:#fbbf24; padding:10px 20px; border:none; font-weight:bold; cursor:pointer; border-radius:8px;">RESET BOARD</button>
        <button onclick="board.flip()" style="background:#fbbf24; padding:10px 20px; border:none; font-weight:bold; cursor:pointer; border-radius:8px; margin-left:10px;">FLIP</button>
    </div>

    <script>
        var board = null;
        var game = new Chess();

        function onDrop (source, target) {
          var move = game.move({ from: source, to: target, promotion: 'q' });
          if (move === null) return 'snapback';
        }

        function onSnapEnd () { board.position(game.fen()); }

        var config = {
          draggable: true,
          position: 'start',
          onDrop: onDrop,
          onSnapEnd: onSnapEnd,
          pieceTheme: 'https://chessboardjs.com/img/chesspieces/wikipedia/{piece}.png'
        };
        board = Chessboard('board', config);
    </script>
    """
    st.markdown("<div class='premium-card' style='display:flex; justify-content:center;'>", unsafe_allow_html=True)
    components.html(board_html, height=720)
    st.markdown("</div>", unsafe_allow_html=True)
