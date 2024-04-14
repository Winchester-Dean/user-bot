from session_config import SessionConfig
from telethon import events

class AFKModule(SessionConfig):
    """AFK module; command: <code>.afk {reason}</code>"""

    async def afk_handler(self, msg):
        try:
            self.afk_reason = msg.text.split(maxsplit=1)[1]
            
            await msg.edit(
                "<b>Now you are in afk mode.</b>",
                parse_mode="html"
            )
        except Exception as error:
            await msg.edit(
                f"<b>⚠️ Error:</b> <code>{error}</code>",
                parse_mode="html"
            )

    async def unafk_handler(self, msg):
        try:
            self.afk_reason = None

            await msg.edit(
                "<b>You are out of afc mode.</b>",
                parse_mode="html"
            )
        except Exception as error:
            await msg.edit(
                f"<b>⚠️ Error:</b> <code>{error}</code>",
                parse_mode="html"
            )
    
    async def afk_notification(self, event):
        if self.afk_reason:
            if event.is_reply and event.reply_to_msg_id:
                replied_to = await event.get_reply_message()
                if replied_to.sender_id == (await self.client.get_me()).id:
                    await event.reply(
                        f"<b>{self.afk_reason}</b>",
                        parse_mode="html"
                    )
            elif event.message.mentioned:
                await event.reply(
                    f"<b>{self.afk_reason}</b>",
                    parse_mode="html"
                )

    def start(self):
        self.afk_reason = None
        
        self.client.add_event_handler(
            self.afk_handler,
            events.NewMessage(pattern="^[./-_=]*(?i)\.afk")
        )
        
        self.client.add_event_handler(
            self.unafk_handler,
            events.NewMessage(pattern="^[./-_=]*(?i)\.unafk")
        )
        
        self.client.add_event_handler(
            self.afk_notification,
            events.NewMessage(incoming=True)
        )

