# https://github.com/Winchester-Dean
# Copyright (C) 2022  Winchester-Dean

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of the License

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with this program.
# If not, see <https://www.gnu.org/licenses/>.

from session_config import SessionConfig
from telethon import events

class ExampleModule(SessionConfig):
    """Example module command: .example"""
    def start(self):
        @self.client.on(
            events.NewMessage(
                pattern=".example"
            )
        )
        async def example_handler(msg):
            await msg.edit("Example")
