import os
import inspect
import utils

from typing import List, Callable, Awaitable, Union
from importlib import import_module
from telethon import events

class HelpModule:
    """View all modules list; command: <code>.help</code>"""

    def __init__(self, directory: str = "modules"):
        self.all_modules: List[Union[Callable, Awaitable]] = []
        self.files = os.listdir(directory)

        for file in self.files:
            if file.endswith(".py"):
                file = file[:-3]

                self.modules = import_module(
                    f"{directory}.{file}"
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
    
    async def help_handler(self, msg):
        try:
            text = (
                "<b>💪 All modules:</b>\n\n"
            )

            for module in self.all_modules:
                name, doc = module
                
                text += "<b>🔹 {}: {}</b>".format(
                    name, doc
                )
            
            await msg.edit(
                text,
                parse_mode="html"
            )
        except Exception as error:
            await msg.edit(
                self.strings["error"].format(error),
                parse_mode="html"
            )
    
    def start(self):
        self.client.add_event_handler(
            self.help_handler,
            events.NewMessage(pattern="^[./-_=]*(?i)\.help")
        )
