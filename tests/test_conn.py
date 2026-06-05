import asyncio
import asyncpg
import sys

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

async def main():
    conn = await asyncpg.connect(
        user="postgres",
        password="12344321",
        host="127.0.0.1",
        port=5432,
        database="fuel_flow_test",
        ssl="disable",
    )
    print("Connected!")
    await conn.close()

asyncio.run(main())