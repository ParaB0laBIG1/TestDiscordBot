import disnake
from disnake.ext import commands
from config import REPORT_CHANNEL_ID, SERVER_ID


class SlowmodeCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot

    @commands.slash_command(
        guild_ids=[SERVER_ID],
        name="set_slowmode", 
        description="Включить медленый режим"
        )
    
    async def set_slowmode(self, inter, seconds: int):
        """Установить медленный режим в канале"""

        await inter.channel.edit(slowmode_delay=seconds)
        await inter.send(f'Медленный режим установлен на {seconds} секунд.')

def setup(bot: commands.Bot):
    bot.add_cog(SlowmodeCommand(bot))