    async function login() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const response = await fetch(API + "/auth/login", {
        method: "POST",
        headers: authHeaders(true),
        body: JSON.stringify({ email, password })
    });

    const data = await response.json();

    console.log(response.status);
    console.log(data);

    if (response.status === 200) {
        localStorage.setItem("token", data.access_token);
        localStorage.setItem("rol", data.rol);
        localStorage.setItem("user_id", data.user_id);
        localStorage.setItem("nombre", data.nombre);
        localStorage.setItem("apellidos", data.apellidos);
        localStorage.setItem("email", data.email);

        window.location.href = "menu.html";
    } else {
        alert(data.detail || "Error al iniciar sesión");
    }
    }