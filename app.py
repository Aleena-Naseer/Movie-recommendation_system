
import streamlit as st
import pickle
import pandas as pd
import base64
from pathlib import Path
from html import escape

st.set_page_config(
    page_title="CineMatch | Discover Your Next Film",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

BASE_DIR = Path(__file__).resolve().parent

@st.cache_resource
def load_data():
    with open(BASE_DIR / "movie_dict.pkl", "rb") as file:
        movie_dict = pickle.load(file)

    with open(BASE_DIR / "top_similar.pkl", "rb") as file:
        top_similar = pickle.load(file)

    movie_df = pd.DataFrame(movie_dict)
    return movie_df, top_similar


movies, top_similar = load_data()


def get_background():
    image_path = BASE_DIR / "assets" / "cinema.jpg"

    if not image_path.exists():
        return ""

    with open(image_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode("utf-8")

    suffix = image_path.suffix.lower()
    image_type = "image/png" if suffix == ".png" else "image/jpeg"

    return f"data:{image_type};base64,{encoded}"


background_image = get_background()



def recommend(movie):
    matches = movies.index[movies["title"] == movie]

    if len(matches) == 0:
        return []

    movie_index = matches[0]
    recommended_indices = top_similar[movie_index][:5]

    results = []

    for index in recommended_indices:
        title = movies.iloc[index]["title"]

        if title not in results:
            results.append(title)

    return results

# ---------------- CSS ----------------
background_css = (
    f"""
    background-image:        linear-gradient(
            180deg,
            rgba(8, 10, 12, 0.66),
            rgba(8, 10, 12, 0.94) 480px,
            #080a0c 100%
        ),
        url("{background_image}");
    """
    if background_image
    else "background: radial-gradient(ellipse at top, #22231f, #080a0c 65%);"
)

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');

:root {{
    --gold: #d7b56d;
    --gold-light: #f0d99c;
    --surface: rgba(20, 22, 24, 0.90);
    --border: rgba(215, 181, 109, 0.23);
    --muted: #a3a5a7;
    --white: #f6f4ef;
}}

.stApp {{
    {background_css}
    background-size: cover;
    background-position: center top;
    background-attachment: fixed;
    background-repeat: no-repeat;
    color: var(--white);
    font-family: 'DM Sans', sans-serif;
}}

.block-container {{
    max-width: 1320px;
    padding: 1.5rem 2rem 3rem;
}}

#MainMenu, footer {{
    visibility: hidden;
}}

header[data-testid="stHeader"] {{
    background: transparent;
}}

div[data-testid="stDecoration"] {{
    display: none;
}}

/* Navigation-style brand */
.brand {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.65rem 0 1.2rem;
    border-bottom: 1px solid rgba(255,255,255,0.10);
    margin-bottom: 2.7rem;
}}

.brand-name {{
    font-size: 1.25rem;
    font-weight: 700;
    letter-spacing: 1.8px;
    color: var(--white);
}}

.brand-name span {{
    color: var(--gold);
}}

.brand-tag {{
    font-size: 0.72rem;
    letter-spacing: 2px;
    color: #b7b6ae;
    text-transform: uppercase;
}}

/* Hero */
.hero {{
    text-align: center;
    padding: 2.8rem 0 2.6rem;
}}

.eyebrow {{
    color: var(--gold);
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 4px;
    text-transform: uppercase;
    margin-bottom: 1.3rem;
}}

.hero h1 {{
    font-family: 'Playfair Display', Georgia, serif;
    font-size: clamp(2.7rem, 6vw, 5.1rem);
    font-weight: 600;
    line-height: 1.12;
    letter-spacing: -1.7px;
    color: #fffdf8;
    margin: 0;
}}

.hero h1 span {{
    color: var(--gold-light);
}}

.hero p {{
    max-width: 590px;
    margin: 1.4rem auto 0;
    color: #c0c0bd;
    font-size: 1rem;
    line-height: 1.9;
}}

/* Search panel */
.search-panel {{
    max-width: 800px;
    margin: 0 auto 3.5rem;
    padding: 1.7rem;
    background: rgba(15, 17, 18, 0.89);
    border: 1px solid var(--border);
    border-radius: 18px;
    box-shadow: 0 18px 60px rgba(0,0,0,0.24);
}}

.panel-label {{
    color: var(--gold-light);
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 1.25rem;
    margin-bottom: 0.4rem;
}}

.panel-caption {{
    color: var(--muted);
    font-size: 0.86rem;
    margin-bottom: 1.3rem;
}}

/* Dropdown */
div[data-baseweb="select"] > div {{
    background: #17191b;
    border: 1px solid #45433a;
    border-radius: 10px;
    min-height: 49px;
}}

div[data-baseweb="select"] > div:hover {{
    border-color: var(--gold);
}}

div[data-baseweb="select"] * {{
    color: #f7f5ef;
}}

