
import streamlit as st
import pandas as pd
import ast
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide"
)

@st.cache_data
def load_data():
    movies = pd.read_csv("tmdb_5000_movies.csv")
    credits = pd.read_csv("tmdb_5000_credits.csv")

    movies = movies.merge(credits, on="title")
    movies = movies[
        ["movie_id", "title", "overview",
         "genres", "keywords", "cast", "crew"]
    ]

    movies.dropna(inplace=True)

    def convert(text):
        return [item["name"] for item in ast.literal_eval(text)]

    def convert_cast(text):
        return [
            item["name"]
            for item in ast.literal_eval(text)[:3]
        ]

    def fetch_director(text):
        for item in ast.literal_eval(text):
            if item["job"] == "Director":
                return [item["name"]]
        return []

    movies["genres"] = movies["genres"].apply(convert)
    movies["keywords"] = movies["keywords"].apply(convert)
    movies["cast"] = movies["cast"].apply(convert_cast)
    movies["crew"] = movies["crew"].apply(fetch_director)
    movies["overview"] = movies["overview"].apply(
        lambda x: x.split()
    )

    for column in ["genres", "keywords", "cast", "crew"]:
        movies[column] = movies[column].apply(
            lambda items: [item.replace(" ", "") for item in items]
        )

    movies["tags"] = (
        movies["overview"]
        + movies["genres"]
        + movies["keywords"]
        + movies["cast"]
        + movies["crew"]
    )

    new_df = movies[["movie_id", "title", "tags"]].copy()
    new_df["tags"] = new_df["tags"].apply(
        lambda items: " ".join(items).lower()
    )

    ps = PorterStemmer()

    def stem(text):
        return " ".join(ps.stem(word) for word in text.split())

    new_df["tags"] = new_df["tags"].apply(stem)

    return new_df


@st.cache_resource
def create_vectors(tags):
    cv = CountVectorizer(
        max_features=5000,
        stop_words="english"
    )
    vectors = cv.fit_transform(tags)
    return vectors


st.title("🎬 Movie Recommender System")
st.write(
    "Select a movie and discover five similar movies "
    "based on genres, story, cast and keywords."
)

try:
    with st.spinner("Loading movie database..."):
        movies = load_data()
        vectors = create_vectors(movies["tags"].tolist())

    selected_movie = st.selectbox(
        "Choose a movie",
        sorted(movies["title"].unique())
    )

    if st.button("Recommend Movies", type="primary"):
        index = movies[movies["title"] == selected_movie].index[0]

        scores = cosine_similarity(
            vectors[index], vectors
        ).flatten()

        similar_indices = scores.argsort()[::-1]
        recommendations = []

        for i in similar_indices:
            if i != index:
                title = movies.iloc[i]["title"]
                if title not in recommendations:
                    recommendations.append(title)
                if len(recommendations) == 5:
                    break

        st.subheader("Movies You May Like")

        columns = st.columns(5)

        for column, title in zip(columns, recommendations):
            with column:
                st.markdown("### 🎥")
                st.write(title)

except FileNotFoundError:
    st.error(
        "Dataset files are missing. Please upload "
        "tmdb_5000_movies.csv and tmdb_5000_credits.csv "
        "to your GitHub repository."
    )
except Exception as error:
    st.error(f"Something went wrong: {error}")
