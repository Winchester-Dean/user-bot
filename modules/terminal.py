# https://github.com/Winchester-Dean
# Copyright (C) 2022  Winchester-Dean

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of the License

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with this program.
# If not, see <https://www.gnu.org/licenses/>.

import utils
import os
import asyncio

from session_config import SessionConfig
from telethon import events


class TerminalModule(SessionConfig):
    """Command: 
        .terminal {command}"""
    async def run_command(self, msg, cmd):
        if len(cmd.split(" ")) > 1 and cmd.split(" ")[0] == "sudo":
            needsswitch = True

            for word in cmd.split(" ", 1)[1].split(" "):
                if word[0] != "-":
                    break
                
                if word == "-S":
                    needsswitch = False
                
            if needsswitch:
                cmd = "".join(
                    [
                        cmd.split(" ", 1)[0],
                        "-S",
                        cmd.split(" ", 1)[1]
                    ]
                )
        
        try:
            sproc = await asyncio.create_subprocess_shell(
                cmd,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=utils.get_base_dir()
            )

            stdout, stderr = await sproc.communicate()
            stdout = stdout.decode()
            stderr = stderr.decode()
            await msg.edit(
                f"✔️ <b>Result:</b>\n<code>{stdout}</code>\n"
                f"<b>Stderr:</b>\n<code>{stderr}</code>",
                parse_mode="html"
            )
        except Exception as error:
            await msg.edit(
                f"⚠ <b>Error:</b> <code>{error}</code>",
                parse_mode="html"
            )

    async def terminal_handler(self, msg):
        try:
            await self.run_command(
                msg,
                await utils.get_args_raw(msg)
            )
        except Exception as error:
            await msg.edit(
                f"⚠ <b>Error:</b> <code>{error}</code>",
                parse_mode="html"
            )

    def start(self):
        self.client.add_event_handler(
            self.terminal_handler,
            events.NewMessage(pattern=".terminal")
        )
