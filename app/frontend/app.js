const movieGrid = document.getElementById("movieGrid");
const recommendationGrid = document.getElementById("recommendationGrid");

const movieSearch = document.getElementById("movieSearch");
const recommendButton = document.getElementById("recommendButton");
const backButton = document.getElementById("backButton");

const selectedCount = document.getElementById("selectedCount");
const selectedMovieTitle = document.getElementById("selectedMovieTitle");

const recommendationsSection = document.getElementById(
    "recommendationsSection"
);


// ========================================
// STATE
// ========================================

let movies = [];
let selectedMovie = null;


// ========================================
// LOAD MOVIES
// ========================================

async function loadMovies() {

    try {

        const response = await fetch(
            "/movies/popular?limit=20"
        );

        if (!response.ok) {
            throw new Error(
                `API error: ${response.status}`
            );
        }

        movies = await response.json();

        renderMovies(movies);

    } catch (error) {

        console.error(
            "Failed to load movies:",
            error
        );

        movieGrid.innerHTML = `
            <p>
                Unable to load movies.
            </p>
        `;
    }
}


// ========================================
// CREATE MOVIE CARD
// ========================================
function createMovieCard(movie, index) {
    const card = document.createElement("article");
    card.className = "movie-card";
    card.dataset.movieTitle = movie.title;

    const genres = (movie.genres || "Unknown")
        .split("|")
        .join(" · ");

    const firstGenre = (movie.genres || "Movie").split("|")[0];

    card.innerHTML = `
        <span class="movie-number">${String(index + 1).padStart(2, "0")}</span>
        <span class="movie-check">✓</span>
    `;

    const poster = document.createElement("div");
    poster.className = "movie-poster-placeholder";

    if (movie.poster_url) {
        const image = document.createElement("img");
        image.className = "movie-poster";
        image.src = movie.poster_url;
        image.alt = `${movie.title} poster`;
        image.loading = "lazy";

        image.onerror = () => {
            image.remove();
            poster.classList.add("poster-fallback");
            poster.textContent = `🎬 ${firstGenre}`;
        };

        poster.appendChild(image);
    } else {
        poster.classList.add("poster-fallback");
        poster.textContent = `🎬 ${firstGenre}`;
    }

    const info = document.createElement("div");
    info.className = "movie-card-info";

    const heading = document.createElement("h3");
    heading.className = "movie-title";
    heading.textContent = movie.title;

    const genreText = document.createElement("p");
    genreText.className = "movie-genres";
    genreText.textContent = genres;

    info.append(heading, genreText);
    card.append(poster, info);

    card.addEventListener("click", () => {
        selectMovie(movie, card);
    });

    return card;
}


// ========================================
// RENDER MOVIES
// ========================================

function renderMovies(movieList) {

    movieGrid.innerHTML = "";

    if (movieList.length === 0) {

        movieGrid.innerHTML = `
            <p class="no-results">
                No movies found.
            </p>
        `;

        return;
    }

    movieList.forEach((movie, index) => {

        const card = createMovieCard(movie, index);

        movieGrid.appendChild(card);

    });
}


// ========================================
// SELECT MOVIE
// ========================================

function selectMovie(movie, card) {

    document
        .querySelectorAll(".movie-card")
        .forEach(existingCard => {

            existingCard.classList.remove("selected");

        });

    card.classList.add("selected");

    selectedMovie = movie;

    selectedCount.textContent = "1";

    recommendButton.disabled = false;

}


// ========================================
// SEARCH
// ========================================

let searchTimeout;

movieSearch.addEventListener("input", () => {

    clearTimeout(searchTimeout);

    const query = movieSearch.value.trim();

    if (!query) {

        movieGrid.innerHTML = "";

        return;
    }

    searchTimeout = setTimeout(
        async () => {

            try {

                const response = await fetch(
                    `/movies/search?q=${encodeURIComponent(query)}&limit=20`
                );

                if (!response.ok) {
                    throw new Error(
                        `Search error: ${response.status}`
                    );
                }

                const results =
                    await response.json();

                movies = results;

                renderMovies(results);

            } catch (error) {

                console.error(
                    "Search failed:",
                    error
                );

                movieGrid.innerHTML = `
                    <p>
                        Search failed. Please try again.
                    </p>
                `;
            }

        },
        300
    );
});


// ========================================
// GET RECOMMENDATIONS
// ========================================

recommendButton.addEventListener(
    "click",
    async () => {

        if (!selectedMovie) {
            return;
        }

        recommendButton.disabled = true;

        recommendButton.querySelector("span").textContent =
            "Finding movies...";

        try {

            const encodedTitle =
                encodeURIComponent(
                    selectedMovie.title
                );

            const response = await fetch(
                `/recommend/movie/${encodedTitle}?n=10`
            );

            if (!response.ok) {

                throw new Error(
                    `API error: ${response.status}`
                );

            }

            const data = await response.json();

            selectedMovieTitle.textContent =
                selectedMovie.title;

            renderRecommendations(
                data.recommendations
            );

            recommendationsSection
                .classList
                .remove("hidden");

            recommendationsSection
                .scrollIntoView({
                    behavior: "smooth"
                });

        } catch (error) {

            console.error(
                "Recommendation error:",
                error
            );

            alert(
                "Unable to get recommendations. " +
                "Make sure the API server is running."
            );

        } finally {

            recommendButton.disabled = false;

            recommendButton.querySelector("span").textContent =
                "Find Similar Movies";

        }

    }
);


// ========================================
// RENDER RECOMMENDATIONS
// ========================================


function renderRecommendations(recommendations) {
    recommendationGrid.innerHTML = "";

    recommendations.forEach((movie, index) => {
        const card = document.createElement("article");
        card.className = "movie-card";

        const genres = (movie.genres || "Unknown")
            .split("|")
            .join(" · ");

        const score = (
            (movie.similarity_score || 0) * 100
        ).toFixed(1);

        const number = document.createElement("span");
        number.className = "movie-number";
        number.textContent = String(index + 1).padStart(2, "0");

        const poster = document.createElement("div");
        poster.className = "movie-poster-placeholder";

        if (movie.poster_url) {
            const image = document.createElement("img");
            image.className = "movie-poster";
            image.src = movie.poster_url;
            image.alt = `${movie.title} poster`;
            image.loading = "lazy";

            image.onerror = () => {
                image.remove();
                poster.classList.add("poster-fallback");
                poster.textContent = "🎬 Poster unavailable";
            };

            poster.appendChild(image);
        } else {
            poster.classList.add("poster-fallback");
            poster.textContent = "🎬 Poster unavailable";
        }

        const info = document.createElement("div");
        info.className = "movie-card-info";

        const match = document.createElement("div");
        match.className = "movie-score";
        match.textContent = `${score}% match`;

        const title = document.createElement("h3");
        title.className = "movie-title";
        title.textContent = movie.title || "Unknown movie";

        const genreText = document.createElement("p");
        genreText.className = "movie-genres";
        genreText.textContent = genres;

        info.append(match, title, genreText);
        card.append(number, poster, info);
        recommendationGrid.appendChild(card);
    });
}



// ========================================
// BACK BUTTON
// ========================================

backButton.addEventListener(
    "click",
    () => {

        recommendationsSection
            .classList
            .add("hidden");

        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });

    }
);


// ========================================
// INITIALIZE
// ========================================

loadMovies();