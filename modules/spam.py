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
    """Command: 
        .spam {count} {sleep} {text}"""
    async def spam_module_handler(self, msg):
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
            self.spam_module_handler,
            events.NewMessage(pattern=".spam")
        )
