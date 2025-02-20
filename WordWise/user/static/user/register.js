async function checkUser() {
    try {
        const response = await fetch("/user/info/");
        const result = await response.json();

        if (response.ok) {
            document.getElementById("user-label").textContent = "Logged in as: " + result.username;
            document.getElementById("logout-btn").style.display = "block";
        } else {
            document.getElementById("user-label").textContent = "Not logged in";
            document.getElementById("logout-btn").style.display = "none";
        }
    } catch (error) {
        console.error("Error checking user:", error);
    }
}

async function hashPassword(password) {
    const encoder = new TextEncoder();
    const data = encoder.encode(password);
    const hashBuffer = await crypto.subtle.digest('SHA-256', data);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    return hashArray.map(byte => byte.toString(16).padStart(2, '0')).join('');
}

async function registerUser(event) {
    event.preventDefault();
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirmPassword").value;
    const csrfToken = document.getElementById("csrf_token").value;

    if (password !== confirmPassword) {
        alert("Passwords do not match");
        return;
    }

    try {
        const hashedPassword = await hashPassword(password);

        const response = await fetch("/user/register/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({ username, password: hashedPassword }) // Sending hashed password
        });

        const result = await response.json();
        if (response.ok) {
            alert("User registered successfully!");
            window.location.href = "/user/login";
        } else {
            alert(result.error);
        }
    } catch (error) {
        console.error("Error registering user:", error);
    }
}

async function logoutUser() {
    try {
        await fetch("/user/logout/");
        window.location.href = "/user/login";
    } catch (error) {
        console.error("Error logging out:", error);
    }
}

document.addEventListener("DOMContentLoaded", () => {
    let passwordField = document.getElementById("password");
    let submit_btn = document.getElementById("submit-btn");
    let pass_warn_len = document.getElementById("password-char-text");
    let pass_warn_upc = document.getElementById("password-upc-char");
    let pass_warn_sp = document.getElementById("password-sp-char");

    passwordField.addEventListener("input", () => {
        let pass = passwordField.value;

        let length_pass = pass.length >= 8;
        let upc_pass = /[A-Z]/.test(pass);
        let spc_pass = /[0-9]/.test(pass) && /[^a-zA-Z0-9]/.test(pass);

        pass_warn_len.textContent = length_pass ? "PASS" : "FAIL";
        pass_warn_upc.textContent = upc_pass ? "PASS" : "FAIL";
        pass_warn_sp.textContent = spc_pass ? "PASS" : "FAIL";

        submit_btn.disabled = !(length_pass && upc_pass && spc_pass);
    });
});

window.onload = checkUser;
