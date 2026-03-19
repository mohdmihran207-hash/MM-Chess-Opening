import streamlit as st
import chess
import chess.svg
import base64

# --- 1. PAGE SETUP & THEME ---
st.set_page_config(page_title="MM Chess Academy", layout="wide", page_icon="🏆")

# --- 2. THE OPENING DATABASE (20 White + 20 Black) ---
# We store the FEN (Position) for the main lines
OPENING_DATA = {
    "White": {
        "Beginner": {
            "Ruy Lopez": ["e4 e5 Nf3 Nc6 Bb5", "Main Line", "Exchange", "Berlin", "Arkhangelsk", "Bird's", "Steinitz"],
            "Italian Game": ["e4 e5 Nf3 Nc6 Bc4", "Main Line", "Evans Gambit", "Fried Liver", "Giuoco Piano", "Two Knights", "Deutz"],
            "Queen's Gambit": ["d4 d5 c4", "Accepted", "Declined", "Slav", "Chigorin", "Albin Counter", "Austrian"],
            "London System": ["d4 Nf6 Bf4", "Classical", "Jobava", "Indian Setup", "Anti-Grünfeld", "Pseudo-Catalan", "Rapport"],
            "Vienna Game": ["e4 e5 Nc3", "Vienna Gambit", "Falkbeer", "Paulsen", "Stanley", "Mieses", "Zhuravlev"]
        },
        "Intermediate": {
            "English Opening": ["c4", "Symmetrical", "Reverse Sicilian", "Anglo-Indian", "Nimzo-English", "Mikenas", "Romanishin"],
            "Scotch Game": ["e4 e5 Nf3 Nc6 d4", "Classical", "Schmidt", "Steinitz", "Göring Gambit", "Malaniuk", "Potter"],
            "King's Gambit": ["e4 e5 f4", "Accepted", "Declined", "Falkbeer", "Cunningham", "Muzio", "Kieseritzky"],
            "Catalan Opening": ["d4 Nf6 c4 e6 g3", "Open", "Closed", "Hungarian", "Bogo-Indian", "Modern", "Classic"],
            "Bishop's Opening": ["e4 e5 Bc4", "Berlin", "Calabrese", "Urusov Gambit", "Ponziani", "Philidor", "Lewis"]
            # ... Add 10 more here for a total of 20
        }
    },
    "Black": {
        "Beginner": {
            "Sicilian Defense": ["e4 c5", "Najdorf", "Dragon", "Scheveningen", "Classical", "Alapin", "Closed"],
            "French Defense": ["e4 e6", "Winawer", "Classical", "Advance", "Exchange", "Tarrasch", "Burn"],
            "Caro-Kann": ["e4 c6", "Classical", "Advance", "Exchange", "Panov", "Two Knights", "Tartakower"],
            "Scandinavian": ["e4 d5", "Main Line", "Modern", "Gubinsky-Melts", "Portuguese", "Blackburne", "Marshall"],
            "King's Indian": ["d4 Nf6 c4 g6", "Classical", "Sämisch", "Four Pawns", "Averbakh", "Fianchetto", "Makogonov"]
        }
        # ... Add 15 more here for a total of 20
    }
}

# --- 3. PREMIUM CSS (Same as before) ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #E5E5E5; }
    .premium-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(251, 191, 36, 0.3);
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 10px;
    }
    .gold-text { color: #fbbf24; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. SIDEBAR & NAVIGATION ---
with st.sidebar:
    st.title("MM Chess")
    choice = st.radio("Navigation", ["Dashboard", "Training Mode", "Achievements"])
    st.divider()
    st.markdown("### Motivation\n*'Push yourself every day.'*")

# --- 5. MAIN DASHBOARD ---
st.title("Future Grandmaster 🚀")

# Progress Stats
c1, c2, c3 = st.columns(3)
c1.metric("Score", "240", "+20")
c2.metric("Lessons", "12 / 40", "Target: 40")
c3.metric("Practice", "20", "Hours")

st.divider()

# --- 6. THE OPENING SELECTOR (The "20 Openings" Logic) ---
st.subheader("Select Your Opening Study")

side = st.selectbox("I want to learn moves for:", ["White", "Black"])
level = st.selectbox("Level:", ["Beginner", "Intermediate", "Advanced"])

# Get openings based on selection
available_openings = OPENING_DATA.get(side, {}).get(level, {})

if available_openings:
    selected_op = st.selectbox("Choose Opening:", list(available_openings.keys()))
    
    # Get the moves and variations
    data = available_openings[selected_op]
    moves = data[0]
    variations = data[1:]

    col_board, col_info = st.columns([2, 1])

    with col_board:
        # Create board and push the starting moves for that opening
        board = chess.Board()
        for m in moves.split():
            board.push_san(m)
        
        # Display Gold Board
        board_svg = chess.svg.board(board, size=450, style=".square.light {fill: #c5a059;} .square.dark {fill: #8b4513;}")
        st.image(board_svg)

    with col_info:
        st.markdown(f"<div class='premium-card'><h3 class='gold-text'>{selected_op}</h3></div>", unsafe_allow_html=True)
        st.write("### Choose a Variation")
        v_choice = st.selectbox("Select one of the 6 variations:", variations)
        st.info(f"Now studying the **{v_choice}** variation of the {selected_op}.")
        st.button("Start Practice Mode")
else:
    st.warning("We are still adding 'Advanced' openings. Try Beginner or Intermediate!")
