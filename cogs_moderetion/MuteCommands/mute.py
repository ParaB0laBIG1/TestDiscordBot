import disnake
from disnake.ext import commands
from embeds.embeds import answer_embed
from config import SERVER_ID, TIMEOUT_ROLE_ID, MODER_ROLE_ID, ADMIN_ROLE_ID
from cogs_moderetion.MuteCommands.check_role import has_moder_role, has_admin_or_main_role
from embeds.embeds import answer_embed
from cogs_moderetion.MuteCommands.timeout_utilits import TimeOut

time_values = {
    "мин": lambda x: x * 60,
    "час": lambda x: x * 3600,
    "день": lambda x: x * 86400,
    "неделя": lambda x: x * 604800,
    "мес": lambda x: x * 2629746,
    "год": lambda x: x * 31556952,
    "сек": lambda x: x,
}

allowed_role_ids = [MODER_ROLE_ID, ADMIN_ROLE_ID]

class MuteCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot

        self.timeout = TimeOut(bot=self.bot)

    @commands.slash_command(
        guild_ids=[SERVER_ID],
        name="mute",
        description="Мут участника",
    )
    @commands.cooldown(30, 86400, commands.BucketType.user)
    async def mute(self, inter, member: disnake.User, time: str, reason: str, channel: disnake.TextChannel = None):
        """
        Command for issuing timeout
        """
        try:
            if member == inter.author:
                await inter.response.send_message("Вы не можете использовать команду на себе!", ephemeral=True)
                return


            if await has_moder_role(inter):
                if await has_admin_or_main_role(inter=inter, member=member):
                    print("Выдача мута")
                    await self.timeout.timeout(inter=inter, member=member, time=time, channel=channel, reason=reason)
                else:
                    await inter.response.send_message("Извините, но ваша роль ниже роли того, на кого вы хотите применить команду", ephemeral=True)
            else:
                await answer_embed(text="Недостаточно прав", description="Извините, но у вас нету прав для отправки этой команды", error=True)
        except Exception as e:
            print(f"Ошибка при выдаче мута: {e}")
            await inter.response.send_message("произошла неизвестная ошибка, свяжитесь с администрацией для дополнительной информации")

    @mute.error
    async def mute_error(self, inter, error):
        if isinstance(error, commands.CommandOnCooldown):
            await inter.response.send_message(embed=await answer_embed(text="Извините, но в день можно наложить только 30 мутов",
                                                        description="Подождите 24 часа перед новым использованием", error=True), ephemeral=True)

def setup(bot: commands.Bot):
    bot.add_cog(MuteCommands(bot))
