from disnake.ext import commands
from config import SERVER_ID

class TestCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(
        guild_ids=[SERVER_ID],
        name="test"
    )
    async def test(self, inter):
        await inter.response.send_message("Test")

def setup(bot: commands.Bot):
    bot.add_cog(TestCommand(bot))
