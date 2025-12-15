# Documentación Técnica y Arquitectura

## 1. Estructura del Proyecto
El proyecto sigue una arquitectura modular con separación de responsabilidades:
* `app.py`: Punto de entrada y configuración de la aplicación.
* `models.py`: Definición de los modelos de base de datos (SQLAlchemy).
* `routes.py`: Implementación de todos los controladores de la API (Blueprint `api/v1`).
* `/frontend`: Contiene la lógica del lado del cliente.

## 2. Diseño de la Base de Datos
Utilizamos [PostgreSQL/MySQL/SQLite] con el siguiente esquema relacional:
* **`workshop`**: `id` (PK), `name`, `date`, `time`, `category`, etc.
* **`registration`**: `id` (PK), `workshop_id` (FK), `student_email`, `registration_date`.

## 3. Arquitectura de la API
La API utiliza un prefijo `/api/v1` y maneja los siguientes códigos de estado:
* **200 OK / 201 Created:** Petición exitosa.
* **400 Bad Request:** Datos de entrada inválidos (ej: fecha mal formateada).
* **401 Unauthorized:** Intento de acceso a rutas de administrador sin clave.
* **404 Not Found:** Recurso inexistente (ej: ID de taller no válido).

## 4. Estrategia de Autenticación
La validación de administrador se simula mediante el encabezado HTTP: `X-Admin-Key: SECRETO_ADMIN_123` en el módulo `routes.py`.
