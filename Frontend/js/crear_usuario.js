    function validarAccesoSecretaria() {
    const rol = localStorage.getItem("rol");

    if (rol !== "secretariaAcademica") {
        alert("No tienes permisos para entrar aquí");
        window.location.href = "menu.html";
    }
    }

    function mostrarCamposRol() {
    const rol = document.getElementById("rol").value;

    document.getElementById("bloquePrograma").style.display = "none";
    document.getElementById("bloqueUnidad").style.display = "none";
    document.getElementById("bloqueFacultad").style.display = "none";

    document.getElementById("programaId").value = "";
    document.getElementById("unidadId").value = "";
    document.getElementById("facultadId").value = "";

    if (rol === "estudiante") {
        document.getElementById("bloquePrograma").style.display = "block";
    } else if (rol === "docente") {
        document.getElementById("bloqueUnidad").style.display = "block";
    } else if (rol === "secretariaAcademica") {
        document.getElementById("bloqueFacultad").style.display = "block";
    }
    }

    function asignarProgramaId() {
    const select = document.getElementById("programaSelect");
    document.getElementById("programaId").value = select.value;
    }

    function asignarUnidadId() {
    const select = document.getElementById("unidadSelect");
    document.getElementById("unidadId").value = select.value;
    }

    function asignarFacultadId() {
    const select = document.getElementById("facultadSelect");
    document.getElementById("facultadId").value = select.value;
    }

    async function crearUsuario() {
    const idUsuario = Number(document.getElementById("idUsuario").value);
    const nombre = document.getElementById("nombre").value.trim();
    const apellidos = document.getElementById("apellidos").value.trim();
    const email = document.getElementById("email").value.trim();
    const telefono = document.getElementById("telefono").value.trim();
    const clave = document.getElementById("clave").value.trim();
    const rol = document.getElementById("rol").value;

    const programaId = document.getElementById("programaId").value.trim();
    const unidadId = document.getElementById("unidadId").value.trim();
    const facultadId = document.getElementById("facultadId").value.trim();

    if (
        Number.isNaN(idUsuario) ||
        !nombre ||
        !apellidos ||
        !email ||
        !telefono ||
        !clave ||
        !rol
    ) {
        alert("Completa todos los campos obligatorios");
        return;
    }

    const vinculacion = {
        rol: rol,
        fecha: new Date().toISOString(),
        estado: "activo"
    };

    if (rol === "estudiante") {
        if (!programaId) {
        alert("Debes seleccionar un programa académico");
        return;
        }
        vinculacion.programaId = programaId;
    }

    if (rol === "docente") {
        if (!unidadId) {
        alert("Debes seleccionar una unidad académica");
        return;
        }
        vinculacion.unidadId = unidadId;
    }

    if (rol === "secretariaAcademica") {
        if (!facultadId) {
        alert("Debes seleccionar una facultad");
        return;
        }
        vinculacion.facultadId = facultadId;
    }

    const payload = {
        _id: idUsuario,
        nombre: nombre,
        apellidos: apellidos,
        email: email,
        telefonos: [telefono],
        password: [
        {
            clave: clave,
            fechaCambio: new Date().toISOString(),
            estado: "activa"
        }
        ],
        vinculacion: [vinculacion]
    };

    console.log("Payload usuario:", JSON.stringify(payload, null, 2));

    try {
        const response = await fetch(API + "/usuarios/", {
        method: "POST",
        headers: authHeaders(true),
        body: JSON.stringify(payload)
        });

        const data = await response.json();
        console.log("Respuesta backend:", data);

        if (!response.ok) {
        alert(data.detail || "Error al crear usuario");
        return;
        }

        alert("Usuario creado correctamente");
        window.location.href = "menu.html";
    } catch (error) {
        console.error("Error creando usuario:", error);
        alert("No se pudo conectar con el backend");
    }
    }

    validarAccesoSecretaria();