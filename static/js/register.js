const form = document.getElementById("registerForm");

const toggleBtn = document.getElementById("togglePassword");
const passwordInput = document.getElementById("password");

if (toggleBtn && passwordInput) {

    toggleBtn.addEventListener("click", function () {

        passwordInput.type =
            passwordInput.type === "password" ? "text" : "password";

    });

}

const toggleConfirmBtn = document.getElementById("toggleConfirmPassword");
const confirmPasswordInput = document.getElementById("confirmPassword");

if (toggleConfirmBtn && confirmPasswordInput) {

    toggleConfirmBtn.addEventListener("click", function () {

        confirmPasswordInput.type =
            confirmPasswordInput.type === "password" ? "text" : "password";

    });

}

form.addEventListener("submit", async (event) => {

    event.preventDefault();

    const data = {

        full_name:
        document.getElementById("fullname").value,

        username:
        document.getElementById("username").value,

        email:
        document.getElementById("email").value,

        password:
        document.getElementById("password").value,

        institution:
        document.getElementById("institution").value,

        country:
        document.getElementById("country").value,

        role:
        document.getElementById("role").value

    };

    const response = await fetch("/api/register", {

        method: "POST",

        headers: {

            "Content-Type":"application/json"

        },

        body: JSON.stringify(data)

    });

    const result = await response.json();

    if(result.success){

        PhytoDialog.toast(result.message, "success");

        setTimeout(() => {
            window.location.href="/login";
        }, 1200);

    }

    else{

        PhytoDialog.toast(result.message, "error");

    }

});