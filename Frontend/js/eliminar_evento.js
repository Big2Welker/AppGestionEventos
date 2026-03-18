    let eventosCargados = [];

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
        contenedor.innerHTML = "<p>No hay eventos disponibles.</p>";
        return;
    }

    eventos.forEach(evento => {
        const eventoId = evento.id || evento._id;

        const div = document.createElement("div");
        div.className = "evento-card";

        div.innerHTML = `
        <h3>${evento.nombre}</h3>
        <p><strong>ID:</strong> ${eventoId}</p>
        <p><strong>Estado:</strong> ${evento.estado}</p>
        <p><strong>Tipo:</strong> ${evento.tipo}</p>
        <button onclick="eliminarEvento('${eventoId}', '${evento.nombre}')">Eliminar</button>
        `;

        contenedor.appendChild(div);
    });
    }

    async function eliminarEvento(id, nombre) {
    const confirmar = confirm(`¿Seguro que deseas eliminar el evento "${nombre}"?`);
    if (!confirmar) return;

    try {
        const response = await fetch(API + `/eventos/${id}`, {
        method: "DELETE",
        headers: authHeaders()
        });

        const data = await response.json();

        if (!response.ok) {
        alert(data.detail || "Error al eliminar evento");
        return;
        }

        alert("Evento eliminado correctamente");
        cargarEventos();
    } catch (error) {
        console.error("Error eliminando evento:", error);
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

    cargarEventos();