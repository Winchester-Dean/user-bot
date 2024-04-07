import os
import inspect

from typing import List, Callable, Awaitable, Union
from importlib import import_module
from session_config import SessionConfig
from telethon import events

class HelpModule(SessionConfig):
    """View all modules; command: <code>.help</code>"""

    def __init__(
        self, directory: str = "modules"
    ):
        self.all_modules: List[Union[Callable, Awaitable]] = []
        self.files = os.listdir(directory)

        for file in self.files:
            if file.endswith(".py"):
                file = file[:3]

                self.modules = import_module(
                    f"{directory}:{file}"
                )

                for classname, classobj in inspect.getmembers(
                    self.modules, inspect.isclass
                ):
                    if classname.endswith("Module"):
                        self.all_modules.append((
                            classname,
                            classobj.__doc__
                        ))
    
    async def help(self, msg):
        try:
            text = (
                "<b>💪 All modules:</b>\n\n"
            )

            for index, module in enumerate(
                self.all_modules
            ):
                name, doc = module

                text += "{}. <b>{}:</b> {}\n".format(
                    index + 1, classname, doc
                )
            
            await msg.edit(text, parse_mode="html")
        except Exception as error:
            await msg.edit(
                f"⚠ <b>Error: </b><code>{error}</code>",
                parse_mode="html"
            )
    
    def start(self):
        self.client.add_event_handler(
            self.help,
            events.NewMessage(pattern=r"^[./-_=]*(?i)\.help$")
        )