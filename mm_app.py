import streamlit as st
import chess

# Branding your app
st.set_page_config(page_title="MM Chess", page_icon="♟️")
st.title("MM: Chess Opening Learner")

# Initialize the board state
if 'fen' not in st.session_state:
    st.session_state.fen = chess.STARTING_FEN

# Draw the board (Text version for the first test)
board = chess.Board(st.session_state.fen)
st.markdown("### Current Board")
st.code(board)

# Input for moves
move = st.text_input("Enter your move (e.g., e4, d4, Nf3):")

if st.button("Play Move"):
    try:
        board.push_san(move)
        st.session_state.fen = board.fen()
        st.success(f"Move {move} played!")
        st.rerun()
    except:
        st.error("Invalid move. Try something like 'e4'.")

if st.button("Reset Game"):
    st.session_state.fen = chess.STARTING_FEN
    st.rerun()
