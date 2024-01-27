import disnake
from disnake.ext import commands

async def music_info_embed(inter, track_info, queue):
    embed = disnake.Embed(
        title=track_info["title"],
        color=disnake.Colour.yellow(),
        url=track_info["url"],
    )

    embed.set_author(
        name=track_info["author"],
        url=track_info["url"],
        icon_url=track_info["thumbnail"]
    )

    embed.set_thumbnail(track_info["thumbnail"])

    if queue:
        number = 1
        embed.add_field(
            name="В очереди: ",
            value = "\n".join([f"{number + i + 1}. `[{track['duration']}]` [{track['title']}]({track['url']}) от {inter.author.name}" 
                            for i, track in enumerate(queue)]),
            inline=False
        )
    else:
        embed.add_field(
            name="В очереди: ",
            value="Нету",
            inline=False
        )

    return embed
