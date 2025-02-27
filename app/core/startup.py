from database.database import create_db_and_tables, drop_all_tables


async def on_startup():
    await create_db_and_tables()


async def on_shutdown():
    await drop_all_tables()
