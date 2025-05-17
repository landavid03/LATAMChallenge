API Gestion de Usuarios

Se desarrollo esta API haciendo uso del framework de python FastAPI.

IP productiva:
    https://user-management-api-584421432926.us-central1.run.app/api/v1/docs

Frontend de prueba:
  https://react-frontend-584421432926.us-central1.run.app/

Funcionalidades de la API
    Operaciones CRUD: Crear, consultar, actualizar y eliminar usuarios.
    Validación de datos: Se validan los usuarios haciendo uso de Pydantic.
    Documentación automática: Se documentaron los Endpoints con OpenAPI/Swagger.
    Manejo de errores: Se agregaron excepciones y Manejo de errores.
    Base de datos: Se hizo uso de sqlLite y de ORM se uso SQLAlchemy.
    Pruebas automatizadas: Se realizaron los tests con pytest.
    Despliegue en la nube: Se hizo la configuración para desplegar en GCP.
    Logging: Se realizo un registro básico de eventos y errores.


Estructura del Proyecto
    El proyecto está organizado con una arquitectura modular y limpia que incluye:
      Separación de responsabilidades (rutas, modelos, esquemas, lógica de negocio)
      Manejo de errores
      Gestión de configuraciones

Tecnologías Utilizadas
    Python: Lenguaje de programacion
    SqlLite: Base de datos
    FastAPI: Framework para APIs web
    SQLAlchemy: ORM potente y flexible
    Pydantic: Validación de datos
    Pytest: Framework de pruebas
    Docker: Contenerización del proyecto
    Google Cloud Run: Despliegue sin servidores
    Google Cloud Build: CI / CD

Endpoints Principales
    GET /api/v1/users/: Obtiene todos los usuarios con paginación y filtros
    GET /api/v1/users/{id}: Obtiene un usuario por ID
    POST /api/v1/users/: Crea un nuevo usuario
    PUT /api/v1/users/{id}: Actualiza un usuario existente
    DELETE /api/v1/users/{id}: Elimina un usuario

Validación de Datos
    Validación de todos los campos con modelos de Pydantic
    Comprobación de tipos, restricciones en campos y validación de emails
    Validación de roles permitidos: admin, user, guest

Manejo de Errores
    Clases de excepciones para distintos errores
    Códigos HTTP adecuados para cada response
    Mensajes de error

Integración con Base de Datos
    ORM SQLAlchemy para hacer las operaciones
    Soporte para distintos motores de base de datos (unicamente modificando el cliente)
    Manejo de sesiones y transacciones


Pruebas Automatizadas
    Pruebas de cada endpoint
    Pruebas de cada operación CRUD

CI/CD
    Configuración con Google Cloud Build
    Archivo de cloudbuild.yml para despligue automatico
    Pipeline automatizado: construcción, pruebas y despliegue
    Manejo de variables de entorno

Ejecucion
    Instrucciones de Ejecucion en local

      Instalar requerimientos:
        Version de python 3.10
          pip install -r requirements.txt

      Ejecutar el servidor:
        uvicorn app.main:app --reload

      Visualizar la documentacion
        http://localhost:8000/api/v1/docs

    Instrucciones de Ejecucion en local con Docker

      Construir imagen:
        docker build -t user-management-api .

      Ejecutar contenedor:
        docker run -d -p 8000:8000 --name user-api user-management-api

      Visualizar la documentacion
        http://localhost:8000/api/v1/docs

    Instucciones de Ejecucion directa a cloud run:

      Instalar y configurar gcloud

      Dar permisos al archivo deploy.sh
        chmod +x ./deploy.sh

      Ejecutar archivo deploy.sh
        ./deploy.sh

    Dentro del repositorio se encuentra una coleccion de POSTMAN para probar los Endpoints

Posibles mejoras:
  Implementacion de Autenticacion
  Manejo de roles
  Implementacion de cache
  Filtros avanzados


Extra:

  Frontend basico deployado con react conectado al cloud run para pruebas.
  Ip: https://react-frontend-584421432926.us-central1.run.app/
