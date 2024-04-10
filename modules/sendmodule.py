import utils
import os
import inspect

from importlib import import_module
from session_config import SessionConfig
from telethon import events

class SendModule(SessionConfig):
    """Send module; command <code>.sendmodule {module name}</code>"""
    async def sendmodule(self, msg):
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
            self.sendmodule,
            events.NewMessage(pattern="^[./-_=]*(?i)\.sendmodule")
        )