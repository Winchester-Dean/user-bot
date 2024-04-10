import random

from session_config import SessionConfig
from telethon import events

class TagAllModule(SessionConfig):
    """Tag all users in chat; command: <code>.tagall</code>"""
    async def tag_all_handler(self, msg):
        try:
            users = await self.client.get_participants(
                msg.chat_id
            )

            await msg.edit(
                "❗ <b>Taging started</b>",
                parse_mode="html"
            )
            for user in users:
                text = "<a href='tg://user?id={}'>{}</a>".format(
                    user.id,
                    random.choice(
                        [
                            '😈',
                            '😱',
                            '💩'
                        ]
                    )
                )

                await self.client.send_message(
                    msg.chat_id,
                    text,
                    parse_mode="html"
                )

            await msg.edit(
                "✔️ <b>Taging endend</b>",
                parse_mode="html"
            )
        except Exception as error:
            await msg.edit(
                f"⚠️ <b>Error</b> <code>{error}</code>",
                parse_mode="html"
            )

    def start(self):
        self.client.add_event_handler(
            self.tag_all_handler,
            events.NewMessage(pattern="^[./-_=]*(?i)\.tagall")
        )
