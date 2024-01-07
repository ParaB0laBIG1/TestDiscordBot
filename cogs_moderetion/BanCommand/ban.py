import disnake
from disnake.ext import commands
from config import SERVER_ID

class BanCommand(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()
        self.bot = bot

    @commands.slash_command(
        guild_ids=[SERVER_ID],
        name="user_ban",
        description="Забанить пользователя"
    )
    @commands.cooldown(10, 86000, commands.BucketType.user)
    async def ban(self, inter, member: disnake.User, reason: str, time: str = None):
        await member.ban(reason=reason)
        await inter.response.send_message(f"Ban user: {member.mention}")
        

def setup(bot: commands.Bot):
    bot.add_cog(BanCommand(bot=bot))
