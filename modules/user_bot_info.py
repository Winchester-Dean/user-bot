# https://github.com/Winchester-Dean
# Copyright (C) 2022  Winchester-Dean

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of the License

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with this program.
# If not, see <https://www.gnu.org/licenses/>.

from git import Repo
from session_config import SessionConfig
from telethon import events

class UserBotInfoModule(SessionConfig):
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
                    f"<strong>Link:</strong> <a href='{self.get_remote_url()}'>user-bot</a>\n"
                    "<strong>Author:</strong> <a href='tg://user?id=5209528492'>Dean Winchester</a>\n"
                    "<strong>Telegram channel:</strong> <a href='https://t.me/Winchester_Community'>@Winchester_Community</a>\n"
                    "<strong>GitHub:</strong> <a href='https://github.com/Winchester-Dean'>Link</a>\n"
                    "<strong>License:</strong> <a href='https://github.com/Winchester-Dean/user-bot/blob/main/LICENCE'>GNU GPL v3</a>\n"
                    f"<strong>Commit:</strong> <a href='{self.get_remote_url()}/commit/{self.get_current_commit()}'>Link</a> <strong>by {self.get_author_name()}</strong>\n"
                    "<strong>Documentation:</strong> <a href='https://user-bot-documentation'>Link</a>"
                )

                await msg.edit(text, parse_mode="html")
            except Exception as error:
                await msg.edit(
                    f"Error: <code>{error}</code>",
                    parse_mode="html"
                )
