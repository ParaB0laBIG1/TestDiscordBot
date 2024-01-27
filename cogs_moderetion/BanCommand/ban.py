import disnake
from disnake.ext import commands
from config import SERVER_ID
from cogs_moderetion.BanCommand.ban_utilits import BanUtilits
from embeds.embeds import answer_embed
from checking_perm import CheckPermissions


class BanCommand(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()

        self.bot = bot
        self.ban_u = BanUtilits(self.bot)

    @commands.slash_command(
        guild_ids=[SERVER_ID],
        name="user_ban",
        description="Забанить пользователя"
    )
    @commands.cooldown(10, 120, commands.BucketType.user)
    async def ban(self, inter, участник: disnake.User, причина: str, время: str = None):
        member = участник
        reason = причина
        time = время
        await self.ban_u.give_ban(inter=inter, member=member, time=time, reason=reason)
        
    @ban.error
    async def ban_error(self, inter, error):
        self.check_perm = CheckPermissions(inter, command="ban")

        if isinstance(error, commands.CommandOnCooldown):
            await inter.response.send_message(embed=await answer_embed(text="Извините, но в день можно банить только 10 раз",
                                                        description="Подождите 24 часа перед новым использованием, также в целях безлпасности будет с вас будет снята роль", error=True), ephemeral=True)
            await self.check_perm.remove_admin_roles(member=inter.author)

def setup(bot: commands.Bot):
    bot.add_cog(BanCommand(bot=bot))
