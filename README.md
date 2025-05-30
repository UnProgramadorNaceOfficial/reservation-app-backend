1# 🚀 Levantando el Proyecto Django

¡Bienvenido! 🎉 En este tutorial, aprenderás a configurar y ejecutar nuestro proyecto Django desde cero. 🐍✨

## 📌 Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

- **Python** (versión 3.8 o superior) 🐍  
- **Pip** (gestor de paquetes de Python) 📦  
- **Virtualenv** (ya incluido en el proyecto) 🏕️  

## 🛠️ Instalación y Configuración

### 1️⃣ Clonar el Repositorio

```bash
git clone https://github.com/ElizabethEscobar04/tendenciastda2025
cd reservas_inteligentes
```

### 2️⃣ Activar el Entorno Virtual

El entorno virtual (`venv`) ya está incluido en el proyecto, por lo que solo debes activarlo:

```bash
# macOS/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3️⃣ Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4️⃣ Aplicar Migraciones y Cargar Datos Iniciales

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5️⃣ Crear un Superusuario (Opcional)

Si deseas acceder al **panel de administración de Django**, ejecuta:

```bash
python manage.py createsuperuser
```

### 6️⃣ Ejecutar el Servidor 🚀

```bash
python manage.py runserver
```

Ahora, abre tu navegador y visita:

```
http://127.0.0.1:8000/
```

🎉 ¡Tu aplicación Django está corriendo! 🎈

---

## 📡 Endpoints de la API

Aquí están los principales endpoints de la API:

| Módulo         | Endpoint                                          |
|---------------|--------------------------------------------------|
| **Clientes**  | `http://localhost:8000/cliente/api/v1/cliente`   |
| **Reservas**  | `http://localhost:8000/reserva/api/v1/reserva`   |
| **Establecimientos** | `http://localhost:8000/establecimiento/api/v1/establecimiento` |

---

## 📂 Estructura del Proyecto

El proyecto está organizado de la siguiente manera:

```
proyecto-django/
│── venv/              # Entorno virtual
│── manage.py          # Comando de administración
│── cliente/           # Aplicación de gestion de clientes
│── establecimiento/   # Aplicación de gestion de establecimientos
│── reserva/           # Aplicación de gestion de reservas
│── global_project/    # Configuración del proyecto
│── usuario/           # Aplicacion de gestion de usuarios
```
---
🚀 ¡Feliz programación con Django! 🦄🔥
