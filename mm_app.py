import streamlit as st
import chess
import chess.svg
import base64

# --- 1. PREMIUM PAGE CONFIG ---
st.set_page_config(page_title="MM Chess Academy", layout="wide", page_icon="🏆")

# --- 2. THE MASTER DATABASE (50 OPENINGS TOTAL) ---
OPENINGS = {
    "White": {
        "Beginner (5)": {
            "Ruy Lopez": ["e4 e5 Nf3 Nc6 Bb5", "Main Line", "Exchange", "Berlin", "Arkhangelsk", "Bird's", "Steinitz"],
            "Italian Game": ["e4 e5 Nf3 Nc6 Bc4", "Main Line", "Evans Gambit", "Fried Liver", "Giuoco Piano", "Two Knights", "Deutz"],
            "Queen's Gambit": ["d4 d5 c4", "Accepted", "Declined", "Slav", "Chigorin", "Albin Counter", "Austrian"],
            "London System": ["d4 Nf6 Bf4", "Classical", "Jobava", "Indian Setup", "Anti-Grünfeld", "Pseudo-Catalan", "Rapport"],
            "Vienna Game": ["e4 e5 Nc3", "Vienna Gambit", "Falkbeer", "Paulsen", "Stanley", "Mieses", "Zhuravlev"]
        },
        "Intermediate (15)": {
            "English Opening": ["c4", "Symmetrical", "Reverse Sicilian", "Anglo-Indian", "Nimzo-English", "Mikenas", "Romanishin"],
            "Scotch Game": ["e4 e5 Nf3 Nc6 d4", "Classical", "Schmidt", "Göring", "Malaniuk", "Potter", "Steinitz"],
            "King's Gambit": ["e4 e5 f4", "Accepted", "Declined", "Falkbeer", "Cunningham", "Muzio", "Kieseritzky"],
            "Catalan Opening": ["d4 Nf6 c4 e6 g3", "Open", "Closed", "Hungarian", "Bogo-Indian", "Modern", "Classic"],
            "Evans Gambit": ["e4 e5 Nf3 Nc6 Bc4 Bc5 b4", "Accepted", "Declined", "Tartakower", "Richardson", "Pierce", "Stone"],
            "Scandinavian": ["e4 d5", "Main Line", "Modern", "Gubinsky-Melts", "Portuguese", "Blackburne", "Marshall"],
            "Alekhine Defense": ["e4 Nf6", "Modern", "Exchange", "Four Pawns", "Alburt", "Scandinavian", "Mokele"],
            "Benko Gambit": ["d4 Nf6 c4 c5 d5 b5", "Accepted", "Declined", "Zaitsev", "Nescafe Frappe", "Fully Accepted", "Modern"],
            "Grünfeld Defense": ["d4 Nf6 c4 g6 Nc3 d5", "Exchange", "Russian", "Taimanov", "Brinckmann", "Stockholm", "Closed"],
            "Nimzo-Indian": ["d4 Nf6 c4 e6 Nc3 Bb4", "Classical", "Rubinstein", "Sämisch", "Kasparov", "Leningrad", "Spielmann"],
            "Dutch Defense": ["d4 f5", "Leningrad", "Stonewall", "Classical", "Staunton Gambit", "Hopton", "Ilyin-Zhenevsky"],
            "Bird's Opening": ["f4", "Dutch Variation", "From's Gambit", "Lasker", "Williams", "Swiss", "Polar Bear"],
            "Benoni Defense": ["d4 Nf6 c4 c5 d5 e6", "Modern", "Classical", "Four Pawns", "Taimanov", "Fianchetto", "Knight's Tour"],
            "Trompowsky Attack": ["d4 Nf6 Bg5", "Classical", "Big Center", "Vaganian", "Poisoned Pawn", "Raptor", "Borg"],
            "Petrov's Defense": ["e4 e5 Nf3 Nf6", "Classical", "Steinitz", "Three Knights", "Modern", "Stafford Gambit", "Karklins"]
        },
        "Advanced (5)": {
            "Reti Opening": ["Nf3 d5 c4", "King's Indian", "Symmetrical", "London", "Capablanca", "Lasker", "Advance"],
            "King's Indian Attack": ["Nf3 d5 g3", "Closed", "French Structure", "Sicilian Structure", "Yugoslav", "Spassky", "Modern"],
            "Larsen's Opening": ["b3", "Classical", "Modern", "Indian", "English", "Symmetrical", "Polish"],
            "Smith-Morra Gambit": ["e4 c5 d4 cxd4 c3", "Accepted", "Declined", "Siberian Trap", "Chicago", "Finegold", "Morphy"],
            "Grob's Attack": ["g4", "Standard", "Romford", "Spike", "Keene", "Zilbermints", "Fritz"]
        }
    },
    "Black": {
        "Beginner (5)": {
            "Sicilian Defense": ["e4 c5", "Najdorf", "Dragon", "Scheveningen", "Classical", "Alapin", "Closed"],
            "French Defense": ["e4 e6", "Winawer", "Classical", "Advance", "Exchange", "Tarrasch", "Burn"],
            "Caro-Kann": ["e4 c6", "Classical", "Advance", "Exchange", "Panov", "Two Knights", "Tartakower"],
            "Scandinavian": ["e4 d5", "Main Line", "Modern", "Gubinsky-Melts", "Portuguese", "Blackburne", "Marshall"],
            "King's Indian": ["d4 Nf6 c4 g6", "Classical", "Sämisch", "Four Pawns", "Averbakh", "Fianchetto", "Makogonov"]
        },
        "Intermediate (15)": {
            "Modern Defense": ["e4 g6 d4 Bg7", "Standard", "Averbakh", "Pirc Transition", "Three Pawns", "Gurgenidze", "Mad Dog"],
            "Pirc Defense": ["e4 d6 d4 Nf6 Nc3 g6", "Austrian Attack", "Classical", "150 Attack", "Byrne", "Argentine", "Holmov"],
            "Nimzowitsch Defense": ["e4 Nc6", "Kennedy", "Declined", "Scandinavian", "Lean", "Colorado", "Wheeler"],
            "Philidor Defense": ["e4 e5 Nf3 d6", "Antoshin", "Hanham", "Exchange", "Larsen", "Berger", "Lion"],
            "Bogo-Indian": ["d4 Nf6 c4 e6 Nf3 Bb4+", "Nimzowitsch", "Vitolinsh", "Wade", "Grunfeld-style", "Modern", "Exchange"],
            "Chigorin Defense": ["d4 d5 c4 Nc6", "Janowski", "Costa", "Romford", "Alatortsev", "Leningrad", "Marshall"],
            "Albin Counter-Gambit": ["d4 d5 c4 e5", "Lasker Trap", "Spassky", "Keres", "Modern", "Exchange", "Janowski"],
            "Budapest Gambit": ["d4 Nf6 c4 e5", "Adler", "Rubinstein", "Fajarowicz", "Alekhine", "Sajtar", "Main Line"],
            "Old Indian": ["d4 Nf6 c4 d6", "Janowski", "Ukrainian", "Tartakower", "Main Line", "Exchange", "Fianchetto"],
            "Owen's Defense": ["e4 b6", "Guatemala", "Matov", "Wind", "Smith", "Modern", "Classical"],
            "Englund Gambit": ["d4 e5", "Soller", "Felbecker", "Zilbermints", "Hartlaub", "Blackburne", "Main Line"],
            "Rat Defense": ["d4 d6", "Spike", "Balogh", "English", "Lisitsin", "Modern", "Classical"],
            "St. George Defense": ["e4 a6", "Three Pawns", "Italian Style", "Sicilian Style", "Classic", "Modern", "Transfer"],
            "Hippopotamus": ["e4 e6 d4 d6", "Closed", "Flexible", "Symmetrical", "Fianchetto", "Mountain", "River"],
            "Polish Defense": ["d4 b5", "Spassky", "Tartakower", "Modern", "Exchange", "Symmetrical", "Classical"]
        },
        "Advanced (5)": {
            "Grunfeld Defense": ["d4 Nf6 c4 g6 Nc3 d5", "Exchange", "Russian", "Taimanov", "Brinckmann", "Stockholm", "Closed"],
            "Nimzo-Indian": ["d4 Nf6 c4 e6 Nc3 Bb4", "Classical", "Rubinstein", "Sämisch", "Kasparov", "Leningrad", "Spielmann"],
            "Benoni Defense": ["d4 Nf6 c4 c5 d5 e6", "Modern", "Classical", "Four Pawns", "Taimanov", "Fianchetto", "Knight's Tour"],
            "Dutch Defense": ["d4 f5", "Leningrad", "Stonewall", "Classical", "Staunton Gambit", "Hopton", "Ilyin-Zhenevsky"],
            "Benko Gambit": ["d4 Nf6 c4 c5 d5 b5", "Accepted", "Declined", "Zaitsev", "Nescafe Frappe", "Fully Accepted", "Modern"]
        }
    }
}

