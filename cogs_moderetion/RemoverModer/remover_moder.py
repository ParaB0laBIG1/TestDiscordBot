import disnake
from disnake.ext import commands
from config import SERVER_ID, ADMIN_ROLE_ID, MODER_ROLE_ID

class RemoveModerCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot

    @commands.slash_command(
        guild_ids=[SERVER_ID],
        name="remove_moder",
        description="Снять с модерки"
    )
    async def remove_moder(self, inter, member: disnake.Member):
        self.roly_moder = inter.guild.get_role(MODER_ROLE_ID)

        if await self.check_admin_role(inter):
            if not await self.check_moder_role(member):
                await inter.response.send_message(f"{member.mention} не имеет роли модератора", ephemeral=True)
            else:
                await self.remover_role(inter, member)
        else:
            await inter.response.send_message(f"У вас нету прав для выполнения этой команды", ephemeral=True)

    async def remover_role(self, inter, member):
        await member.remove_roles(self.roly_moder)
        await inter.response.send_message(f"Роль модератора была снята с {member.mention}", ephemeral=True)

    async def check_admin_role(self, inter):
        author_roles = [role.id for role in inter.author.roles]

        if ADMIN_ROLE_ID in author_roles:
            return True
        else:
            return False

    async def check_moder_role(self, member):
        member_roles = [role.id for role in member.roles]

        if MODER_ROLE_ID in member_roles:
            return True
        else:
            return False

def setup(bot: commands.Bot):
    bot.add_cog(RemoveModerCommand(bot))
