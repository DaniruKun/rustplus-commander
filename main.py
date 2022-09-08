import asyncio
import os
import nest_asyncio
from rustplus import RustSocket, CommandOptions, Command

import db

IP = os.getenv('RUST_SERVER_IP') or 'rust.watsonindustries.live'
PORT = os.getenv('RUST_SERVER_PORT') or '28079'
STEAMID = os.getenv('STEAM_ID')
PLAYERTOKEN = os.getenv('RUST_PLAYER_TOKEN')

RESP_PREFIX = "COMMANDER>> "

nest_asyncio.apply()

options = CommandOptions(prefix="!")
rust_socket = RustSocket(
    IP, PORT, STEAMID, PLAYERTOKEN, command_options=options)


@rust_socket.command
async def ping(command: Command):
    await rust_socket.send_team_message(f"{RESP_PREFIX}Pong, {command.sender_name}!")

@rust_socket.command
async def register(command: Command):
    message: str
    name, entity_id, *_ = command.args
    
    try:
        db.register_entity(name, entity_id, command.sender_name)
        message = f"{RESP_PREFIX}Registered entity with name: {name}"
    except:
        message = f"{RESP_PREFIX}Failed to register entity, is the name unique?"
    await rust_socket.send_team_message(message)
    
@rust_socket.command
async def turn_on(command: Command):
    name, *_ = command.args
    message: str
    (_, entity_id, _owner) = db.get_entity_by_name(name)
    try:
            
        message = f"{RESP_PREFIX}Turned on Smart Switch {name}"
    except:
        message = f"{RESP_PREFIX}Did not find Smart Switch with name: {name}!"
    await rust_socket.turn_on_smart_switch(eid=int(entity_id))
    await rust_socket.send_team_message(message)

# Entrypoint

async def main():
    db.init_switches_table()
    print('Connecting to socket at host: ', IP)
    await rust_socket.connect()
    print(f"It is {(await rust_socket.get_time()).time} on the server!")
    await rust_socket.hang()

asyncio.run(main())
