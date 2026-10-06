def precision_at_k(
    recommended_items,
    relevant_items,
    k
):
    """
    Calculate Precision@K.
    """
    recommended_top_k = recommended_items[:k]

    relevant_count = sum(
        item in relevant_items
        for item in recommended_top_k
    )

    return relevant_count / k
def recall_at_k(
    recommended_items,
    relevant_items,
    k
):
    """
    Calculate Recall@K.
    """
    if len(relevant_items) == 0:
        return 0.0

    recommended_top_k = recommended_items[:k]

    relevant_count = sum(
        item in relevant_items
        for item in recommended_top_k
    )

    return relevant_count / len(relevant_items)
import numpy as np


def ndcg_at_k(
    recommended_items,
    relevant_items,
    k
):
    """
    Calculate NDCG@K.
    """
    recommended_top_k = recommended_items[:k]

    dcg = 0.0

    for position, item in enumerate(
        recommended_top_k,
        start=1
    ):
        if item in relevant_items:
            dcg += 1 / np.log2(position + 1)

    ideal_relevant = min(
        len(relevant_items),
        k
    )

    idcg = sum(
        1 / np.log2(position + 1)
        for position in range(
            1,
            ideal_relevant + 1
        )
    )

    if idcg == 0:
        return 0.0

    return dcg / idcg