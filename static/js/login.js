const form = document.getElementById("loginForm");
const errorBox = document.getElementById("loginError");
const loginCard = document.querySelector(".login-card");
const passwordInput = document.getElementById("password");

const toggleBtn = document.getElementById("togglePassword");

if (toggleBtn && passwordInput) {

    toggleBtn.addEventListener("click", function () {

        passwordInput.type =
            passwordInput.type === "password" ? "text" : "password";

    });

}

function showError(message) {

    errorBox.textContent = message;
    errorBox.style.display = "block";

    // Restart the shake animation every time so repeated
    // wrong attempts still give visible feedback.
    loginCard.classList.remove("shake");
    void loginCard.offsetWidth; // force reflow to restart animation
    loginCard.classList.add("shake");

    passwordInput.value = "";
    passwordInput.focus();
}

function hideError() {

    errorBox.style.display = "none";
    errorBox.textContent = "";
}

form.addEventListener("submit", async function(e){

    e.preventDefault();

    hideError();

    const submitBtn = form.querySelector(".login-btn");
    submitBtn.disabled = true;

    const data={

        email:
        document.getElementById("email").value,

        password:
        passwordInput.value

    };

    try {

        const response=await fetch("/api/login",{

            method:"POST",

            headers:{

                "Content-Type":"application/json"

            },

            body:JSON.stringify(data)

        });

        const result=await response.json();

        if(result.success){

        if(result.user.role==="Admin"){

            window.location.href="/admin-home";

        }

        else{

            window.location.href="/";

        }

    }

        else{

            showError(result.message || "Login failed. Please try again.");

        }

    } catch (err) {

        showError("Something went wrong. Please check your connection and try again.");

    } finally {

        submitBtn.disabled = false;

    }

});
