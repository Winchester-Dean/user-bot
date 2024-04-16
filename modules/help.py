import os
import inspect
import utils

from typing import List, Callable, Awaitable, Union
from importlib import import_module
from telethon import events

class HelpModule:
    """View all modules list; command: <code>.help</code>"""

    strings = {
        "error": "⚠ <b>Error:</b> <code>{error}</code>",
        "no_module": "<b>Oops... the module was not found :(</b>",
        "no_command": "<b>No commands found for this module...</b>",
        "error_command": "⚠ <b>Error using the command</b>"
    }

    def __init__(self, directory: str = "modules"):
        self.commands = {}
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
    
    def add_module_commands(self, module_commands):
        module_name = module_commands["name"]
        self.commands[module_name] = {
            "descryption": module_commands["descryption"],
            "commands": module_commands["commands"]
        }
    
    async def help_handler(self, msg):
        try:
            text = (
                "<b>💪 All modules:</b>\n\n"
            )

            args = utils.get_args(msg)
            if len(args) == 1:
                for index, module in enumerate(
                    self.all_modules, start=1
                ):
                    name, doc = module
                    text += "<b>{}. {}: {}</b>".format(
                        index, name, doc
                    )
            elif len(args) == 2:
                module_name = args[1]
                for module in self.all_modules:
                    name, doc = module
                    if module_name == name:
                        if name in self.commands:
                            commands_info = self.commands[name]["commands"]
                            descryption = self.commands[name]["descryption"]
                            
                            text += "<b>Module: {}\nDescryption: {}\nCommands: {}\n</b>".format(
                                name, descryption, commands
                            )

                            for command, info in commands_info.items():
                                text += f"{command}: {info}\n"
                        else:
                            await msg.edit(
                                self.strings["no_command"],
                                parse_mode="html"
                            )
                    else:
                        await msg.edit(
                            self.strings["no_module"],
                            parse_mode="html"
                        )
            else:
                await msg.edit(
                    self.strings["error_command"],
                    parse_mode="html"
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