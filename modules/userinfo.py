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
            "Account creation date: {create_date}"
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
                strings["loading"],
                parse_mode="html"
            )

            reply_msg = await msg.get_reply_message()
            user_id = reply_msg.sender_id

            user = await self.client(
                GetFullUserRequest(user_id)
            )

            info = {
                "user_id": str(user.user.id),
                "username": user.user.username,
                "first_name": user.user.first_name,
                "last_name": user.user.last_name,
                "phone": user.user.phone,
                "bio": user.user.about,
                "deleted": user.user.deleted,
                "bot": user.user.bot,
                "scam": user.user.scam,
                "fake": user.user.fake,
                "blocked": user.user.blocked,
                "create_date": user.user.date.strftime("%Y-%m-%d %H-%M-%S"),
            }

            formatted_info = strings["userinfo"].format(**info)

            await msg.edit(formatted_info, parse_mode="html")
        except Exception as error:
            await msg.edit(
                f"⚠ <b>Error:</b> <code>{error}</code>",
                parse_mode="html"
            )
    
    def start(self):
        self.client.add_event_handler(
            self.userinfo,
            events.NewMessage(pattern="^[./-_=]*(?i)\.info$")
        )