// Usar API_URL y funciones globales (mismo patrón que otros archivos)
const API_URL_ADMIN = window.API_URL || "http://127.0.0.1:5001/api";

function getAuthHeader() {
    const token = window.getToken ? window.getToken() : localStorage.getItem("token");
    return {
        "Content-Type": "application/json",
        "Authorization": token ? `Bearer ${token}` : ""
    };
}

// Ejecutar al abrir la página
document.addEventListener("DOMContentLoaded", () => {
    loadAllComplaintsAdmin();
});

async function loadAllComplaintsAdmin() {
    const el = document.getElementById("admin-complaints");
    if (!el) return;

    el.innerHTML = `<div class="loading">Cargando...</div>`;

    try {
        const res = await fetch(`${API_URL_ADMIN}/complaints/all`, {
            method: "GET",
            headers: getAuthHeader()
        });

        const data = await res.json();

        if (!res.ok) {
            el.innerHTML = `
                <div class="list-empty">
                    Error: ${data.error || data.msg || "No se pudieron cargar las quejas."}
                </div>`;
            return;
        }

        // El backend devuelve {complaints: [...], count: ...}
        const complaints = data.complaints || (Array.isArray(data) ? data : []);

        if (!Array.isArray(complaints) || complaints.length === 0) {
            el.innerHTML = `<div class="list-empty">No hay quejas registradas.</div>`;
            return;
        }

        let html = "";
        complaints.forEach(c => {
            html += `
                <div class="card complaint-card">
                    <h3>${c.title}</h3>
                    <p class="muted">${c.description || ""}</p>

                    <p>
                        <strong>Número:</strong> #${c.complaint_number}<br>
                        <strong>Estado:</strong> ${c.status}<br>
                        <strong>Usuario ID:</strong> ${c.user_id}
                    </p>

                    <a href="./complaint-detail.html?id=${c.id}" class="btn-small btn-blue">
                        Ver detalle
                    </a>
                </div>
            `;
        });

        el.innerHTML = html;

    } catch (err) {
        console.error("Error al cargar quejas:", err);
        el.innerHTML = `<div class="list-empty">No se pudo conectar con el servidor. Verifica que el backend esté corriendo.</div>`;
    }
}

// Hacer función disponible globalmente
window.loadAllComplaintsAdmin = loadAllComplaintsAdmin;
