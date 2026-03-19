import streamlit as st
import chess
import chess.svg
import base64

# --- 1. PAGE SETUP & THEME CONFIG ---
st.set_page_config(page_title="MM Chess Academy", layout="wide", page_icon="🏆")

# A function to get images for background (we are using a placeholder or a very small hosted image to avoid issues).
# For a production app, you can host your own assets for a true 1:1 match.
BG_IMG = "https://images.unsplash.com/photo-1529699211952-734e80c4d42b?q=80&w=2000"

# --- 2. ADVANCED CSS (The Design System) ---
st.markdown(f"""
    <style>
    /* Main background - Dark wood / gold vibe */
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), url('{BG_IMG}');
        background-size: cover;
        background-attachment: fixed;
        color: #E5E5E5;
        font-family: 'Times New Roman', Times, serif; /* Seríf font for classic feel */
    }}

    /* Hide standard Streamlit header and footer */
    header {{ visibility: hidden; }}
    footer {{ visibility: hidden; }}

    /* Gold Metallic Card Style (Glassmorphism + Gold Border) */
    [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"] > div.stMarkdown,
    [data-testid="stColumn"] > div {{
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(200, 160, 50, 0.03) 100%);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(251, 191, 36, 0.3);
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        color: #FFFFFF;
    }}

    /* Global Headings */
    h1, h2, h3, h4 {{
        color: #fbbf24; /* Primary Gold Color */
        font-family: 'Georgia', serif;
    }}

    /* --- SIDEBAR CUSTOMIZATION (Match your Left Menu) --- */
    section[data-testid="stSidebar"] {{
        background: linear-gradient(rgba(0,0,0,0.9), rgba(0,0,0,0.85)), url('{BG_IMG}');
        background-size: cover;
        border-right: 1px solid rgba(251, 191, 36, 0.3);
    }}
    .sidebar-logo {{
        text-align: center;
        margin-bottom: 2rem;
    }}
    .sidebar-item {{
        background: rgba(255, 255, 255, 0.03);
        padding: 15px;
        margin-bottom: 10px;
        border-radius: 8px;
        color: #E5E5E5;
        cursor: pointer;
        display: flex;
        align-items: center;
        border: 1px solid transparent;
    }}
    .sidebar-item:hover {{
        border: 1px solid #fbbf24;
        background: rgba(251, 191, 36, 0.05);
    }}
    .sidebar-item-icon {{
        margin-right: 10px;
        color: #fbbf24;
    }}

    /* --- GOLD CHESSBOARD COLORS (Perfect Match) --- */
    .square.light {{ fill: #c5a059; }} /* Light squares are Bronze/Light Gold */
    .square.dark {{ fill: #8b4513; }}  /* Dark squares are Brown/Mahogany */
    /* Adjust Piece colors if needed, standard SVG is okay for now */
    </style>
    """, unsafe_allow_html=True)


