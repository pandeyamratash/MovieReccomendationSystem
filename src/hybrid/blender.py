import numpy as np


def normalize_scores(scores):
    """
    Normalize scores to the range [0, 1].
    """
    scores = np.asarray(scores, dtype=float)

    min_score = np.min(scores)
    max_score = np.max(scores)

    if max_score == min_score:
        return np.zeros_like(scores)

    return (
        (scores - min_score)
        / (max_score - min_score)
    )
def blend_scores(
    content_scores,
    collaborative_scores,
    content_weight=0.25
):
    """
    Combine normalized content and collaborative scores.

    The final production weights are:
        Content = 25%
        Collaborative = 75%
    """
    normalized_content = normalize_scores(
        content_scores
    )

    normalized_collaborative = normalize_scores(
        collaborative_scores
    )

    collaborative_weight = 1 - content_weight

    hybrid_scores = (
        content_weight * normalized_content
        + collaborative_weight * normalized_collaborative
    )

    return hybrid_scores