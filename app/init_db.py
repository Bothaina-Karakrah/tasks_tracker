"""
Ran it using "python init_db.py"
Check the database using "psql -U bothainakarakrah -d tasks_db;"
then "dt"
"""
import asyncio
import asyncpg
from config import SQL_DATABASE_URI

async def create_tables():
    conn = await asyncpg.connect(SQL_DATABASE_URI)
    with open("schemas.sql", "r") as f:
        sql = f.read()
    await conn.execute(sql)
    await conn.close()

if __name__ == "__main__":
    asyncio.run(create_tables())