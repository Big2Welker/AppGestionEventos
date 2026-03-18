# AppGestionEventos
Integrantes Sebastian Rojas Herrera, Juan Davdid Bedoya Cabrera

# Gestor de Eventos Académicos

Sistema web para la gestión de eventos académicos, desarrollado con **FastAPI**, **MongoDB Atlas** y **frontend en HTML, CSS y JavaScript**, desplegado sobre **máquinas virtuales Ubuntu usando Vagrant**.

---

## Tabla de contenido

1. [Descripción del proyecto](#descripción-del-proyecto)
2. [Arquitectura general](#arquitectura-general)
3. [Tecnologías utilizadas](#tecnologías-utilizadas)
4. [Estructura del proyecto](#estructura-del-proyecto)
5. [Requisitos previos](#requisitos-previos)
6. [Configuración del entorno](#configuración-del-entorno)
7. [Despliegue con Vagrant](#despliegue-con-vagrant)
8. [Configuración del backend](#configuración-del-backend)
9. [Configuración del frontend](#configuración-del-frontend)
10. [Configuración de Nginx](#configuración-de-nginx)
11. [Servicios systemd](#servicios-systemd)
12. [Acceso a la aplicación](#acceso-a-la-aplicación)
13. [Pruebas recomendadas](#pruebas-recomendadas)
14. [Problemas comunes](#problemas-comunes)
15. [Autores](#autores)

---

Actualmente, las instituciones universitarias enfrentan retos significativos al gestionar sus actividades académicas y culturales de forma manual o desintegrada. Esta situación genera una serie de inconvenientes críticos:
 * Descontrol Informativo: Dificultad para registrar, organizar y evaluar las actividades institucionales.
 * Información Fragmentada: Los datos se encuentran dispersos, impidiendo un análisis posterior efectivo.
 * Falta de Visibilidad: Es complicado identificar métricas clave, como el uso de instalaciones o la cantidad de eventos aprobados por facultad.


## Descripción del proyecto

**Gestor de Eventos Académicos** es una aplicación web orientada a la administración de eventos dentro de un entorno académico.

Permite:

* autenticación de usuarios
* gestión de usuarios por rol
* creación, edición, visualización y eliminación de eventos
* evaluación de eventos
* consulta de instalaciones y ocupación
* separación lógica del backend en dominios funcionales tipo microservicios

---

## Arquitectura general

El sistema fue desplegado en **2 máquinas virtuales Ubuntu** usando **Vagrant**:

### VM 1: `web`

Responsabilidades:

* Servir el frontend estático
* Ejecutar **Nginx**
* Funcionar como reverse proxy hacia los microservicios del backend

IP privada:

* `192.168.100.10`

### VM 2: `app`

Responsabilidades:

* Ejecutar los microservicios del backend en FastAPI
* Gestionar la conexión con MongoDB Atlas

IP privada:

* `192.168.100.11`

### Base de datos

La persistencia se maneja con **MongoDB Atlas**, es decir, la base de datos se encuentra alojada en la nube.

---

## Tecnologías utilizadas

### Backend

* Python
* FastAPI
* Uvicorn
* Beanie
* Motor
* Pydantic
* python-jose
* python-dotenv

### Frontend

* HTML5
* CSS3
* JavaScript

### Infraestructura

* Ubuntu Server 22.04
* Vagrant
* VirtualBox
* Nginx
* systemd

### Base de datos

* MongoDB Atlas

---

## Estructura del proyecto

```text
Proyecto/
│── Vagrantfile
│── Backend/
│   │── .env
│   │── requirements.txt
│   │── app/
│   │   │── main.py
│   │   │── common_app.py
│   │   │── auth_main.py
│   │   │── usuarios_main.py
│   │   │── eventos_main.py
│   │   │── evaluaciones_main.py
│   │   │── instalaciones_main.py
│   │   │── api/
│   │   │── core/
│   │   │── crud/
│   │   │── db/
│   │   │── models/
│   │   │── schemas/
│── frontend/
│   │── index.html
│   │── menu.html
│   │── crear_evento.html
│   │── editar_evento.html
│   │── eliminar_evento.html
│   │── evaluar_evento.html
│   │── ver_eventos.html
│   │── ver_instalaciones.html
│   │── css/
│   │── js/
```

---

## Requisitos previos

Antes de iniciar, asegúrate de tener instalado en tu máquina host:

* [VirtualBox](https://www.virtualbox.org/)
* [Vagrant](https://developer.hashicorp.com/vagrant)
* Git
* Python 3 (opcional para desarrollo local)

Además, debes contar con:

* un cluster activo en **MongoDB Atlas**
* una cadena de conexión válida para Atlas
* acceso de red habilitado en Atlas para la IP correspondiente o temporalmente `0.0.0.0/0`

---

## Configuración del entorno

### 1. Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd <NOMBRE_DEL_PROYECTO>
```

### 2. Configurar el archivo `.env`

Dentro de la carpeta `Backend/`, crear o editar el archivo `.env` con la siguiente información:

```env
MONGO_CONNECTION_STRING=mongodb+srv://usuario:password@cluster.mongodb.net/
MONGO_DB_NAME=nombre_base_datos
```

---

## Despliegue con Vagrant

### Vagrantfile utilizado

```ruby
# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  if Vagrant.has_plugin? "vagrant-vbguest"
    config.vbguest.no_install = true
    config.vbguest.auto_update = false
    config.vbguest.no_remote = true
  end

  config.vm.define :web do |web|
    web.vm.box = "bento/ubuntu-22.04"
    web.vm.hostname = "web"
    web.vm.network :private_network, ip: "192.168.100.10"

    web.vm.provider "virtualbox" do |vb|
      vb.name = "vm-web"
      vb.memory = 1024
      vb.cpus = 1
    end
  end

  config.vm.define :app do |app|
    app.vm.box = "bento/ubuntu-22.04"
    app.vm.hostname = "app"
    app.vm.network :private_network, ip: "192.168.100.11"

    app.vm.provider "virtualbox" do |vb|
      vb.name = "vm-app"
      vb.memory = 1536
      vb.cpus = 1
    end
  end

end
```

### Levantar las máquinas virtuales

```bash
vagrant up
```

### Acceder por SSH

```bash
vagrant ssh web
vagrant ssh app
```

---

## Configuración del backend

Dentro de la VM `app`:

### 1. Instalar dependencias del sistema

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv
```

### 2. Crear entorno virtual

```bash
cd ~
python3 -m venv venv
source ~/venv/bin/activate
```

### 3. Instalar dependencias del proyecto

```bash
cd /vagrant/Backend
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Microservicios definidos

El backend fue dividido en los siguientes microservicios:

* **Auth Service** → puerto `8001`
* **Usuarios Service** → puerto `8002`
* **Eventos Service** → puerto `8003`
* **Evaluaciones Service** → puerto `8004`
* **Instalaciones Service** → puerto `8005`

### 5. Ejecución manual de prueba

```bash
uvicorn app.auth_main:app --host 0.0.0.0 --port 8001
uvicorn app.usuarios_main:app --host 0.0.0.0 --port 8002
uvicorn app.eventos_main:app --host 0.0.0.0 --port 8003
uvicorn app.evaluaciones_main:app --host 0.0.0.0 --port 8004
uvicorn app.instalaciones_main:app --host 0.0.0.0 --port 8005
```

---

## Configuración del frontend

Dentro de la VM `web`:

### 1. Instalar Nginx

```bash
sudo apt update
sudo apt install -y nginx
```

### 2. Copiar archivos del frontend

```bash
sudo mkdir -p /var/www/gestoreventos
sudo cp -r /vagrant/frontend/* /var/www/gestoreventos/
```

### 3. Ajuste importante de JavaScript

Las llamadas del frontend deben consumir rutas relativas, por ejemplo:

```javascript
const API = "/api/v1";
```

Ejemplo de login:

```javascript
fetch(API + "/auth/login", {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify({ email, password })
})
```

No deben usarse rutas como:

```javascript
http://127.0.0.1:8000
http://localhost:8000
```

---

## Configuración de Nginx

Crear el archivo de configuración:

```bash
sudo nano /etc/nginx/sites-available/gestoreventos
```

Contenido sugerido:

```nginx
server {
    listen 80;
    server_name GestorEventos.com www.GestorEventos.com;

    root /var/www/gestoreventos;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api/v1/auth/ {
        proxy_pass http://192.168.100.11:8001/api/v1/auth/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /api/v1/usuarios/ {
        proxy_pass http://192.168.100.11:8002/api/v1/usuarios/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /api/v1/eventos/ {
        proxy_pass http://192.168.100.11:8003/api/v1/eventos/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /api/v1/dashboard/ {
        proxy_pass http://192.168.100.11:8003/api/v1/dashboard/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /api/v1/evaluaciones/ {
        proxy_pass http://192.168.100.11:8004/api/v1/evaluaciones/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /api/v1/instalaciones/ {
        proxy_pass http://192.168.100.11:8005/api/v1/instalaciones/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

Activar el sitio:

```bash
sudo ln -s /etc/nginx/sites-available/gestoreventos /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl reload nginx
```

---

## Servicios systemd

Para mantener los microservicios corriendo automáticamente, se configuraron servicios `systemd`.

Ejemplo para `auth.service`:

```ini
[Unit]
Description=Auth FastAPI Service
After=network.target

[Service]
User=vagrant
WorkingDirectory=/vagrant/Backend
Environment="PATH=/home/vagrant/venv/bin"
ExecStart=/home/vagrant/venv/bin/uvicorn app.auth_main:app --host 0.0.0.0 --port 8001
Restart=always

[Install]
WantedBy=multi-user.target
```

Servicios implementados:

* `auth.service`
* `usuarios.service`
* `eventos.service`
* `evaluaciones.service`
* `instalaciones.service`

Comandos útiles:

```bash
sudo systemctl daemon-reload
sudo systemctl enable auth usuarios eventos evaluaciones instalaciones
sudo systemctl start auth usuarios eventos evaluaciones instalaciones
sudo systemctl status auth usuarios eventos evaluaciones instalaciones
```

---

## Acceso a la aplicación

En Windows, editar el archivo:

```text
C:\Windows\System32\drivers\etc\hosts
```

Agregar:

```text
192.168.100.10 GestorEventos.com
192.168.100.10 www.GestorEventos.com
```

Luego ingresar desde el navegador a:

```text
http://GestorEventos.com
```

---

## Pruebas recomendadas

Se recomienda validar el siguiente flujo completo:

1. Iniciar sesión
2. Ver menú según rol
3. Crear usuario (secretaría académica)
4. Crear evento
5. Ver eventos
6. Evaluar evento
7. Consultar instalaciones
8. Eliminar evento

Además, se pueden validar los microservicios individualmente accediendo a:

* `http://192.168.100.11:8001/docs`
* `http://192.168.100.11:8002/docs`
* `http://192.168.100.11:8003/docs`
* `http://192.168.100.11:8004/docs`
* `http://192.168.100.11:8005/docs`

---

## Problemas comunes

### 1. `API is not defined`

Verificar que `api.js` se cargue antes que los demás archivos JavaScript en cada HTML.

Ejemplo:

```html
<script src="js/api.js"></script>
<script src="js/login.js"></script>
```

### 2. `ERR_CONNECTION_REFUSED`

Ocurre cuando el frontend sigue apuntando a `localhost` o `127.0.0.1`. Deben usarse rutas relativas.

### 3. `Address already in use`

Significa que ya existe un proceso ocupando el puerto.

```bash
pkill -f uvicorn
```

### 4. Nginx no aplica cambios

Recargar configuración:

```bash
sudo systemctl reload nginx
```

### 5. Backend no conecta con Atlas

Revisar:

* variables del archivo `.env`
* acceso de red habilitado en MongoDB Atlas
* cadena de conexión correcta

---
