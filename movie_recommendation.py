import numpy as np 
import pandas as pd 
import ast
import os

movies = pd.read_csv('tmdb_5000_movies.csv')
credits = pd.read_csv('tmdb_5000_credits.csv')

type(movies)
movies.head(1)

credits.head(1)['cast'].values

movies = movies.merge(credits, on='title')
movies = movies[['movie_id','title','overview','genres','keywords','cast','crew']]
movies.head()

movies.isnull().sum()
movies.dropna(inplace=True)

def convert(text):
    L = []
    for i in ast.literal_eval(text):
        L.append(i['name']) 
    return L 


movies['genres'] = movies['genres'].apply(convert)
movies.head()

movies['keywords'] = movies['keywords'].apply(convert) 
movies.head()

def convert3(text):
    L = []
    counter = 0
    for i in ast.literal_eval(text):
        if counter < 3:
            L.append(i['name'])
        counter+=1
    return L 

movies['cast'] = movies['cast'].apply(convert3)
movies.head()

def fetch_director(text):
    L = []
    counter = 0
    for i in ast.literal_eval(text):
        if i['job'] == 'Director':
            L.append(i['name'])
            break
    return L 
movies['crew'] = movies['crew'].apply(fetch_director)
movies['overview'] = movies['overview'].apply(lambda x:x.split())
movies.head()

movies['genres'] = movies['genres'].apply(lambda x: [i.replace(" ", "") for i in x])
movies['keywords'] = movies['keywords'].apply(lambda x: [i.replace(" ", "") for i in x])
movies['cast'] = movies['cast'].apply(lambda x: [i.replace(" ", "") for i in x])
movies['crew'] = movies['crew'].apply(lambda x: [i.replace(" ", "") for i in x])

movies.head()
movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']
new_df = movies[['movie_id', 'title', 'tags']].copy()

new_df['tags'] = new_df['tags'].apply(lambda x: " ".join(x))
new_df['tags'] = new_df['tags'].apply(lambda x: x.lower())
movies.head()

new_df

import nltk
from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()

def stem(text):
   y = []

   for i in text.split():
       y.append(ps.stem(i))

   return " ".join(y)

type(new_df['tags'].iloc[0])
new_df['tags'] = new_df['tags'].apply(stem)

from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=5000, stop_words='english')

print(new_df.shape)

print(type(new_df['tags'].iloc[0]))

print(new_df['tags'].iloc[0])
print(new_df['tags'].head())

vector = cv.fit_transform(new_df['tags']).toarray()

print(new_df['tags'].iloc[0])

from sklearn.metrics.pairwise import cosine_similarity

similarity = cosine_similarity(vector)
new_df[new_df['title'] == 'The Lego Movie'].index[0]

def recommend(movie):
    index = new_df[new_df['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])),reverse=True,key = lambda x: x[1])
    for i in distances[1:6]:
        print(new_df.iloc[i[0]].title)
        
recommend('Gandhi')
