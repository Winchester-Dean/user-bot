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
    """module for viewing information about the user bot,
    command: botinfo"""
    def __init__(self):
        self.repo = Repo()
    
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
                "<b>📃 Documentation:</b> <a href='https://github.com/Winchester-Dean/user-bot-documentation'>Link</a> <strong>by Dean Winchester</strong>"
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
            events.NewMessage(pattern=".botinfo")
        )
