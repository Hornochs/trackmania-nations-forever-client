# TrackMania Nations Forever Client

This Python client is intended to be used with the TM Nations Forever remote procedure endpoint.

The available methods are documented at [ListMethods](/ListMethods.html).

## Usage Example

```python
from gbx_remote_client import GbxRemoteClient as TMClient
import asyncio

async def main():
  HOST = 'localhost'
  PORT = 5000

  async with TMClient(HOST, PORT) as client:
    print('Connected!')
    await client.authenticate('SuperAdmin', 'SuperAdmin')
    print('Authenticated!')

    version = await client.execute('GetVersion')
    print(f'Version: {version}')
    status = await client.execute('GetStatus')
    print(f'Status: {status}')
    response = client.execute('system.listMethods')
    print(f'Methods: {response}')
    player_list = await client.execute('GetPlayerList', 100, 0)
    print(f'Players: {player_list}')


if __name__ == '__main__':
  asyncio.run(main())
```
