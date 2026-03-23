from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import pickle
import pandas as pd

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load dataset
movies = pickle.load(open("movies.pkl", "rb"))

# Preprocess
movies['tags'] = movies['tags'].fillna('')
movies['title_lower'] = movies['title'].str.lower()

# 🔥 CREATE similarity (THIS WAS MISSING)
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(movies['tags'])

similarity = cosine_similarity(vectors)

# Recommendation function
def recommend(movie):
    movie = movie.lower()

    if movie not in movies['title_lower'].values:
        return ["Movie not found"]

    idx = movies[movies['title_lower'] == movie].index[0]
    distances = similarity[idx]

    movie_list = sorted(
        list(enumerate(distances)),
        key=lambda x: x[1],
        reverse=True
    )[1:6]

    return [movies.iloc[i[0]].title for i in movie_list]

# Serve frontend
@app.get("/")
def serve_home():
    return FileResponse("index.html")

# API
@app.get("/recommend/{movie}")
def get_recommendation(movie: str):
    try:
        return {"recommendations": recommend(movie)}
    except:
        return {"recommendations": ["Error occurred"]}