/* Recommend button */
.stButton > button {{
    width: 100%;
    min-height: 49px;
    border-radius: 10px;
    border: 1px solid var(--gold);
    background: linear-gradient(110deg, #f0d99c, #c7a354);
    color: #17140d;
    font-weight: 700;
    font-size: 0.96rem;
    transition: all 0.2s ease;
}}

.stButton > button:hover {{
    background: linear-gradient(110deg, #f8e8ba, #dfbd70);
    border-color: #f8e8ba;
    color: #111;
    box-shadow: 0 7px 24px rgba(215,181,109,0.18);
    transform: translateY(-1px);
}}

/* Recommendations section */
.section-title {{
    font-family: 'Playfair Display', Georgia, serif;
    color: #f8f5ed;
    font-size: clamp(1.65rem, 3vw, 2.15rem);
    font-weight: 600;
    margin: 0 0 0.45rem;
}}

.section-caption {{
    color: var(--muted);
    font-size: 0.88rem;
    margin-bottom: 1.5rem;
}}

.gold-line {{
    width: 48px;
    height: 2px;
    background: var(--gold);
    margin: 0.9rem 0 1.1rem;
}}

/* Movie cards */
.movie-card {{
    min-height: 205px;
    height: 100%;
    padding: 1.3rem 1rem;
    border-radius: 14px;
    background: linear-gradient(
        150deg,
        rgba(31, 32, 31, 0.97),
        rgba(14, 16, 17, 0.97)
    );
    border: 1px solid rgba(215,181,109,0.20);
    box-shadow: 0 8px 24px rgba(0,0,0,0.12);
    overflow-wrap: anywhere;
    transition: transform 0.22s ease, border-color 0.22s ease;
}}

.movie-card:hover {{
    transform: translateY(-4px);
    border-color: rgba(215,181,109,0.72);
}}

.card-top {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
}}

.card-number {{
    color: var(--gold);
    font-size: 0.76rem;
    font-weight: 700;
    letter-spacing: 1.5px;
}}

.card-symbol {{
    color: var(--gold);
    font-size: 1.3rem;
}}

.card-title {{
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 1.08rem;
    font-weight: 600;
    line-height: 1.5;
    color: #faf8f1;
    margin-bottom: 0.7rem;
}}

.card-caption {{
    color: #a4a49d;
    font-size: 0.76rem;
    line-height: 1.5;
}}

/* Empty state */
.empty-state {{
    text-align: center;
    padding: 1.4rem;
    color: #aaa99f;
    background: rgba(20,22,24,0.72);
    border: 1px solid var(--border);
    border-radius: 12px;
}}

/* Footer */
.app-footer {{
    margin-top: 4rem;
    padding: 1.5rem 0 0.7rem;
    border-top: 1px solid rgba(255,255,255,0.10);
    text-align: center;
    color: #92938e;
    font-size: 0.8rem;
    line-height: 2;
}}

.app-footer span {{
    color: var(--gold);
    letter-spacing: 2px;
    font-weight: 700;
}}

/* Responsive */
@media (max-width: 768px) {{
    .block-container {{
        padding: 1rem 1rem 2rem;
    }}

    .brand {{
        margin-bottom: 1.5rem;
    }}

    .brand-tag {{
        font-size: 0.58rem;
        letter-spacing: 1px;
    }}

    .hero {{
        padding: 1.7rem 0 2rem;
    }}

    .hero h1 {{
        letter-spacing: -0.7px;
    }}

    .hero p {{
        font-size: 0.91rem;
    }}

    .search-panel {{
        padding: 1.15rem;
        margin-bottom: 2.5rem;
    }}

    .movie-card {{
        min-height: 160px;
        padding: 1rem 0.8rem;
    }}

    .card-title {{
        font-size: 0.95rem;
    }}
}}

@media (prefers-reduced-motion: reduce) {{
    .movie-card, .stButton > button {{
        transition: none;
    }}
}}
</style>
""", unsafe_allow_html=True)


# ---------------- BRAND ----------------
st.markdown("""
<div class="brand">
    <div class="brand-name">CINE<span>MATCH</span></div>
</div>
""", unsafe_allow_html=True)


# ---------------- HERO ----------------
st.markdown("""
<div class="hero">
    <div class="eyebrow">✦ Curated for your next movie night ✦</div>
    <h1>Find Your Next<br><span>Favorite Film.</span></h1>
    <p>
        Every great movie leads to another.
        Choose a film you love and discover five similar titles
        selected by your recommendation engine.
    </p>
</div>
""", unsafe_allow_html=True)


# ---------------- MOVIE SELECTOR ----------------
st.markdown("""
""", unsafe_allow_html=True)

selected_movie_name = st.selectbox(
    "Choose a movie",
    movies["title"].dropna().values,
    label_visibility="collapsed",
    key="movie_selector"
)

if st.button("✦   Discover Recommendations", use_container_width=True):
    st.session_state["recommendations"] = recommend(selected_movie_name)
    st.session_state["selected_title"] = selected_movie_name


# ---------------- RECOMMENDATIONS ----------------
if "recommendations" in st.session_state:
    recommendations = st.session_state["recommendations"]
    selected_title = st.session_state["selected_title"]

    st.markdown(
        f'<div class="section-title">Films picked for you</div>'
        f'<div class="gold-line"></div>'
        f'<div class="section-caption">Because you selected '
        f'<strong>{escape(str(selected_title))}</strong> · ',
        unsafe_allow_html=True
    )

    if recommendations:
        columns = st.columns(5, gap="medium")

        for index, movie in enumerate(recommendations):
            safe_movie = escape(str(movie))

            with columns[index]:
                st.markdown(f"""
                <div class="movie-card">
                    <div class="card-top">
                        <div class="card-number">{index + 1:02d}</div>
                    </div>
                    <div class="card-title">{safe_movie}</div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.markdown(
            '<div class="empty-state">'
            'No recommendations found for this selection.'
            '</div>',
            unsafe_allow_html=True
        )


# ---------------- FOOTER ----------------
st.markdown("""
<div class="app-footer">
    <span>CINEMATCH</span><br>
    A little inspiration for your next movie night.
</div>
""", unsafe_allow_html=True)
