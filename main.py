import asyncio
import logging
import os
import nest_asyncio
from rustplus import RustSocket, CommandOptions, Command

import db

IP = os.getenv('RUST_SERVER_IP') or 'rust.watsonindustries.live'
PORT = os.getenv('RUST_SERVER_PORT') or '28015'
STEAMID = int(os.getenv('STEAM_ID'))
PLAYERTOKEN = int(os.getenv('RUST_PLAYER_TOKEN'))

RESP_PREFIX = os.getenv('RESP_PREFIX') or "COMMANDER>> "

logging.basicConfig(level=logging.INFO)

nest_asyncio.apply()

options = CommandOptions(prefix="!")
rust_socket = RustSocket(
    IP, PORT, STEAMID, PLAYERTOKEN, command_options=options)


@rust_socket.command
async def ping(command: Command):
    logging.info('Got ping request')
    await rust_socket.send_team_message(f"{RESP_PREFIX}Pong, {command.sender_name}!")


@rust_socket.command
async def register(command: Command):
    message: str
    name, entity_id, *_ = command.args
    logging.info(
        f"Got register request for entity: [{entity_id}] with name: [{name}]")

    try:
        await db.register_entity(name, entity_id, command.sender_name)
        message = await f"{RESP_PREFIX}Registered entity with name: {name}"
    except:
        message = f"{RESP_PREFIX}Failed to register entity, is the name unique?"
    await rust_socket.send_team_message(message)


@rust_socket.command
async def turn_on(command: Command):
    name, *_ = command.args
    message: str
    entity_id: str

    logging.info(f"Got turn on request for device with name: [{name}]")
    try:
        (_, entity_id, _owner) = await db.get_entity_by_name(name)
        message = f"{RESP_PREFIX}Turned on Smart Switch {name}"
        await rust_socket.turn_on_smart_switch(eid=int(entity_id))
    except:
        message = f"{RESP_PREFIX}Did not find Smart Switch with name: {name}!"
    await rust_socket.send_team_message(message)


@rust_socket.command
async def turn_off(command: Command):
    name, *_ = command.args
    message: str
    entity_id: str

    logging.info(f"Got turn off request for device with name: [{name}]")
    try:
        (_, entity_id, _owner) = await db.get_entity_by_name(name)
        message = f"{RESP_PREFIX}Turned off Smart Switch {name}"
        await rust_socket.turn_off_smart_switch(eid=int(entity_id))
    except:
        message = f"{RESP_PREFIX}Did not find Smart Switch with name: {name}!"
    await rust_socket.send_team_message(message)


@rust_socket.command
async def list_all():
    message: str

    logging.info(f"Got list all request")
    try:
        results = await db.get_all_entities()
        message = f"{RESP_PREFIX}Listing entities:\n{results}"
    except:
        message = f"{RESP_PREFIX}Failed to list entities!"
    await rust_socket.send_team_message(message)
    


async def main():
    await db.init_switches_table()
    logging.info(f"Connecting to socket at host: {IP} port: {PORT}")
    await rust_socket.connect()
    logging.info(f"It is {(await rust_socket.get_time()).time} on the server!")
    await rust_socket.hang()

# Entrypoint
if __name__ == "__main__":
    asyncio.run(main())
