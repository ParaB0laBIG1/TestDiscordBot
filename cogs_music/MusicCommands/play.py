import disnake
import youtube_dl
import asyncio
from disnake.ext import commands
from datetime import timedelta
from config import SERVER_ID
from cogs_music.MusicModule.music_embed import music_info_embed
from cogs_music.MusicModule.buttons import create_button_view

class PlayCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot

        self.voice_clients = {}
        self.queue = {}
        self.repeat_queue = {}

        self.ydl_options = {"format": 'bestaudio/best', "socket_timeout": 5}
        self.ytdl = youtube_dl.YoutubeDL(self.ydl_options)
        self.ffmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn', }

        self.loop = asyncio.get_event_loop()
        self.data = None

        self.repeat = False

    async def play(self, inter, url: str):
        try:
            self.server_id = inter.guild.id

            if self.server_id not in self.voice_clients:
                
                if await self.connect_to_voice(inter):
                    await self.save_to_queue(url)
                    
                    await self.play_music(inter, self.server_id)
            else:        
                await inter.response.send_message("Загрузка..", ephemeral=True, delete_after=20)

                await self.save_to_queue(url)
                await inter.edit_original_message("Трек добавлен в очередь!")

        except Exception as e:
            print(f"Ошибка: {e}")
            await inter.send("Произошла ошибка, пожалуйста, свяжитесь с администрацией для получения дополнительной информации!!!", ephemeral=True)

    async def connect_to_voice(self, inter):
        author_voice = inter.author.voice
        if author_voice:
            self.voice_client = await author_voice.channel.connect()
            self.voice_clients[self.voice_client.guild.id] = self.voice_client
            await inter.send(content="Запускаю музыку...")
            return self.voice_client
            
        else:
            await inter.response.send_message("Чтобы использовать эту команду, необходимо находиться в голосовом канале", ephemeral=True)
            return False

    async def add_to_queue(self, server_id, song_data, youtube_url):
        if server_id not in self.queue:
            self.queue[server_id] = []

        duration_seconds = song_data.get('duration', 0)

        # Convert duration to a more human-readable format (HH:MM:SS)
        duration_formatted = str(timedelta(seconds=duration_seconds))

        data = {
            "url": str(youtube_url),
            "info_url": song_data.get("url"),
            "title": song_data.get("title", "None"),
            "author": song_data.get("uploader", "None"),
            "thumbnail": song_data.get("thumbnail"),
            "duration" : duration_formatted

        }

        self.queue[server_id].append(data)

    async def save_to_queue(self, url):
        """
            Сохраняем в очередь музыку
        """
        song_data = await asyncio.to_thread(self.ytdl.extract_info, url, False)
        await self.add_to_queue(self.server_id, song_data, url)

    async def play_music(self, inter, server_id):
        """
        Запускаем музыку
        """
        
        if server_id in self.queue and self.queue[server_id]:
            
            self.song_info = self.queue[server_id][0]  # Получаем информацию о текущей песне без удаления из очереди
            song_url = self.song_info["info_url"]

            await self.edit_original_message(inter, server_id)

            player = disnake.FFmpegOpusAudio(song_url, **self.ffmpeg_options)

            def after_playing(e):
                self.queue[server_id].pop(0)
                self.loop.create_task(self.play_music(inter, server_id))

            self.voice_client.play(player, after=after_playing)
        else:
            await asyncio.sleep(5)
            await self.voice_clients[server_id].disconnect()
            del self.voice_clients[server_id]


    async def edit_original_message(self, inter, server_id):
        """
        Изменяем сообщения
        """
        new_embed = await music_info_embed(inter, track_info=self.song_info, queue=self.queue[server_id])
        new_components = await create_button_view(inter, self.queue, server_id)

        # Используем метод edit_original_message для редактирования сообщения
        await inter.edit_original_message(content="", embed=new_embed, components=new_components)
