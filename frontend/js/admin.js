import { API_URL, apiGet } from "./api.js";
import { getToken, requireAdmin } from "./utils.js";

// Ejecutar al abrir la página
document.addEventListener("DOMContentLoaded", () => {
    requireAdmin();   // Evita que usuarios normales entren aquí
    loadAllComplaintsAdmin();
});

async function loadAllComplaintsAdmin() {
    const el = document.getElementById("admin-complaints");
    const token = getToken();

    el.innerHTML = `<div class="loading">Cargando...</div>`;

    try {
        const res = await fetch(`${API_URL}/complaints/all`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            }
        });

        const data = await res.json();

        if (!res.ok) {
            el.innerHTML = `
                <div class="list-empty">
                    Error: ${data.error || data.msg || "No se pudieron cargar las quejas."}
                </div>`;
            return;
        }

        if (!Array.isArray(data) || data.length === 0) {
            el.innerHTML = `<div class="list-empty">No hay quejas registradas.</div>`;
            return;
        }

        let html = "";
        data.forEach(c => {
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
        el.innerHTML = `<div class="list-empty">No se pudo conectar con el servidor.</div>`;
    }
}
