import pandas as pd

from src.evaluation.metrics import (
    precision_at_k,
    recall_at_k,
    ndcg_at_k
)


def evaluate_recommendations(
    recommendations_by_user,
    relevant_items_by_user,
    k=10
):
    """
    Evaluate recommendations across multiple users.

    recommendations_by_user:
        dict[user_id] -> list of recommended movieIds

    relevant_items_by_user:
        dict[user_id] -> set of relevant movieIds
    """

    results = []

    for user_id, recommended_items in (
        recommendations_by_user.items()
    ):
        relevant_items = relevant_items_by_user.get(
            user_id,
            set()
        )

        results.append({
            "userId": user_id,
            "precision@k": precision_at_k(
                recommended_items,
                relevant_items,
                k
            ),
            "recall@k": recall_at_k(
                recommended_items,
                relevant_items,
                k
            ),
            "ndcg@k": ndcg_at_k(
                recommended_items,
                relevant_items,
                k
            )
        })

    return pd.DataFrame(results)