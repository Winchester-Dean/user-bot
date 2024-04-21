import re
import youtube_dl
from session_config import SessionConfig
from telethon import events

class YouTubeDownloader(SessionConfig):
    async def download_video(self, msg, url):
        try:
            ydl_opts = {
                'format': 'best',
                'outtmpl': '%(title)s.%(ext)s',
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info_dict)
                await msg.edit(f"Video downloaded: {filename}")
        except Exception as e:
            await msg.edit(f"Error: {e}")

    async def download_audio(self, msg, url):
        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': '%(title)s.%(ext)s',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info_dict)
                await msg.edit(f"Audio downloaded: {filename}")
        except Exception as e:
            await msg.edit(f"Error: {e}")

    def handle_video_download(self, msg):
        match = re.match(r"^[./-_=]*(?i)\.dl\s+video\s+(https?://\S+)", msg.text)
        if match:
            url = match.group(1)
            self.download_video(msg, url)

    def handle_audio_download(self, msg):
        match = re.match(r"^[./-_=]*(?i)\.dl\s+audio\s+(https?://\S+)", msg.text)
        if match:
            url = match.group(1)
            self.download_audio(msg, url)

    def start(self):
        self.client.add_event_handler(
            self.handle_video_download,
            events.NewMessage(pattern=r"^[./-_=]*(?i)\.dl\s+video")
        )

        self.client.add_event_handler(
            self.handle_audio_download,
            events.NewMessage(pattern=r"^[./-_=]*(?i)\.dl\s+audio")
        )
