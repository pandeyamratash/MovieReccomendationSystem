import pandas as pd


def build_movie_tags(tags):
    """
    Group all tags per movie into a single space-separated string.

    Input:  tags dataframe with columns [userId, movieId, tag, timestamp]
    Output: dataframe with columns [movieId, tag]
    """
    tags = tags.copy()
    tags["tag"] = tags["tag"].fillna("").astype(str)

    movie_tags = (
        tags.groupby("movieId")["tag"]
        .apply(lambda x: " ".join(x))
        .reset_index()
    )
    return movie_tags


def build_movie_features(movies, tags):
    """
    Combine movies + grouped tags into a single movie_features
    dataframe, with both a plain 'content' column and a
    genre-weighted 'weighted_content' column.

    Input:
        movies: dataframe [movieId, title, genres]
        tags:   dataframe [userId, movieId, tag, timestamp]

    Output:
        dataframe [movieId, title, genres, tag, content, weighted_content]
    """
    movie_tags = build_movie_tags(tags)

    movie_features = movies.merge(
        movie_tags,
        on="movieId",
        how="left"
    )
    movie_features["tag"] = movie_features["tag"].fillna("")

    genres_spaced = movie_features["genres"].str.replace("|", " ", regex=False)

    # Plain content: genres + tags
    movie_features["content"] = genres_spaced + " " + movie_features["tag"]

    # Weighted content: genres counted twice so they dominate similarity more than tags
    movie_features["weighted_content"] = (
        genres_spaced + " " + genres_spaced + " " + movie_features["tag"]
    )

    return movie_features


def save_movie_features(movie_features, path):
    """
    Save the movie_features dataframe to CSV.
    """
    movie_features.to_csv(path, index=False)