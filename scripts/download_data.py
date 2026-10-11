
import requests
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
DATA_DIR.mkdir(parents=True, exist_ok=True)

FILES = {
    "movies.csv": "https://drive.google.com/uc?export=download&id=1DsnvQhZzQ6Dex8en9HtjNyUok6EKzTds",
    "tags.csv": "https://drive.google.com/uc?export=download&id=1j5wTYpq4i6wVHKC0tRJaOaOxjXl38V_d",
}

for filename, url in FILES.items():
    destination = DATA_DIR / filename
    print(f"Downloading {filename}...")

    response = requests.get(url, timeout=180)
    response.raise_for_status()

    if "text/html" in response.headers.get("Content-Type", "").lower():
        raise RuntimeError(
            f"Google Drive returned a confirmation page instead of {filename}. "
            "The file may not be publicly accessible or may require download confirmation."
        )

    destination.write_bytes(response.content)

    if destination.stat().st_size == 0:
        raise RuntimeError(f"{filename} downloaded as an empty file.")

    print(f"Saved {filename} ({destination.stat().st_size:,} bytes)")

print("Dataset downloads complete.")
