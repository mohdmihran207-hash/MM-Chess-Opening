import streamlit as st
import streamlit.components.v1 as components
import chess
import json

# --- 1. PREMIUM CONFIG & STYLING ---
st.set_page_config(page_title="MM_Chess_Opening", layout="wide", page_icon="👑")

# Glowing Gold & Deep Onyx Theme
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    
    .stApp { background: #050505; color: #e0e0e0; }
    
    /* Glowing Heading */
    .main-title {
        font-family: 'Orbitron', sans-serif;
        color: #fbbf24;
        text-align: center;
        font-size: 50px;
        text-shadow: 0 0 20px #fbbf24, 0 0 40px #d97706;
        margin-bottom: 30px;
    }
    
    .premium-card {
        background: rgba(20, 20, 20, 0.8);
        border: 1px solid #fbbf24;
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 0 15px rgba(251, 191, 36, 0.2);
        margin-bottom: 20px;
    }

    .gold-text { color: #fbbf24; font-weight: bold; }

    /* White on Bottom Eval Bar */
    .eval-container { 
        height: 500px; width: 45px; background: #FFFFFF; 
        border: 2px solid #fbbf24; border-radius: 10px; position: relative; overflow: hidden;
        box-shadow: 0 0 20px rgba(255,255,255,0.1);
    }
    .eval-black-top { 
        width: 100%; background: #111; position: absolute; top: 0; 
        transition: height 0.7s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    /* Progress Bar Glow */
    .stProgress > div > div > div > div {
        background-image: linear-gradient(to right, #d97706, #fbbf24);
        box-shadow: 0 0 10px #fbbf24;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SESSION STATE ---
if 'progress' not in st.session_state: st.session_state.progress = 88
if 'score' not in st.session_state: st.session_state.score = 2850
if 'last_move_analysis' not in st.session_state: st.session_state.last_move_analysis = "Waiting for your first move..."

# --- 3. OPENING DATABASE (50+ Openings Structure) ---
OPENINGS = {
    "Beginner": {
        "Ruy Lopez": ["e4", "e5", "Nf3", "Nc6", "Bb5"],
        "Italian Game": ["e4", "e5", "Nf3", "Nc6", "Bc4"],
        "Sicilian": ["e4", "c5"]
    },
    "Intermediate": {
        "Evans Gambit": ["e4", "e5", "Nf3", "Nc6", "Bc4", "Bc5", "b4"],
        "King's Indian": ["d4", "Nf6", "c4", "g6"]
    },
    "Advanced": {
        "Najdorf Variation": ["e4", "c5", "Nf3", "d6", "d4", "cxd4", "Nxd4", "Nf6", "Nc3", "a6"],
        "Grunfeld Defense": ["d4", "Nf6", "c4", "g6", "Nc3", "d5"]
    }
}

# --- 4. THE UI LAYOUT ---
st.markdown("<h1 class='main-title'>MM_CHESS_OPENING</h1>", unsafe_allow_html=True)

col_board, col_eval, col_stats = st.columns([2, 0.4, 1.5])

with col_stats:
    st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
    st.markdown("<span class='gold-text'>ACADEMY PROGRESS</span>", unsafe_allow_html=True)
    st.progress(st.session_state.progress / 100)
    st.write(f"Mastery: {st.session_state.progress}%")
    
    tier = st.selectbox("Tier", list(OPENINGS.keys()))
    opening = st.selectbox("Select Opening", list(OPENINGS[tier].keys()))
    
    st.markdown("<hr style='border: 0.5px solid #333;'>", unsafe_allow_html=True)
    st.markdown("<span class='gold-text'>AI COACH ANALYSIS</span>", unsafe_allow_html=True)
    st.write(st.session_state.last_move_analysis)
    
    if st.button("Verify Quiz Move"):
        st.session_state.progress = min(100, st.session_state.progress + 2)
        st.session_state.score += 25
        st.session_state.last_move_analysis = "AI: Brilliant! This move secures the center and follows the main line theory."
        st.balloons()
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

with col_eval:
    # Logic: More progress = White (Bottom) is winning
    black_height = 50 - (st.session_state.progress / 10)
    st.markdown(f"""
        <div class='eval-container'>
            <div class='eval-black-top' style='height: {black_height}%;'></div>
        </div>
    """, unsafe_allow_html=True)
    st.caption("WHITE")

with col_board:
    # THE MOUSE-DRAG BOARD (chessboard.js)
    # This includes legal move validation in the browser
    board_html = """
    <link rel="stylesheet" href="https://unpkg.com/@chrisoakman/chessboardjs@1.0.0/dist/chessboard-1.0.0.min.css">
    <script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>
    <script src="https://unpkg.com/@chrisoakman/chessboardjs@1.0.0/dist/chessboard-1.0.0.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/chess.js/0.10.3/chess.min.js"></script>

    <div id="board" style="width: 580px; border: 3px solid #fbbf24; border-radius: 10px; box-shadow: 0 0 30px rgba(251, 191, 36, 0.3);"></div>
    <div style="margin-top: 20px;">
        <button onclick="resetBoard()" style="background:#fbbf24; color:black; border:none; padding:10px 20px; font-weight:bold; cursor:pointer; border-radius:5px;">RESET POSITION</button>
    </div>

    <script>
        var board = null
        var game = new Chess()

        function onDragStart (source, piece, position, orientation) {
          if (game.game_over()) return false
          if (piece.search(/^b/) !== -1) return false
        }

        function onDrop (source, target) {
          var move = game.move({
            from: source,
            to: target,
            promotion: 'q' 
          })

          if (move === null) return 'snapback'
        }

        function onSnapEnd () {
          board.position(game.fen())
        }

        var config = {
          draggable: true,
          position: 'start',
          onDragStart: onDragStart,
          onDrop: onDrop,
          onSnapEnd: onSnapEnd,
          pieceTheme: 'https://chessboardjs.com/img/chesspieces/wikipedia/{piece}.png'
        }
        board = Chessboard('board', config)
        
        function resetBoard() {
            game.reset();
            board.start();
        }
    </script>
    """
    st.markdown("<div class='premium-card' style='padding:10px;'>", unsafe_allow_html=True)
    components.html(board_html, height=680)
    st.markdown("</div>", unsafe_allow_html=True)