# --- 3. SIDEBAR (The Left Menu from your Image) ---
with st.sidebar:
    st.markdown("""
        <div class='sidebar-logo'>
            <img src='https://via.placeholder.com/100x100.png?text=🏆' width='80'><br>
            <h1>MM Chess</h1>
            <small style='color: #fbbf24;'>ACADEMY</small>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div class='sidebar-item'><span class='sidebar-item-icon'>🏠</span>Dashboard</div>", unsafe_allow_html=True)
    st.markdown("<div class='sidebar-item'><span class='sidebar-item-icon'>📖</span>Openings Library</div>", unsafe_allow_html=True)
    st.markdown("<div class='sidebar-item'><span class='sidebar-item-icon'>🏆</span>Achievements</div>", unsafe_allow_html=True)
    
    st.divider()
    st.markdown("<h4 style='color: #fbbf24;'>Motivation</h4>", unsafe_allow_html=True)
    st.markdown("<p style='font-style: italic; color: #E5E5E5;'>\"Push yourself every day.\"</p>", unsafe_allow_html=True)


# --- 4. MAIN DASHBOARD CONTENT ---

# Top Header
st.markdown("<h1 style='text-align: left;'>Future Grandmaster 🚀</h1>", unsafe_allow_html=True)
st.write("Explore our comprehensive chess openings.")

# Row 1: The Stats Cards (Score, Progress, Lessons)
st.divider()
col1, col2, col3, col4 = st.columns([1, 1.5, 1, 1])

with col1:
    st.markdown("""
        <div class='premium-card'>
            <span style='color: #fbbf24; font-size: 1.2rem; font-weight: bold;'>⭐ Score</span><br>
            <h1 style='font-size: 3rem;'>240</h1>
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class='premium-card'>
            <span style='color: #fbbf24;'>📚 Progress</span><br>
            <h1 style='font-size: 1.5rem;'>40%</h1>
        </div>
        """, unsafe_allow_html=True)
    # Streamlit progress bar (will make this Gold with CSS later)
    st.progress(0.4)

with col3:
    st.markdown("""
        <div class='premium-card'>
            <span style='color: #fbbf24;'>Lessons Completed</span><br>
            <h1 style='font-size: 2.5rem;'>12</h1>
        </div>
        """, unsafe_allow_html=True)

with col4:
    # This acts as the placeholder for the fancy "White to Move" button area
    st.markdown("""
        <div class='premium-card' style='text-align: center; border: 1px solid transparent; background: rgba(251, 191, 36, 0.1);'>
            <span style='color: #E5E5E5;'>Next Lesson:</span><br>
            <span style='color: #fbbf24; font-weight: bold;'>White to move</span>
        </div>
        """, unsafe_allow_html=True)

# --- 5. POPULAR OPENINGS SECTION ---
st.markdown("### Popular Openings")
# In Streamlit we use tabs for the White/Black filter buttons from your image
tab1, tab2, tab3 = st.tabs(["⬜ White Openings", "⬛ Black Openings", "All Openings"])

with tab1:
    col_w1, col_w2 = st.columns(2)
    with col_w1:
        st.markdown("""
            <div class='premium-card' style='margin-bottom: 10px; border-radius: 8px;'>
                <b style='color:#fbbf24;'>Ruy Lopez</b><br>
                <small style='color:#E5E5E5;'>White opens the bishop...</small>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("""
            <div class='premium-card' style='margin-bottom: 10px; border-radius: 8px;'>
                <b style='color:#fbbf24;'>Itlaian Game</b><br>
                <small style='color:#E5E5E5;'>One of the green moments...</small>
            </div>
            """, unsafe_allow_html=True)
        # Add more cards as needed
    with col_w2:
        st.markdown("""
            <div class='premium-card' style='margin-bottom: 10px; border-radius: 8px;'>
                <b style='color:#fbbf24;'>Sicilian Defense</b><br>
                <small style='color:#E5E5E5;'>The most popular response...</small>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("""
            <div class='premium-card' style='margin-bottom: 10px; border-radius: 8px;'>
                <b style='color:#fbbf24;'>Queen's Gambit</b><br>
                <small style='color:#E5E5E5;'>One of the oldest openings...</small>
            </div>
            """, unsafe_allow_html=True)

with tab2:
    st.warning("We need to add the 20 Black Openings here next!")

# --- 6. THE PREMIUM GOLD CHESSBOARD (Perfect Match) ---
# This matches the location of the main training board in your image
st.divider()
st.subheader("Interactive Practice Board")

if 'board' not in st.session_state:
    st.session_state.board = chess.Board()

# Create a clean board SVG with your GOLD/BRONZE color scheme
# We are customizing the standard SVG to match the wood grain
board_svg = chess.svg.board(st.session_state.board, size=450, style="""
    .square.light { fill: #c5a059; } 
    .square.dark { fill: #8b4513; }
""")

# Convert the SVG to Base64 so we can show it as an image easily
b64 = base64.b64encode(board_svg.encode('utf-8')).decode('utf-8')
html = f'<img src="data:image/svg+8b64;base64,{b64}"/>'

# Use a column layout just like your image, board on right
col_empty, col_board = st.columns([1, 1.5])
with col_board:
    st.markdown(html, unsafe_allow_html=True)
    st.button("Learning Mode")
    st.button("Practice Mode")
