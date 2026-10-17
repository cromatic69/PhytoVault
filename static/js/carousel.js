"use strict";

document.addEventListener("DOMContentLoaded", function () {

    const track = document.getElementById("plantCarousel");

    if (!track) {
        return;
    }

    const prevBtn = document.querySelector(".carousel-prev");
    const nextBtn = document.querySelector(".carousel-next");

    function scrollByCard(direction) {

        const card = track.querySelector(".plant-card");
        const gap = 24;
        const distance = card ? card.offsetWidth + gap : 300;

        track.scrollBy({
            left: direction * distance,
            behavior: "smooth"
        });

    }

    if (prevBtn) {
        prevBtn.addEventListener("click", () => scrollByCard(-1));
    }

    if (nextBtn) {
        nextBtn.addEventListener("click", () => scrollByCard(1));
    }

});
