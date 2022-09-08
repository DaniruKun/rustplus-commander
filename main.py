import asyncio
import nest_asyncio
from rustplus import RustSocket, CommandOptions, Command

IP = 'rust.watsonindustries.live'
PORT = '28079'
STEAMID = 76561198069874815
PLAYERTOKEN = 165487861

nest_asyncio.apply()

options = CommandOptions(prefix="!")
rust_socket = RustSocket(
    IP, PORT, STEAMID, PLAYERTOKEN, command_options=options)


@rust_socket.command
async def kek(command: Command):
    await rust_socket.send_team_message(f"Kek, {command.sender_name}")


async def main():
    print('Connecting to socket at host: ', IP)
    await rust_socket.connect()
    print(f"It is {(await rust_socket.get_time()).time}")
    await rust_socket.hang()

asyncio.run(main())
