import disnake
from disnake.ext import commands
from cogs_music.MusicModule.buttons import btns

from cogs_music.MusicCommands.play import PlayCommand
from cogs_music.MusicCommands.stop import StopCommand
from cogs_music.MusicCommands.pause import PauseCommand
from cogs_music.MusicCommands.resume import ResumeCommand
from config import SERVER_ID

class MusicModule(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.play = PlayCommand(self.bot)
        self.stop = StopCommand()
        self.pause = PauseCommand()
        self.resume = ResumeCommand()

    @commands.slash_command(
        guild_ids=[SERVER_ID],
        name='играть',
        description="Играть музыку"
    )
    async def play_music(self, inter, url):
        # Логика проигрывания музыки
        await self.play.play(inter, url)

    @commands.slash_command(name='пауза')
    async def pause_music(self, inter):
        # Логика приостановки проигрывания музыки
        await self.pause.pause_music(inter, server_id=self.play.server_id, voice_clients=self.play.voice_clients)

    @commands.slash_command(name='продолжить')
    async def resume_music(self, inter):
        # Логика продплжения проигрывания музыки
        await self.resume.resume_music(inter, server_id=self.play.server_id, voice_clients=self.play.voice_clients)
    
    @commands.slash_command(name='стоп')
    async def stop_music_command(self, inter):
        await self.stop.stop_music(inter, server_id=self.play.server_id, voice_clients=self.play.voice_clients)

    @commands.Cog.listener()
    async def on_button_click(self, inter: disnake.MessageInteraction):
        await inter.response.defer()
        custom_id = inter.data['custom_id']
        if custom_id == "stop":
            await self.stop_music_command(inter)
        elif custom_id == 'pause':
            btns['pause']['emoji'] = '▶️'
            btns['pause']['label'] = 'resume'

            await self.pause_music(inter)
            await self.play.edit_original_message(inter, server_id=self.play.server_id)
            
        elif custom_id == 'resume':
            btns['pause']['emoji'] = '⏸️'
            btns['pause']['label'] = 'pause'

            await self.resume_music(inter)
            await self.play.edit_original_message(inter, server_id=self.play.server_id)
        elif custom_id == 'repeat':
            if self.play.repeat != True:
                self.play.repeat = True
                btns['repeat']['emoji'] = '🔂'
                await self.play.edit_original_message(inter, server_id=self.play.server_id)
            else:
                self.play.repeat = False
                btns['repeat']['emoji'] = '🔁'
                await self.play.edit_original_message(inter, server_id=self.play.server_id)

            

def setup(bot):
    bot.add_cog(MusicModule(bot))
