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
        self.all_modules = List[Union[Callable, Awaitable]] = []
        self.files = os.listdir(directory)

        for file in self.files:
            if file.endswith(".py"):
                file = file[:3]

                self.modules = import_module(
                    f"{directory}:{file}"
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
            "[cold white]\t\tAll modules list:[/]\n"
        )
        for index, module in enumerate(self.all_modules):
            class_name, instance, doc = module

            console.print(
                "[bold white]\t\t{}.[/]: [bold green]{}[/]".format(
                    index + 1, class_name
                )
            )

            print()
        
        with self.client:
            for modules in self.all_modules:
                modules[1].start()

if __name__ == "__main__":
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
    
    console.print("""[bold mageta]
Copyright (C) 2024 https://github.com/Winchester-Dean/user-bot
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it under certain conditions.
    [/]""")

    Main().start()
