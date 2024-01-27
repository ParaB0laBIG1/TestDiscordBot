import disnake
import datetime
from disnake.ext import commands

async def answer_embed(title: str, text: str, description: str,error: bool):
    if error:
        embed = disnake.Embed(
            title=title,
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
    
    embed_for_logs = disnake.Embed(
        title="Отчет",
        color=disnake.Colour.yellow()
    )

    embed_for_logs.add_field(name=f"Выдал(а) мут:", value=f"{inter.author.mention}", inline=False) 
    embed_for_logs.add_field(name=f"Нарушитель:", value=f"{member.mention}", inline=False)
    embed_for_logs.add_field(name=f"Время наказание: ", value=f"{time}", inline=False)
    if channel:
        embed_for_logs.add_field(name=f"Канал: ", value=f"{channel.mention}", inline=False)
    else:
        embed_for_logs.add_field(name=f"Канал: ", value=f"Все каналы(включая войс)", inline=False)

    embed_for_logs.add_field(name=f"Причина: ", value=f"{reason}", inline=False)
    embed_for_logs.timestamp = datetime.datetime.now()

    return embed_for_logs

async def seding_kick_logs(inter, member, reason):
    embed_for_logs = disnake.Embed(
        title="Отчет",
        color=disnake.Colour.yellow()
    )
    embed_for_logs.add_field(name=f"Выгнал(a) с сервера:", value=f"{inter.author.mention}", inline=False) 
    embed_for_logs.add_field(name=f"Нарушитель:", value=f"{member.mention}", inline=False)
    embed_for_logs.add_field(name=f"Причина: ", value=f"{reason}", inline=False)
    
    return embed_for_logs

async def seding_ban_logs(inter, member, reason, time):
    embed_for_logs = disnake.Embed(
        title="Отчет",
        color=disnake.Colour.yellow()
    )
    embed_for_logs.add_field(name=f"Выдал(а) бан:", value=f"{inter.author.mention}", inline=False) 
    embed_for_logs.add_field(name=f"Нарушитель:", value=f"{member.mention}", inline=False)
    if time:
        embed_for_logs.add_field(name=f"Время наказание: ", value=f"{time}", inline=False)
    else:
        embed_for_logs.add_field(name=f"Время наказание: ", value="навсегда", inline=False)
    embed_for_logs.add_field(name=f"Причина: ", value=f"{reason}", inline=False)
    
    return embed_for_logs

async def seding_warning_in_logs(name: str, value: str):
    embed = disnake.Embed(
        title="Предопреждения",
        color=disnake.Colour.red(),
        timestamp=datetime.datetime.now(),
    )

    embed.add_field(name=name, value=value)
    return embed
