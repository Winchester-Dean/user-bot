# https://github.com/KrasProject-2021
# Copyright (C) 2022  KrasProject-2021

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of the License

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with this program.
# If not, see <https://www.gnu.org/licenses/>.

import random

from tgclient import TGCLIENT
from telethon import events

class TagAllModule(TGCLIENT):
    """Tag all nodule command: .tagall"""
    def start(self):
        @self.client.on(
            events.NewMessage(
                pattern=".tagall"
            )
        )
        async def tag_all_handler(msg):
            users = await self.client.get_participants(
                msg.chat_id
            )

            for user in users:
                text = "<a href='tg://user?id={}'>{}</a>".format(
                    user.id,
                    random.choice(
                        [
                            '😈',
                            '😱',
                            '🤡',
                            '🦌',
                            '💩'
                        ]
                    )
                )

                await self.client.send_message(
                    msg.chat_id,
                    text,
                    parse_mode="html"
                )
