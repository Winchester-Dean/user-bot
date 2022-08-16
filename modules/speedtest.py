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

from speedtest import Speedtest
from session_config import SessionConfig
from telethon import events
from typing import Tuple


class SpeedTestModule(SessionConfig):
    """Module for speed testing, command: speedtest"""
    async def speedtest_handler(self, msg):
        try:
            await msg.edit(
                "<b>✡️ Speed testing...</b>",
                parse_mode="html"
            )

            results = await asyncio.run(self.speedtester)

            await msg.edit(f"""
<b>Results:\n\n</b>
<b>🔽 Download:</b>
<code>{round(results[0] / 1024 / 1024)}</code>\n
<b>🔼 Upload:</b>
<code>{round(results[1] / 1024 / 1024)}</code>\n
<b>Ping:</b>
<code>{round(results[2], 3)}</code>
                """,
                parse_mode="html"
            )
        except Exception as error:
            await msg.edit(
                f"⚠️ <b>Error:</b> <code>{error}</code>",
                parse_mode="html"
            )

    @staticmethod
    def speedtester() -> Tuple[float, float, float]:
        s = Speedtest()

        s.get_servers()
        s.get_best_server()
        s.download()
        s.upload()
        res = s.results.dict()
        return res["download"], res["upload"], res["ping"]
    
    def start(self):
        self.client.add_event_handler(
            self.speedtest_handler,
            events.NewMessage(pattern=".speedtest")
        )
