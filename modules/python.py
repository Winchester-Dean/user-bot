import utils

from io import StringIO
from contextlib import redirect_stdout
from session_config import SessionConfig
from telethon import events

class PythonModule(SessionConfig):
    """Python module; command: 
        <code>.python {code}</code> and/or <code>.eval {code}</code>"""
    async def python(self, msg):
        try:
            await msg.edit(
                "<b>Executing...</b>",
                parse_mode="html"
            )

            code = await utils.get_args_raw(msg)
            stdout = StringIO()

            with redirect_stdout(stdout):
                exec(code)

            text = (
                "<b>✡️ Code:\n</b>"
                f"<code>{code}</code>\n"
                "\n<b>✔️ Result:\n</b>"
                f"<code>{stdout.getvalue()}</code>"
            )

            await msg.edit(text, parse_mode="html")
        except Exception as error:
            await msg.edit(
                f"⚠ <b>Error:</b> <code>{error}</code>",
                parse_mode="html"
            )

    async def eval(self, msg):
        try:
            await msg.edit(
                "<b>Executing...</b>",
                parse_mode="html"
            )

            code = await utils.get_args_raw(msg)
            result = eval(
                code,
                {
                    "__builtins__": {}
                }
            )

            text = (
                "<b>✡️ Expression:\n</b>"
                f"<code>{code}</code>\n"
                "\n<b>✔️ Result:\n</b>"
                f"<code>{result}</code>"
            )

            await msg.edit(text, parse_mode="html")
        except Exception as error:
            await msg.edit(
                f"⚠ <b>Error:</b> <code>{error}</code>",
                parse_mode="html"
            )

    def start(self):
        self.client.add_event_handler(
            self.python,
            events.NewMessage(pattern="^[./-_=]*(?i)\.python")
        )
        self.client.add_event_handler(
            self.eval,
            events.NewMessage(pattern="^[./-_=]*(?i)\.eval")
        )
