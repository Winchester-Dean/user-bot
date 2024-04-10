from time import perf_counter
from session_config import SessionConfig
from telethon import events

class PingModule(SessionConfig):
    """Check internet ping; command: <code>.ping</code>"""
    async def ping(self, msg):
        try:
            start = perf_counter()
            await msg.edit("Testing...")
            end = perf_counter()
            await msg.edit(
                "<b>Ping:</b> {}s".format(
                    round(end - start, 3)
                ),
                parse_mode="html"
            )
        except Exception as error:
            await msg.edit(
                f"⚠ <b>Error:</b> <code>{error}</code>",
                parse_mode="html"
            )
    
    def start(self):
        self.client.add_event_handler(
            self.ping,
            events.NewMessage(pattern="^[./-_=]*(?i)\.ping")
        )
