# pyright: reportMissingImports=false
from fastapi import FastAPI

from src.model_loader import (
    load_content_models
)

from src.content_based.similarity import (
    create_movie_index,
    recommend_movies
)


app = FastAPI(
    title="Movie Recommendation System",
    description="Hybrid movie recommendation API",
    version="1.0.0"
)


# Load content-based model artifacts once
movie_features, tfidf_vectorizer, tfidf_matrix = (
    load_content_models()
)

movie_indices = create_movie_index(
    movie_features
)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "movie-recommendation-api"
    }


@app.get("/recommend/movie/{movie_title}")
def recommend_similar_movies(
    movie_title: str,
    n: int = 10
):
    recommendations = recommend_movies(
        movie_title,
        movie_features,
        tfidf_matrix,
        movie_indices,
        n=n
    )

    if isinstance(recommendations, str):
        return {
            "error": recommendations
        }

    return {
        "movie": movie_title,
        "recommendations": (
            recommendations
            .to_dict(orient="records")
        )
    }