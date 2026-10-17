"use strict";

function initImagePreview() {

    const input = document.getElementById("imageInput");
    const preview = document.getElementById("imagePreview");

    if (!input || !preview) {
        return;
    }

    input.addEventListener("change", () => {

        const file = input.files[0];

        if (!file) {
            return;
        }

        const reader = new FileReader();

        reader.onload = (e) => {
            preview.src = e.target.result;
        };

        reader.readAsDataURL(file);

    });

}

document.addEventListener("DOMContentLoaded", initImagePreview);
