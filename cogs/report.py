import disnake
import datetime
from disnake.ext import commands
from disnake import ui
from disnake import ButtonStyle


class ReprtCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(
            guild_ids=[919221014506930236],
            name="report",
            description="Репорт на участника",
    )
    async def report(self, inter, user: disnake.User, message: str):

        channel = self.bot.get_channel(1188107095598452786)
        
        self.embed = disnake.Embed(
            title="Report",
            color=disnake.Colour.yellow(),
            timestamp=datetime.datetime.now()
        )

        self.embed.add_field(name="Подал:", value=f"{inter.author.mention}")
        self.embed.add_field(name="Подали на:", value=f"{user.mention}")
        self.embed.add_field(name="Причина:", value=f"{message}")
        
        await inter.response.send_message("Жалоба отправлена", ephemeral=True)
        # await channel.send(message)
        await channel.send(embed=self.embed, view=TakeReportButton(bot=self.bot))


class TakeReportButton(disnake.ui.View):
    def __init__(self, bot: commands.Bot):
        super().__init__()

        self.bot = bot
        
        self.pressing = False

    @disnake.ui.button(label='Взять на расмотрения', style=ButtonStyle.green, custom_id='take_report')
    async def take_report_button(self, button: disnake.ui.Button, inter):
        channel = self.bot.get_channel(1188107095598452786)
        
        if self.pressing == False:
            print(f"До нажания: {self.pressing}")
            taken_message = f"{inter.author.mention} взял заявку на рассмотрение"
            await channel.send(taken_message)
            self.pressing = True

            print(f"После нажатия: {self.pressing}")
        elif self.pressing == True:
            await inter.response.send_message("Жалоба уже взята на расмотрения", ephemeral=True)


def setup(bot: commands.Bot):
    bot.add_cog(ReprtCommand(bot))