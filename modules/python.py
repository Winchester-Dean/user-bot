# https://github.com/Winchester-Dean
# Copyright (C) 2022  Winchester-Dean

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of the License
                                                           # This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;                           # without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.     
# You should have received a copy of the GNU General Public License along with this program.
# If not, see <https://www.gnu.org/licenses/>.

import utils

from io import StringIO
from contextlib import redirect_stdout
from session_config import SessionConfig
from telethon import events

class PythonModule(SessionConfig):
    """Command: 
        .python {code} and .eval {code}"""
    async def python_module_handler(self, msg):
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
                f"⚠ Error: <code>{error}</code>",
                parse_mode="html"
            )

    async def eval_handler(self, msg):
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
                f"⚠ Error: <code>{error}</code>",
                parse_mode="html"
            )

    def start(self):
        self.client.add_event_handler(
            self.python_module_handler,
            events.NewMessage(pattern=".python")
        )
        self.client.add_event_handler(
            self.eval_handler,
            events.NewMessage(pattern=".eval")
        )
