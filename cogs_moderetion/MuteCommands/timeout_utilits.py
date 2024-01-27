import disnake
import asyncio
from disnake.ext import commands
from config import MODER_ROLE_ID, ADMIN_ROLE_ID, overwrite_text_and_voice, TIMEOUT_ROLE_ID, CHANNEL_HISTORY_PUNISHMENTS_ID, time_values, convert_to_seconds
from embeds.embeds import seding_mute_logs, answer_embed, seding_warning_in_logs
from checking_perm import CheckPermissions

allowed_role_ids = [MODER_ROLE_ID, ADMIN_ROLE_ID]


class TimeOut():
    def __init__(self, bot: commands.Bot):
        super().__init__()

        self.bot = bot

    async def timeout(self, inter, member, time, channel, reason):
        """
        issuing mute
        """
        self.check_perm = CheckPermissions(inter, command="mute")

        self.role_timeout = inter.guild.get_role(TIMEOUT_ROLE_ID)
        self.time_letter = time[-3:]
        self.time_seconds = await convert_to_seconds(time, self.time_letter)
        self.logs_channel = self.bot.get_channel(CHANNEL_HISTORY_PUNISHMENTS_ID)

        if await self.check_perm.check_permissions_on_mute(member):
            if channel:
                await self.mute_in_channel(inter, member, time, self.time_letter, channel)
                await self.logs_channel.send(embed=await seding_mute_logs(inter=inter, member=member, reason=reason, time=time, channel=channel))
            else:
                await self.mute_in_all_channels(inter, member, time, self.time_letter, channel)
                await self.logs_channel.send(embed=await seding_mute_logs(inter=inter, member=member, reason=reason, time=time, channel=channel))
        else:
            await inter.response.send_message(embed=await answer_embed(title="Ограничения",error=True, text="Не достаточно прав", 
                                description="Извините, но у вас нету подходящей роли для использувание этой команды"), ephemeral=True)
            await self.logs_channel.send(embed=await seding_warning_in_logs(name="Предупреждения", 
                                        value=f"{inter.author.mention} попытался выдать мут участнику {member.mention}"))


    async def mute_in_channel(self, inter, member, time, time_letter, channel):
        """
            mute in channel
        """
        await asyncio.sleep(1)
        if time_letter in time_values:
            await channel.set_permissions(member, overwrite=overwrite_text_and_voice)
            asyncio.create_task(self.remove_mute_after_delay(inter, member, channel, self.time_seconds))
            await inter.response.send_message(content=f"{member.mention} был успешно ограничен в отправке сообщений на {time} в канале {channel.name}.", ephemeral=True)

        else:
            await inter.response.send_message(content=f"Недопустимое значение времени: {time}")

    async def mute_in_all_channels(self, inter, member, time, time_letter, channel):
        """
        issuing timeout in all channels (via role)
        """
        timeout_role = inter.guild.get_role(TIMEOUT_ROLE_ID)

        await asyncio.sleep(1)

        if time_letter in time_values:
            await member.add_roles(timeout_role)
            asyncio.create_task(self.remove_mute_after_delay(inter, member=member, channel=channel, time_seconds=self.time_seconds))
            await inter.response.send_message(content=f"{member.mention} был успешно ограничен в отправке сообщений на {time} во всех каналах.", ephemeral=True)

    async def remove_mute_after_delay(self, inter, member, channel, time_seconds):
        """
        removal of mute after the deadline
        """
        await asyncio.sleep(time_seconds)
        if channel:
            await channel.set_permissions(member, overwrite=None)
            await self.logs_channel.send(embed=await answer_embed(title="Наказание истекло!",text="Наказание снято!", 
                                                            description=f"{member.mention} больше не ограничен в отправке сообщений в канале {channel.name}.", error=False))
        else:
            await member.remove_roles(self.role_timeout)
            await self.logs_channel.send(embed=await answer_embed(title="Наказание истекло!",text="Наказание снято!", 
                                        description=f"{member.mention} больше не ограничен в отправке сообщений" ,error=False))