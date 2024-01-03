import disnake


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
    

async def seding_mute_logs(inter, member, reason, time):
    embed = disnake.Embed(
        title="Отчет",
    )

    embed.add_field(name="Выдал мут:", value=inter.author.mention, inline=False)
    embed.add_field(name="Получатель мута:", value=member.mention, inline=False)
    embed.add_field(name="Причина:", value=reason, inline=False)
    embed.add_field(name="Время:", value=time, inline=False)
    return embed