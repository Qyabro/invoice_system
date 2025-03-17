# Invoice System

Sistema de cálculo y análisis de facturación de energía utilizando **Python** y **PostgreSQL**, capaz de manejar cálculos complejos, grandes volúmenes de datos y optimizaciones avanzadas.

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

## Instalación

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

![Logo del Proyecto](assets/endpoints.png)

## Endpoints

| Método | Ruta                |          Descripción               |
|---------|--------------------|------------------------------------|
| POST    | /calculate-invoice | Calcula factura                    |
| GET     | /client-statistics | Estadisticas del cliente           |
| GET     | /system-load       | Carga del sistema por hora         |
| POST    | /concept           | Calculo independiente de conceptos |

