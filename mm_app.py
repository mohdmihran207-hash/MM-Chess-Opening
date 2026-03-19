import streamlit as st
import chess
import chess.svg

# Branding
st.set_page_config(page_title="MM Chess", page_icon="♟️")
st.title("MM: Chess Opening Learner")

# Start the game logic
if 'board' not in st.session_state:
    st.session_state.board = chess.Board()

# Create two columns: one for the board, one for info
col1, col2 = st.columns([2, 1])

with col1:
    # This creates a clean SVG image of the board
    board_svg = chess.svg.board(st.session_state.board, size=400)
    st.image(board_svg, use_container_width=True)

with col2:
    st.subheader("Controls")
    move = st.text_input("Enter Move (e.g. e4, Nf3):", key="move_input")
    
    if st.button("Play Move"):
        try:
            st.session_state.board.push_san(move)
            st.rerun()
        except:
            st.error("Invalid move!")

    if st.button("Reset MM Board"):
        st.session_state.board.reset()
        st.rerun()

# This part will tell you the Opening Name (Basic version)
fen = st.session_state.board.fen()
if fen.startswith("rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR"):
    st.info("Opening: King's Pawn Opening (1. e4)")
elif fen.startswith("rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR"):
    st.info("Opening: Queen's Pawn Opening (1. d4)")
