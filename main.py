from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import pickle
import pandas as pd

app = FastAPI()

# CORS (important)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load data
movies = pickle.load(open("movies.pkl", "rb"))


def recommend(movie):
    movie = movie.lower()
    movies['title_lower'] = movies['title'].str.lower()

    if movie not in movies['title_lower'].values:
        return ["Movie not found"]

    idx = movies[movies['title_lower'] == movie].index[0]
    distances = similarity[idx]

    movie_list = sorted(list(enumerate(distances)), key=lambda x: x[1], reverse=True)[1:6]

    return [movies.iloc[i[0]].title for i in movie_list]

# Serve HTML
@app.get("/")
def serve_home():
    return FileResponse("index.html")

# API
@app.get("/recommend/{movie}")
def get_recommendation(movie: str):
    return {"recommendations": recommend(movie)}
