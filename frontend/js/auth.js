// Usar API_URL de api.js (debe estar cargado antes)
// Si no está definido, usar el valor por defecto
const API_URL = window.API_URL || "http://127.0.0.1:5001/api";

// Función helper para obtener token de forma segura
function getTokenSafe() {
    if (window.getToken) {
        return window.getToken();
    }
    return localStorage.getItem("token");
}

// Función helper para obtener usuario de forma segura
function getCurrentUserSafe() {
    if (window.getCurrentUser) {
        return window.getCurrentUser();
    }
    const u = localStorage.getItem("user");
    return u ? JSON.parse(u) : null;
}

// Requiere que el usuario esté logueado, si no redirige a login
function requireAuth() {
    if (!getTokenSafe()) {
        window.location.href = "login.html";
    }
}

// Requiere que usuario sea admin
function requireAdmin() {
    const user = getCurrentUserSafe();
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
        const res = await fetch(`${API_URL}/auth/login`, {
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
        console.error("Error de conexión:", err);
        alert("No se pudo conectar con el servidor. Verifica que el backend esté corriendo.");
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
        const res = await fetch(`${API_URL}/auth/register`, {
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
        console.error("Error de conexión:", err);
        alert("No se pudo conectar con el servidor. Verifica que el backend esté corriendo.");
    }
}

// Hacer funciones disponibles globalmente
window.login = login;
window.registerUser = registerUser;
window.requireAuth = requireAuth;
window.requireAdmin = requireAdmin;
window.logout = logout;
window.loadProfile = loadProfile;

function loadProfile() {
    const user = getCurrentUserSafe();
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
