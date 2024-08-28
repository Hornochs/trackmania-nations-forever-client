from gbx_remote_client import GbxRemoteClient


class TrackManiaClient(GbxRemoteClient):
  async def get_version(self):
    return await self.execute('GetVersion')
  
  async def get_status(self):
    return await self.execute('GetStatus')
  
  async def get_player_list(self, max_players: int, start_index: int) -> list:
    return await self.execute('GetPlayerList', max_players, start_index)

  async def enable_callbacks(self) -> bool:
    return await self.execute('EnableCallbacks', True)
  
  async def disable_callbacks(self) -> bool:
    return await self.execute('EnableCallbacks', False)
