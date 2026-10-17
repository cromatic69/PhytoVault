const form = document.getElementById("forgotPasswordForm");
const errorBox = document.getElementById("formError");
const successBox = document.getElementById("formSuccess");

function showError(message) {

    successBox.style.display = "none";
    errorBox.textContent = message;
    errorBox.style.display = "block";

}

function showSuccess(message) {

    errorBox.style.display = "none";
    successBox.textContent = message;
    successBox.style.display = "block";

}

form.addEventListener("submit", async function (e) {

    e.preventDefault();

    const email = document.getElementById("email").value.trim();

    const submitBtn = form.querySelector(".login-btn");
    submitBtn.disabled = true;

    try {

        const response = await fetch("/api/forgot-password", {

            method: "POST",

            headers: {

                "Content-Type": "application/json"

            },

            body: JSON.stringify({ email: email })

        });

        const result = await response.json();

        if (result.success) {

            showSuccess(result.message);

            setTimeout(function () {

                window.location.href =
                    "/reset-password?email=" + encodeURIComponent(email);

            }, 1200);

        } else {

            showError(result.message || "Something went wrong. Please try again.");
            submitBtn.disabled = false;

        }

    } catch (err) {

        showError("Something went wrong. Please check your connection and try again.");
        submitBtn.disabled = false;

    }

});
