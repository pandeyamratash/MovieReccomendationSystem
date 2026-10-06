import numpy as np


def remove_seen_movies(
    scores,
    movie_features,
    seen_movie_ids
):
    """
    Prevent movies already seen by the user
    from appearing in recommendations.
    """
    filtered_scores = np.asarray(
        scores,
        dtype=float
    ).copy()

    seen_mask = movie_features["movieId"].isin(
        seen_movie_ids
    )

    filtered_scores[
        seen_mask.values
    ] = -np.inf

    return filtered_scores
def get_top_k(
    scores,
    movie_features,
    k=10
):
    """
    Return the top-k movies ranked by score.
    """
    top_indices = np.argsort(scores)[-k:][::-1]

    recommendations = movie_features.iloc[
        top_indices
    ][
        ["movieId", "title", "genres"]
    ].copy()

    recommendations["score"] = scores[
        top_indices
    ]

    return recommendations
from src.hybrid.blender import blend_scores


def rank_hybrid_recommendations(
    content_scores,
    collaborative_scores,
    movie_features,
    seen_movie_ids,
    k=10,
    content_weight=0.25
):
    """
    Generate final ranked recommendations from
    content and collaborative scores.
    """

    hybrid_scores = blend_scores(
        content_scores,
        collaborative_scores,
        content_weight=content_weight
    )

    filtered_scores = remove_seen_movies(
        hybrid_scores,
        movie_features,
        seen_movie_ids
    )

    recommendations = get_top_k(
        filtered_scores,
        movie_features,
        k=k
    )

    return recommendations