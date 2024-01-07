import disnake
from disnake.ext import commands
from config import SERVER_ID, CHANNEL_HISTORY_PUNISHMENTS_ID
from embeds.embeds import answer_embed, seding_kick_logs
from checking_perm import CheckPermissions


class KickCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot

    @commands.slash_command(
        guild_ids=[SERVER_ID],
        name="kick_member",
        description="Кикнуть человека с сервера"
    )
    @commands.cooldown(30, 86400, commands.BucketType.user)
    async def kick(self, inter, member: disnake.User, reason):
        """
        kick a member from the server
        """
        self.check_perm = CheckPermissions(inter=inter, command="kick")
        self.logs_channel = self.bot.get_channel(CHANNEL_HISTORY_PUNISHMENTS_ID)

        try:
            if await self.check_perm.check_perm_on_kick_and_ban(member=member):
                await member.kick()
                await inter.send(f"{member} был успешно кикнут с сервера")
                await self.logs_channel.send(embed=await seding_kick_logs(inter=inter, member=member, reason=reason))
            else:
                await inter.response.send_message(embed=await answer_embed(error=True, text="Не достаточно прав", 
                        description="Извините, но у вас нету подходящей роли для использувание этой команды"))
        except Exception as e:
            print(f"Ошибка: {e}")

    @kick.error
    async def mute_error(self, inter, error):
        """
            Error handler
        """
        if isinstance(error, commands.CommandOnCooldown):
            await inter.response.send_message(embed=await answer_embed(text="Извините, но в день можно кикнуть только 10 человек",
                                                        description="Подождите 24 часа перед новым использованием, также в целях безопасности будет снята роль(свяжитесь  с администацией)", error=True), ephemeral=True)

def setup(bot: commands.Bot):
    bot.add_cog(KickCommand(bot))   