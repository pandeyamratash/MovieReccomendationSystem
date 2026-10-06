import numpy as np
import pandas as pd

from src.hybrid.blender import (
    normalize_scores,
    blend_scores
)

from src.hybrid.ranker import (
    remove_seen_movies,
    get_top_k,
    rank_hybrid_recommendations
)


def create_test_movies():
    return pd.DataFrame({
        "movieId": [1, 2, 3, 4, 5],
        "title": [
            "Movie A",
            "Movie B",
            "Movie C",
            "Movie D",
            "Movie E"
        ],
        "genres": [
            "Action",
            "Comedy",
            "Drama",
            "Sci-Fi",
            "Thriller"
        ]
    })


def test_normalize_scores():
    scores = np.array([10, 20, 30])

    normalized = normalize_scores(scores)

    assert normalized.min() == 0
    assert normalized.max() == 1


def test_seen_movies_are_removed():
    movies = create_test_movies()

    scores = np.array([
        0.9,
        0.8,
        0.7,
        0.6,
        0.5
    ])

    filtered = remove_seen_movies(
        scores,
        movies,
        {1, 2}
    )

    assert filtered[0] == -np.inf
    assert filtered[1] == -np.inf
    assert filtered[2] == 0.7


def test_top_k():
    movies = create_test_movies()

    scores = np.array([
        0.1,
        0.5,
        0.9,
        0.3,
        0.7
    ])

    recommendations = get_top_k(
        scores,
        movies,
        k=3
    )

    assert len(recommendations) == 3
    assert recommendations.iloc[0]["movieId"] == 3


def test_hybrid_recommendations():
    movies = create_test_movies()

    content_scores = np.array([
        0.9,
        0.7,
        0.2,
        0.8,
        0.4
    ])

    collaborative_scores = np.array([
        0.3,
        0.9,
        0.8,
        0.4,
        0.7
    ])

    recommendations = rank_hybrid_recommendations(
        content_scores,
        collaborative_scores,
        movies,
        {2},
        k=3,
        content_weight=0.25
    )

    assert len(recommendations) == 3
    assert 2 not in recommendations["movieId"].values