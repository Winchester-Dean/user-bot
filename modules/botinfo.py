import os
import inspect
import contextlib

from importlib import import_module
from git import Repo
from session_config import SessionConfig
from telethon import events

class UserBotInfoModule(SessionConfig):
    """Module for viewing information about the user bot;
    command: <code>.botinfo</code>"""

    strings = {
        "name": "Bot Info",
        "loading": "<b>Getting bot information...</b>",
        "botinfo": (
            "<b>"
            "\t\t<a href='{bot_url}'>Winchester-Dean/user-bot</a><br><br>"
            "🛐 Author: Dean Winchester<br>"
            "☑️ GitHub: <a href='https://github.com/Winchester-Dean'>Link</a><br>"
            "📝 License: <a href='https://github.com/Winchester-Dean/user-bot/blob/main/LICENCE'>GNU GPL v3</a><br>"
            "📂 Commit: <a href='{bot_url}/commit/{commit}'>Link</a> <b>by {author}<br>"
            "📃 Documentation: <a href='https://github.com/Winchester-Dean/user-bot-documentation'>Link</a>"
            "Modules count: {modules_count}"
            "</b>"
        ),
    }

    def __init__(self):
        self.repo = Repo()
    
    def get_modules_count(self):
        directory: str = "modules"
        files = os.listdir(directory)

        modules_list = []

        for file in files:
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
                        modules_list.append(classname)
        
        return len(modules_list)
    
    def get_current_commit(self):
        return self.repo.heads[0].commit.hexsha
    
    def get_author_name(self):
        return self.repo.heads[0].commit.author.name
    
    def get_remote_url(self):
        return list(self.repo.remote().urls)[0]

    async def user_bot_info(self, msg):
        try:
            await msg.edit(self.strings["loading"], parse_mode="html")

            info = {
                "bot_url": "n/a",
                "commit": "n/a",
                "author": "n/a",
                "modules_count": "n/a"
            }

            with contextlib.suppress(Exception):
                info["bot_url"] = self.get_remote_url()
            
            with contextlib.suppress(Exception):
                info["commit"] = self.get_current_commit()
            
            with contextlib.suppress(Exception):
                info["author"] = self.get_author_name()
            
            with contextlib.suppress(Exception):
                info["modules_count"] = self.get_modules_count()

            await msg.edit(self.strings["botinfo"].format(**info), parse_mode="html")
        except Exception as error:
            await msg.edit(
                f"⚠️ <b>Error:</b> <code>{error}</code>",
                parse_mode="html"
            )

    def start(self):
        self.client.add_event_handler(
            self.user_bot_info,
            events.NewMessage(pattern="^[./-_=]*(?i)\.botinfo")
        )
