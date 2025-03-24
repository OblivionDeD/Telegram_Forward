from telethon import TelegramClient, events

api_id_user = ...
api_hash_user = ''
BOT_USERNAME = ''

# Чаты, откуда будем забирать сообщения
SOURCE_CHAT_IDS = [
    -1000000000000,
    -1000000000000,
    -1000000000000,
]

client = TelegramClient('user_session', api_id_user, api_hash_user)

@client.on(events.NewMessage(chats=SOURCE_CHAT_IDS))
async def handler(event):

    msg = event.message
    text_content = msg.text or ""

    command_str = f"/send source={event.chat_id} text={text_content}"

    await client.send_message(BOT_USERNAME, command_str)
    print("[USER_SESSION] The command was sent:", command_str)

    if msg.media:
        await client.send_file(
            BOT_USERNAME,
            file=msg.media,
            caption=""  
        )
        print("[USER_SESSION] Sent to the media bot")

with client:
    print("[USER_SESSION] Launch. Waiting for new messages...")
    client.run_until_disconnected()
