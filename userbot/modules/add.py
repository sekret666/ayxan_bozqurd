# Kopyalama atan balası

from userbot.cmdhelp import CmdHelp
from telethon.tl import functions
from telethon.tl.functions.messages import GetFullChatRequest
from telethon.errors import (
    ChannelInvalidError,
    ChannelPrivateError,
    ChannelPublicGroupNaError)
from telethon.tl.functions.channels import GetFullChannelRequest
from userbot.events import register as aykhan

async def get_chatinfo(event):
    chat = event.pattern_match.group(1)
    chat_info = None
    if chat:
        try:
            chat = int(chat)
        except ValueError:
            pass
    if not chat:
        if event.reply_to_msg_id:
            replied_msg = await event.get_reply_message()
            if replied_msg.fwd_from and replied_msg.fwd_from.channel_id is not None:
                chat = replied_msg.fwd_from.channel_id
        else:
            chat = event.chat_id
    try:
        chat_info = await event.client(GetFullChatRequest(chat))
    except BaseException:
        try:
            chat_info = await event.client(GetFullChannelRequest(chat))
        except ChannelInvalidError:
            await event.reply("`Səhv Kanal/Qrup`")
            return None
        except ChannelPrivateError:
            await event.reply("`Bu özəl bir kanal/qrupdur və ya oradan mənə qadağa qoyulub`")
            return None
        except ChannelPublicGroupNaError:
            await event.reply("`Kanal və ya superqrup yoxdur`")
            return None
        except (TypeError, ValueError):
            await event.reply("`Səhv Kanal/Qrup`")
            return None
    return chat_info


@aykhan(outgoing=True, pattern=r"^\.add(?: |$)(.*)")
async def get_users(event):
    sender = await event.get_sender()
    me = await event.client.get_me()
    if not sender.id == me.id:
        ram = await event.reply("`Əlavə olunur...`")
    else:
        ram = await event.edit("`Əlavə olunur biraz gözləyin...`")
    ramubotteam = await get_chatinfo(event)
    chat = await event.get_chat()
    if event.is_private:
        return await ram.edit("`Üzr istəyirik, bura bir istifadəçi əlavə edin`")
    s = 0
    f = 0
    error = 'None'

    await ram.edit("**Terminal vəziyyəti**\n\n`İstifadəçilərin toplanması.......`")
    async for user in event.client.iter_participants(ramubotteam.full_chat.id):
        try:
            if error.startswith("Too"):
                return await ram.edit(f"**Terminal Xəta ilə Tamamlandı**\n(`Telethon Limit Xətası Alıb Zəhmət olmasa Daha Sonra Yenidən Sınayın`)\n**Xəta** : \n`{error}`\n\n• Uğurlu: \n `{s}` istifadəçi \n• Uğursuz: \n `{f}` istifadəçi")
            await event.client(functions.channels.InviteToChannelRequest(channel=chat, users=[user.id]))
            s = s + 1
            await ram.edit(f"**Terminal Çalışır...**\n\n• Uğurlu: \n `{s}` istifadəçi \n• Uğursuz: \n `{f}` istifadəçi\n\n**× Son Səhv:** `{error}`")
        except Exception as e:
            error = str(e)
            f = f + 1
    return await ram.edit(f"**Terminal Bitdi** \n\n• Uğurla `{s}` istifadəçi dəvət olundu \n• Uğursuz `{f}` istifadəçi")
# Köməy
CmdHelp('add').add_command(
   'add', '<qrup username>', 'Linkini yazdığınız qrupdan istifadəçiləri daşıyar 🙂'
).add()
# Support
# BozQurd - add.py
