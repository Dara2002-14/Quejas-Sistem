
/**
 * Configuración y funciones de API
 * Maneja todas las peticiones HTTP al backend
 */

export const API_URL = "http://127.0.0.1:5001/api";

// También hacer disponible globalmente para scripts no-module
window.API_URL = API_URL;


/**
 * Maneja errores de respuesta HTTP
 */
async function handleResponse(response) {
    const contentType = response.headers.get("content-type");
    
    if (!contentType || !contentType.includes("application/json")) {
        throw new Error("La respuesta del servidor no es JSON");
    }

    const data = await response.json();
    
    if (!response.ok) {
        const error = new Error(data.error || `Error HTTP: ${response.status}`);
        error.status = response.status;
        error.data = data;
        throw error;
    }
    
    return data;
}


/**
 * Realiza una petición GET
 * @param {string} endpoint - Endpoint de la API (sin /api)
 * @param {string|null} token - Token JWT opcional
 * @returns {Promise<Object>} Datos de la respuesta
 */
export async function apiGet(endpoint, token = null) {
    try {
        const headers = { "Content-Type": "application/json" };
        if (token) {
            headers["Authorization"] = `Bearer ${token}`;
        }

        const response = await fetch(`${API_URL}/${endpoint}`, {
            method: "GET",
            headers,
            credentials: "include"
        });

        return await handleResponse(response);
    } catch (error) {
        if (error.name === "TypeError" && error.message.includes("fetch")) {
            throw new Error("Error de conexión. Verifica que el servidor esté corriendo.");
        }
        throw error;
    }
}


/**
 * Realiza una petición POST
 * @param {string} endpoint - Endpoint de la API (sin /api)
 * @param {Object} data - Datos a enviar
 * @param {string|null} token - Token JWT opcional
 * @returns {Promise<Object>} Datos de la respuesta
 */
export async function apiPost(endpoint, data = {}, token = null) {
    try {
        const headers = { "Content-Type": "application/json" };
        if (token) {
            headers["Authorization"] = `Bearer ${token}`;
        }

        const response = await fetch(`${API_URL}/${endpoint}`, {
            method: "POST",
            headers,
            body: JSON.stringify(data),
            credentials: "include"
        });

        return await handleResponse(response);
    } catch (error) {
        if (error.name === "TypeError" && error.message.includes("fetch")) {
            throw new Error("Error de conexión. Verifica que el servidor esté corriendo.");
        }
        throw error;
    }
}


/**
 * Realiza una petición PUT
 * @param {string} endpoint - Endpoint de la API (sin /api)
 * @param {Object} data - Datos a enviar
 * @param {string|null} token - Token JWT opcional
 * @returns {Promise<Object>} Datos de la respuesta
 */
export async function apiPut(endpoint, data = {}, token = null) {
    try {
        const headers = { "Content-Type": "application/json" };
        if (token) {
            headers["Authorization"] = `Bearer ${token}`;
        }

        const response = await fetch(`${API_URL}/${endpoint}`, {
            method: "PUT",
            headers,
            body: JSON.stringify(data),
            credentials: "include"
        });

        return await handleResponse(response);
    } catch (error) {
        if (error.name === "TypeError" && error.message.includes("fetch")) {
            throw new Error("Error de conexión. Verifica que el servidor esté corriendo.");
        }
        throw error;
    }
}


/**
 * Realiza una petición DELETE
 * @param {string} endpoint - Endpoint de la API (sin /api)
 * @param {string|null} token - Token JWT opcional
 * @returns {Promise<Object>} Datos de la respuesta
 */
export async function apiDelete(endpoint, token = null) {
    try {
        const headers = { "Content-Type": "application/json" };
        if (token) {
            headers["Authorization"] = `Bearer ${token}`;
        }

        const response = await fetch(`${API_URL}/${endpoint}`, {
            method: "DELETE",
            headers,
            credentials: "include"
        });

        return await handleResponse(response);
    } catch (error) {
        if (error.name === "TypeError" && error.message.includes("fetch")) {
            throw new Error("Error de conexión. Verifica que el servidor esté corriendo.");
        }
        throw error;
    }
}
