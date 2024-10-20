from enum import Enum
from typing import Callable
from .gbx_remote_client import GbxRemoteClient


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

  async def enable_callbacks(self) -> bool:
    """Allow the GameServer to call you back."""
    return await self.execute('EnableCallbacks', True)
  
  async def disable_callbacks(self) -> bool:
    """Disable the GameServer from calling you back."""
    return await self.execute('EnableCallbacks', False)
  
  async def echo(self, text_1: str = 'echo param 1', text_2: str = 'echo param 2') -> bool:
    return await self.execute('Echo', text_1, text_2)

  async def change_auth_password(self, login: str, new_password: str) -> bool:
    """Change the password for the specified login/user. Only available to SuperAdmin."""
    return await self.execute('ChangeAuthPassword', login, new_password)

  async def get_version(self) -> dict:
    """Returns a struct with the Name, Version and Build of the application remotely controlled."""
    return await self.execute('GetVersion')

  async def call_vote(self, command: str) -> bool:
    """Call a vote for a command. Only available to Admin."""
    return await self.execute('CallVote', command)

  async def call_vote_ex(self, command: str, ratio: float, timeout: int, voters: int) -> bool:
    """Extended call vote with additional parameters. Only available to Admin."""
    return await self.execute('CallVoteEx', command, ratio, timeout, voters)

  async def internal_call_vote(self) -> bool:
    """Used internally by the game."""
    return await self.execute('InternalCallVote')

  async def cancel_vote(self) -> bool:
    """Cancel the current vote. Only available to Admin."""
    return await self.execute('CancelVote')

  async def get_current_call_vote(self) -> dict:
    """Returns the vote currently in progress."""
    return await self.execute('GetCurrentCallVote')

  async def set_call_vote_timeout(self, timeout: int) -> bool:
    """Set a new timeout for waiting for votes. Only available to Admin."""
    return await self.execute('SetCallVoteTimeOut', timeout)

  async def get_call_vote_timeout(self) -> dict:
    """Get the current and next timeout for waiting for votes."""
    return await self.execute('GetCallVoteTimeOut')

  async def set_call_vote_ratio(self, ratio: float) -> bool:
    """Set a new default ratio for passing a vote. Only available to Admin."""
    return await self.execute('SetCallVoteRatio', ratio)

  async def get_call_vote_ratio(self) -> float:
    """Get the current default ratio for passing a vote."""
    return await self.execute('GetCallVoteRatio')

  async def set_call_vote_ratios(self, ratios: list) -> bool:
    """Set new ratios for passing specific votes. Only available to Admin."""
    return await self.execute('SetCallVoteRatios', ratios)

  async def get_call_vote_ratios(self) -> list:
    """Get the current ratios for passing votes."""
    return await self.execute('GetCallVoteRatios')

  async def chat_send_server_message(self, message: str) -> bool:
    """Send a text message to all clients without the server login. Only available to Admin."""
    return await self.execute('ChatSendServerMessage', message)

  async def chat_send_server_message_to_language(self, messages: list, login: str = "") -> bool:
    """Send a localized text message to clients. Only available to Admin."""
    return await self.execute('ChatSendServerMessageToLanguage', messages, login)

  async def chat_send_server_message_to_id(self, message: str, player_id: int) -> bool:
    """Send a text message to a client by PlayerId. Only available to Admin."""
    return await self.execute('ChatSendServerMessageToId', message, player_id)

  async def chat_send_server_message_to_login(self, message: str, login: str) -> bool:
    """Send a text message to a client by login. Only available to Admin."""
    return await self.execute('ChatSendServerMessageToLogin', message, login)

  async def chat_send(self, message: str) -> bool:
    """Send a text message to all clients. Only available to Admin."""
    return await self.execute('ChatSend', message)

  async def chat_send_to_language(self, messages: list, login: str = "") -> bool:
    """Send a localized text message to clients or a specific login. Only available to Admin."""
    return await self.execute('ChatSendToLanguage', messages, login)

  async def chat_send_to_login(self, message: str, login: str) -> bool:
    """Send a text message to a client by login. Only available to Admin."""
    return await self.execute('ChatSendToLogin', message, login)

  async def chat_send_to_id(self, message: str, player_id: int) -> bool:
    """Send a text message to a client by PlayerId. Only available to Admin."""
    return await self.execute('ChatSendToId', message, player_id)

  async def get_chat_lines(self) -> list:
    """Returns the last chat lines. Maximum of 40 lines. Only available to Admin."""
    return await self.execute('GetChatLines')

  async def chat_enable_manual_routing(self, enable: bool, auto_forward: bool = False) -> bool:
    """Enable manual routing of chat messages. Only available to Admin."""
    return await self.execute('ChatEnableManualRouting', enable, auto_forward)

  async def chat_forward_to_login(self, text: str, sender_login: str, dest_login: str) -> bool:
    """Forward a text message on behalf of a sender to a specific destination login. Only available if manual routing is enabled."""
    return await self.execute('ChatForwardToLogin', text, sender_login, dest_login)

  async def send_notice(self, message: str, avatar_login: str = '', max_duration: int = 3) -> bool:
    """Display a notice on all clients. Only available to Admin."""
    return await self.execute('SendNotice', message, avatar_login, max_duration)

  async def send_notice_to_id(self, player_id: int, message: str, avatar_id: int = 255, max_duration: int = 3) -> bool:
    """Display a notice on the client with the specified PlayerId. Only available to Admin."""
    return await self.execute('SendNoticeToId', player_id, message, avatar_id, max_duration)

  async def send_notice_to_login(self, login: str, message: str, avatar_login: str = '', max_duration: int = 3) -> bool:
    """Display a notice on the client with the specified login. Only available to Admin."""
    return await self.execute('SendNoticeToLogin', login, message, avatar_login, max_duration)

  async def send_display_manialink_page(self, xml: str, timeout: int, hide_on_click: bool) -> bool:
    """Display a manialink page on all clients. Only available to Admin."""
    return await self.execute('SendDisplayManialinkPage', xml, timeout, hide_on_click)

  async def send_display_manialink_page_to_id(self, player_id: int, xml: str, timeout: int, hide_on_click: bool) -> bool:
    """Display a manialink page on the client with the specified PlayerId. Only available to Admin."""
    return await self.execute('SendDisplayManialinkPageToId', player_id, xml, timeout, hide_on_click)

  async def send_display_manialink_page_to_login(self, login: str, xml: str, timeout: int, hide_on_click: bool) -> bool:
    """Display a manialink page on the client with the specified login. Only available to Admin."""
    return await self.execute('SendDisplayManialinkPageToLogin', login, xml, timeout, hide_on_click)

  async def send_hide_manialink_page(self) -> bool:
    """Hide the displayed manialink page on all clients. Only available to Admin."""
    return await self.execute('SendHideManialinkPage')

  async def send_hide_manialink_page_to_id(self, player_id: int) -> bool:
    """Hide the displayed manialink page on the client with the specified PlayerId. Only available to Admin."""
    return await self.execute('SendHideManialinkPageToId', player_id)

  async def send_hide_manialink_page_to_login(self, login: str) -> bool:
    """Hide the displayed manialink page on the client with the specified login. Only available to Admin."""
    return await self.execute('SendHideManialinkPageToLogin', login)

  async def get_manialink_page_answers(self) -> list:
    """Returns the latest results from the current manialink page."""
    return await self.execute('GetManialinkPageAnswers')

  async def kick(self, login: str, message: str = '') -> bool:
    """Kick the player with the specified login, with an optional message. Only available to Admin."""
    return await self.execute('Kick', login, message)

  async def kick_id(self, player_id: int, message: str = '') -> bool:
    """Kick the player with the specified PlayerId, with an optional message. Only available to Admin."""
    return await self.execute('KickId', player_id, message)

  async def ban(self, login: str, message: str = '') -> bool:
    """Ban the player with the specified login, with an optional message. Only available to Admin."""
    return await self.execute('Ban', login, message)

  async def ban_and_blacklist(self, login: str, message: str, save: bool = True) -> bool:
    """Ban the player with the specified login, add them to the blacklist, and optionally save the new list. Only available to Admin."""
    return await self.execute('BanAndBlackList', login, message, save)

  async def ban_id(self, player_id: int, message: str = '') -> bool:
    """Ban the player with the specified PlayerId, with an optional message. Only available to Admin."""
    return await self.execute('BanId', player_id, message)

  async def unban(self, login: str) -> bool:
    """Unban the player with the specified client name. Only available to Admin."""
    return await self.execute('UnBan', login)

  async def clean_ban_list(self) -> bool:
    """Clean the ban list of the server. Only available to Admin."""
    return await self.execute('CleanBanList')

  async def get_ban_list(self, max_infos: int, start_index: int) -> list:
    """Returns the list of banned players. Only available to Admin."""
    return await self.execute('GetBanList', max_infos, start_index)

  async def blacklist(self, login: str) -> bool:
    """Blacklist the player with the specified login. Only available to SuperAdmin."""
    return await self.execute('BlackList', login)

  async def blacklist_id(self, player_id: int) -> bool:
    """Blacklist the player with the specified PlayerId. Only available to SuperAdmin."""
    return await self.execute('BlackListId', player_id)

  async def unblacklist(self, login: str) -> bool:
    """Unblacklist the player with the specified login. Only available to SuperAdmin."""
    return await self.execute('UnBlackList', login)

  async def clean_blacklist(self) -> bool:
    """Clean the blacklist of the server. Only available to SuperAdmin."""
    return await self.execute('CleanBlackList')

  async def get_blacklist(self, max_infos: int, start_index: int) -> list:
    """Returns the list of blacklisted players. Only available to SuperAdmin."""
    return await self.execute('GetBlackList', max_infos, start_index)

  async def load_blacklist(self, filename: str) -> bool:
    """Load the blacklist file with the specified file name. Only available to Admin."""
    return await self.execute('LoadBlackList', filename)

  async def save_blacklist(self, filename: str) -> bool:
    """Save the blacklist in the file with specified file name. Only available to Admin."""
    return await self.execute('SaveBlackList', filename)

  async def add_guest(self, login: str) -> bool:
    """Add the player with the specified login on the guest list. Only available to Admin."""
    return await self.execute('AddGuest', login)

  async def add_guest_id(self, player_id: int) -> bool:
    """Add the player with the specified PlayerId on the guest list. Only available to Admin."""
    return await self.execute('AddGuestId', player_id)

  async def remove_guest(self, login: str) -> bool:
    """Remove the player with the specified login from the guest list. Only available to Admin."""
    return await self.execute('RemoveGuest', login)

  async def remove_guest_id(self, player_id: int) -> bool:
    """Remove the player with the specified PlayerId from the guest list. Only available to Admin."""
    return await self.execute('RemoveGuestId', player_id)

  async def clean_guest_list(self) -> bool:
    """Clean the guest list of the server. Only available to Admin."""
    return await self.execute('CleanGuestList')

  async def get_guest_list(self, max_infos: int, start_index: int) -> list:
    """Returns the list of players on the guest list. Only available to Admin."""
    return await self.execute('GetGuestList', max_infos, start_index)

  async def load_guest_list(self, filename: str) -> bool:
    """Load the guest list file with the specified file name. Only available to Admin."""
    return await self.execute('LoadGuestList', filename)

  async def save_guest_list(self, filename: str) -> bool:
    """Save the guest list in the file with specified file name. Only available to Admin."""
    return await self.execute('SaveGuestList', filename)

  async def set_buddy_notification(self, login: str, enabled: bool) -> bool:
    """Sets whether buddy notifications should be sent in the chat. Only available to Admin."""
    return await self.execute('SetBuddyNotification', login, enabled)

  async def get_buddy_notification(self, login: str) -> bool:
    """Gets whether buddy notifications are enabled for the specified login."""
    return await self.execute('GetBuddyNotification', login)

  async def write_file(self, filename: str, data: str) -> bool:
    """Write the data to the specified file. The filename is relative to the Tracks path. Only available to Admin."""
    return await self.execute('WriteFile', filename, data)

  async def tunnel_send_data_to_id(self, player_id: int, data: str) -> bool:
    """Send the data to the specified player. Only available to Admin."""
    return await self.execute('TunnelSendDataToId', player_id, data)

  async def tunnel_send_data_to_login(self, login: str, data: str) -> bool:
    """Send the data to the specified player by login. Only available to Admin."""
    return await self.execute('TunnelSendDataToLogin', login, data)

  async def echo(self, text_1: str = 'echo param 1', text_2: str = 'echo param 2') -> bool:
    """Just log the parameters and invoke a callback. Only available to Admin."""
    return await self.execute('Echo', text_1, text_2)

  async def ignore(self, login: str) -> bool:
    """Ignore the player with the specified login. Only available to Admin."""
    return await self.execute('Ignore', login)

  async def ignore_id(self, player_id: int) -> bool:
    """Ignore the player with the specified PlayerId. Only available to Admin."""
    return await self.execute('IgnoreId', player_id)

  async def unignore(self, login: str) -> bool:
    """Unignore the player with the specified login. Only available to Admin."""
    return await self.execute('UnIgnore', login)

  async def unignore_id(self, player_id: int) -> bool:
    """Unignore the player with the specified PlayerId. Only available to Admin."""
    return await self.execute('UnIgnoreId', player_id)

  async def clean_ignore_list(self) -> bool:
    """Clean the ignore list of the server. Only available to Admin."""
    return await self.execute('CleanIgnoreList')

  async def get_ignore_list(self, max_infos: int, start_index: int) -> list:
    """Returns the list of ignored players. Only available to Admin."""
    return await self.execute('GetIgnoreList', max_infos, start_index)

  async def pay(self, login: str, coppers: int, label: str) -> int:
    """Pay coppers from the server account to a player, returns the BillId. Only available to Admin."""
    return await self.execute('Pay', login, coppers, label)

  async def send_bill(self, login_from: str, coppers: int, label: str, login_to: str = '') -> int:
    """Create a bill, send it to a player, and return the BillId. Only available to Admin."""
    return await self.execute('SendBill', login_from, coppers, label, login_to)

  async def get_bill_state(self, bill_id: int) -> dict:
    """Returns the current state of a bill."""
    return await self.execute('GetBillState', bill_id)

  async def get_server_coppers(self) -> int:
    """Returns the current number of coppers on the server account."""
    return await self.execute('GetServerCoppers')

  async def get_system_info(self) -> dict:
    """Get some system infos, including connection rates (in kbps)."""
    return await self.execute('GetSystemInfo')

  async def set_connection_rates(self, download_rate: int, upload_rate: int) -> bool:
    """Set the download and upload rates (in kbps)."""
    return await self.execute('SetConnectionRates', download_rate, upload_rate)

  async def set_server_name(self, name: str) -> bool:
    """Set a new server name in utf8 format. Only available to Admin."""
    return await self.execute('SetServerName', name)

  async def get_server_name(self) -> str:
    """Get the server name in utf8 format."""
    return await self.execute('GetServerName')

  async def set_server_comment(self, comment: str) -> bool:
    """Set a new server comment in utf8 format. Only available to Admin."""
    return await self.execute('SetServerComment', comment)

  async def get_server_comment(self) -> str:
    """Get the server comment in utf8 format."""
    return await self.execute('GetServerComment')

  async def set_hide_server(self, hide: int) -> bool:
    """Set whether the server should be hidden from the public server list. Only available to Admin."""
    return await self.execute('SetHideServer', hide)

  async def get_hide_server(self) -> int:
    """Get whether the server wants to be hidden from the public server list."""
    return await self.execute('GetHideServer')

  async def is_relay_server(self) -> bool:
    """Returns true if this is a relay server."""
    return await self.execute('IsRelayServer')

  async def set_server_password(self, password: str) -> bool:
    """Set a new password for the server. Only available to Admin."""
    return await self.execute('SetServerPassword', password)

  async def get_server_password(self) -> str:
    """Get the server password if called as Admin or Super Admin, else returns if a password is needed or not."""
    return await self.execute('GetServerPassword')

  async def set_server_password_for_spectator(self, password: str) -> bool:
    """Set a new password for the spectator mode. Only available to Admin."""
    return await self.execute('SetServerPasswordForSpectator', password)

  async def get_server_password_for_spectator(self) -> str:
    """Get the password for spectator mode if called as Admin or Super Admin, else returns if a password is needed or not."""
    return await self.execute('GetServerPasswordForSpectator')

  async def set_max_players(self, max_players: int) -> bool:
    """Set a new maximum number of players. Only available to Admin. Requires a challenge restart to be taken into account."""
    return await self.execute('SetMaxPlayers', max_players)

  async def get_max_players(self) -> dict:
    """Get the current and next maximum number of players allowed on server."""
    return await self.execute('GetMaxPlayers')

  async def set_max_spectators(self, max_spectators: int) -> bool:
    """Set a new maximum number of Spectators. Only available to Admin. Requires a challenge restart to be taken into account."""
    return await self.execute('SetMaxSpectators', max_spectators)

  async def get_max_spectators(self) -> dict:
    """Get the current and next maximum number of Spectators allowed on server."""
    return await self.execute('GetMaxSpectators')

  async def enable_p2p_upload(self, enable: bool) -> bool:
    """Enable or disable peer-to-peer upload from server. Only available to Admin."""
    return await self.execute('EnableP2PUpload', enable)

  async def is_p2p_upload(self) -> bool:
    """Returns if the peer-to-peer upload from server is enabled."""
    return await self.execute('IsP2PUpload')

  async def enable_p2p_download(self, enable: bool) -> bool:
    """Enable or disable peer-to-peer download for server. Only available to Admin."""
    return await self.execute('EnableP2PDownload', enable)

  async def is_p2p_download(self) -> bool:
    """Returns if the peer-to-peer download for server is enabled."""
    return await self.execute('IsP2PDownload')

  async def allow_challenge_download(self, allow: bool) -> bool:
    """Allow clients to download challenges from the server. Only available to Admin."""
    return await self.execute('AllowChallengeDownload', allow)

  async def is_challenge_download_allowed(self) -> bool:
    """Returns if clients can download challenges from the server."""
    return await self.execute('IsChallengeDownloadAllowed')

  async def auto_save_replays(self, enable: bool) -> bool:
    """Enable the autosaving of all replays on the server. Only available to SuperAdmin."""
    return await self.execute('AutoSaveReplays', enable)

  async def auto_save_validation_replays(self, enable: bool) -> bool:
    """Enable the autosaving on the server of validation replays. Only available to SuperAdmin."""
    return await self.execute('AutoSaveValidationReplays', enable)

  async def is_auto_save_replays_enabled(self) -> bool:
    """Returns if autosaving of all replays is enabled on the server."""
    return await self.execute('IsAutoSaveReplaysEnabled')

  async def is_auto_save_validation_replays_enabled(self) -> bool:
    """Returns if autosaving of validation replays is enabled on the server."""
    return await self.execute('IsAutoSaveValidationReplaysEnabled')

  async def save_current_replay(self, filename: str = '') -> bool:
    """Saves the current replay. Pass a filename, or '' for an automatic filename. Only available to Admin."""
    return await self.execute('SaveCurrentReplay', filename)

  async def save_best_ghosts_replay(self, login: str, filename: str = '') -> bool:
    """Saves a replay with the ghost of all the players' best race. Only available to Admin."""
    return await self.execute('SaveBestGhostsReplay', login, filename)

  async def get_validation_replay(self, login: str) -> str:
    """Returns a replay containing the data needed to validate the current best time of the player."""
    return await self.execute('GetValidationReplay', login)

  async def set_ladder_mode(self, mode: int) -> bool:
    """Set a new ladder mode between ladder disabled (0) and forced (1). Only available to Admin."""
    return await self.execute('SetLadderMode', mode)

  async def get_ladder_mode(self) -> dict:
    """Get the current and next ladder mode on server."""
    return await self.execute('GetLadderMode')

  async def get_ladder_server_limits(self) -> dict:
    """Get the ladder points limit for the players allowed on this server."""
    return await self.execute('GetLadderServerLimits')

  async def set_vehicle_net_quality(self, quality: int) -> bool:
    """Set the network vehicle quality to Fast (0) or High (1). Only available to Admin."""
    return await self.execute('SetVehicleNetQuality', quality)

  async def get_vehicle_net_quality(self) -> dict:
    """Get the current and next network vehicle quality on server."""
    return await self.execute('GetVehicleNetQuality')

  async def set_server_options(self, options: dict) -> bool:
    """Set new server options using the struct passed as parameters. Only available to Admin."""
    return await self.execute('SetServerOptions', options)

  async def get_server_options(self, version: int = 0) -> dict:
    """Returns a struct containing the server options. Optional parameter for compatibility."""
    return await self.execute('GetServerOptions', version)

  async def set_server_pack_mask(self, pack_mask: str) -> bool:
    """Defines the packmask of the server. Only available to Admin."""
    return await self.execute('SetServerPackMask', pack_mask)

  async def get_server_pack_mask(self) -> str:
    """Get the packmask of the server."""
    return await self.execute('GetServerPackMask')

  async def set_forced_mods(self, override: bool, mods: list) -> bool:
    """Set the mods to apply on the clients. Requires a challenge restart. Only available to Admin."""
    return await self.execute('SetForcedMods', override, mods)

  async def get_forced_mods(self) -> dict:
    """Get the mods settings."""
    return await self.execute('GetForcedMods')

  async def set_forced_music(self, override: bool, url_or_filename: str) -> bool:
    """Set the music to play on the clients. Requires a challenge restart. Only available to Admin."""
    return await self.execute('SetForcedMusic', override, url_or_filename)

  async def get_forced_music(self) -> dict:
    """Get the music setting."""
    return await self.execute('GetForcedMusic')

  async def set_forced_skins(self, skins: list) -> bool:
    """Defines a list of remappings for player skins. Only available to Admin."""
    return await self.execute('SetForcedSkins', skins)

  async def get_forced_skins(self) -> list:
    """Get the current forced skins."""
    return await self.execute('GetForcedSkins')

  async def get_last_connection_error_message(self) -> str:
    """Returns the last error message for an internet connection. Only available to Admin."""
    return await self.execute('GetLastConnectionErrorMessage')

  async def set_referee_password(self, password: str) -> bool:
    """Set a new password for the referee mode. Only available to Admin."""
    return await self.execute('SetRefereePassword', password)

  async def get_referee_password(self) -> str:
    """Get the password for referee mode if called as Admin or Super Admin."""
    return await self.execute('GetRefereePassword')

  async def set_referee_mode(self, mode: int) -> bool:
    """Set the referee validation mode. Only available to Admin."""
    return await self.execute('SetRefereeMode', mode)

  async def get_referee_mode(self) -> int:
    """Get the referee validation mode."""
    return await self.execute('GetRefereeMode')

  async def set_use_changing_validation_seed(self, use: bool) -> bool:
    """Set whether the game should use a variable validation seed or not. Only available to Admin."""
    return await self.execute('SetUseChangingValidationSeed', use)

  async def get_use_changing_validation_seed(self) -> dict:
    """Get the current and next value of UseChangingValidationSeed."""
    return await self.execute('GetUseChangingValidationSeed')

  async def set_warm_up(self, warm_up: bool) -> bool:
    """Sets whether the server is in warm-up phase or not. Only available to Admin."""
    return await self.execute('SetWarmUp', warm_up)

  async def get_warm_up(self) -> bool:
    """Returns whether the server is in warm-up phase."""
    return await self.execute('GetWarmUp')

  async def challenge_restart(self) -> bool:
    """Restarts the challenge. Only available to Admin."""
    return await self.execute('ChallengeRestart')

  async def restart_challenge(self) -> bool:
    """Restarts the challenge. Only available to Admin."""
    return await self.execute('RestartChallenge')

  async def next_challenge(self) -> bool:
    """Switch to next challenge. Only available to Admin."""
    return await self.execute('NextChallenge')

  async def stop_server(self) -> bool:
    """Stop the server. Only available to SuperAdmin."""
    return await self.execute('StopServer')

  async def force_end_round(self) -> bool:
    """In Rounds or Laps mode, force the end of round without waiting for all players to give up/finish. Only available to Admin."""
    return await self.execute('ForceEndRound')

  async def set_game_infos(self, game_infos: dict) -> bool:
    """Set new game settings using the struct passed as parameters. Only available to Admin."""
    return await self.execute('SetGameInfos', game_infos)

  async def get_current_game_info(self, version: int = 0) -> dict:
    """Returns the current game settings. Optional parameter for compatibility."""
    return await self.execute('GetCurrentGameInfo', version)

  async def get_next_game_info(self, version: int = 0) -> dict:
    """Returns the game settings for the next challenge. Optional parameter for compatibility."""
    return await self.execute('GetNextGameInfo', version)

  async def get_game_infos(self, version: int = 0) -> dict:
    """Returns the current and next game settings. Optional parameter for compatibility."""
    return await self.execute('GetGameInfos', version)

  async def set_game_mode(self, mode: int) -> bool:
    """Set a new game mode. Only available to Admin."""
    return await self.execute('SetGameMode', mode)

  async def get_game_mode(self) -> int:
    """Get the current game mode."""
    return await self.execute('GetGameMode')

  async def set_chat_time(self, chat_time: int) -> bool:
    """Set a new chat time value in milliseconds. Only available to Admin."""
    return await self.execute('SetChatTime', chat_time)

  async def get_chat_time(self) -> dict:
    """Get the current and next chat time."""
    return await self.execute('GetChatTime')

  async def set_finish_timeout(self, finish_timeout: int) -> bool:
    """Set a new finish timeout (for rounds/laps mode) value in milliseconds. Only available to Admin."""
    return await self.execute('SetFinishTimeout', finish_timeout)

  async def get_finish_timeout(self) -> dict:
    """Get the current and next FinishTimeout."""
    return await self.execute('GetFinishTimeout')

  async def set_all_warm_up_duration(self, duration: int) -> bool:
    """Set the automatic warm-up phase in all modes. Only available to Admin."""
    return await self.execute('SetAllWarmUpDuration', duration)

  async def get_all_warm_up_duration(self) -> dict:
    """Get whether the automatic warm-up phase is enabled in all modes."""
    return await self.execute('GetAllWarmUpDuration')

  async def set_disable_respawn(self, disable: bool) -> bool:
    """Set whether to disallow players to respawn. Only available to Admin."""
    return await self.execute('SetDisableRespawn', disable)

  async def get_disable_respawn(self) -> dict:
    """Get whether players are disallowed to respawn."""
    return await self.execute('GetDisableRespawn')

  async def set_force_show_all_opponents(self, value: int) -> bool:
    """Set whether to override the players preferences and always display all opponents. Only available to Admin."""
    return await self.execute('SetForceShowAllOpponents', value)

  async def get_force_show_all_opponents(self) -> dict:
    """Get whether players are forced to show all opponents."""
    return await self.execute('GetForceShowAllOpponents')

  async def set_time_attack_limit(self, limit: int) -> bool:
    """Set a new time limit for time attack mode. Only available to Admin."""
    return await self.execute('SetTimeAttackLimit', limit)

  async def get_time_attack_limit(self) -> dict:
    """Get the current and next time limit for time attack mode."""
    return await self.execute('GetTimeAttackLimit')

  async def set_time_attack_synch_start_period(self, period: int) -> bool:
    """Set a new synchronized start period for time attack mode. Only available to Admin."""
    return await self.execute('SetTimeAttackSynchStartPeriod', period)

  async def get_time_attack_synch_start_period(self) -> dict:
    """Get the current and synchronized start period for time attack mode."""
    return await self.execute('GetTimeAttackSynchStartPeriod')

  async def set_laps_time_limit(self, limit: int) -> bool:
    """Set a new time limit for laps mode. Only available to Admin."""
    return await self.execute('SetLapsTimeLimit', limit)

  async def get_laps_time_limit(self) -> dict:
    """Get the current and next time limit for laps mode."""
    return await self.execute('GetLapsTimeLimit')

  async def set_nb_laps(self, nb_laps: int) -> bool:
    """Set a new number of laps for laps mode. Only available to Admin."""
    return await self.execute('SetNbLaps', nb_laps)

  async def get_nb_laps(self) -> dict:
    """Get the current and next number of laps for laps mode."""
    return await self.execute('GetNbLaps')

  async def set_round_forced_laps(self, laps: int) -> bool:
    """Set a new number of laps for rounds mode. Only available to Admin."""
    return await self.execute('SetRoundForcedLaps', laps)

  async def get_round_forced_laps(self) -> dict:
    """Get the current and next number of laps for rounds mode."""
    return await self.execute('GetRoundForcedLaps')

  async def set_round_points_limit(self, limit: int) -> bool:
    """Set a new points limit for rounds mode. Only available to Admin."""
    return await self.execute('SetRoundPointsLimit', limit)

  async def get_round_points_limit(self) -> dict:
    """Get the current and next points limit for rounds mode."""
    return await self.execute('GetRoundPointsLimit')

  async def set_round_custom_points(self, points: list, relax_constraints: bool = False) -> bool:
    """Set the points used for the scores in rounds mode. Only available to Admin."""
    return await self.execute('SetRoundCustomPoints', points, relax_constraints)

  async def get_round_custom_points(self) -> list:
    """Gets the points used for the scores in rounds mode."""
    return await self.execute('GetRoundCustomPoints')

  async def set_use_new_rules_round(self, use: bool) -> bool:
    """Set if new rules are used for rounds mode. Only available to Admin."""
    return await self.execute('SetUseNewRulesRound', use)

  async def get_use_new_rules_round(self) -> dict:
    """Get if the new rules are used for rounds mode."""
    return await self.execute('GetUseNewRulesRound')

  async def set_team_points_limit(self, limit: int) -> bool:
    """Set a new points limit for team mode. Only available to Admin."""
    return await self.execute('SetTeamPointsLimit', limit)

  async def get_team_points_limit(self) -> dict:
    """Get the current and next points limit for team mode."""
    return await self.execute('GetTeamPointsLimit')

  async def set_max_points_team(self, max_points: int) -> bool:
    """Set a new number of maximum points per round for team mode. Only available to Admin."""
    return await self.execute('SetMaxPointsTeam', max_points)

  async def get_max_points_team(self) -> dict:
    """Get the current and next number of maximum points per round for team mode."""
    return await self.execute('GetMaxPointsTeam')

  async def set_use_new_rules_team(self, use: bool) -> bool:
    """Set if new rules are used for team mode. Only available to Admin."""
    return await self.execute('SetUseNewRulesTeam', use)

  async def get_use_new_rules_team(self) -> dict:
    """Get if the new rules are used for team mode."""
    return await self.execute('GetUseNewRulesTeam')

  async def set_cup_points_limit(self, limit: int) -> bool:
    """Set the points needed for victory in Cup mode. Only available to Admin."""
    return await self.execute('SetCupPointsLimit', limit)

  async def get_cup_points_limit(self) -> dict:
    """Get the points needed for victory in Cup mode."""
    return await self.execute('GetCupPointsLimit')

  async def set_cup_rounds_per_challenge(self, rounds: int) -> bool:
    """Sets the number of rounds before going to next challenge in Cup mode. Only available to Admin."""
    return await self.execute('SetCupRoundsPerChallenge', rounds)

  async def get_cup_rounds_per_challenge(self) -> dict:
    """Get the number of rounds before going to next challenge in Cup mode."""
    return await self.execute('GetCupRoundsPerChallenge')

  async def set_cup_warm_up_duration(self, duration: int) -> bool:
    """Set whether to enable the automatic warm-up phase in Cup mode. Only available to Admin."""
    return await self.execute('SetCupWarmUpDuration', duration)

  async def get_cup_warm_up_duration(self) -> dict:
    """Get whether the automatic warm-up phase is enabled in Cup mode."""
    return await self.execute('GetCupWarmUpDuration')

  async def set_cup_nb_winners(self, nb_winners: int) -> bool:
    """Set the number of winners to determine before the match is considered over. Only available to Admin."""
    return await self.execute('SetCupNbWinners', nb_winners)

  async def get_cup_nb_winners(self) -> dict:
    """Get the number of winners to determine before the match is considered over."""
    return await self.execute('GetCupNbWinners')

  async def get_current_challenge_index(self) -> int:
    """Returns the current challenge index in the selection, or -1 if the challenge is no longer in the selection."""
    return await self.execute('GetCurrentChallengeIndex')

  async def get_next_challenge_index(self) -> int:
    """Returns the challenge index in the selection that will be played next."""
    return await self.execute('GetNextChallengeIndex')

  async def set_next_challenge_index(self, index: int) -> bool:
    """Sets the challenge index in the selection that will be played next."""
    return await self.execute('SetNextChallengeIndex', index)

  async def get_current_challenge_info(self) -> dict:
    """Returns a struct containing the infos for the current challenge."""
    return await self.execute('GetCurrentChallengeInfo')

  async def get_next_challenge_info(self) -> dict:
    """Returns a struct containing the infos for the next challenge."""
    return await self.execute('GetNextChallengeInfo')

  async def get_challenge_info(self, filename: str) -> dict:
    """Returns a struct containing the infos for the challenge with the specified filename."""
    return await self.execute('GetChallengeInfo', filename)

  async def check_challenge_for_current_server_params(self, filename: str) -> bool:
    """Returns a boolean if the challenge with the specified filename matches the current server settings."""
    return await self.execute('CheckChallengeForCurrentServerParams', filename)

  async def get_challenge_list(self, max_infos: int, start_index: int) -> list:
    """Returns a list of challenges among the current selection of the server."""
    return await self.execute('GetChallengeList', max_infos, start_index)

  async def add_challenge(self, filename: str) -> bool:
    """Add the challenge with the specified filename at the end of the current selection. Only available to Admin."""
    return await self.execute('AddChallenge', filename)

  async def add_challenge_list(self, filenames: list) -> int:
    """Add the list of challenges with the specified filenames at the end of the current selection. Only available to Admin."""
    return await self.execute('AddChallengeList', filenames)

  async def remove_challenge(self, filename: str) -> bool:
    """Remove the challenge with the specified filename from the current selection. Only available to Admin."""
    return await self.execute('RemoveChallenge', filename)

  async def remove_challenge_list(self, filenames: list) -> int:
    """Remove the list of challenges with the specified filenames from the current selection. Only available to Admin."""
    return await self.execute('RemoveChallengeList', filenames)

  async def insert_challenge(self, filename: str) -> bool:
    """Insert the challenge with the specified filename after the current challenge. Only available to Admin."""
    return await self.execute('InsertChallenge', filename)

  async def insert_challenge_list(self, filenames: list) -> int:
    """Insert the list of challenges with the specified filenames after the current challenge. Only available to Admin."""
    return await self.execute('InsertChallengeList', filenames)

  async def choose_next_challenge(self, filename: str) -> bool:
    """Set as next challenge the one with the specified filename, if it is present in the selection. Only available to Admin."""
    return await self.execute('ChooseNextChallenge', filename)

  async def choose_next_challenge_list(self, filenames: list) -> int:
    """Set as next challenges the list of challenges with the specified filenames, if they are present in the selection. Only available to Admin."""
    return await self.execute('ChooseNextChallengeList', filenames)

  async def load_match_settings(self, filename: str) -> int:
    """Set a list of challenges defined in the playlist with the specified filename as the current selection of the server. Only available to Admin."""
    return await self.execute('LoadMatchSettings', filename)

  async def append_playlist_from_match_settings(self, filename: str) -> int:
    """Add a list of challenges defined in the playlist with the specified filename at the end of the current selection. Only available to Admin."""
    return await self.execute('AppendPlaylistFromMatchSettings', filename)

  async def save_match_settings(self, filename: str) -> int:
    """Save the current selection of challenge in the playlist with the specified filename, as well as the current gameinfos. Only available to Admin."""
    return await self.execute('SaveMatchSettings', filename)

  async def insert_playlist_from_match_settings(self, filename: str) -> int:
    """Insert a list of challenges defined in the playlist with the specified filename after the current challenge. Only available to Admin."""
    return await self.execute('InsertPlaylistFromMatchSettings', filename)

  async def get_player_list(self, max_players: int, start_index: int, version: int = 0) -> list:
    """Returns the list of players on the server."""
    return await self.execute('GetPlayerList', max_players, start_index, version)

  async def get_player_info(self, login: str, version: int = 0) -> dict:
    """Returns a struct containing the infos on the player with the specified login."""
    return await self.execute('GetPlayerInfo', login, version)

  async def get_detailed_player_info(self, login: str) -> dict:
    """Returns a struct containing the detailed infos on the player with the specified login."""
    return await self.execute('GetDetailedPlayerInfo', login)

  async def get_main_server_player_info(self, version: int = 0) -> dict:
    """Returns a struct containing the player infos of the game server. Only available to Admin."""
    return await self.execute('GetMainServerPlayerInfo', version)

  async def get_current_ranking(self, max_infos: int, start_index: int) -> list:
    """Returns the current rankings for the race in progress."""
    return await self.execute('GetCurrentRanking', max_infos, start_index)

  async def get_current_ranking_for_login(self, login: str) -> list:
    """Returns the current ranking for the race in progress of the player with the specified login."""
    return await self.execute('GetCurrentRankingForLogin', login)

  async def force_scores(self, scores: list, silent_mode: bool = False) -> bool:
    """Force the scores of the current game. Only available in rounds and team mode."""
    return await self.execute('ForceScores', scores, silent_mode)

  async def force_player_team(self, login: str, team: int) -> bool:
    """Force the team of the player. Only available in team mode."""
    return await self.execute('ForcePlayerTeam', login, team)

  async def force_player_team_id(self, player_id: int, team: int) -> bool:
    """Force the team of the player by PlayerId. Only available in team mode."""
    return await self.execute('ForcePlayerTeamId', player_id, team)

  async def force_spectator(self, login: str, mode: int) -> bool:
    """Force the spectating status of the player. Only available to Admin."""
    return await self.execute('ForceSpectator', login, mode)

  async def force_spectator_id(self, player_id: int, mode: int) -> bool:
    """Force the spectating status of the player by PlayerId. Only available to Admin."""
    return await self.execute('ForceSpectatorId', player_id, mode)

  async def force_spectator_target(self, spectator_login: str, target_login: str, camera_type: int) -> bool:
    """Force spectators to look at a specific player. Only available to Admin."""
    return await self.execute('ForceSpectatorTarget', spectator_login, target_login, camera_type)

  async def force_spectator_target_id(self, spectator_id: int, target_id: int, camera_type: int) -> bool:
    """Force spectators to look at a specific player by PlayerId. Only available to Admin."""
    return await self.execute('ForceSpectatorTargetId', spectator_id, target_id, camera_type)

  async def spectator_release_player_slot(self, login: str) -> bool:
    """Free a player slot held by a spectator. Only available to Admin."""
    return await self.execute('SpectatorReleasePlayerSlot', login)

  async def spectator_release_player_slot_id(self, player_id: int) -> bool:
    """Free a player slot held by a spectator by PlayerId. Only available to Admin."""
    return await self.execute('SpectatorReleasePlayerSlotId', player_id)

  async def manual_flow_control_enable(self, enable: bool) -> bool:
    """Enable control of the game flow. Only available to Admin."""
    return await self.execute('ManualFlowControlEnable', enable)

  async def manual_flow_control_proceed(self) -> bool:
    """Allows the game to proceed. Only available to Admin."""
    return await self.execute('ManualFlowControlProceed')

  async def manual_flow_control_is_enabled(self) -> int:
    """Returns whether the manual control of the game flow is enabled."""
    return await self.execute('ManualFlowControlIsEnabled')

  async def manual_flow_control_get_cur_transition(self) -> str:
    """Returns the transition that is currently blocked, or '' if none. Only available to Admin."""
    return await self.execute('ManualFlowControlGetCurTransition')

  async def check_end_match_condition(self) -> str:
    """Returns the current match ending condition."""
    return await self.execute('CheckEndMatchCondition')

  async def get_network_stats(self) -> dict:
    """Returns a struct containing the networks stats of the server. Only available to SuperAdmin."""
    return await self.execute('GetNetworkStats')

  async def start_server_lan(self) -> bool:
    """Start a server on LAN, using the current configuration. Only available to SuperAdmin."""
    return await self.execute('StartServerLan')

  async def start_server_internet(self, credentials: dict) -> bool:
    """Start a server on the internet using the specified login and password. Only available to SuperAdmin."""
    return await self.execute('StartServerInternet', credentials)

  async def get_status(self) -> dict:
    """Returns the current status of the server."""
    return await self.execute('GetStatus')

  async def quit_game(self) -> bool:
    """Quit the application. Only available to SuperAdmin."""
    return await self.execute('QuitGame')

  async def game_data_directory(self) -> str:
    """Returns the path of the game data directory. Only available to Admin."""
    return await self.execute('GameDataDirectory')

  async def get_tracks_directory(self) -> str:
    """Returns the path of the tracks directory. Only available to Admin."""
    return await self.execute('GetTracksDirectory')

  async def get_skins_directory(self) -> str:
    """Returns the path of the skins directory. Only available to Admin."""
    return await self.execute('GetSkinsDirectory')
