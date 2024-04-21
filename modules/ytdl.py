import youtube_dl

from session_config import SessionConfig
from telethon import events

class YouTubeDLModule(SessionConfig):
    """Module for downloading audio, video from YouTube; command: <code>.dl {format} {link}</code>"""

    async def dl_video(self, url, msg, chat_id):
        try:
            await msg.edit(
                "📥 <b>Downloading video...</b>",
                parse_mode="html"
            )

            ytdl_opts = {
                "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
            }

            with youtube_dl.YoutubeDL(ytdl_opts) as ytdl:
                info_dict = ytdl.extract_info(                                 url, download=True
                )
                filename = ytdl.prepare_filename(info_dict)

                await self.client.send_file(
                    chat_id, filename
                )

            await msg.edit(                                                "✔️ Download complete",
                parse_mode="html"
            )
        except Exception as error:
            await msg.edit(
                f"⚠️ <b>Error:</b> <code>{error}</code>",
                parse_mode="html"
            )

    async def dl_audio(self, url, msg, chat_id):
        try:
            await msg.edit(
                "📥 <b>Downloading audio...</b>",
                parse_mode="html"
            )

            ytdl_opts = {
                "format": "bestaudio/best",
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }],
            }

            with youtube_dl.YoutubeDL(ytdl_opts) as ytdl:
                info_dict = ytdl.extract_info(
                    url, download=True
                )
                filename = ytdl.prepare_filename(info_dict)

                await self.client.send_file(
                    chat_id, filename
                )

            await msg.edit(
                "✔️ Download complete",
                parse_mode="html"
            )
        except Exception as error:
            await msg.edit(
                f"⚠️ <b>Error:</b> <code>{error}</code>",
                parse_mode="html"
            )

    async def dl_image(self, url, msg, chat_id):
        try:
            await msg.edit(
                "📥 <b>Downloading image...</b>",
                parse_mode="html"                                      )

            ytdl_opts = {                                                  "format": "best",                                          "writethumbnail": True,
            }

            with youtube_dl.YoutubeDL(ytdl_opts) as ytdl:
                info_dict = ytdl.extract_info(
                    url, download=True
                )
                thumbnail = info_dict['thumbnails'][0]['url']

                await self.client.send_file(
                    chat_id, thumbnail                                     )

            await msg.edit(                                                "✔️ Download complete",
                parse_mode="html"
            )
        except Exception as error:
            await msg.edit(
                f"⚠️ <b>Error:</b> <code>{error}</code>",
                parse_mode="html"
            )

    async def ytdl_handler(self, msg):
        try:
            chat_id = msg.chat_id
            command = msg.text.split(maxsplit=2)
            url = command[2]

            if not url.startswith(
                "https://www.youtube.com/watch?v="
            ):
                await event.respond("Invalid YouTube URL!")
                return

            if "&" in url:
                url = url.split("&")[0]

            if "/playlist" in url:
                await event.respond(
                    "Playlist download is not supported!"
                )
                return

            if command[1] == "audio":
                await self.dl_audio(url, msg, chat_id)
            elif command[1] == "image":
                await self.dl_image(url, msg, chat_id)
            else:
                await self.dl_video(url, msg, chat_id)

        except Exception as error:
            await msg.edit(f"⚠️ <b>Error:</b> <code>{error}</code>",
                parse_mode="html"
            )

    def start(self):
        self.client.add_event_handler(
            self.ytdl_handler,
            events.NewMessage(
                pattern="^[./-_=]*(?i)\.dl"
            )
        )
