﻿# Techno Shop E-commerce

## Descripción

Techno Shop es una tienda en línea construida con Django para la asignatura "Programación Web" impartida en Duoc UC Sede Concepción. Este proyecto permite a los usuarios navegar, buscar productos, agregarlos al carrito de compras y realizar pedidos. Los administradores pueden gestionar productos, categorías, pedidos y usuarios.

## Características

- Autenticación de usuarios (registro, inicio de sesión, cierre de sesión).
- Autenticacion para usuarios administradores mediante "dominio/admin"
- Navegación de productos por categorías.
- Búsqueda de productos.
- Carrito de compras.
- Gestión de pedidos.
- Panel de administración para gestionar productos, categorías, pedidos y usuarios.

## Requisitos

- Python
- Django
- SQLite (por defecto)

## Instalación

Sigue estos pasos para configurar el proyecto localmente:

1. **Clona el repositorio:**
    ```sh
    git clone https://github.com/salvadorbravo09/duocuc-programacion-web-django.git
    cd duocuc-programacion-web-django
    ```

2. **Crea y activa un entorno virtual:**
    ```sh
    python -m venv venv
    source venv/bin/activate   # En Windows usa `venv\Scripts\activate`
    ```

3. **Instala las dependencias:**
    ```sh
    pip install -r requirements.txt
    ```

5. **Realiza las migraciones de la base de datos:**
    ```sh
    python manage.py migrate
    ```

6. **Crea un superusuario para acceder al panel de administración:**
    ```sh
    python manage.py createsuperuser
    ```

7. **Ejecuta el servidor de desarrollo:**
    ```sh
    python manage.py runserver
    ```

8. **Accede a la aplicación:**
    Abre tu navegador y ve a `http://localhost:8000`.

9. **Acceder como superusuario**
    Acceder a `http://localhost:8000/admin`

## Uso

Una vez que el servidor está en ejecución, puedes:

- Registrarte e iniciar sesión.
- Navegar por los productos y agregarlos al carrito.
- Realizar un pedido.
- Acceder al panel de administración en `http://localhost:8000/admin` para gestionar el contenido de la tienda.
