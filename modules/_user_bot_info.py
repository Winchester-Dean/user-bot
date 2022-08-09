# https://github.com/KrasProject-2021
# Copyright (C) 2022  KrasProject-2021

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of the License

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with this program.
# If not, see <https://www.gnu.org/licenses/>.

from git import Repo
from tgclient import TGCLIENT
from telethon import events

class UserBotInfoModule(TGCLIENT):
    """User bot info command: .botinfo"""
    def __init__(self):
        self.repo = Repo()
    
    def get_current_commit(self):
        return self.repo.heads[0].commit.hexsha
    
    def get_author_name(self):
        return self.repo.heads[0].commit.author.name
    
    def get_remote_url(self):
        return list(self.repo.remote().urls)[0]
    
    def start(self):
        @self.client.on(
            events.NewMessage(
                pattern=".botinfo"
            )
        )
        async def user_bot_info(msg):
            try:
                text = (
                    "Link: <a href='"
                    f"{self.get_remote_url()}'>"
                    "user-bot</a>\n"
                    "Author: <a href='"
                    "tg://user?id=5209528492'>"
                    "Dean Winchester</a>\n"
                    "Telegram channel: <a href='"
                    "https://t.me/Winchester_Community'>"
                    "@Winchester Community</a>\n"
                    "GitHub: <a href='"
                    "https://github.com/Winchester-Dean'>"
                    "link</a>\n"
                    "License: <a href='"
                    "https://github.com/Winchester-Dean/"
                    "user-bot/blob/main/LICENCE'>"
                    "GNU GPL v3</a>\n"
                    "Commit: <a href='"
                    f"{self.get_remote_url()}/commit/"
                    f"{self.get_current_commit()}'>Link</a>"
                    f" by {self.get_author_name()}"
                )

                await msg.edit(text, parse_mode="html")
            except Exception as error:
                await msg.edit(
                    f"Error: <code>{error}</code>",
                    parse_mode="html"
                )
