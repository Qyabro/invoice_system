from datetime import datetime, timedelta
from fastapi import HTTPException
from app.db.connection import get_db_connection
from app.db.queries import *
from app.models.schemas import Item, Params

async def calculate_invoice(item: Item):
    if not (2000 <= item.year <= 2100):
        raise HTTPException(status_code=400, detail="El año debe estar entre 2000 y 2100")
    if not (1 <= item.month <= 12):
        raise HTTPException(status_code=400, detail="El mes no es válido")
    if item.client_id <= 0:
        raise HTTPException(status_code=400, detail="El client_id debe ser un número positivo")

    next_year, next_month = (item.year + 1, 1) if item.month == 12 else (item.year, item.month + 1)
    start_date = datetime(item.year, item.month, 1)
    end_date = datetime(next_year, next_month, 1)

    conn = await get_db_connection()
    try:
        result = await conn.fetch(GET_INVOICE_QUERY, item.client_id, start_date, end_date)
        return [dict(record) for record in result]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener la factura: {str(e)}")
    finally:
        await conn.close()

async def calculate_statistics(client_id: int, year: int, month: int):
    if client_id <= 0:
        raise HTTPException(status_code=400, detail="El client_id debe ser un número positivo")
    if not (2000 <= year <= 2100):
        raise HTTPException(status_code=400, detail="El año debe estar entre 2000 y 2100")
    if not (1 <= month <= 12):
        raise HTTPException(status_code=400, detail="El mes no es válido")

    next_year, next_month = (year + 1, 1) if month == 12 else (year, month + 1)
    start_date = datetime(year, month, 1)
    end_date = datetime(next_year, next_month, 1)

    conn = await get_db_connection()
    try:
        result = await conn.fetch(GET_STATISTICS_QUERY, client_id, start_date, end_date)
        return [dict(record) for record in result]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener estadísticas: {str(e)}")
    finally:
        await conn.close()

async def calculate_load(year: int, month: int, day: int):
    if not (2000 <= year <= 2100):
        raise HTTPException(status_code=400, detail="El año debe estar entre 2000 y 2100")
    if not (1 <= month <= 12):
        raise HTTPException(status_code=400, detail="El mes no es válido")
    
    # Validar dia de acuerdo al mes y año
    try:
        start_date = datetime(year, month, day)
    except ValueError:
        raise HTTPException(status_code=400, detail="El día no es válido para el mes y año especificados")

    # Calcular el día siguiente:
    end_date = start_date + timedelta(days=1)

    conn = await get_db_connection()
    try:
        result = await conn.fetch(GET_LOAD_QUERY, start_date, end_date)
        return [dict(record) for record in result]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener la carga del sistema: {str(e)}")
    finally:
        await conn.close()

async def calculate_variable(item: Params):
    if not (2000 <= item.year <= 2100):
        raise HTTPException(status_code=400, detail="El año debe estar entre 2000 y 2100")
    if not (1 <= item.month <= 12):
        raise HTTPException(status_code=400, detail="El mes no es válido")
    if item.client_id <= 0:
        raise HTTPException(status_code=400, detail="El client_id debe ser un número positivo")
    if item.option not in [1, 2, 3, 4]:
        raise HTTPException(status_code=400, detail="La opción no es válida")

    next_year, next_month = (item.year + 1, 1) if item.month == 12 else (item.year, item.month + 1)
    start_date = datetime(item.year, item.month, 1)
    end_date = datetime(next_year, next_month, 1)

    conn = await get_db_connection()
    try:
        match item.option:
            case 1:  # EA
                query = GET_EA_QUERY
            case 2:  # EC
                query = GET_EC_QUERY
            case 3:  # EE1
                query = GET_EE1_QUERY
            case 4:  # EE2
                query = GET_EE2_QUERY
        
        result = await conn.fetch(query, item.client_id, start_date, end_date)
        return [dict(record) for record in result]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener el concepto: {str(e)}")
    finally:
        await conn.close()
