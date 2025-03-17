import asyncpg

used_db = "postgres"
pass_db = "root"
DATABASE_URL = f'postgresql://{used_db}:{pass_db}@localhost:5432/billing_system'

async def get_db_connection():
    return await asyncpg.connect(DATABASE_URL)
