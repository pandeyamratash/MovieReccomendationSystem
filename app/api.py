# pyright: reportMissingImports=false

from pathlib import Path

import numpy as np
from scipy import sparse
from sklearn.metrics.pairwise import linear_kernel

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.config import CONTENT_WEIGHT

from src.model_loader import (
    load_content_models,
    load_collaborative_models
)

from src.content_based.similarity import (
    create_movie_index,
    recommend_movies
)

from src.hybrid.ranker import (
    rank_hybrid_recommendations
)
from src.tmdb_posters import get_movie_poster

app = FastAPI(
    title="Movie Recommendation System",
    description="Hybrid movie recommendation API",
    version="1.0.0"
)


# --------------------------------------------------
# Load model artifacts
# --------------------------------------------------

movie_features, tfidf_vectorizer, tfidf_matrix = (
    load_content_models()
)

movie_indices = create_movie_index(
    movie_features
)

collaborative_models = (
    load_collaborative_models()
)


# Map movie features to collaborative-model indices
movie_feature_to_train_index = (
    movie_features["movieId"]
    .map(
        collaborative_models["movie_id_to_index"]
    )
    .fillna(-1)
    .astype(int)
    .to_numpy()
)


# --------------------------------------------------
# Health endpoint
# --------------------------------------------------

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "movie-recommendation-api"
    }

@app.get("/movies/popular")
def get_popular_movies(limit: int = 20):
    movies = movie_features[
        movie_features["title"].notna()
    ].head(limit).copy()

    results = []

    for _, movie in movies.iterrows():
        title = str(movie["title"])
        poster_url = get_movie_poster(title)

        results.append({
            "movieId": int(movie["movieId"]),
            "title": title,
            "genres": str(movie["genres"]),
            "poster_url": poster_url,
        })

    return results
# --------------------------------------------------
# Content-based recommendation
# --------------------------------------------------

@app.get("/movies/search")
def search_movies(q: str, limit: int = 20):
    if not q.strip():
        return []

    matches = movie_features[
        movie_features["title"]
        .str.contains(q, case=False, na=False, regex=False)
    ].head(limit)

    results = []

    for _, movie in matches.iterrows():
        title = str(movie["title"])

        results.append({
            "movieId": int(movie["movieId"]),
            "title": title,
            "genres": str(movie["genres"]),
            "poster_url": get_movie_poster(title),
        })

    return results

# --------------------------------------------------
# Movie-to-movie content recommendation
# --------------------------------------------------



@app.get("/recommend/movie/{movie_title}")
def recommend_movie(movie_title: str, n: int = 10):
    recommendations = recommend_movies(
        movie_title,
        movie_features,
        tfidf_matrix,
        movie_indices,
        n=n,
    )

    if isinstance(recommendations, str):
        return {"error": recommendations}

    results = []

    for _, movie in recommendations.iterrows():
        title = str(movie["title"])
        movie_data = movie.to_dict()
        movie_data["poster_url"] = get_movie_poster(title)
        results.append(movie_data)

    return {
        "movie": movie_title,
        "model": "content-based",
        "recommendations": results,
    }

# --------------------------------------------------
# Hybrid recommendation logic
# --------------------------------------------------

def generate_hybrid_user_recommendations(
    user_id,
    n=10
):
    # Check whether the user exists
    user_id_to_index = (
        collaborative_models["user_id_to_index"]
    )

    if user_id not in user_id_to_index:
        return None

    # Get movies the user liked
    user_liked_movies = (
        collaborative_models["user_liked_movies"]
        .get(user_id, set())
    )

    if not user_liked_movies:
        return []

    # Map movie IDs to content-model indices
    movie_id_to_feature_index = {
        movie_id: idx
        for idx, movie_id in enumerate(
            movie_features["movieId"]
        )
    }

    liked_movie_indices = [
        movie_id_to_feature_index[movie_id]
        for movie_id in user_liked_movies
        if movie_id in movie_id_to_feature_index
    ]

    if not liked_movie_indices:
        return []

    # Build user's content profile
    user_profile = sparse.csr_matrix(
        tfidf_matrix[
            liked_movie_indices
        ].mean(axis=0)
    )

    content_scores = linear_kernel(
        user_profile,
        tfidf_matrix
    ).flatten()

    # Generate collaborative scores
    user_idx = user_id_to_index[user_id]

    user_vector = (
        collaborative_models["user_factors"]
        [user_idx]
    )

    movie_factors = (
        collaborative_models["movie_factors"]
    )

    svd_scores = (
        movie_factors @ user_vector
    )

    # Expand collaborative scores to all
    # content-model movies
    collaborative_scores = np.zeros(
        len(movie_features)
    )

    valid_mask = (
        movie_feature_to_train_index >= 0
    )

    collaborative_scores[valid_mask] = (
        svd_scores[
            movie_feature_to_train_index[
                valid_mask
            ]
        ]
    )

    # Movies already rated by the user
    seen_movies = (
        collaborative_models[
            "user_rated_movies"
        ].get(user_id, set())
    )

    # Final hybrid ranking
    recommendations = (
        rank_hybrid_recommendations(
            content_scores,
            collaborative_scores,
            movie_features,
            seen_movies,
            k=n,
            content_weight=CONTENT_WEIGHT
        )
    )

    return recommendations


# --------------------------------------------------
# Personalized recommendation endpoint
# --------------------------------------------------

@app.get("/recommend/user/{user_id}")
def recommend_for_user(
    user_id: int,
    n: int = 10
):
    recommendations = (
        generate_hybrid_user_recommendations(
            user_id,
            n=n
        )
    )

    if recommendations is None:
        return {
            "error": f"userId {user_id} not found."
        }

    if len(recommendations) == 0:
        return {
            "error": (
                f"No recommendations available "
                f"for userId {user_id}."
            )
        }

    return {
        "userId": user_id,
        "model": "hybrid",
        "content_weight": CONTENT_WEIGHT,
        "collaborative_weight": (
            1 - CONTENT_WEIGHT
        ),
        "recommendations": (
            recommendations
            .to_dict(orient="records")
        )
    }


# --------------------------------------------------
# Frontend
# --------------------------------------------------

FRONTEND_DIR = (
    Path(__file__).resolve().parent / "frontend"
)

POSTERS_DIR = FRONTEND_DIR / "posters"


app.mount(
    "/posters",
    StaticFiles(
        directory=POSTERS_DIR
    ),
    name="posters"
)


app.mount(
    "/",
    StaticFiles(
        directory=FRONTEND_DIR,
        html=True
    ),
    name="frontend"
)