import disnake
import datetime
import sqlite3
from disnake.ext import commands
from disnake import ButtonStyle
from disnake import TextInputStyle
from config import REPORT_CHANNEL_ID, SERVER_ID, VIOLATION_LOG_ID

conn = sqlite3.connect('datebase\complaints.db')
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

            await channel.send(f"{admin_mention} {moder_mention} Поступила новая жалоба!", embed=embed)
            
            await inter.response.send_message("Жалоба успешно отправлена. Администрация рассмотрит ее в ближайшее время.", ephemeral=True)
            await channel.send(embed=embed, view=TakeReportButton(bot=self.bot, submitter_mention=self.submitter_mention))


            self.save_complaints_in_db(user_id=inter.author.id, complaint_from=inter.author.mention, complaint_to=user.mention, status="without checking")



class TakeReportButton(disnake.ui.View):
    def __init__(self, bot: commands.Bot, submitter_mention: str):
        super().__init__()

        self.bot = bot
        self.verdict = VerdictMessage(self.bot)
        self.pressing = False
        self.submitter_mention = submitter_mention

    def delete_complaints_from_db(self, user_id):
        c.execute("DELETE FROM complaints WHERE user_id = ?", (user_id,))
        conn.commit()

    @disnake.ui.button(label='Взять на рассмотрение', style=ButtonStyle.green, custom_id='take_report')
    async def take_report_button(self, button: disnake.ui.Button, inter):
        channel = self.bot.get_channel(REPORT_CHANNEL_ID)

        if not self.pressing:
            taken_message = f"{inter.author.mention} взял(а) заявку на рассмотрение"
            self.delete_complaints_from_db(user_id=self.submitter_mention)
            await inter.channel.send(taken_message)
            await inter.response.send_message("Пожалуста выберите какой приговор вынести нарушителю", view=self.verdict, ephemeral=True)
            self.pressing = True
        else:
            await inter.response.send_message("Жалоба уже взята на рассмотрение", ephemeral=True)


class VerdictMessage(disnake.ui.View):
    def __init__(self, bot: commands.Bot):
        super().__init__()

        self.bot = bot

    @disnake.ui.button(label='Вердикт', style=ButtonStyle.green, custom_id='verdict_id')
    async def send_message_for_verdict(self, button: disnake.ui.Button, inter):
        await inter.response.send_modal(modal=VerdictModal(self.bot))


class VerdictModal(disnake.ui.Modal):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        components = [
            disnake.ui.TextInput(
                label="Ник", placeholder="Ник нарушителя", style=TextInputStyle.short, custom_id="Ник нарушителя", max_length=50,
            ),
            disnake.ui.TextInput(
                label="Наказание", placeholder="Какое наказание вы дали?", custom_id="Наказание", style=TextInputStyle.short,
            ),
            disnake.ui.TextInput(
                label="Нарушения",  placeholder="Какое было нарушения?", custom_id="Описания нарушения", style=TextInputStyle.paragraph,
            ),
        ]
        super().__init__(title="Create Tag", custom_id="create_tag", components=components)


    async def callback(self, inter: disnake.ModalInteraction):
        channel = self.bot.get_channel(VIOLATION_LOG_ID)
        embed = disnake.Embed(title="Отчет")
        
        for key, value in inter.text_values.items():
            embed.add_field(
                name=key,
                value=value[:1024],
                inline=False,
            )
        await inter.response.send_message("Вердикт был отправлен в журнал", ephemeral=True)
        await channel.send(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(ReportCommand(bot))
