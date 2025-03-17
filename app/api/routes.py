from fastapi import APIRouter, Query
from app.models.schemas import Item, Params
from app.services.invoice import calculate_invoice, calculate_statistics, calculate_load, calculate_variable

router = APIRouter()

@router.post("/calculate-invoice/")
async def get_invoice(item: Item):
    return await calculate_invoice(item)

@router.get("/client-statistics")
async def get_statistics(client_id: int = Query(...), year: int = Query(..., ge=2000, le=2100), month: int = Query(..., ge=1, le=12)):
    return await calculate_statistics(client_id, year, month)

@router.get("/system-load")
async def get_load(year: int = Query(..., ge=2000, le=2100), month: int = Query(..., ge=1, le=12), day: int = Query(..., ge=1, le=31)):
    return await calculate_load(year, month, day)

@router.post("/concept/")
async def get_variable(item: Params):
    return await calculate_variable(item)