# --- 3. THE PREMIUM CSS ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), 
                    url('https://images.unsplash.com/photo-1529699211952-734e80c4d42b?q=80&w=2000');
        background-size: cover; background-attachment: fixed; color: #E5E5E5;
    }
    .premium-card {
        background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(12px);
        border: 1px solid rgba(251, 191, 36, 0.3); border-radius: 15px;
        padding: 20px; margin-bottom: 15px;
    }
    .gold-text { color: #fbbf24; font-family: 'Georgia', serif; font-weight: bold; }
    h1, h2, h3 { color: #fbbf24; }
    .stButton>button { background: rgba(251, 191, 36, 0.1); border: 1px solid #fbbf24; color: white; width: 100%; border-radius: 8px; }
    .stButton>button:hover { background: #fbbf24 !important; color: black !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. SESSION STATE (Score Tracking) ---
if 'score' not in st.session_state: st.session_state.score = 240
if 'lessons' not in st.session_state: st.session_state.lessons = 12

# --- 5. SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='text-align:center;'>MM Chess</h1><p style='text-align:center; color:#fbbf24;'>ACADEMY</p>", unsafe_allow_html=True)
    st.divider()
    st.markdown("<div class='premium-card'><span class='gold-text'>Motivation</span><br><i>'Push yourself every day.'</i></div>", unsafe_allow_html=True)
    side = st.radio("Choose Side", ["White", "Black"])
    level = st.radio("Skill Level", ["Beginner (5)", "Intermediate (15)", "Advanced (5)"])

# --- 6. DASHBOARD ---
st.markdown("<h1>Future Grandmaster 🚀</h1>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1: st.markdown(f"<div class='premium-card'><span class='gold-text'>Score</span><br><h2>{st.session_state.score}</h2></div>", unsafe_allow_html=True)
with c2: st.markdown(f"<div class='premium-card'><span class='gold-text'>Lessons Done</span><br><h2>{st.session_state.lessons} / 50</h2></div>", unsafe_allow_html=True)
with c3: st.markdown(f"<div class='premium-card'><span class='gold-text'>Progress</span><br><h2>{int((st.session_state.lessons/50)*100)}%</h2></div>", unsafe_allow_html=True)

# --- 7. SELECTOR & BOARD ---
available = OPENINGS.
