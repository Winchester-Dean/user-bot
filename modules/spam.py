# https://github.com/Winchester-Dean
# Copyright (C) 2022  Winchester-Dean

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of the License

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with this program.
# If not, see <https://www.gnu.org/licenses/>.

import asyncio

from session_config import SessionConfig
from telethon import events

class SpamModule(SessionConfig):
    """Spam module command: 
        .spam {count} {sleep} {text}"""
    def start(self):
        @self.client.on(
            events.NewMessage(
                pattern=".spam"
            )
        )
        async def spam_handler(msg):
            try:
                message = msg.message.text.split(
                    maxsplit=3
                )
                if len(message) > 2:
                    pass
                else:
                    await msg.edit("Error...")
                    return
                
                count = message[1]
                if count.isdigit():
                    count = int(count)
                else:
                    await msg.edit("Error...")
                    return

                sleep = message[2]
                if sleep.isdigit():
                    sleep = int(sleep)
                else:
                    await msg.edit("Error...")
                    return

                text = "".join(
                    message[3]
                )

                await msg.edit("Spam started!")

                for i in range(count):
                    await self.client.send_message(
                        msg.chat_id,
                        text
                    )

                    await asyncio.sleep(sleep)
                
                await msg.edit("Spam endend!")
            except Exception as error:
                await msg.edit(
                    f"Error: <code>{error}</code>",
                    parse_mode="html"
                )
