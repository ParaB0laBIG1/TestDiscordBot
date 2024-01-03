import disnake
from disnake.ext import commands
from config import SERVER_ID, TIMEOUT_ROLE_ID, overwrite_text_and_voice


class CreateChannel(commands.Cog):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        print(f'Создан новый канал: {channel.name} ({channel.id})')
        
        role_id = TIMEOUT_ROLE_ID
        role = channel.guild.get_role(role_id)
        if role:
            await channel.set_permissions(role, overwrite=overwrite_text_and_voice)

def setup(bot: commands.Bot):
    bot.add_cog(CreateChannel(bot))