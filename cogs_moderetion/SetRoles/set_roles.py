import disnake
from disnake.ext import commands
from config import SERVER_ID, ID_ROLE_MAIN


class SetRole(commands.Cog):
    def __init__(self, bot: commands.Cog):
        super().__init__()
        self.bot =  bot


        self.roles = [
            1188484736881000545, # Властилин
            1188484736881000544, # Император
            1188484736881000543, # Легенда
            1188484736881000542, # Патопсихолог
            1188484736881000541, # Почетный
            1188484736881000540, # Возвышенный
            1188484736881000539, # Здравомыслящий
            1188484736851656826, # Получеловек
            1188484736809701444, # Неандерталец
            1188484736809701443, # Шизоид
            1188484736809701440 # Активист
        ]

    @commands.slash_command(
        guild_ids=[SERVER_ID],
        name="episode"
    )
    async def episode(self, inter):
        self.main_role = inter.author.get_role(ID_ROLE_MAIN)

        if self.main_role in inter.author.roles:
            await self.new_role(inter=inter)
        else:
            await inter.response.send_message("У вас нету права на эту команду")
            
    async def new_role(self, inter):
        guild = inter.guild
        try:
            members = await guild.fetch_members(limit=None).flatten()

            for member in members:
                for role_id in self.roles[:len(self.roles)-1]:
                    role = guild.get_role(role_id)
                    if role and role in member.roles:
                        await member.remove_roles(role)

                new_role_id = self.roles[len(self.roles)-1]
                new_role = guild.get_role(new_role_id)
                if new_role:
                    await member.add_roles(new_role)

            await inter.response.send_message("Роли успешно обновлены")
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            await inter.response.send_message("Произошла ошибка, проверьте правильность использования команды", ephemeral=True)


def setup(bot: commands.Bot):
    bot.add_cog(SetRole(bot))