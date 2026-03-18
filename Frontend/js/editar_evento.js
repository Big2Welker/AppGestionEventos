    let eventoActualId = null;

    function convertirFechaParaInput(fechaISO) {
    if (!fechaISO) return "";
    const fecha = new Date(fechaISO);
    return fecha.toISOString().split("T")[0];
    }

    async function buscarEvento() {
    const id = document.getElementById("buscarId").value.trim();

    if (!id) {
        alert("Ingresa un ID de evento");
        return;
    }

    try {
        const response = await fetch(API + `/eventos/${id}`, {
        method: "GET",
        headers: authHeaders()
        });

        const data = await response.json();
        console.log("Evento encontrado:", data);

        if (!response.ok) {
        alert(data.detail || "No se encontró el evento");
        return;
        }

        eventoActualId = id;
        llenarFormulario(data);
    } catch (error) {
        console.error("Error buscando evento:", error);
        alert("No se pudo conectar con el backend");
    }
    }

    function llenarFormulario(evento) {
    document.getElementById("formEditar").style.display = "block";

    document.getElementById("nombre").value = evento.nombre || "";
    document.getElementById("estado").value = evento.estado || "registrado";
    document.getElementById("tipo").value = evento.tipo || "academico";
    document.getElementById("capacidad").value = evento.capacidad || "";

    const realizacion = evento.realizacion || {};
    const instalaciones = realizacion.instalaciones || [];
    const primeraInstalacion = instalaciones.length > 0 ? instalaciones[0] : {};

    document.getElementById("instalacionId").value = primeraInstalacion.instalacionId || "";
    document.getElementById("capacidadInstalacion").value = primeraInstalacion.capacidadInstalacion || "";
    document.getElementById("fecha").value = convertirFechaParaInput(realizacion.fecha);
    document.getElementById("horaInicio").value = realizacion.horaInicio || "";
    document.getElementById("horaFin").value = realizacion.horaFin || "";

    const organizadores = evento.organizador || [];
    const primerOrganizador = organizadores.length > 0 ? organizadores[0] : {};

    document.getElementById("usuarioId").value = primerOrganizador.usuarioId || "";
    document.getElementById("avalPDF").value = primerOrganizador.avalPDF || "";
    document.getElementById("tipoAval").value = primerOrganizador.tipoAval || "directorPrograma";
    document.getElementById("tipoOrganizador").value = primerOrganizador.tipo || "principal";

    const organizaciones = evento.organizacion || [];
    const primeraOrganizacion = organizaciones.length > 0 ? organizaciones[0] : {};

    document.getElementById("organizacionId").value = primeraOrganizacion.organizacionId || "";
    document.getElementById("participante").value = primeraOrganizacion.participante || "";
    document.getElementById("nombreParticipante").value = primeraOrganizacion.nombreParticipante || "";
    document.getElementById("certificadoParticipacion").value = primeraOrganizacion.certificadoParticipacion || "";
    }

    async function actualizarEvento() {
    if (!eventoActualId) {
        alert("Primero busca un evento");
        return;
    }

    const nombre = document.getElementById("nombre").value.trim();
    const estado = document.getElementById("estado").value;
    const tipo = document.getElementById("tipo").value;
    const instalacionId = document.getElementById("instalacionId").value.trim();
    const capacidadInstalacion = parseInt(document.getElementById("capacidadInstalacion").value);
    const fecha = document.getElementById("fecha").value;
    const horaInicio = document.getElementById("horaInicio").value;
    const horaFin = document.getElementById("horaFin").value;
    const usuarioId = parseInt(document.getElementById("usuarioId").value);
    const avalPDF = document.getElementById("avalPDF").value.trim();
    const tipoAval = document.getElementById("tipoAval").value;
    const tipoOrganizador = document.getElementById("tipoOrganizador").value;
    const capacidad = parseInt(document.getElementById("capacidad").value);

    if (
        !nombre ||
        !instalacionId ||
        !fecha ||
        !horaInicio ||
        !horaFin ||
        isNaN(capacidad) ||
        isNaN(capacidadInstalacion) ||
        isNaN(usuarioId)
    ) {
        alert("Completa los campos obligatorios");
        return;
    }

    const evento = {
        nombre: nombre,
        estado: estado,
        tipo: tipo,
        realizacion: {
        instalaciones: [
            {
            instalacionId: instalacionId,
            capacidadInstalacion: capacidadInstalacion
            }
        ],
        fecha: new Date(fecha).toISOString(),
        horaInicio: horaInicio,
        horaFin: horaFin
        },
        organizador: [
        {
            usuarioId: usuarioId,
            avalPDF: avalPDF,
            tipoAval: tipoAval,
            tipo: tipoOrganizador
        }
        ],
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

    console.log("Payload actualización:", evento);

    try {
        const response = await fetch(API + `/eventos/${eventoActualId}`, {
        method: "PUT",
        headers: authHeaders(true),
        body: JSON.stringify(evento)
        });

        const data = await response.json();
        console.log("Respuesta actualización:", data);

        if (!response.ok) {
        alert(data.detail || "Error al actualizar el evento");
        return;
        }

        alert("Evento actualizado correctamente");
    } catch (error) {
        console.error("Error actualizando evento:", error);
        alert("No se pudo conectar con el backend");
    }
    }