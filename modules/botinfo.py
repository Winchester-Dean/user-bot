import os
import inspect

from importlib import import_module
from git import Repo
from session_config import SessionConfig
from telethon import events

class UserBotInfoModule(SessionConfig):
    """Module for viewing information about the user bot;
    command: <code>.botinfo</code>"""
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
            text = (
                f"\t\t<a href='{self.get_remote_url()}'>Winchester-Dean/user-bot</a>\n"
                f"<b>🔗 Link:</b> <a href='{self.get_remote_url()}'>user-bot</a>\n"
                "<b>🛐 Author:</b> <a href='tg://user?id=5209528492'>Dean Winchester</a>\n"
                "<b>❗ Telegram channel:</b> <a href='https://t.me/Winchester_Community'>@Winchester_Community</a>\n"
                "<b>☑️  GitHub:</b> <a href='https://github.com/Winchester-Dean'>Link</a>\n"
                "<b>📝 License:</b> <a href='https://github.com/Winchester-Dean/user-bot/blob/main/LICENCE'>GNU GPL v3</a>\n"
                f"<b>📂 Commit:</b> <a href='{self.get_remote_url()}/commit/{self.get_current_commit()}'>Link</a> <b>by {self.get_author_name()}</b>\n"
                "<b>📃 Documentation:</b> <a href='https://github.com/Winchester-Dean/user-bot-documentation'>Link</a> <strong>by Dean Winchester</strong>\n"
                f"<b>Modules count: {self.get_modules_count()}</b>"
            )

            await msg.edit(text, parse_mode="html")
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
