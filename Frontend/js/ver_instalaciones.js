    async function cargarInstalaciones() {
    try {
        const response = await fetch(API + "/instalaciones/ocupacion", {
        method: "GET",
        headers: authHeaders()
        });

        const data = await response.json();
        console.log("Instalaciones:", data);

        if (!response.ok) {
        alert(data.detail || "Error al obtener instalaciones");
        return;
        }

        mostrarInstalaciones(data);
    } catch (error) {
        console.error("Error cargando instalaciones:", error);
        alert("No se pudo conectar con el backend");
    }
    }

    function mostrarInstalaciones(instalaciones) {
    const contenedor = document.getElementById("contenedorInstalaciones");
    contenedor.innerHTML = "";

    if (!instalaciones || instalaciones.length === 0) {
        contenedor.innerHTML = `<p class="vacio">No hay instalaciones registradas.</p>`;
        return;
    }

    instalaciones.forEach(inst => {
        const card = document.createElement("div");
        card.className = "instalacion-card";

        let eventosHTML = "";

        if (!inst.eventos || inst.eventos.length === 0) {
        eventosHTML = `<p class="vacio">No hay eventos ocupando esta instalación.</p>`;
        } else {
        eventosHTML = "<ul>";
        inst.eventos.forEach(ev => {
            const fecha = ev.fecha ? new Date(ev.fecha).toLocaleDateString() : "Sin fecha";

            eventosHTML += `
            <li>
                <strong>Evento:</strong> ${ev.nombre}<br>
                <strong>Fecha:</strong> ${fecha}<br>
                <strong>Hora inicio:</strong> ${ev.horaInicio}<br>
                <strong>Hora fin:</strong> ${ev.horaFin}<br>
                <strong>Capacidad usada:</strong> ${ev.capacidadUsada}
            </li>
            <br>
            `;
        });
        eventosHTML += "</ul>";
        }

        card.innerHTML = `
        <h3>${inst.instalacionId}</h3>
        <p><strong>Ubicación:</strong> ${inst.ubicacion}</p>
        <p><strong>Tipo:</strong> ${inst.tipo}</p>
        <p><strong>Capacidad:</strong> ${inst.capacidad}</p>

        <details>
            <summary>Eventos que ocupan esta instalación</summary>
            ${eventosHTML}
        </details>
        `;

        contenedor.appendChild(card);
    });
    }

    cargarInstalaciones();