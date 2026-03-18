    let instalacionesDisponibles = [];

    function getUserIdLogueado() {
    const userId = localStorage.getItem("user_id");
    if (!userId || userId.trim() === "") return null;
    return Number(userId);
    }

    function getNombreCompletoLogueado() {
    const nombre = localStorage.getItem("nombre") || "";
    const apellidos = localStorage.getItem("apellidos") || "";
    return `${nombre} ${apellidos}`.trim();
    }

    async function cargarInstalaciones() {
    try {
        const response = await fetch(API + "/instalaciones/ocupacion", {
        method: "GET",
        headers: authHeaders()
        });

        const data = await response.json();

        if (!response.ok) {
        alert(data.detail || "Error al cargar instalaciones");
        return;
        }

        instalacionesDisponibles = data;
        filtrarInstalacionesPorCapacidad();
    } catch (error) {
        console.error("Error cargando instalaciones:", error);
    }
    }

    function filtrarInstalacionesPorCapacidad() {
    const capacidadValor = document.getElementById("capacidad").value.trim();
    const capacidadEvento = capacidadValor !== "" ? Number(capacidadValor) : null;

    const selects = document.querySelectorAll(".selector-instalacion");
    selects.forEach(select => llenarOpcionesInstalacion(select, capacidadEvento));
    }

    function llenarOpcionesInstalacion(select, capacidadEvento) {
    const valorActual = select.value;
    select.innerHTML = `<option value="">Seleccione instalación</option>`;

    let instalacionesFiltradas = instalacionesDisponibles;

    if (capacidadEvento !== null && !Number.isNaN(capacidadEvento)) {
        instalacionesFiltradas = instalacionesDisponibles.filter(
        inst => inst.capacidad >= capacidadEvento
        );
    }

    instalacionesFiltradas.forEach(inst => {
        const id = inst.instalacionId || inst._id || inst.id;
        const tipo = inst.tipo || "sin tipo";
        const ubicacion = inst.ubicacion || "sin ubicación";
        const capacidad = inst.capacidad || 0;

        const option = document.createElement("option");
        option.value = id;
        option.textContent = `${id} - ${tipo} - ${ubicacion} - capacidad ${capacidad}`;
        option.dataset.capacidad = capacidad;

        select.appendChild(option);
    });

    if (valorActual) {
        select.value = valorActual;
    }
    }

    function agregarSelectorInstalacion() {
    const contenedor = document.getElementById("instalacionesSeleccionadasContainer");

    const bloque = document.createElement("div");
    bloque.className = "instalacion-item";
    bloque.innerHTML = `
        <details open>
        <summary>Seleccionar instalación</summary>
        <select class="selector-instalacion" onchange="actualizarInstalacionSeleccionada(this)"></select>
        <input class="instalacionId" placeholder="ID instalación" readonly>
        <input class="capacidadInstalacion" type="number" placeholder="Capacidad instalación" readonly>
        <button type="button" onclick="this.parentElement.parentElement.remove()">Eliminar instalación</button>
        </details>
    `;

    contenedor.appendChild(bloque);

    const select = bloque.querySelector(".selector-instalacion");
    const capacidadValor = document.getElementById("capacidad").value.trim();
    const capacidadEvento = capacidadValor !== "" ? Number(capacidadValor) : null;

    llenarOpcionesInstalacion(select, capacidadEvento);
    }

    function actualizarInstalacionSeleccionada(select) {
    const bloque = select.closest(".instalacion-item");
    const inputId = bloque.querySelector(".instalacionId");
    const inputCapacidad = bloque.querySelector(".capacidadInstalacion");
    const opcion = select.options[select.selectedIndex];

    if (!select.value) {
        inputId.value = "";
        inputCapacidad.value = "";
        return;
    }

    inputId.value = select.value;
    inputCapacidad.value = opcion.dataset.capacidad || "";
    }

    function agregarOrganizadorSecundario() {
    const contenedor = document.getElementById("organizadoresSecundariosContainer");

    const bloque = document.createElement("div");
    bloque.className = "organizador-secundario-item";
    bloque.innerHTML = `
        <input class="usuarioIdSecundario" type="number" placeholder="ID usuario secundario">
        <input class="avalPDFSecundario" placeholder="Aval PDF secundario">

        <select class="tipoAvalSecundario">
        <option value="directorPrograma">directorPrograma</option>
        <option value="directorDocencia">directorDocencia</option>
        </select>

        <button type="button" onclick="this.parentElement.remove()">Eliminar organizador</button>
        <hr>
    `;

    contenedor.appendChild(bloque);
    }

    function recolectarInstalaciones() {
    const items = document.querySelectorAll(".instalacion-item");

    return Array.from(items)
        .map(item => {
        const instalacionId = item.querySelector(".instalacionId").value.trim();
        const capacidadInstalacionValor = item.querySelector(".capacidadInstalacion").value.trim();

        return {
            instalacionId: instalacionId,
            capacidadInstalacion: capacidadInstalacionValor !== "" ? Number(capacidadInstalacionValor) : null
        };
        })
        .filter(inst =>
        inst.instalacionId !== "" &&
        inst.capacidadInstalacion !== null &&
        !Number.isNaN(inst.capacidadInstalacion)
        );
    }

    function recolectarOrganizadoresSecundarios() {
    const items = document.querySelectorAll(".organizador-secundario-item");

    return Array.from(items)
        .map(item => {
        const usuarioIdValor = item.querySelector(".usuarioIdSecundario").value.trim();
        const avalPDF = item.querySelector(".avalPDFSecundario").value.trim();

        return {
            usuarioId: usuarioIdValor !== "" ? Number(usuarioIdValor) : null,
            avalPDF: avalPDF,
            tipoAval: item.querySelector(".tipoAvalSecundario").value,
            tipo: "secundario"
        };
        })
        .filter(org =>
        org.usuarioId !== null &&
        !Number.isNaN(org.usuarioId) &&
        org.avalPDF !== ""
        );
    }

    async function crearEvento() {
    const nombre = document.getElementById("nombre").value.trim();
    const tipo = document.getElementById("tipo").value;
    const fecha = document.getElementById("fecha").value;
    const horaInicio = document.getElementById("horaInicio").value;
    const horaFin = document.getElementById("horaFin").value;
    const capacidadValor = document.getElementById("capacidad").value.trim();
    const capacidad = capacidadValor !== "" ? Number(capacidadValor) : null;

    const avalPDFPrincipal = document.getElementById("avalPDFPrincipal").value.trim();
    const tipoAvalPrincipal = document.getElementById("tipoAvalPrincipal").value;
    const userIdPrincipal = getUserIdLogueado();

    if (userIdPrincipal === null || Number.isNaN(userIdPrincipal)) {
        alert("No se encontró el usuario logueado. Vuelve a iniciar sesión.");
        return;
    }

    const instalaciones = recolectarInstalaciones();

    if (
        !nombre ||
        !fecha ||
        !horaInicio ||
        !horaFin ||
        capacidad === null ||
        Number.isNaN(capacidad) ||
        instalaciones.length === 0
    ) {
        alert("Completa los campos obligatorios y agrega al menos una instalación válida.");
        return;
    }

    if (!avalPDFPrincipal) {
        alert("El aval PDF del organizador principal es obligatorio.");
        return;
    }

    const organizadorPrincipal = {
        usuarioId: userIdPrincipal,
        avalPDF: avalPDFPrincipal,
        tipoAval: tipoAvalPrincipal,
        tipo: "principal"
    };

    const organizadoresSecundarios = recolectarOrganizadoresSecundarios();
    const organizador = [organizadorPrincipal, ...organizadoresSecundarios];

    const evento = {
        nombre: nombre,
        estado: "registrado",
        tipo: tipo,
        realizacion: {
        instalaciones: instalaciones,
        fecha: new Date(fecha).toISOString(),
        horaInicio: horaInicio,
        horaFin: horaFin
        },
        organizador: organizador,
        capacidad: capacidad
    };

    const organizacionId = document.getElementById("organizacionId").value.trim();
    const participante = document.getElementById("participante").value;
    const nombreParticipante = document.getElementById("nombreParticipante").value.trim();
    const certificadoParticipacion = document.getElementById("certificadoParticipacion").value.trim();

    if (
        organizacionId !== "" &&
        participante !== "" &&
        nombreParticipante !== "" &&
        certificadoParticipacion !== ""
    ) {
        evento.organizacion = [
        {
            organizacionId: organizacionId,
            participante: participante,
            nombreParticipante: nombreParticipante,
            certificadoParticipacion: certificadoParticipacion
        }
        ];
    }

    console.log("Payload enviado JSON:", JSON.stringify(evento, null, 2));

    try {
        const response = await fetch(API + "/eventos/", {
        method: "POST",
        headers: authHeaders(true),
        body: JSON.stringify(evento)
        });

        const data = await response.json();

        if (response.ok) {
        alert("Evento creado correctamente");
        window.location.href = "ver_eventos.html";
        } else {
        alert(data.detail || "Error al crear evento");
        }
    } catch (error) {
        console.error("Error en fetch:", error);
        alert("No se pudo conectar con el backend");
    }
    }

    window.addEventListener("DOMContentLoaded", () => {
    const userId = getUserIdLogueado();
    const nombreCompleto = getNombreCompletoLogueado();

    if (userId === null || Number.isNaN(userId)) {
        alert("No se encontró el usuario logueado. Vuelve a iniciar sesión.");
        window.location.href = "index.html";
        return;
    }

    const campoUsuario = document.getElementById("usuarioPrincipalInfo");
    if (campoUsuario) {
        campoUsuario.value = `${nombreCompleto} - ID: ${userId}`;
    }

    agregarSelectorInstalacion();
    cargarInstalaciones();
    });