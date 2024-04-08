from session_config import SessionConfig
from telethon import events
from telethon.tl.functions.users import GetFullUserRequest

class UserInfoModule(SessionConfig):
    """A module for obtaining information about the user through a response to his message;
    command: <code>.info</code>"""
    async def userinfo(self, msg):
        try:
            if not msg.is_reply:
                return await msg.edit(
                    "⚠ <b>This command must be sent as a reply to one's message!</b>",
                    parse_mode="html"
                )

            reply_msg = await self.client.get_message(
                msg.peer_id,
                ids = msg.reply_to.reply_to_msg_id
            )

            user_id = reply_msg.from_id

            user = await self.client(
                GetFullUserRequest(user_id)
            )

            strings = {
                name: "UserInfo",
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
                    "Account creation date: {create_date}"
                    "</b>"
                ),
            }

            info = {
                "user_id": "na/a",
                "username": "n/a",
                "first_name": "n/a",
                "last_name": "n/a",
                "phone": "n/a",
                "bio": "n/a",
                "deleted": "n/a",
                "bot": "n/a",
                "scam": "n/a",
                "fake": "n/a",
                "blocked": "n/a",
                "create_date": "n/a"
            }

            await msg.edit(
                self.strings("loading"),
                parse_mode="html"
            )

            info["user_id"] = user.user.id
            info["username"] = user.user.username
            info["first_name"] = user.user.first_name
            info["last_name"] = user.user.last_name
            info["phone"] = user.user.phone
            info["bio"] = user.user.about
            info["deleted"] = user.user.deleted
            info["bot"] = user.user.bot
            info["scam"] = user.user.scam
            info["fake"] = user.user.fake
            info["blocked"] = user.user.blocked
            info["create_date"] = user.user.date.strftime("%Y-%m-%d %H-%M:%S")

            await msg.edit(
                self.strings("userinfo").format(**info),
                parse_mode="html"
            )
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