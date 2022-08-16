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
import inspect

from importlib import import_module
from session_config import SessionConfig
from telethon import events

class SendModule(SessionConfig):
    """Send module command: sendmodule"""
    async def send_module_handler(self, msg):
        try:
            directory: str = "modules"
            for file in os.listdir(directory):
                if file.endswith(".py"):
                    file = file[:-3]

                    modules = import_module(
                        f"{directory}.{file}"
                    )

                    for classname, classobj in inspect.getmembers(
                        modules,
                        inspect.isclass
                    ):
                        if classname.endswith("Module"):
                            module_name = await utils.get_args_raw(msg)

                            if module_name == classname:
                                await msg.edit(
                                    "<b>👀 Sending...</b>",
                                    parse_mode="html"
                                )

                                try:
                                    await self.client.send_file(
                                        msg.chat_id,
                                        f"{directory}/{file}.py",
                                        caption=(
                                            f"<b>Module file name:</b> <code>{file}.py</code>\n"
                                            f"<b>Module class name:</b> <code>{classname}</code>\n"
                                        ),
                                        parse_mode="html"
                                    )
                                except Exception as error:
                                    await msg.edit(
                                        f"⚠️ <b>Error:</b> <code>{error}</code>",
                                        parse_mode="html"
                                    )

                                await msg.edit(
                                    "<b>✔️ Sendend!</b>",
                                    parse_mode="html"
                                )
        except Exception as error:
            await msg.edit(
                f"<b>⚠️ Error:</b> <code>{error}</code>",
                parse_mode="html"
            )

    def start(self):
        self.client.add_event_handler(
            self.send_module_handler,
            events.NewMessage(pattern=".sendmodule")
        )
