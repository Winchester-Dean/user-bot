# https://github.com/Winchester-Dean
# Copyright (C) 2022  Winchester-Dean

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of the License

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with this program.
# If not, see <https://www.gnu.org/licenses/>.

import telethon
import os
import shlex

from telethon.tl.types import PeerUser, PeerChat, PeerChannel

def get_base_dir():
    return get_dir("user-bot")

def get_dir(mod):
    return os.path.abspath(
        os.path.dirname(
            os.path.abspath(
                mod
            )
        )
    )

async def get_args(message):
    try:
        try:
            message = message.message
        except AttributeError:
            pass
        
        if not message:
            return False
        
        message = message.split(maxsplit=1)
        if len(message) <= 1:
            return []

        message = message[1]
        try:
            split = shlex.split(message)
        except ValueError:
            return message

        return list(filter(x, split))
    except Exception as error:
        await message.edit(
            f"⚠ <b>Error:</b> <code>{error}</code>",
            parse_mode="html"
        )
        return

async def get_args_raw(msg):
    try:
        try:
            message = msg.message.text
        except AttributeError as error:
            await msg.edit(
                f"⚠ <b>Error:</b> <code>{error}</code>",
                parse_mode="html"
            )
            pass
        
        if not message:
            return False
        
        args = message.split(maxsplit=1)
        if len(args) > 1:
            return args[1]
        
        return ""
    except Exception as error:
        await msg.edit(
            f"⚠ <b>Error:</b> <code>{error}</code>",
            parse_mode="html"
        )

async def get_user(message):
    try:
        try:
            return await message.client.get_entity(
                message.sender_id
            )
        except ValueError:
            pass
        
        if isinstance(
            message.to_id,
            PeerUser
        ):
            try:
                await message.client.get_dialogs()
            except telethon.rpcerrorlist.BotMethodInvalid:
                return None
            
            return await message.client.get_entity(
                message.sender_id
            )
        
        if isinstance(
            message.to_id,
            (
                PeerChannel,
                PeerChat
            )
        ):
            for user in message.client.iter_participants(
                message.to_id,
                aggressive=True
            ):
                if user.id == message.sender_id:
                    return user
            
            return None
        
        return None
    except Exception as error:
        await message.edit(
            f"⚠ <b>Error:</b> <code>{error}</code>",
            parse_mode="html"
        )
