const form = document.getElementById("resetPasswordForm");
const errorBox = document.getElementById("formError");
const successBox = document.getElementById("formSuccess");

const toggleBtn = document.getElementById("togglePassword");
const passwordInput = document.getElementById("password");

if (toggleBtn && passwordInput) {

    toggleBtn.addEventListener("click", function () {

        passwordInput.type =
            passwordInput.type === "password" ? "text" : "password";

    });

}

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
    const otp = document.getElementById("otp").value.trim();
    const password = passwordInput.value;
    const confirmPassword = document.getElementById("confirmPassword").value;

    if (password !== confirmPassword) {

        showError("Passwords do not match.");
        return;

    }

    const submitBtn = form.querySelector(".login-btn");
    submitBtn.disabled = true;

    try {

        const response = await fetch("/api/reset-password", {

            method: "POST",

            headers: {

                "Content-Type": "application/json"

            },

            body: JSON.stringify({
                email: email,
                otp: otp,
                password: password
            })

        });

        const result = await response.json();

        if (result.success) {

            showSuccess(result.message + " Redirecting to login...");

            setTimeout(function () {

                window.location.href = "/login";

            }, 1500);

        } else {

            showError(result.message || "Something went wrong. Please try again.");
            submitBtn.disabled = false;

        }

    } catch (err) {

        showError("Something went wrong. Please check your connection and try again.");
        submitBtn.disabled = false;

    }

});
