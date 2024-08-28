# TrackMania Nations Forever Client

This Python client is intended to be used with the TM Nations Forever remote procedure endpoint.

The available methods are documented at [ListMethods](/ListMethods.html).

## Usage Example

```python
from trackmania_client import TrackManiaClient as TMClient
import asyncio

async def main():
  HOST = 'localhost'
  PORT = 5000

  async with TMClient(HOST, PORT) as client:
    print('Connected!')
    await client.authenticate('SuperAdmin', 'SuperAdmin')
    print('Authenticated!')

    version = await client.get_version()
    print(f'Version: {version}')
    status = await client.get_status()
    print(f'Status: {status}')
    player_list = await client.get_player_list(100, 0)
    print(f'Players: {player_list}')


if __name__ == '__main__':
  asyncio.run(main())
```

## Callback Usage
```python
from trackmania_client import TrackManiaClient as TMClient
import asyncio

def callback_handler(callback: str, data: tuple):
  print(f'Callback: {callback}, {data}')

async def main():
  HOST = 'localhost'
  PORT = 5000

  async with TMClient(HOST, PORT) as client:
    print('Connected!')
    await client.authenticate('SuperAdmin', 'SuperAdmin')
    print('Authenticated!')

    client.register_general_callback_handler(callback_handler)

    result = await client.enable_callbacks()
    print(f'Callbacks enabled: {result}')

    echo = await client.echo()
    print(f'Echo: {echo}')

    client.unregister_general_callback_handler(callback_handler)

    result = await client.disable_callbacks()
    print(f'Callbacks disabled: {result}')

    echo = await client.echo()


if __name__ == '__main__':
  asyncio.run(main())
```

Output:
```
Connected!
Authenticated!
Callbacks enabled: True
Callback: TrackMania.Echo, echo param 2
Echo: True
Callbacks disabled: True
```

Handlers can also be registered to specific callbacks:
```python
from trackmania_client import TrackManiaCallback as TMCallback

client.register_callback_handler(TMCallback.ECHO, echo_callback_handler)
client.unregister_callback_handler(TMCallback.ECHO, echo_callback_handler)
```
