import json

from session_config import SessionConfig
from telethon import events
from telethon.tl.functions.users import GetFullUserRequest

class UserInfoModule(SessionConfig):
    """A module for obtaining information about the user through a response to his message;
    command: <code>.info</code>"""

    strings = {
        "loading": (
            "<b>Getting information...</b>"
        ),
        "userinfo": (
            "<b>🙇 User info:\n\n"
            "🆔 ID: <code>{user_id}</code>\n"
            "✡️ UserName: @{username}\n"
            "First name: {first_name}\n"
            "Last name: {last_name}\n"
            "📞 Phone: {phone}\n"
            "🔤 Bio: {bio}\n"
            "❌ Is deleted: {deleted}\n"
            "🤖 Is bot: {bot}\n"
            "🚫 Is scam: {scam}\n"
            "👎 Is fake: {fake}\n"
            "❔ Is blocked: {blocked}\n"
            "🔗 User link: <a href='tg://user?id={user_id}'>link</a>\n"
            "</b>"
        ),
    }

    async def userinfo(self, msg):
        try:
            if not msg.is_reply:
                return await msg.edit(
                    "⚠ <b>This command must be sent as a reply to one's message!</b>",
                    reply_msg="html"
                )
            
            await msg.edit(
                self.strings["loading"],
                parse_mode="html"
            )

            reply_msg = await msg.get_reply_message()
            uuser_id = reply_msg.sender_id

            user = await self.client.get_entity(uuser_id)

            info = {
                "user_id": str(user.id),
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "phone": user.phone,
                "bio": getattr(user, "about", False),
                "deleted": user.deleted,
                "bot": user.bot,
                "scam": getattr(user, "scam", False),
                "fake": getattr(user, "fake", False),
                "blocked": getattr(user, "blocked", False),
            }

            formatted_info = self.strings["userinfo"].format(**info)

            await msg.edit(formatted_info, parse_mode="html")
        except Exception as error:
            await msg.edit(
                f"⚠ <b>Error:</b> <code>{error}</code>",
                parse_mode="html"
            )
    
    def start(self):
        self.client.add_event_handler(
            self.userinfo,
            events.NewMessage(pattern="^[./-_=]*(?i)\.info")
        )
