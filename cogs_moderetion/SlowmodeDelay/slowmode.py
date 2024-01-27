import disnake
from disnake.ext import commands
from config import CHANNEL_HISTORY_PUNISHMENTS_ID, SERVER_ID
from checking_perm import CheckPermissions
from embeds.embeds import seding_mute_logs, answer_embed


class SlowmodeCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        
        self.bot = bot

    @commands.slash_command(
        guild_ids=[SERVER_ID],
        name="slowmode", 
        description="Включить медленый режим"
        )
    
    async def set_slowmode(self, inter, секунды: int, канал: disnake.TextChannel):
        """Установить медленный режим в канале"""
        seconds = секунды
        channel = канал

            
        self.report_channel = self.bot.get_channel(CHANNEL_HISTORY_PUNISHMENTS_ID)
        self.check_perm = CheckPermissions(inter, command="mute")

        if await self.check_perm.check_perm_on_slowmode():
            await channel.edit(slowmode_delay=seconds)
            await inter.response.send_message(embed=await answer_embed(text="Медленый режим",
                                                        description=f"Был включен медленый режим на {seconds} секунд в канале {channel}", error=False))

            self.embed = disnake.Embed(
                title="Отчет"
            )
            self.embed.add_field(name="Медленый режим включен", 
                                value=f"{inter.author.mention} включил медленый режим в чате {channel.mention} на {seconds} секунд", inline=False)
            await self.report_channel.send(embed=self.embed)

        else:
            await inter.response.send_message(embed=await answer_embed(title="Ограничения", error=True, text="Не достаточно прав", description="Извините, но у вас нету подходящей роли для использувание этой команды"))

def setup(bot: commands.Bot):
    bot.add_cog(SlowmodeCommand(bot))