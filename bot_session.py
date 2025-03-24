import re
import logging
import json
import os
from telethon import TelegramClient, events
from telethon.tl.types import PeerChannel, PeerChat, PeerUser, MessageMediaWebPage

logging.basicConfig(format='[%(levelname)s] %(asctime)s - %(name)s - %(message)s', level=logging.INFO)

api_id_bot = ...
api_hash_bot = ''
bot_token = ''

FORWARD_RULES = {
    -1000000000000: {'target_chat': -1001111111111},
    -1000000000000: {'target_chat': -1001111111111},
    -1000000000000: {'target_chat': -1001111111111},
}

bot = TelegramClient('bot_session', api_id_bot, api_hash_bot)

cmd_pattern = re.compile(r'^/send\s+source=(-?\d+)\s+text=([\s\S]*)$', re.IGNORECASE)
SAVE_FILE = 'last_source.json'
last_source_by_user = {}

def load_last_source():
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, dict):
                    for k, v in data.items():
                        last_source_by_user[int(k)] = int(v)
        except Exception as e:
            logging.warning(f"Read error {SAVE_FILE}: {e}")

def save_last_source():
    try:
        data = {str(k): v for k, v in last_source_by_user.items()}
        with open(SAVE_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logging.warning(f"Writing error {SAVE_FILE}: {e}")

@bot.on(events.NewMessage)
async def handle_messages(event):
    if event.is_private and (await event.get_sender()).bot:
        return
    msg = event.message
    msg_text = (msg.raw_text or "").strip()
    sender = await event.get_sender()
    user_id = sender.id if sender else 0
    match = cmd_pattern.match(msg_text)
    if match:
        source_chat_id = int(match.group(1))
        user_text = match.group(2).strip()
        last_source_by_user[user_id] = source_chat_id
        rule = FORWARD_RULES.get(source_chat_id)
        if not rule:
            await event.reply(f"No rule for source={source_chat_id}.")
            return
        target_chat_id = rule['target_chat']
        try:
            if msg.media:
                if isinstance(msg.media, MessageMediaWebPage):
                    await bot.send_message(target_chat_id, user_text)
                else:
                    await bot.send_file(target_chat_id, file=msg.media, caption=user_text)
            else:
                await bot.send_message(target_chat_id, user_text)
            await event.reply(f"[Command /send] {source_chat_id} → {target_chat_id}")
        except Exception as e:
            await event.reply(f"Error: {e}")
        return
    fwd_header = msg.fwd_from
    if fwd_header:
        from_id = fwd_header.from_id
        if not from_id:
            return
        if isinstance(from_id, PeerChannel):
            source_chat_id = -1000000000000 + from_id.channel_id
        elif isinstance(from_id, PeerChat):
            source_chat_id = -from_id.chat_id
        elif isinstance(from_id, PeerUser):
            source_chat_id = from_id.user_id
        else:
            source_chat_id = None
        if source_chat_id and source_chat_id in FORWARD_RULES:
            target_chat_id = FORWARD_RULES[source_chat_id]['target_chat']
            content_text = msg.text or ""
            try:
                if msg.media:
                    if isinstance(msg.media, MessageMediaWebPage):
                        await bot.send_message(target_chat_id, content_text)
                    else:
                        await bot.send_file(target_chat_id, file=msg.media, caption=content_text)
                else:
                    await bot.send_message(target_chat_id, content_text)
                await event.reply(f"[Forwarded] {source_chat_id} → {target_chat_id}")
            except Exception as e:
                await event.reply(f"Error: {e}")
        return
    last_source = last_source_by_user.get(user_id)
    if last_source:
        rule = FORWARD_RULES.get(last_source)
        if rule:
            target_chat_id = rule['target_chat']
            content_text = msg.text or ""
            try:
                if msg.media:
                    if isinstance(msg.media, MessageMediaWebPage):
                        await bot.send_message(target_chat_id, content_text)
                    else:
                        await bot.send_file(target_chat_id, file=msg.media, caption=content_text)
                else:
                    await bot.send_message(target_chat_id, content_text)
                await event.reply(f"[Last Source] {last_source} → {target_chat_id}")
            except Exception as e:
                await event.reply(f"Error: {e}")
        else:
            await event.reply(f"Memorized source={last_source}, but there's no rule.")
    else:
        await event.reply("No active source. /send source=... text=...")

def main():
    load_last_source()
    bot.start(bot_token=bot_token)
    bot.run_until_disconnected()
    save_last_source()

if __name__ == '__main__':
    main()
