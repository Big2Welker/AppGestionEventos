const rol = localStorage.getItem("rol");

if (!rol) {
  window.location.href = "index.html";
}

const acciones = document.getElementById("acciones");

function crearBoton(texto, destino) {
  const btn = document.createElement("button");
  btn.textContent = texto;
  btn.onclick = () => {
    window.location.href = destino;
  };
  acciones.appendChild(btn);
}

crearBoton("Ver eventos", "ver_eventos.html");

if (rol === "estudiante" || rol === "docente") {
  crearBoton("Crear evento", "crear_evento.html");
  crearBoton("Editar evento", "editar_evento.html");
  crearBoton("Ver instalaciones", "ver_instalaciones.html");
  crearBoton("Eliminar evento", "eliminar_evento.html");
}

if (rol === "secretariaAcademica") {
  crearBoton("Evaluar eventos", "evaluar_evento.html");
  crearBoton("Crear usuario", "crear_usuario.html");
}