import asyncio
from disnake.ext import commands
from checking_perm import CheckPermissions
from embeds.embeds import answer_embed, seding_warning_in_logs, seding_ban_logs
from config import CHANNEL_HISTORY_PUNISHMENTS_ID, time_values, convert_to_seconds


class BanUtilits():
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()

        self.bot = bot

    async def give_ban(self, inter, member, time, reason):
        """
        issuing ban
        """
        self.check_perm = CheckPermissions(inter, command="ban")
        self.logs_channel = self.bot.get_channel(CHANNEL_HISTORY_PUNISHMENTS_ID)

        if await self.check_perm.check_perm_on_kick_and_ban(member=member):
            if time:
                self.time_letter = time[-3:]
                self.time_seconds = await convert_to_seconds(time, self.time_letter)

                await asyncio.sleep(1)
                if self.time_letter in time_values:
                    await member.ban(reason=reason)
                    await inter.response.send_message(f"{member.mention} был успешно забанен на {time}",ephemeral=True)
                    asyncio.create_task(self.remove_ban_after_delay(inter, member, self.time_seconds))
                    await self.logs_channel.send(embed=await seding_ban_logs(inter=inter, member=member, reason=reason, time=time))
            else:
                await member.ban(reason=reason)
                await inter.response.send_message(f"{member.mention} был успешно забанен навсегда", ephemeral=True)
                await self.logs_channel.send(embed=await seding_ban_logs(inter=inter, member=member, reason=reason, time=time))
        else:
            await inter.response.send_message(embed=await answer_embed(error=True, title="Ограничения",text="Не достаточно прав", 
                                                    description="Извините, но у вас нету подходящей роли для использувание этой команды"), ephemeral=True)
            await self.logs_channel.send(embed=await seding_warning_in_logs(name="Попытка бана:", 
                                                    value=f"{inter.author.mention} попытался выдать бан пользувателю {member.mention} не имея на это прав"))
            
    async def remove_ban_after_delay(self, inter, member, time_seconds):
        """
        removal of mute after the deadline
        """
        await asyncio.sleep(time_seconds)
        await member.unban(reason="Время бана истекло")
        await self.logs_channel.send(embed=await answer_embed(title="Наказание истекло" , text="Наказания снято", 
                                description=f"{member.mention} был успешно разбанин полсе {time_seconds} секунд нахждения в блокировке", error=False))