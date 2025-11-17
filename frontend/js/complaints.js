async function loadMyComplaints() {
    const listEl = document.getElementById("complaints-list");
    try {
        const res = await fetch(API_URL + "/api/complaints/mine", {
            headers: authHeader()
        });
        const data = await res.json();

        if (!res.ok) {
            listEl.innerHTML = `<div class="list-empty">Error: ${data.error || "No se pudieron cargar las quejas"}</div>`;
            return;
        }

        if (!data.complaints || data.complaints.length === 0) {
            listEl.innerHTML = `<div class="list-empty">Aún no has registrado ninguna queja.</div>`;
            return;
        }

        let html = "";
        data.complaints.forEach(c => {
            const status = (c.status || "").toLowerCase();
            let statusClass = "badge-status-pendiente";
            if (status.includes("proceso") || status.includes("en ")) statusClass = "badge-status-en";
            if (status.includes("resuelt")) statusClass = "badge-status-resuelta";

            html += `
                <div class="card" style="margin-bottom: 12px;">
                    <h3>${c.title}</h3>
                    <p class="muted">${c.description || ""}</p>
                    <p>
                        <span class="badge ${statusClass}">${c.status}</span>
                        ${c.complaint_number ? `<span class="tag">#${c.complaint_number}</span>` : ""}
                    </p>
                    <button class="btn-secondary" onclick="goToDetail(${c.id})">
                        Ver detalle
                    </button>
                </div>
            `;
        });

        listEl.innerHTML = html;
    } catch (err) {
        listEl.innerHTML = `<div class="list-empty">No se pudo conectar con el servidor.</div>`;
    }
}

function goToDetail(id) {
    window.location.href = "complaint-detail.html?id=" + encodeURIComponent(id);
}

async function createComplaint() {
    const title = document.getElementById("title").value.trim();
    const description = document.getElementById("description").value.trim();
    const msgEl = document.getElementById("create-message");

    if (!title || !description) {
        msgEl.textContent = "Completa título y descripción.";
        msgEl.style.color = "red";
        return;
    }

    try {
        const res = await fetch(API_URL + "/api/complaints/", {
            method: "POST",
            headers: authHeader(),
            body: JSON.stringify({ title, description })
        });

        const data = await res.json();

        if (!res.ok) {
            msgEl.textContent = data.error || "No se pudo crear la queja.";
            msgEl.style.color = "red";
            return;
        }

        msgEl.textContent = "Queja creada correctamente.";
        msgEl.style.color = "green";
        setTimeout(() => {
            window.location.href = "my-complaints.html";
        }, 1000);
    } catch (err) {
        msgEl.textContent = "No se pudo conectar con el servidor.";
        msgEl.style.color = "red";
    }
}

async function loadComplaintDetail() {
    const params = new URLSearchParams(window.location.search);
    const id = parseInt(params.get("id"), 10);
    const container = document.getElementById("detail-container");
    if (!id || !container) return;

    try {
        // No tenemos endpoint /complaints/<id>, así que cargamos todas las mías y filtramos
        const res = await fetch(API_URL + "/api/complaints/mine", {
            headers: authHeader()
        });
        const data = await res.json();

        if (!res.ok || !data.complaints) {
            container.innerHTML += `<p class="muted">No se pudo cargar la queja.</p>`;
            return;
        }

        const c = data.complaints.find(x => x.id === id);
        if (!c) {
            container.innerHTML += `<p class="muted">No se encontró la queja con ID ${id}.</p>`;
            return;
        }

        const status = (c.status || "").toLowerCase();
        let statusClass = "badge-status-pendiente";
        if (status.includes("proceso") || status.includes("en ")) statusClass = "badge-status-en";
        if (status.includes("resuelt")) statusClass = "badge-status-resuelta";

        let trackerHtml = "";
        if (c.tracker && c.tracker.length > 0) {
            trackerHtml = "<h3>Seguimiento</h3>";
            trackerHtml += "<ul>";
            c.tracker.forEach(t => {
                trackerHtml += `
                    <li class="muted">
                        [${t.timestamp}] <strong>${t.action}</strong>
                        ${t.note ? " - " + t.note : ""}
                    </li>
                `;
            });
            trackerHtml += "</ul>";
        }

        container.innerHTML = `
            <h2>${c.title}</h2>
            <p>${c.description || ""}</p>
            <p>
                <span class="badge ${statusClass}">${c.status}</span>
                ${c.complaint_number ? `<span class="tag">#${c.complaint_number}</span>` : ""}
            </p>
            <p class="muted">
                Creada: ${c.created_at || "N/D"}<br>
                Dueño ID: ${c.user_id || "N/D"}
            </p>
            ${trackerHtml}
            <button class="btn-secondary" onclick="window.history.back()">Volver</button>
        `;
    } catch (err) {
        container.innerHTML += `<p class="muted">Error al conectarse con el servidor.</p>`;
    }
}
