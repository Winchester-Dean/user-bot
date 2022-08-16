# https://github.com/Winchester-Dean
# Copyright (C) 2022  Winchester-Dean

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of the License

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with this program.
# If not, see <https://www.gnu.org/licenses/>.

import random

from session_config import SessionConfig
from telethon import events

class TagAllModule(SessionConfig):
    """Tag all users in chat, command: tagall"""
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
            events.NewMessage(pattern=".tagall")
        )
