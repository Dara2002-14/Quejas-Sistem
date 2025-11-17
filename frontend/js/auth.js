// Requiere que el usuario esté logueado, si no redirige a login
function requireAuth() {
    if (!getToken()) {
        window.location.href = "login.html";
    }
}

// Requiere que usuario sea admin
function requireAdmin() {
    const user = getCurrentUser();
    const label = document.getElementById("admin-role-label");
    if (label && user) label.innerText = user.role || "(desconocido)";
    if (!user || user.role !== "admin") {
        alert("Solo administradores pueden ver esta página.");
        window.location.href = "index.html";
    }
}

async function login() {
    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();

    if (!username || !password) {
        alert("Completa usuario y contraseña.");
        return;
    }

    try {
        const res = await fetch(API_URL + "/api/auth/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password })
        });

        const data = await res.json();

        if (!res.ok) {
            alert(data.error || "Error al iniciar sesión");
            return;
        }

        localStorage.setItem("token", data.token);
        localStorage.setItem("user", JSON.stringify(data.user));
        window.location.href = "index.html";
    } catch (err) {
        alert("No se pudo conectar con el servidor.");
    }
}

async function registerUser() {
    const username = document.getElementById("reg_username").value.trim();
    const email = document.getElementById("reg_email").value.trim();
    const password = document.getElementById("reg_password").value.trim();

    if (!username || !email || !password) {
        alert("Completa usuario, correo y contraseña.");
        return;
    }

    try {
        const res = await fetch(API_URL + "/api/auth/register", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, email, password })
        });

        const data = await res.json();

        if (!res.ok) {
            alert(data.error || "Error al registrarse");
            return;
        }

        alert("Cuenta creada. Ahora inicia sesión.");
        window.location.href = "login.html";
    } catch (err) {
        alert("No se pudo conectar con el servidor.");
    }
}

function loadProfile() {
    const user = getCurrentUser();
    const el = document.getElementById("profile-info");
    if (!user || !el) return;

    el.innerHTML = `
        <p><strong>Usuario:</strong> ${user.username}</p>
        <p><strong>Correo:</strong> ${user.email}</p>
        <p><strong>Rol:</strong> ${user.role}</p>
        <p><strong>ID:</strong> ${user.id}</p>
    `;
}

function logout() {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    window.location.href = "login.html";
}
