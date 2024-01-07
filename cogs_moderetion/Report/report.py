import disnake
import datetime
import sqlite3
from disnake.ext import commands
from disnake import ButtonStyle
from disnake import TextInputStyle
from config import REPORT_CHANNEL_ID, SERVER_ID, ID_COMMAND_CHANNEL

conn = sqlite3.connect('database\complaints.db')
c = conn.cursor()

REPORT_CHANNEL_ID = REPORT_CHANNEL_ID
SERVER_ID = SERVER_ID


class ReportCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.submitter_mention = None

    def save_complaints_in_db(self, user_id: int, complaint_from, complaint_to, status: str):
        c.execute("INSERT INTO complaints VALUES (?, ?, ?, ?)", (user_id, complaint_from, complaint_to, status))
        conn.commit()

    def get_complaints_from_db(self, user_id):
        c.execute('SELECT * FROM complaints WHERE user_id = ? AND status != "resolved"', (user_id,))
        existing_complaint = c.fetchone()
        return existing_complaint

    @commands.slash_command(
        guild_ids=[SERVER_ID],
        name="report",
        description="Репорт на участника",
    )
    async def report(self, inter, user: disnake.User, message: str):
        channel = self.bot.get_channel(REPORT_CHANNEL_ID)

        ADMIN_ID = 1188484736977473625
        MODER_ID = 1188484736977473619

        admin_role = inter.guild.get_role(ADMIN_ID)
        moder_role = inter.guild.get_role(MODER_ID)

        embed = disnake.Embed(
            title="Report",
            color=disnake.Colour.yellow(),
            timestamp=datetime.datetime.now()
        )

        embed.add_field(name="Подал:", value=f"{inter.author.mention}")
        embed.add_field(name="Подали на:", value=f"{user.mention}")
        embed.add_field(name="Причина:", value=f"{message}")

        self.submitter_mention = inter.author.id

        if self.get_complaints_from_db(inter.author.id):
            await inter.response.send_message('Перед тем как отправить новую жалобу, дождитесь рассмотрения предыдущей!', ephemeral=True)
        else:
            # Упоминаем админа и модера
            admin_mention = admin_role.mention if admin_role else "Администратор не найден"
            moder_mention = moder_role.mention if moder_role else "Модератор не найден"

            await channel.send(f"{admin_mention} {moder_mention} Поступила новая жалоба!")
            
            await inter.response.send_message("Жалоба успешно отправлена. Администрация рассмотрит ее в ближайшее время.", ephemeral=True)
            await channel.send(embed=embed, view=TakeReportButton(bot=self.bot, submitter_mention=self.submitter_mention))

            self.save_complaints_in_db(user_id=inter.author.id, complaint_from=inter.author.mention, complaint_to=user.mention, status="without checking")

class TakeReportButton(disnake.ui.View):
    def __init__(self, bot: commands.Bot, submitter_mention: str):
        super().__init__()

        self.bot = bot
        self.pressing = False
        self.submitter_mention = submitter_mention

    def delete_complaints_from_db(self, user_id):
        c.execute("DELETE FROM complaints WHERE user_id = ?", (user_id,))
        conn.commit()

    @disnake.ui.button(label='Взять на рассмотрение', style=ButtonStyle.green, custom_id='take_report')
    async def take_report_button(self, button: disnake.ui.Button, inter):
        channel = self.bot.get_channel(ID_COMMAND_CHANNEL)
        self.close_report = CloseReport(bot=self.bot)

        if not self.pressing:
            taken_message = f"{inter.author.mention} взял(а) заявку на рассмотрение"
            message = f"Пожалуста, перейдите в канал {channel.mention} выдайте наказание нарушителю командой, и ТОЛЬКО после этого нажмите на кнопку 'Закрыть жалобу'!!!"

            self.delete_complaints_from_db(user_id=self.submitter_mention)
            await inter.channel.send(taken_message)
            await inter.response.send_message(message, view=self.close_report, ephemeral=True)
            self.pressing = True
        else:
            await inter.response.send_message("Жалоба уже взята на рассмотрение", ephemeral=True)

class CloseReport(disnake.ui.View):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        
        self.bot = bot

    @disnake.ui.button(label='Закрыть жалобу', style=ButtonStyle.green, custom_id='close_report')
    async def close_report(self, button: disnake.ui.Button, inter):
        await inter.response.send_message(f"{inter.author.mention} закрыл(а) жалобу")


def setup(bot: commands.Bot):
    bot.add_cog(ReportCommand(bot))