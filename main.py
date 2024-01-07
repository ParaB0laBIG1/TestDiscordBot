import disnake
from disnake.ext import commands
from config import TOKEN

bot = commands.Bot()
token = TOKEN


@bot.event
async def on_ready():
    print("Бот готов!")


bot.load_extension("cogs_moderetion.Report.report")
bot.load_extension("cogs_moderetion.MuteCommands.mute")
bot.load_extension("cogs_moderetion.SlowmodeDelay.slowmode")
bot.load_extension("cogs_moderetion.CreateChannel.channel_create")
bot.load_extension("cogs_moderetion.RemoverModer.remover_moder")
bot.load_extension("cogs_moderetion.SetRoles.set_roles")
bot.load_extension("cogs_moderetion.KickCommand.kick_member")
bot.load_extension("cogs_moderetion.BanCommand.ban")

bot.load_extension("cogs_rank.rank_system")

bot.load_extension("cogs_music.play_command")


bot.run(token)