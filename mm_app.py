import streamlit as st
import chess
import chess.svg

# 1. Page Configuration
st.set_page_config(page_title="MM Chess Academy", layout="wide")

# 2. Premium CSS (The Secret Sauce)
st.markdown("""
    <style>
    /* Main background with dark wood/gold vibe */
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), 
                    url('https://images.unsplash.com/photo-1529699211952-734e80c4d42b?auto=format&fit=crop&q=80&w=2000');
        background-size: cover;
        color: #E5E5E5;
    }
    
    /* Premium Glass Cards */
    .premium-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(251, 191, 36, 0.3);
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
    }

    /* Gold Text */
    .gold-text {
        color: #fbbf24;
        font-family: 'Serif';
        font-weight: bold;
    }

    /* Progress Bar Color */
    .stProgress > div > div > div > div {
        background-color: #fbbf24;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar Navigation (Left side of your image)
with st.sidebar:
    st.markdown("<h1 style='color:#fbbf24;'>MM Chess</h1>", unsafe_allow_html=True)
    st.button("🏠 Dashboard")
    st.button("📖 Openings Library")
    st.button("🏆 Achievements")
    
    st.markdown("---")
    st.markdown("<div class='premium-card'><b>Motivation</b><br>'Push yourself every day.'</div>", unsafe_allow_html=True)

# 4. Main Dashboard Area
st.markdown("<h1 style='text-align: left;'>Future Grandmaster 🚀</h1>", unsafe_allow_html=True)
st.write("Explore our comprehensive chess openings.")

# Top Row: Stats (Score, Lessons, Progress)
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("<div class='premium-card'><span class='gold-text'>Score</span><br><h2>240</h2></div>", unsafe_allow_html=True)
with c2:
    st.markdown("<div class='premium-card'><span class='gold-text'>Progress</span><br><h2>40%</h2></div>", unsafe_allow_html=True)
    st.progress(0.4)
with c3:
    st.markdown("<div class='premium-card'><span class='gold-text'>Lessons Done</span><br><h2>12</h2></div>", unsafe_allow_html=True)

# 5. The "Popular Openings" section
st.markdown("### Popular Openings")
tab1, tab2, tab3 = st.tabs(["White", "Black", "All"])

with tab1:
    col_w1, col_w2 = st.columns(2)
    with col_w1:
        st.markdown("<div class='premium-card'><b>Ruy Lopez</b><br><small>White opens the bishop...</small></div>", unsafe_allow_html=True)
        st.markdown("<div class='premium-card'><b>Italian Game</b><br><small>One of the great moves...</small></div>", unsafe_allow_html=True)
    with col_w2:
        st.markdown("<div class='premium-card'><b>Sicilian Defense</b><br><small>The most popular response...</small></div>", unsafe_allow_html=True)
        st.markdown("<div class='premium-card'><b>Queen's Gambit</b><br><small>One of the oldest openings...</small></div>", unsafe_allow_html=True)

# 6. Learning Board at Bottom
st.divider()
st.subheader("Interactive Practice Board")
board = chess.Board()
board_svg = chess.svg.board(board, size=400, style="""
    .square.light { fill: #d1b48c; }
    .square.dark { fill: #8b4513; }
""")
st.image(board_svg, width=450)
