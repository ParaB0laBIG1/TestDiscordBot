import disnake
import asyncio
import youtube_dl

from cogs_music.MusicModule.music_embed import music_info_embed
from cogs_music.MusicModule.buttons import create_button_view
from config import SERVER_ID

from datetime import timedelta


class MusicUtilits():
    def __init__(self):
        super().__init__()

        self.queue = {}

        self.ydl_options = {"format": 'bestaudio/best', "socket_timeout": 5}
        self.ffmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn', }
        self.ytdl = youtube_dl.YoutubeDL(self.ydl_options)

    async def add_to_queue(self, server_id, song_data, youtube_url):
        self.queue[server_id] = []

        duration_seconds = song_data.get('duration', 0)
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

    async def save_to_queue(self, url, server_id):
        """
            Сохраняем в очередь музыку
        """
        song_data = await asyncio.to_thread(self.ytdl.extract_info, url, False)
        await self.add_to_queue(server_id, song_data, url)

    async def edit_original_message(self, inter, server_id, song_info):
        """
        Изменяем сообщения
        """
        if server_id in self.queue:
            print(self.queue[server_id])

            new_embed = await music_info_embed(inter, track_info=song_info, queue=self.queue[server_id])
            new_components = await create_button_view(inter, self.queue, server_id)

            # Используем метод edit_original_message для редактирования сообщения
            await inter.edit_original_message(content="", embed=new_embed, components=new_components)
        else:
            print(f"Ключ {server_id} отсутствует в self.queue.")

