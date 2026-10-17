document.addEventListener("DOMContentLoaded", function () {

    // ==========================
    // Search bar
    // ==========================
    const searchInput = document.getElementById("searchInput");
    const searchButton = document.getElementById("searchButton");

    if (searchInput && searchButton) {

        async function runSearch() {

            const keyword = searchInput.value.trim();

            if (keyword === "") {

                window.location.href = "/database";
                return;

            }

            try {

                const response = await fetch(
                    "/api/search?q=" + encodeURIComponent(keyword)
                );

                const results = await response.json();

                const lowerKeyword = keyword.toLowerCase();

                // If there's exactly one match, or one result whose
                // common/scientific name matches the search term
                // directly, take the user straight to that plant's
                // profile page instead of the full database list.
                let target = null;

                if (results.length === 1) {

                    target = results[0];

                } else if (results.length > 1) {

                    target = results.find(function (plant) {

                        const commonName =
                            (plant.commonName || "").toLowerCase();

                        const scientificName =
                            (plant.scientificName || "").toLowerCase();

                        return (
                            commonName === lowerKeyword ||
                            scientificName === lowerKeyword
                        );

                    });

                }

                if (target) {

                    window.location.href = "/plant/" + target.id;

                } else {

                    window.location.href =
                        "/database?search=" +
                        encodeURIComponent(keyword);

                }

            } catch (err) {

                // If the search API call fails for any reason,
                // fall back to the previous behaviour so the user
                // still gets results instead of a dead button.
                window.location.href =
                    "/database?search=" +
                    encodeURIComponent(keyword);

            }

        }

        searchButton.addEventListener("click", runSearch);

        searchInput.addEventListener("keydown", function (e) {

            if (e.key === "Enter") {

                e.preventDefault();
                runSearch();

            }

        });

    }

    // ==========================
    // Navbar user dropdown
    // ==========================
    const userDropdown = document.querySelector(".user-dropdown");

    if (userDropdown) {

        const userBtn = userDropdown.querySelector(".user-btn");
        const dropdownMenu = userDropdown.querySelector(".dropdown-menu");

        userBtn.addEventListener("click", function (e) {

            e.preventDefault();
            e.stopPropagation();

            dropdownMenu.classList.toggle("show");

        });

        // Keep the menu open when clicking inside it (so links are
        // actually selectable), but close it when clicking anywhere
        // else on the page.
        document.addEventListener("click", function (e) {

            if (!userDropdown.contains(e.target)) {

                dropdownMenu.classList.remove("show");

            }

        });

        // Close the menu after choosing an option.
        dropdownMenu.addEventListener("click", function (e) {

            if (e.target.closest("a")) {

                dropdownMenu.classList.remove("show");

            }

        });

    }

});
