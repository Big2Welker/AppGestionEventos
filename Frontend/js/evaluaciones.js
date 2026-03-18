    let evaluacionesGlobal = []

    function toggleFormularioEvaluacion() {
    const form = document.getElementById("formEvaluacion")
    form.style.display = form.style.display === "none" ? "block" : "none"
    }

    function limpiarFormularioEvaluacion() {
    document.getElementById("evaluacionId").value = ""
    document.getElementById("estadoEvaluacion").value = ""
    document.getElementById("fechaEvaluacion").value = ""
    document.getElementById("justificacionEvaluacion").value = ""
    document.getElementById("eventoIdEvaluacion").value = ""
    document.getElementById("usuarioIdEvaluacion").value = ""
    document.getElementById("tituloFormularioEvaluacion").textContent = "Crear Evaluación"
    document.getElementById("formEvaluacion").style.display = "none"
    }

    async function cargarEvaluaciones() {
    try {
        const response = await fetch(`${API}/evaluaciones/evaluaciones/`, {
        method: "GET",
        headers: authHeaders()
        })

        const data = await response.json()
        evaluacionesGlobal = Array.isArray(data) ? data : []
        renderEvaluaciones(evaluacionesGlobal)
    } catch (error) {
        console.error("Error cargando evaluaciones:", error)
    }
    }

    function renderEvaluaciones(evaluaciones) {
    const contenedor = document.getElementById("listaEvaluaciones")
    contenedor.innerHTML = ""

    if (!evaluaciones.length) {
        contenedor.innerHTML = "<p>No hay evaluaciones.</p>"
        return
    }

    evaluaciones.forEach(ev => {
        const id = ev.id || ev._id

        const card = document.createElement("div")
        card.className = "card"

        card.innerHTML = `
        <h3>Evaluación ${id}</h3>
        <p><strong>Estado:</strong> ${ev.estado ?? ""}</p>
        <p><strong>Evento:</strong> ${ev.eventoId ?? ""}</p>
        <p><strong>Usuario:</strong> ${ev.usuarioId ?? ""}</p>
        <button onclick="obtenerEvaluacion('${id}')">Ver detalle</button>
        <button onclick="editarEvaluacion('${id}')">Editar</button>
        <button onclick="eliminarEvaluacion('${id}')">Eliminar</button>
        `

        contenedor.appendChild(card)
    })
    }

    async function obtenerEvaluacion(id) {
    try {
        const response = await fetch(`${API}/evaluaciones/evaluaciones/${id}`, {
        method: "GET",
        headers: authHeaders()
        })

        const data = await response.json()
        alert(JSON.stringify(data, null, 2))
    } catch (error) {
        console.error("Error obteniendo evaluación:", error)
    }
    }

    async function guardarEvaluacion() {
    const id = document.getElementById("evaluacionId").value

    const payload = {
        estado: document.getElementById("estadoEvaluacion").value,
        fechaEvaluacion: new Date(document.getElementById("fechaEvaluacion").value).toISOString(),
        justificacion: document.getElementById("justificacionEvaluacion").value,
        eventoId: document.getElementById("eventoIdEvaluacion").value,
        usuarioId: parseInt(document.getElementById("usuarioIdEvaluacion").value)
    }

    const url = id
        ? `${API}/evaluaciones/evaluaciones/${id}`
        : `${API}/evaluaciones/evaluaciones/`

    const method = id ? "PUT" : "POST"

    try {
        const response = await fetch(url, {
        method,
        headers: authHeaders(true),
        body: JSON.stringify(payload)
        })

        const data = await response.json()

        if (!response.ok) {
        alert(data.detail || "Error guardando evaluación")
        return
        }

        limpiarFormularioEvaluacion()
        cargarEvaluaciones()
    } catch (error) {
        console.error("Error guardando evaluación:", error)
    }
    }

    async function editarEvaluacion(id) {
    try {
        const response = await fetch(`${API}/evaluaciones/evaluaciones/${id}`, {
        method: "GET",
        headers: authHeaders()
        })

        const ev = await response.json()

        document.getElementById("evaluacionId").value = ev.id || ev._id || ""
        document.getElementById("estadoEvaluacion").value = ev.estado || ""
        document.getElementById("fechaEvaluacion").value =
        ev.fechaEvaluacion ? new Date(ev.fechaEvaluacion).toISOString().split("T")[0] : ""
        document.getElementById("justificacionEvaluacion").value = ev.justificacion || ""
        document.getElementById("eventoIdEvaluacion").value = ev.eventoId || ""
        document.getElementById("usuarioIdEvaluacion").value = ev.usuarioId || ""

        document.getElementById("tituloFormularioEvaluacion").textContent = "Actualizar Evaluación"
        document.getElementById("formEvaluacion").style.display = "block"
    } catch (error) {
        console.error("Error cargando evaluación para editar:", error)
    }
    }

    async function eliminarEvaluacion(id) {
    if (!confirm("¿Seguro que deseas eliminar esta evaluación?")) return

    try {
        const response = await fetch(`${API}/evaluaciones/evaluaciones/${id}`, {
        method: "DELETE",
        headers: authHeaders()
        })

        const data = await response.json()

        if (!response.ok) {
        alert(data.detail || "Error eliminando evaluación")
        return
        }

        cargarEvaluaciones()
    } catch (error) {
        console.error("Error eliminando evaluación:", error)
    }
    }