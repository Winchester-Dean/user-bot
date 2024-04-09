import utils
import os
import asyncio

from session_config import SessionConfig
from telethon import events

class TerminalModule(SessionConfig):
    """Module for running bash command in terminal; command: 
        <code>.terminal {command}</code>"""
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

    async def terminal(self, msg):
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
            self.terminal,
            events.NewMessage(pattern="^[./-_=]*(?i)\.terminal$")
        )
