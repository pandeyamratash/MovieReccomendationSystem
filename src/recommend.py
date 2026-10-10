from src.content_based.vectorizer import load_movie_features
from src.content_based.similarity import (
    create_movie_index,
    recommend_movies
)


def get_content_recommendations(
    movie_title,
    movie_features_path,
    tfidf_matrix,
    n=10
):
    movie_features = load_movie_features(
        movie_features_path
    )

    movie_indices = create_movie_index(
        movie_features
    )

    return recommend_movies(
        movie_title,
        movie_features,
        tfidf_matrix,
        movie_indices,
        n=n
    )