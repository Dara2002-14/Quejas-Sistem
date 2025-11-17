
export const API_URL = "http://127.0.0.1:5001/api";  
// IMPORTANTE: Asegúrate que Flask esté corriendo en este puerto


export async function apiGet(endpoint, token = null) {
    const headers = { "Content-Type": "application/json" };
    if (token) headers["Authorization"] = `Bearer ${token}`;

    const res = await fetch(`${API_URL}/${endpoint}`, {
        method: "GET",
        headers,
    });
    return await res.json();
}

export async function apiPost(endpoint, data = {}, token = null) {
    const headers = { "Content-Type": "application/json" };
    if (token) headers["Authorization"] = `Bearer ${token}`;

    const res = await fetch(`${API_URL}/${endpoint}`, {
        method: "POST",
        headers,
        body: JSON.stringify(data),
    });
    return await res.json();
}

export async function apiPut(endpoint, data = {}, token = null) {
    const headers = { "Content-Type": "application/json" };
    if (token) headers["Authorization"] = `Bearer ${token}`;

    const res = await fetch(`${API_URL}/${endpoint}`, {
        method: "PUT",
        headers,
        body: JSON.stringify(data),
    });
    return await res.json();
}
