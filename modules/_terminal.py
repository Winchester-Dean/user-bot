# https://github.com/KrasProject-2021
# Copyright (C) 2022  KrasProject-2021

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of the License

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with this program.
# If not, see <https://www.gnu.org/licenses/>.

import os
import asyncio

from tgclient import TGCLIENT
from telethon import events


class TerminalModule(TGCLIENT):
    """Terminal module command: .terminal {command}"""
    def get_base_dir(self):
        return self.get_dir("user-bot")
    
    def get_dir(self, mod):
        return os.path.abspath(
            os.path.dirname(
                os.path.abspath(
                    mod
                )
            )
        )
    
    async def get_args_raw(self, msg):
        try:
            try:
                message = msg.message.text
            except AttributeError:
                pass
            except Exception as error:
                await msg.edit(
                    f"Error: <code>{error}</code>",
                    parse_mode="html"
                )
                return
            
            if not message:
                return False
            
            args = message.split(maxsplit=1)
            if len(args) > 1:
                return args[1]
            
            return ""
        except Exception as error:
            await msg.edit(
                f"Error: <code>{error}</code>",
                parse_mode="html"
            )
    
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
                cwd=self.get_base_dir()
            )

            stdout, stderr = await sproc.communicate()
            stdout = stdout.decode()
            await msg.edit(
                f"Result:\n<code>{stdout}</code>\n"
                f"<code>{stderr}</code>",
                parse_mode="html"
            )
        except Exception as error:
            await msg.edit(
                f"Error: <code>{error}</code>",
                parse_mode="html"
            )

    def start(self):
        @self.client.on(
            events.NewMessage(
                pattern=".terminal"
            )
        )
        async def terminal_handler(msg):
            try:
                await self.run_command(
                    msg,
                    await self.get_args_raw(msg)
                )
            except Exception as error:
                await msg.edit(
                    f"Error: <code>{error}</code>",
                    parse_mode="html"
                )
