import numpy as np
import pandas as pd
from scipy import sparse

from src.content_based.vectorizer import (
    create_tfidf_vectorizer
)

from src.content_based.similarity import (
    create_movie_index,
    recommend_movies
)


def create_test_movies():
    movies = pd.DataFrame({
        "movieId": [1, 2, 3, 4, 5],
        "title": [
            "Movie A",
            "Movie B",
            "Movie C",
            "Movie D",
            "Movie E"
        ],
        "genres": [
            "Action|Adventure",
            "Action|Thriller",
            "Comedy|Drama",
            "Sci-Fi|Action",
            "Romance|Drama"
        ],
        "tag": [
            "hero adventure",
            "hero suspense",
            "funny emotional",
            "space future",
            "love emotional"
        ]
    })

    movies["weighted_content"] = (
        movies["genres"].str.replace(
            "|", " ", regex=False
        )
        + " "
        + movies["genres"].str.replace(
            "|", " ", regex=False
        )
        + " "
        + movies["tag"]
    )

    return movies


def test_create_tfidf_vectorizer():
    movies = create_test_movies()

    vectorizer, matrix = create_tfidf_vectorizer(
        movies,
        max_features=100
    )

    assert vectorizer is not None
    assert matrix.shape[0] == len(movies)
    assert matrix.shape[1] > 0


def test_movie_index():
    movies = create_test_movies()

    movie_indices = create_movie_index(
        movies
    )

    assert movie_indices["Movie A"] == 0
    assert movie_indices["Movie C"] == 2


def test_recommend_movies():
    movies = create_test_movies()

    vectorizer, tfidf_matrix = (
        create_tfidf_vectorizer(
            movies,
            max_features=100
        )
    )

    movie_indices = create_movie_index(
        movies
    )

    recommendations = recommend_movies(
        "Movie A",
        movies,
        tfidf_matrix,
        movie_indices,
        n=2
    )

    assert len(recommendations) == 2

    assert "Movie A" not in (
        recommendations["title"].values
    )

    assert "similarity_score" in (
        recommendations.columns
    )


def test_unknown_movie():
    movies = create_test_movies()

    vectorizer, tfidf_matrix = (
        create_tfidf_vectorizer(
            movies,
            max_features=100
        )
    )

    movie_indices = create_movie_index(
        movies
    )

    result = recommend_movies(
        "Unknown Movie",
        movies,
        tfidf_matrix,
        movie_indices,
        n=2
    )

    assert isinstance(result, str)
    assert "not found" in result.lower()