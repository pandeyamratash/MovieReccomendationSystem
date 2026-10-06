import numpy as np
from scipy.sparse import csr_matrix

from src.collaborative.matrix_factorization import (
    fit_svd,
    recommend_for_user
)


def create_test_matrix():
    return csr_matrix([
        [5, 4, 0, 0, 1],
        [4, 5, 0, 1, 0],
        [0, 1, 5, 4, 0],
        [1, 0, 4, 5, 0]
    ])


def test_fit_svd():

    matrix = create_test_matrix()

    svd, user_factors, movie_factors = fit_svd(
        matrix,
        n_components=2,
        random_state=42
    )

    assert svd is not None

    assert user_factors.shape == (
        matrix.shape[0],
        2
    )

    assert movie_factors.shape == (
        matrix.shape[1],
        2
    )


def test_svd_reconstruction_dimensions():

    matrix = create_test_matrix()

    svd, user_factors, movie_factors = fit_svd(
        matrix,
        n_components=2,
        random_state=42
    )

    reconstructed = (
        user_factors @ movie_factors.T
    )

    assert reconstructed.shape == matrix.shape


def test_recommend_for_user():

    matrix = create_test_matrix()

    svd, user_factors, movie_factors = fit_svd(
        matrix,
        n_components=2,
        random_state=42
    )

    user_id_to_index = {
        1: 0,
        2: 1,
        3: 2,
        4: 3
    }

    movie_id_to_index = {
        101: 0,
        102: 1,
        103: 2,
        104: 3,
        105: 4
    }

    index_to_movie_id = {
        0: 101,
        1: 102,
        2: 103,
        3: 104,
        4: 105
    }

    rated_movies = {
        101,
        102
    }

    recommendations = recommend_for_user(
        user_id=1,
        user_id_to_index=user_id_to_index,
        movie_id_to_index=movie_id_to_index,
        index_to_movie_id=index_to_movie_id,
        user_factors=user_factors,
        movie_factors=movie_factors,
        rated_movie_ids_by_user=rated_movies,
        n=2
    )

    assert len(recommendations) == 2

    recommended_ids = {
        item["movieId"]
        for item in recommendations
    }

    assert 101 not in recommended_ids
    assert 102 not in recommended_ids


def test_unknown_user():

    matrix = create_test_matrix()

    svd, user_factors, movie_factors = fit_svd(
        matrix,
        n_components=2,
        random_state=42
    )

    result = recommend_for_user(
        user_id=999,
        user_id_to_index={1: 0},
        movie_id_to_index={
            101: 0,
            102: 1,
            103: 2,
            104: 3,
            105: 4
        },
        index_to_movie_id={
            0: 101,
            1: 102,
            2: 103,
            3: 104,
            4: 105
        },
        user_factors=user_factors,
        movie_factors=movie_factors,
        rated_movie_ids_by_user=set(),
        n=2
    )

    assert isinstance(result, str)
    assert "not found" in result.lower()