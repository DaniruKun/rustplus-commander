# About

RustPlus Commander is a small Python app that allows you to control smart devices in Rust using the team chat.
It is built on top of [Rust+.py](https://rplus.ollieee.xyz)

## Requirements

- Python 3.6+
- SQLite
- A Steam account (and of course a copy of Rust)

You will need to set these environment variables:

- `RUST_SERVER_IP`: hostname or IP address of the target Rust server
- `RUST_SERVER_PORT`: Rust server port, `28015` by default
- `STEAM_ID`: your Steam user ID
- `RUST_PLAYER_TOKEN`: token used for authenticating you with Rust servers, read below

How to get your Rust player token: <https://rplus.ollieee.xyz/getting-started/getting-player-details>

## Running

```bash
pip install -r requirements.txt
python main.py
```

## Usage

In the team chat (either in game or in the Rust+ app), type:

```
!ping
!register somelight <entityid>
!turn_on somelight
```

`entityid` is a unique ID of every entity on the server. It can easily be found by interacting with one (e.g. hitting it) and checking `combatlog` using the F1 console.