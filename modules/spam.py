import asyncio

from session_config import SessionConfig
from telethon import events

class SpamModule(SessionConfig):
    """Module for spam in chat; command: 
        <code>.spam {count} {text} {sleep}</code>"""
    
    async def spam(self, msg):
        try:
            message = msg.message.text.split(
                maxsplit=3
            )
            if len(message) > 2:
                pass
            else:
                await msg.edit(
                    "⚠️ <b>Error...</b>",
                    parse_mode="html"
                )
                return
            
            count = message[1]
            if count.isdigit():
                count = int(count)
            else:
                await msg.edit(
                    "⚠️ <b>Error...</b>",
                    parse_mode="html"
                )
                return
            
            sleep = message[2]
            if sleep.isdigit():
                sleep = int(sleep)
            else:
                await msg.edit(
                    "⚠️ <b>Error...</b>",
                    parse_mode="html"
                )
                return
            
            text = "".join(
                message[3]
            )

            await msg.edit(
                "❗ <b>Spam started!</b>",
                parse_mode="html"
            )

            for i in range(count):
                await self.client.send_message(
                    msg.chat_id,
                    text
                )

                await asyncio.sleep(sleep)

            await msg.edit(
                "✔️ <b>Spam endend!</b>",
                parse_mode="html"
            )
        except Exception as error:
            await msg.edit(
                f"⚠️ <b>Error:</b> <code>{error}</code>",
                parse_mode="html"
            )
    
    def start(self):
        self.client.add_event_handler(
            self.spam,
            events.NewMessage(pattern="^[./-_=]*(?i)\.spam$")
        )