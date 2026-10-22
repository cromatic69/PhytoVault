"use strict";

const tableBody = document.getElementById("tableBody");
const searchPlant = document.getElementById("searchPlant");
const globalSearch = document.getElementById("globalSearch");
const searchBtn = document.getElementById("searchBtn");
const categorySelect = document.getElementById("category");
const familySelect = document.getElementById("family");
const sortSelect = document.getElementById("sort");
const filterBtn = document.getElementById("filterBtn");
const resetBtn = document.getElementById("resetBtn");
const searchField = document.getElementById("searchField");

function esc(value) {

    const d = document.createElement("div");

    d.textContent = value == null ? "" : String(value);

    return d.innerHTML;

}

async function loadPlants() {

    const keyword = (
        (searchPlant && searchPlant.value) ||
        (globalSearch && globalSearch.value) ||
        ""
    ).trim();

    const category = categorySelect ? categorySelect.value : "";
    const family = familySelect ? familySelect.value : "";
    const sort = sortSelect ? sortSelect.value : "";

    const params = new URLSearchParams();

    params.set("q", keyword);

    if (searchField && searchField.value !== "all") params.set("field", searchField.value);

    if (category) params.set("category", category);
    if (family) params.set("family", family);
    if (sort) params.set("sort", sort);

    const response = await fetch("/api/search?" + params.toString());

    const plants = await response.json();

    tableBody.innerHTML = "";

    if (plants.length === 0) {

        tableBody.innerHTML = `

        <tr>

            <td colspan="8">

                No Plants Found

            </td>

        </tr>

        `;

        return;
    }

    plants.forEach(plant => {

        tableBody.innerHTML += `

        <tr>

            <td>${plant.id}</td>

            <td>${esc(plant.commonName)}</td>

            <td><i>${esc(plant.scientificName)}</i></td>

            <td>${esc(plant.family)}</td>

            <td>${esc(plant.part) || "-"}</td>

            <td>${esc(plant.compound) || "-"}</td>

            <td>${esc(plant.medicinalUses) || "-"}</td>

            <td>

                <a href="/plant/${plant.id}">

                    <button class="view-btn">

                        View

                    </button>

                </a>

            </td>

        </tr>

        `;

    });

}

function performSearch() {

    loadPlants();

}

function resetFilters() {

    if (searchPlant) searchPlant.value = "";
    if (globalSearch) globalSearch.value = "";
    if (categorySelect) categorySelect.value = "";
    if (familySelect) familySelect.value = "";
    if (sortSelect) sortSelect.selectedIndex = 0;
    if (searchField) searchField.value = "all";

    loadPlants();

}

if (searchPlant) {

    searchPlant.addEventListener(
        "keyup",
        performSearch
    );
}

if (globalSearch) {

    globalSearch.addEventListener(
        "keyup",
        performSearch
    );
}

if (searchBtn) {

    searchBtn.addEventListener(
        "click",
        performSearch
    );
}

if (filterBtn) {

    filterBtn.addEventListener(
        "click",
        performSearch
    );
}

if (searchField) {

    searchField.addEventListener(
        "change",
        performSearch
    );
}

if (resetBtn) {

    resetBtn.addEventListener(
        "click",
        resetFilters
    );
}

window.onload = function () {

    // honour ?search=...&field=... (navbar search, profile-page links)
    const urlParams = new URLSearchParams(window.location.search);

    if (urlParams.get("search") && searchPlant) {
        searchPlant.value = urlParams.get("search");
    }

    if (urlParams.get("field") && searchField) {
        searchField.value = urlParams.get("field");
    }

    loadPlants();

};
