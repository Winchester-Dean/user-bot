from modules.help import HelpModule
from telethon import events

class ExampleModule:
    """Example module; command: <code>.example</code>"""
    def __init__(self):
        self.commands = {
            "name": "ExampleModule",
            "descryption": "The module is intended as an example for creating other models for this userbot",
            "commands": ".example"
        }

        self.help_module = HelpModule()
        self.help_module.add_module_commands(self.commands)

    async def example_handler(self, msg):
        await msg.edit(
            "<b>Example</b>",
            parse_mode="html"
        )

    def start(self):
        self.client.add_event_handler(
            self.example_handler,
            events.NewMessage(pattern="^[./-_=]*(?i)\.example")
        )
