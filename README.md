🚗 Autorent - API REST para Sistema de Alquiler de Vehículos
📋 Información del Proyecto
Alumno: [Javier Muñoz Esqueta]
Usuario GitHub: @javmunozesq
Asignatura: Acceso a Datos
Fecha: Enero 2026

📖 Descripción del Proyecto
Autorent es una API REST completa desarrollada con FastAPI que gestiona un sistema de alquiler de vehículos. El proyecto implementa acceso a datos sin ORM, utilizando conexión directa a base de datos mediante sentencias SQL con mysql-connector-python.
Características Principales
✅ CRUD Completo para todas las entidades (Clientes, Vehículos, Reservas, Pagos)
✅ Acceso a Datos sin ORM - SQL directo a MariaDB/MySQL
✅ Arquitectura Modular - Separación de controllers, database, schemas
✅ Manejo de Errores Robusto - Excepciones personalizadas y logging
✅ Validación de Datos - Usando Pydantic
✅ Interfaz Web - Templates HTML con Jinja2
✅ API REST Documentada - Swagger UI automático de FastAPI

🗂️ Estructura del Proyecto
autorent/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Aplicación principal FastAPI
│   ├── database.py             # Funciones de acceso a datos (SQL directo)
│   ├── schemas.py              # Modelos Pydantic para validación
│   ├── controllers/            # Controladores de la API
│   │   ├── __init__.py
│   │   ├── clientes.py         # Endpoints de clientes
│   │   ├── vehiculos.py        # Endpoints de vehículos
│   │   ├── reservas.py         # Endpoints de reservas
│   │   └── pagos.py            # Endpoints de pagos
├── docs/
│   └── init_db.sql            # Script de inicialización de la base de datos
├── .env                        # Variables de entorno (no en Git)
├── .gitignore
├── requirements.txt            # Dependencias del proyecto
└── README.md                   # Este archivo

🛠️ Tecnologías Utilizadas

Python 3.11+
FastAPI - Framework web moderno y rápido
Uvicorn - Servidor ASGI
MariaDB/MySQL - Base de datos relacional
mysql-connector-python - Conector MySQL para Python
Pydantic - Validación de datos
Jinja2 - Motor de plantillas
python-dotenv - Gestión de variables de entorno


🗄️ Modelo de Datos
El sistema gestiona las siguientes entidades:
Tablas Principales

clientes - Información de clientes del sistema
categorias - Categorías de vehículos (Económico, SUV, Lujo, etc.)
modelos - Modelos de vehículos con marca y año
vehiculos - Vehículos disponibles para alquiler
empleados - Empleados del sistema
reservas - Reservas de vehículos realizadas
pagos - Pagos asociados a reservas

Relaciones

Un vehículo pertenece a un modelo
Un modelo pertenece a una categoría
Una reserva está asociada a un cliente y un vehículo
Un pago está asociado a una reserva


🚀 Instalación y Configuración
1. Clonar el Repositorio
bashgit clone https://github.com/tu-usuario/autorent.git
cd autorent
2. Crear Entorno Virtual
bashpython -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
3. Instalar Dependencias
bashpip install -r requirements.txt
4. Configurar Base de Datos
Crear la base de datos ejecutando el script SQL:
bash# Acceder a MariaDB/MySQL
mysql -u root -p

# Ejecutar el script
source docs/init_db.sql
Crear archivo .env en la raíz del proyecto:
envDB_HOST=localhost
DB_USER=root
DB_PASSWORD=tu_contraseña
DB_NAME=autorent
DB_PORT=3306
5. Ejecutar la Aplicación
bashuvicorn app.main:app --reload
La aplicación estará disponible en:

URL: http://localhost:8000
Documentación API: http://localhost:8000/docs
Documentación alternativa: http://localhost:8000/redoc


📡 Endpoints Principales
Clientes

GET /clientes - Listar todos los clientes
GET /clientes/nuevo - Formulario nuevo cliente
POST /clientes/nuevo - Crear cliente
GET /clientes/editar/{id} - Formulario editar cliente
POST /clientes/editar/{id} - Actualizar cliente
DELETE /clientes/{id} - Eliminar cliente

