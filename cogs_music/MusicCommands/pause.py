import disnake
from disnake.ext import commands


class PauseCommand(commands.Cog):
    def __init__(self):
        super().__init__()

    async def pause_music(self, inter, server_id, voice_clients):

        if server_id in voice_clients and voice_clients[server_id].is_playing():
            voice_clients[server_id].pause()
        else:
            await inter.send(content="На данный момент нет проигрываемой музыки.", ephemeral=True)