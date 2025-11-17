// URL del backend Flask
export const API_URL = "http://127.0.0.1:5001";


// Obtener token de sesión
export function getToken() {
    return localStorage.getItem("token");
}

// Obtener usuario actual
export function getCurrentUser() {
    const u = localStorage.getItem("user");
    return u ? JSON.parse(u) : null;
}

// Headers con token
export function authHeader() {
    const t = getToken();
    return {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + t
    };
}

// Redirección si no hay sesión
export function requireAuth() {
    if (!getToken()) window.location.href = "login.html";
}

// Redirección si el usuario NO es admin
export function requireAdmin() {
    const u = getCurrentUser();
    if (!u || u.role !== "admin") {
        alert("Solo administradores pueden entrar aquí.");
        window.location.href = "index.html";
    }
}
