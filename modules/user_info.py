# https://github.com/Winchester-Dean
# Copyright (C) 2022 Winchester-Dean

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of the License

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with this program.
# If not, see <https://www.gnu.org/licenses/>.

from session_config import SessionConfig
from telethon import events
from telethon.tl.functions.users import GetFullUserRequest

class UserInfoModule(SessionConfig):
    """User info module command: .info"""
    def start(self):
        @self.client.on(
            events.NewMessage(
                pattern=".info"
            )
        )
        async def user_info_handler(msg):
            try:
                if not msg.is_reply:
                    await msg.edit(
                        "This command must be sent as a reply to one's message!"
                    )
                    return
                
                reply_msg = await self.client.get_messages(
                    msg.peer_id,
                    ids=msg.reply_to.reply_to_msg_id
                )
                user_id = reply_msg.from_id

                user = await self.client(
                    GetFullUserRequest(
                        user_id
                    )
                )

                await msg.edit(f"""User info:
ID: <code>{user.user.id}</code>
UserName: <code>@{user.user.username}</code>
First name: <code>{user.user.first_name}</code>
Last name: <code>{user.user.last_name}</code>
Phone: <code>{user.user.phone}</code>
Bio: <code>{user.about}</code>
Is deleted: <code>{user.user.deleted}</code>
Is bot: <code>{user.user.bot}</code>
Is scam: <code>{user.user.scam}</code>
Is fake: <code>{user.user.fake}</code>
Is blocked: <code>{user.blocked}</code>
User link: <a href='tg://user?id={user.user.id}'>link</a>
                    """,
                    parse_mode="html"
                )
            except Exception as error:
                await msg.edit(
                    f"Error: <code>{error}</code>",
                    parse_mode="html"
                )
