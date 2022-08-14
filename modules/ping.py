# https://github.com/Winchester-Dean
# Copyright (C) 2022  Winchester-Dean

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of the License

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with this program.
# If not, see <https://www.gnu.org/licenses/>.

from time import perf_counter
from session_config import SessionConfig
from telethon import events

class PingModule(SessionConfig):
    """Command: .ping"""
    async def ping_handler(self, msg):
        try:
            start = perf_counter()
            await msg.edit("Testing...")
            end = perf_counter()
            await msg.edit(
                "Ping: {}s".format(
                    round(end - start, 3)
                )
            )
        except Exception as error:
            await msg.edit(
                    f"⚠ Error: <code>{error}</code>",
                    parse_mode="html"
                )

    def start(self):
        self.client.add_event_handler(
            self.ping_handler,
            events.NewMessage(pattern=".ping")
        )
