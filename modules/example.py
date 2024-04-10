from session_config import SessionConfig
from telethon import events

class ExampleModule(SessionConfig):
    """Example module; command: <code>.example</code>"""
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