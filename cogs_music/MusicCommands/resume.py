import disnake
from disnake.ext import commands


class ResumeCommand(commands.Cog):
    def __init__(self):
        super().__init__()

    async def resume_music(self, inter, server_id, voice_clients):

        if server_id in voice_clients and voice_clients[server_id].is_paused():
            voice_clients[server_id].resume()
        else:
            await inter.send(content="На данный момент музыка не на паузе.", ephemeral=True)