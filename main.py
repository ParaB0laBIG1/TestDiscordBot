import disnake
from disnake.ext import commands
from config import TOKEN

bot = commands.Bot()
token = TOKEN


@bot.event
async def on_ready():
    print("Бот готов!")


bot.load_extension("cogs.report")


bot.run(token)