Vehículos

GET /vehiculos - Listar todos los vehículos
GET /vehiculos/nuevo - Formulario nuevo vehículo
POST /vehiculos/nuevo - Crear vehículo
GET /vehiculos/editar/{id} - Formulario editar vehículo
POST /vehiculos/editar/{id} - Actualizar vehículo
DELETE /vehiculos/{id} - Eliminar vehículo

Reservas

GET /reservas - Listar todas las reservas
GET /reservas/nueva - Formulario nueva reserva
POST /reservas/nueva - Crear reserva
GET /reservas/editar/{id} - Formulario editar reserva
POST /reservas/editar/{id} - Actualizar reserva
DELETE /reservas/{id} - Eliminar reserva

Pagos

POST /pagos/nuevo - Registrar nuevo pago
GET /pagos/{reserva_id} - Obtener pagos de una reserva


💡 Ejemplos de Uso
Crear un Cliente (cURL)
bashcurl -X POST "http://localhost:8000/clientes/nuevo" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "nombre=Juan&apellido=Pérez&email=juan@example.com&telefono=600123456"
Crear una Reserva (cURL)
bashcurl -X POST "http://localhost:8000/reservas/nueva" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "cliente_id=1&vehiculo_id=1&fecha_inicio=2026-02-01&fecha_fin=2026-02-05&total_estimado=200.00"
Registrar un Pago (cURL)
bashcurl -X POST "http://localhost:8000/pagos/nuevo" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "reserva_id=1&monto=200.00&metodo_pago=tarjeta&referencia=TXN123456"

🔧 Características Técnicas
Acceso a Datos Sin ORM
El proyecto utiliza SQL directo mediante mysql-connector-python, sin ningún ORM como SQLAlchemy o Tortoise. Todas las funciones de acceso a datos están en app/database.py:
pythondef fetch_all_clientes() -> List[Dict[str, Any]]:
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM clientes ORDER BY id DESC;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows
Manejo de Excepciones

DatabaseConnectionError: Excepción personalizada para errores de conexión
Global Exception Handlers: Capturan errores y muestran páginas amigables
Logging: Sistema de logging completo con niveles INFO y ERROR

Validación con Pydantic
Todos los datos de entrada se validan usando modelos Pydantic:
pythonclass ClienteCreate(BaseModel):
    nombre: str
    apellido: str
    email: EmailStr
    telefono: Optional[str] = None
    direccion: Optional[str] = None

🧪 Pruebas
Health Check
bashcurl http://localhost:8000/health
Respuesta esperada:
json{
  "status": "ok",
  "service": "autorent"
}
Documentación Interactiva
Visita http://localhost:8000/docs para probar todos los endpoints desde la interfaz de Swagger UI.

📝 Notas Importantes

Seguridad: El archivo .env NO debe subirse a Git (incluido en .gitignore)
Base de Datos: Asegúrate de que MariaDB/MySQL esté ejecutándose antes de iniciar la aplicación
Puerto: Por defecto usa el puerto 8000, puedes cambiarlo con --port
Reload: El flag --reload reinicia automáticamente la app al detectar cambios (solo desarrollo)


🐛 Solución de Problemas
Error: "Can't connect to MySQL server"

Verifica que MySQL/MariaDB esté ejecutándose
Comprueba las credenciales en el archivo .env
Asegúrate de que el puerto sea el correcto (3306 por defecto)

Error: "Database 'autorent' doesn't exist"

Ejecuta el script SQL: mysql -u root -p < docs/init_db.sql

Error: "ModuleNotFoundError"

Asegúrate de haber activado el entorno virtual
Instala las dependencias: pip install -r requirements.txt


📚 Referencias

Documentación FastAPI
MySQL Connector/Python
Pydantic Documentation


📄 Licencia
Este proyecto es un trabajo académico para la asignatura de Acceso a Datos.

👨‍💻 Autor
[Javier Muñoz Esqueta]
Alumno de [ILERNA Madrid]
Enero 2026

🔗 Enlaces

Repositorio GitHub: https://github.com/javmunozesq/API_Autorent
Documentación API: http://localhost:8000/docs