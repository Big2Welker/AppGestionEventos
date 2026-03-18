    let eventosCargados = [];

    async function cargarEventos() {
    try {
        const response = await fetch(API + "/eventos/", {
        method: "GET",
        headers: authHeaders()
        });

        const data = await response.json();
        console.log("Eventos recibidos:", data);

        if (!response.ok) {
        alert(data.detail || "Error al obtener eventos");
        return;
        }

        eventosCargados = data;
        mostrarEventos(eventosCargados);
    } catch (error) {
        console.error("Error cargando eventos:", error);
        alert("No se pudo conectar con el backend");
    }
    }

    function mostrarEventos(eventos) {
    const contenedor = document.getElementById("contenedorEventos");
    contenedor.innerHTML = "";

    if (!eventos || eventos.length === 0) {
        contenedor.innerHTML = `<p class="vacio">No hay eventos registrados.</p>`;
        return;
    }

    eventos.forEach(evento => {
        const card = document.createElement("div");
        card.className = "evento-card";

        const fecha = evento.realizacion?.fecha
        ? new Date(evento.realizacion.fecha).toLocaleDateString()
        : "Sin fecha";

        const horaInicio = evento.realizacion?.horaInicio || "N/A";
        const horaFin = evento.realizacion?.horaFin || "N/A";

        const instalacionesHTML = generarInstalacionesHTML(evento.realizacion?.instalaciones || []);
        const organizadoresHTML = generarOrganizadoresHTML(evento.organizador || []);
        const organizacionesHTML = generarOrganizacionesHTML(evento.organizacion || []);

        card.innerHTML = `
        <h3>${evento.nombre}</h3>
        <p><strong>ID:</strong> ${evento.id || evento._id || "N/A"}</p>
        <p><strong>Estado:</strong> ${evento.estado}</p>
        <p><strong>Tipo:</strong> ${evento.tipo}</p>
        <p><strong>Capacidad:</strong> ${evento.capacidad}</p>

        <details>
            <summary>Realización</summary>
            <p><strong>Fecha:</strong> ${fecha}</p>
            <p><strong>Hora inicio:</strong> ${horaInicio}</p>
            <p><strong>Hora fin:</strong> ${horaFin}</p>

            <details>
            <summary>Instalaciones</summary>
            ${instalacionesHTML}
            </details>
        </details>

        <details>
            <summary>Organizadores</summary>
            ${organizadoresHTML}
        </details>

        <details>
            <summary>Organización externa</summary>
            ${organizacionesHTML}
        </details>
        `;

        contenedor.appendChild(card);
    });
    }

    function generarInstalacionesHTML(instalaciones) {
    if (!instalaciones || instalaciones.length === 0) {
        return `<p class="vacio">No hay instalaciones registradas.</p>`;
    }

    let html = "<ul>";
    instalaciones.forEach(inst => {
        html += `
        <li>
            <strong>ID instalación:</strong> ${inst.instalacionId}<br>
            <strong>Capacidad instalación:</strong> ${inst.capacidadInstalacion}
        </li>
        `;
    });
    html += "</ul>";
    return html;
    }

    function generarOrganizadoresHTML(organizadores) {
    if (!organizadores || organizadores.length === 0) {
        return `<p class="vacio">No hay organizadores registrados.</p>`;
    }

    let html = "<ul>";
    organizadores.forEach(org => {
        html += `
        <li>
            <strong>Usuario ID:</strong> ${org.usuarioId}<br>
            <strong>Tipo aval:</strong> ${org.tipoAval}<br>
            <strong>Tipo organizador:</strong> ${org.tipo}<br>
            <strong>Aval PDF:</strong> ${org.avalPDF ? "[cargado]" : "No disponible"}
        </li>
        `;
    });
    html += "</ul>";
    return html;
    }

    function generarOrganizacionesHTML(organizaciones) {
    if (!organizaciones || organizaciones.length === 0) {
        return `<p class="vacio">No hay organización externa asociada.</p>`;
    }

    let html = "<ul>";
    organizaciones.forEach(org => {
        html += `
        <li>
            <strong>Organización ID:</strong> ${org.organizacionId}<br>
            <strong>Participante:</strong> ${org.participante}<br>
            <strong>Nombre participante:</strong> ${org.nombreParticipante}<br>
            <strong>Certificado:</strong> ${org.certificadoParticipacion ? "[cargado]" : "No disponible"}
        </li>
        `;
    });
    html += "</ul>";
    return html;
    }

    function filtrarEventos() {
    const texto = document.getElementById("buscador").value.toLowerCase().trim();

    const filtrados = eventosCargados.filter(evento =>
        evento.nombre.toLowerCase().includes(texto)
    );

    mostrarEventos(filtrados);
    }

    cargarEventos();