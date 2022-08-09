# https://github.com/KrasProject-2021
# Copyright (C) 2022  KrasProject-2021

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
from tgclient import TGCLIENT

class main(TGCLIENT):
    """Main"""
    def __init__(
        self,
        directory: str = "modules"
    ):
        self.all_modules: List[Union[Callable, Awaitable]] = []
        self.files = os.listdir(directory)

        for file in self.files:
            if file.endswith(".py") and file.startswith("_"):
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
        print("All modules:\n")
        for index, module in enumerate(self.all_modules):
            class_name, instance, doc = module

            print(
                "{}. {}: {}".format(
                    index + 1,
                    class_name,
                    doc
                )
            )
        
        with self.client:
            for modules in self.all_modules:
                modules[1].start()

            self.client.run_until_disconnected()

if __name__ == "__main__":
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

    print(
        "Copyright (C) 2022  https://github.com/KrasProject-2021/user-bot\n"
        "This program comes with ABSOLUTELY NO WARRANTY.\n"
        "This is free software, and you are welcome to redistribute it under certain conditions.\n"
    )

    main().start()
