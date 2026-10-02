# Movie Recommendation System

A content-based movie recommendation system built with Python. It recommends movies based on their genres, keywords, overview, cast, and director.

## Features

- Recommends 5 similar movies
- Uses movie genres, keywords, cast, and director
- Text preprocessing and stemming
- Uses CountVectorizer for feature extraction
- Uses Cosine Similarity to find similar movies

## Technologies

- Python
- Pandas
- NumPy
- NLTK
- Scikit-learn

## Dataset

TMDB 5000 Movies and Credits dataset.

## How It Works

1. Load and merge the movie and credits datasets.
2. Extract genres, keywords, cast, and director.
3. Combine these features with the movie overview.
4. Clean and stem the text.
5. Convert text into numerical vectors using CountVectorizer.
6. Calculate similarity using Cosine Similarity.
7. Recommend the top 5 similar movies.

## 📸 Screenshots

### Recommendation Output
![Recommendation Output](screenshots/recommendation.png)

### Movie Data
![Movie Data](screenshots/movies.png)
