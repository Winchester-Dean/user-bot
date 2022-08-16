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
from rich.console import Console

console = Console()

class Main(SessionConfig):
    def __init__(
        self,
        directory: str = "modules"
    ):
        self.all_modules: List[Union[Callable, Awaitable]] = []
        self.files = os.listdir(directory)

        for file in self.files:
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
                            classobj(),
                            classobj.__doc__
                        ))
    
    def start(self):
        console.print(
            "[bold white]\t\tAll modules:[/]\n"
        )
        for index, module in enumerate(self.all_modules):
            class_name, instance, doc = module

            console.print(
                "[bold white]\t\t{}.[/] [bold green]{}[/]".format(
                    index + 1,
                    class_name
                )
            )

        print()
        
        with self.client:
            for modules in self.all_modules:
                modules[1].start()

            self.client.run_until_disconnected()

if __name__ == "__main__":
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


    console.print("""[bold mageta]
Copyright (C) 2022  https://github.com/Winchester-Dean/user-bot
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it under certain conditions.
    [/]""")

    Main().start()
