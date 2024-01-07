import disnake
import datetime
from disnake.ext import commands
from config import CHANNEL_HISTORY_PUNISHMENTS_ID


bot = commands.Bot()

embed_for_logs = disnake.Embed(
        title="Отчет",
        color=disnake.Colour.yellow(),
        timestamp=datetime.datetime.now(),
    )

async def answer_embed(text,description,error: bool):
    if error:
        embed = disnake.Embed(
            title="Ограничения",
            color=disnake.Colour.red(),
        )
        embed.add_field(name=f"{text}", value=f"{description}")
        return embed
    else:
        embed = disnake.Embed(
            title="Ограничения",
            color=disnake.Colour.green(),
        )
        embed.add_field(name=f"{text}", value=f"{description}")
        return embed
    

async def seding_mute_logs(inter, member, reason, time, channel):
    
    embed_for_logs.add_field(name=f"Выдал(а) мут:", value=f"{inter.author.mention}", inline=False) 
    embed_for_logs.add_field(name=f"Нарушитель:", value=f"{member.mention}", inline=False)
    embed_for_logs.add_field(name=f"Время наказание: ", value=f"{time}", inline=False)
    if channel:
        embed_for_logs.add_field(name=f"Канал: ", value=f"{channel.mention}", inline=False)
    else:
        embed_for_logs.add_field(name=f"Канал: ", value=f"Все каналы(включая войс)", inline=False)

    embed_for_logs.add_field(name=f"Причина: ", value=f"{reason}", inline=False)
    
    return embed_for_logs


async def seding_kick_logs(inter, member, reason):
    embed_for_logs.add_field(name=f"Выгнал с сервера:", value=f"{inter.author.mention}", inline=False) 
    embed_for_logs.add_field(name=f"Нарушитель:", value=f"{member.mention}", inline=False)
    embed_for_logs.add_field(name=f"Причина: ", value=f"{reason}", inline=False)
    
    return embed_for_logs