"""Async SQLite adapter allowing to persist devices."""
import aiosqlite
import logging

DEVICES_DB_FILE = 'devices.db'


async def init_switches_table():
    logging.info('Initializing entity table(s)')
    db = await aiosqlite.connect(DEVICES_DB_FILE)
    await db.execute("CREATE TABLE IF NOT EXISTS switches(name text NOT NULL PRIMARY KEY, entity_id text NOT NULL, owner CHAR)")
    logging.debug('Creating indexes')
    await db.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_switches_name ON switches (name)")


async def register_entity(name: str, eid: str, owner: str) -> None:
    logging.debug(f"Saving entity: {name} - {eid}")
    async with aiosqlite.connect(DEVICES_DB_FILE) as db:
        await db.execute("INSERT INTO switches VALUES(?, ?, ?)", (name, eid, owner))
        await db.commit()


async def get_entity_by_name(name: str):
    async with aiosqlite.connect(DEVICES_DB_FILE) as db:
        async with db.execute("SELECT name, entity_id, owner FROM switches WHERE name = ?", (name,)) as cursor:
            return await cursor.fetchone()


async def get_all_entities():
    formatted_results = ''
    async with aiosqlite.connect(DEVICES_DB_FILE) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute('SELECT * FROM switches') as cursor:
            async for row in cursor:
                formatted_results += "{name},{entity_id},{owner}\n".format_map(
                    row)
            return formatted_results
