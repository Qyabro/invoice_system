# Invoice System

Sistema de cálculo y análisis de facturación de energía utilizando **Python**, **Python** y **PostgreSQL**, capaz de manejar cálculos complejos, grandes volúmenes de datos y optimizaciones avanzadas.

## Características
- API RESTful con FastAPI.
- Base de datos PostgreSQL.


## Estructura del Proyecto

```
backend/
│── venv/              # Entorno virtual
│── assets/            # Carpeta recursos
│── app/
│   ├── main.py        # Punto de entrada de la aplicación
│   ├── api/
│   │   ├── routes.py  # Rutas de la API
│   ├── models/
│   │   ├── schemas.py # Esquemas de datos
│   ├── services/
│   │   ├── invoice.py # Lógica de facturación
│   ├── db/
│   │   ├── connection.py  # Conexión a la BD
│   │   ├── queries.py     # Consultas SQL
│── requirements.txt   # Dependencias
│── .gitignore         # Archivos ignorados por Git
```

## Base de datos

### 1. Crear base de datos
```sql
CREATE DATABASE billing_system
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'es-ES'
    LC_CTYPE = 'es-ES'
    LOCALE_PROVIDER = 'libc'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;
```

### 2. Crear tablas

```sql
CREATE TABLE records (
    id_record INTEGER PRIMARY KEY,     
    id_service INTEGER NOT NULL,
    record_timestamp TIMESTAMP(6) NOT NULL
);

CREATE TABLE services (
    id_service INTEGER PRIMARY KEY,     
    id_market INTEGER NOT NULL,
    cdi INTEGER NOT NULL,
	voltage_level INTEGER NOT NULL
);

CREATE TABLE injection (
    id_record INTEGER PRIMARY KEY,     
    value REAL NOT NULL
);

CREATE TABLE consumption (
    id_record INTEGER PRIMARY KEY,     
    value REAL NOT NULL
);

CREATE TABLE xm_data_hourly_per_agent (     
    record_timestamp TIMESTAMP(6) NOT NULL,
	value REAL NOT NULL
	
);

CREATE TABLE tariffs (
	id_market INTEGER NOT NULL,
	voltage_level INTEGER NOT NULL,
	cdi INTEGER,
	G REAL NOT NULL,
	T REAL NOT NULL,
	D REAL NOT NULL,
	R REAL NOT NULL,
	C REAL NOT NULL,
	P REAL NOT NULL,
	CU REAL NOT NULL
);

```

### 3. Relacionar tablas
```sql
ALTER TABLE injection
ADD CONSTRAINT fk_injection_id_record
FOREIGN KEY (id_record) REFERENCES records(id_record);

ALTER TABLE records
ADD CONSTRAINT fk_records_id_service
FOREIGN KEY (id_service) REFERENCES services(id_service);

ALTER TABLE records
ADD CONSTRAINT fk_records_record_timestamp
FOREIGN KEY (record_timestamp) REFERENCES xm_data_hourly_per_agent(record_timestamp);

ALTER TABLE consumption
ADD CONSTRAINT fk_consumption_id_record
FOREIGN KEY (id_record) REFERENCES consumption(id_record);

ALTER TABLE tariffs
ADD CONSTRAINT fk_tariffs_id_market
FOREIGN KEY (id_market) REFERENCES services(id_market);

ALTER TABLE tariffs
ADD CONSTRAINT fk_tariffs_cdi
FOREIGN KEY (cdi) REFERENCES services(cdi);

ALTER TABLE tariffs
ADD CONSTRAINT fk_tariffs_voltage_level
FOREIGN KEY (voltage_level) REFERENCES services(voltage_level);
```

### 4. Diagrama Entidad Relación (ERD)

![diagrama_ERD](assets/diagrama_ERD.png)

## Instalación y Configuración del proyecto

### 1. Clonar el repositorio
```bash
git clone https://github.com/Qyabro/invoice_system
cd backend
```

### 2. Crear y activar el entorno virtual
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar PostgreSQL
Asegúrate de tener PostgreSQL instalado y configurado. 
Edita `app/db/connection.py` con tus credenciales de base de datos.

### 5. Ejecutar la aplicación
```bash
uvicorn app.main:app --reload
```

### 6. Probar Endpoints

Se puede aprovechar el /docs de FastAPI para probar los endpoins: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

![Prueba API](assets/endpoints.png)

## Endpoints

| Método | Ruta                |          Descripción               |
|---------|--------------------|------------------------------------|
| POST    | /calculate-invoice | Calcula factura                    |
| GET     | /client-statistics | Estadisticas del cliente           |
| GET     | /system-load       | Carga del sistema por hora         |
| POST    | /concept           | Calculo independiente de conceptos |

