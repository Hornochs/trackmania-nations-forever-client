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
