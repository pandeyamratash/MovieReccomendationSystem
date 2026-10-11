
from pathlib import Path

from src.config import MOVIE_FEATURES_PATH, MOVIES_CSV, TAGS_CSV
from src.data.load import load_movies, load_tags
from src.data.preprocessing import build_movie_features, save_movie_features


def main():
    if MOVIE_FEATURES_PATH.exists():
        print(f"Movie features already exist: {MOVIE_FEATURES_PATH}")
        return

    if not MOVIES_CSV.exists():
        raise FileNotFoundError(f"Missing source dataset: {MOVIES_CSV}")

    if not TAGS_CSV.exists():
        raise FileNotFoundError(f"Missing source dataset: {TAGS_CSV}")

    print("Loading movies and tags...")
    movies = load_movies()
    tags = load_tags()

    print("Building movie features...")
    features = build_movie_features(movies, tags)

    MOVIE_FEATURES_PATH.parent.mkdir(parents=True, exist_ok=True)
    save_movie_features(features, MOVIE_FEATURES_PATH)

    print(f"Created {MOVIE_FEATURES_PATH}")
    print(f"Rows: {len(features):,}")


if __name__ == "__main__":
    main()
