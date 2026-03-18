    let eventosCargados = [];

    function getUserIdLogueado() {
    const userId = localStorage.getItem("user_id");
    if (!userId || userId.trim() === "") return null;
    return Number(userId);
    }

    function validarAccesoSecretaria() {
    const rol = localStorage.getItem("rol");
    if (rol !== "secretariaAcademica") {
        alert("No tienes permisos para entrar aquí");
        window.location.href = "menu.html";
    }
    }

    async function cargarEventos() {
    try {
        const response = await fetch(API + "/eventos/", {
        method: "GET",
        headers: authHeaders()
        });

        const data = await response.json();

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
        contenedor.innerHTML = "<p>No hay eventos para evaluar.</p>";
        return;
    }

    eventos.forEach(evento => {
        const eventoId = evento.id || evento._id;
        const fecha = evento.realizacion?.fecha
        ? new Date(evento.realizacion.fecha).toLocaleDateString()
        : "Sin fecha";

        const instalacionesHTML = generarInstalacionesHTML(evento.realizacion?.instalaciones || []);
        const organizadoresHTML = generarOrganizadoresHTML(evento.organizador || []);
        const organizacionesHTML = generarOrganizacionesHTML(evento.organizacion || []);

        const div = document.createElement("div");
        div.className = "evento-card";

        div.innerHTML = `
        <h3>${evento.nombre}</h3>
        <p><strong>ID:</strong> ${eventoId}</p>
        <p><strong>Estado actual:</strong> ${evento.estado}</p>
        <p><strong>Tipo:</strong> ${evento.tipo}</p>
        <p><strong>Capacidad:</strong> ${evento.capacidad}</p>

        <details>
            <summary>Realización</summary>
            <p><strong>Fecha:</strong> ${fecha}</p>
            <p><strong>Hora inicio:</strong> ${evento.realizacion?.horaInicio || "N/A"}</p>
            <p><strong>Hora fin:</strong> ${evento.realizacion?.horaFin || "N/A"}</p>

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

        <hr>

        <h4>Registrar evaluación</h4>

        <select id="estado-${eventoId}" onchange="toggleCampos('${eventoId}')">
            <option value="">Seleccione resultado</option>
            <option value="aprobado">Aprobar</option>
            <option value="rechazado">Rechazar</option>
        </select>

        <textarea id="justificacion-${eventoId}" placeholder="Justificación (si rechaza)" style="display:none;"></textarea>
        <textarea id="acta-${eventoId}" placeholder="Acta de aprobación (si aprueba)" style="display:none;"></textarea>

        <button onclick="guardarEvaluacion('${eventoId}')">Guardar evaluación</button>
        `;

        contenedor.appendChild(div);
    });
    }

    function generarInstalacionesHTML(instalaciones) {
    if (!instalaciones || instalaciones.length === 0) {
        return `<p>No hay instalaciones registradas.</p>`;
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
        return `<p>No hay organizadores registrados.</p>`;
    }

    let html = "<ul>";
    organizadores.forEach(org => {
        html += `
        <li>
            <strong>Usuario ID:</strong> ${org.usuarioId}<br>
            <strong>Tipo aval:</strong> ${org.tipoAval}<br>
            <strong>Tipo:</strong> ${org.tipo}<br>
            <strong>Aval PDF:</strong> ${org.avalPDF ? "[cargado]" : "No disponible"}
        </li>
        `;
    });
    html += "</ul>";
    return html;
    }

    function generarOrganizacionesHTML(organizaciones) {
    if (!organizaciones || organizaciones.length === 0) {
        return `<p>No hay organización externa asociada.</p>`;
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

    function toggleCampos(eventoId) {
    const estado = document.getElementById(`estado-${eventoId}`).value;
    const justificacion = document.getElementById(`justificacion-${eventoId}`);
    const acta = document.getElementById(`acta-${eventoId}`);

    if (estado === "rechazado") {
        justificacion.style.display = "block";
        acta.style.display = "none";
    } else if (estado === "aprobado") {
        justificacion.style.display = "none";
        acta.style.display = "block";
    } else {
        justificacion.style.display = "none";
        acta.style.display = "none";
    }
    }

    async function guardarEvaluacion(eventoId) {
    const estado = document.getElementById(`estado-${eventoId}`).value;
    const justificacion = document.getElementById(`justificacion-${eventoId}`).value.trim();
    const acta = document.getElementById(`acta-${eventoId}`).value.trim();
    const usuarioId = getUserIdLogueado();

    if (!usuarioId) {
        alert("No se encontró el usuario logueado");
        return;
    }

    if (!estado) {
        alert("Selecciona un estado de evaluación");
        return;
    }

    if (estado === "rechazado" && !justificacion) {
        alert("Debes escribir una justificación para rechazar");
        return;
    }

    if (estado === "aprobado" && !acta) {
        alert("Debes escribir el acta de aprobación");
        return;
    }

    const payload = {
        estado: estado,
        fechaEvaluacion: new Date().toISOString(),
        eventoId: eventoId,
        usuarioId: usuarioId
    };

    if (estado === "rechazado") {
        payload.justificacion = justificacion;
    }

    if (estado === "aprobado") {
        payload.actaAprovacion = acta;
    }

    console.log("Payload evaluación:", JSON.stringify(payload, null, 2));

    try {
        const response = await fetch(API + "/evaluaciones/", {
        method: "POST",
        headers: authHeaders(true),
        body: JSON.stringify(payload)
        });

        const data = await response.json();
        console.log("Respuesta evaluación:", data);

        if (!response.ok) {
        alert(data.detail || "Error al guardar evaluación");
        return;
        }

        alert("Evaluación guardada correctamente");
        cargarEventos();
    } catch (error) {
        console.error("Error guardando evaluación:", error);
        alert("No se pudo conectar con el backend");
    }
    }

    function filtrarEventos() {
    const texto = document.getElementById("buscador").value.toLowerCase().trim();

    const filtrados = eventosCargados.filter(evento =>
        evento.nombre.toLowerCase().includes(texto)
    );

    mostrarEventos(filtrados);
    }

    validarAccesoSecretaria();
    cargarEventos();