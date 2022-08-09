# https://github.com/Winchester-Dean
# Copyright (C) 2022  Winchester-Dean

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of the License

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with this program.
# If not, see <https://www.gnu.org/licenses/>.

import os
import inspect

from typing import List, Callable, Awaitable, Union
from importlib import import_module
from session_config import SessionConfig
from telethon import events


class HelpModule(SessionConfig):
    """Help module command: .help"""
    def __init__(
        self,
        directory: str = "modules"
    ):
        self.all_modules: List[Union[Callable, Awaitable]] = []

        for file in os.listdir(directory):
            if file.endswith(".py"):
                file = file[:-3]

                self.modules = import_module(
                    f'{directory}.{file}'
                )

                for classname, classobj in inspect.getmembers(
                    self.modules,
                    inspect.isclass
                ):
                    if classname.endswith("Module"):
                        self.all_modules.append((
                            classname,
                            classobj.__doc__
                        ))
    
    def start(self):
        @self.client.on(
            events.NewMessage(
                pattern=".help"
            )
        )
        async def help_handler(msg):
            try:
                text = (
                    "All modules:\n"
                )

                for index, module in enumerate(self.all_modules):
                    class_name, doc = module

                    text += "{}. <code>{}</code>: {}\n".format(
                        index + 1,
                        class_name,
                        doc
                    )

                await msg.edit(text, parse_mode="html")
            except Exception as error:
                await msg.edit(
                    f"Error: <code>{error}</code>",
                    parse_mode="html"
                )
