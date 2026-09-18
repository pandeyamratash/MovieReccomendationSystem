import pandas as pd
from sklearn.metrics.pairwise import linear_kernel


def create_movie_index(movie_features):
    """
    Create a mapping from movie title to dataframe index.
    """
    return pd.Series(
        movie_features.index,
        index=movie_features["title"]
    ).drop_duplicates()


def recommend_movies(
    movie_title,
    movie_features,
    tfidf_matrix,
    movie_indices,
    n=10
):
    """
    Recommend movies similar to the given movie title.
    """

    if movie_title not in movie_indices:
        return f"Movie '{movie_title}' not found."

    movie_idx = movie_indices[movie_title]

    similarity_scores = linear_kernel(
        tfidf_matrix[movie_idx],
        tfidf_matrix
    ).flatten()

    similar_indices = similarity_scores.argsort()[
        -(n + 1):
    ][::-1]

    similar_indices = [
        idx
        for idx in similar_indices
        if idx != movie_idx
    ][:n]

    recommendations = movie_features.iloc[
        similar_indices
    ][
        ["movieId", "title", "genres"]
    ].copy()

    recommendations["similarity_score"] = (
        similarity_scores[similar_indices]
    )

    return recommendations