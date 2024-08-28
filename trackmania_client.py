from enum import Enum
from typing import Callable
from gbx_remote_client import GbxRemoteClient


class TrackManiaCallback(Enum):
  PLAYER_CONNECT = "TrackMania.PlayerConnect"
  PLAYER_DISCONNECT = "TrackMania.PlayerDisconnect"
  PLAYER_CHAT = "TrackMania.PlayerChat"
  PLAYER_MANIALINK_PAGE_ANSWER = "TrackMania.PlayerManialinkPageAnswer"
  ECHO = "TrackMania.Echo"
  SERVER_START = "TrackMania.ServerStart"
  SERVER_STOP = "TrackMania.ServerStop"
  BEGIN_RACE = "TrackMania.BeginRace"
  END_RACE = "TrackMania.EndRace"
  BEGIN_CHALLENGE = "TrackMania.BeginChallenge"
  END_CHALLENGE = "TrackMania.EndChallenge"
  BEGIN_ROUND = "TrackMania.BeginRound"
  END_ROUND = "TrackMania.EndRound"
  STATUS_CHANGED = "TrackMania.StatusChanged"
  PLAYER_CHECKPOINT = "TrackMania.PlayerCheckpoint"
  PLAYER_FINISH = "TrackMania.PlayerFinish"
  PLAYER_INCOHERENCE = "TrackMania.PlayerIncoherence"
  BILL_UPDATED = "TrackMania.BillUpdated"
  TUNNEL_DATA_RECEIVED = "TrackMania.TunnelDataReceived"
  CHALLENGE_LIST_MODIFIED = "TrackMania.ChallengeListModified"
  PLAYER_INFO_CHANGED = "TrackMania.PlayerInfoChanged"
  MANUAL_FLOW_CONTROL_TRANSITION = "TrackMania.ManualFlowControlTransition"
  VOTE_UPDATED = "TrackMania.VoteUpdated"


class TrackManiaClient(GbxRemoteClient):
  def register_callback_handler(self, callback: TrackManiaCallback | str, handler: Callable[[str, tuple], None]) -> None:
    return super().register_callback_handler(callback, handler)

  def unregister_callback_handler(self, callback: TrackManiaCallback | str, handler: Callable[[str, tuple], None]) -> None:
    return super().unregister_callback_handler(callback, handler)

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
  
  async def echo(self, text_1: str = 'echo param 1', text_2: str = 'echo param 2') -> bool:
    return await self.execute('Echo', text_1, text_2)
