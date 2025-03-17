from pydantic import BaseModel

class Item(BaseModel):
    client_id: int
    year: int
    month: int

class Params(BaseModel):
    client_id: int
    year: int
    month: int
    option: int
