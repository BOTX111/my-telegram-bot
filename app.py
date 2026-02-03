import logging
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant

# Sirf critical errors dikhayega taaki speed bani rahe
logging.basicConfig(level=logging.ERROR)

API_ID = 30829917
API_HASH = "9a6ee85a814e6bbec79a0148e4831315"
BOT_TOKEN = "8401571165:AAFG7Uzv0feUvUClEq16bG7hFLyoxXuoApg"
CHANNEL_USERNAME = "BotXCraft" 
YT_LINK = "https://www.youtube.com/@BotXCraftl" 

# Aapki Photo ID (Naye method se har file type support karega)
FILE_ID = "AgACAgUAAxkBAAMJayFuv7RC8KEzXqxaRv-GaAQnc_YAAoURaxtpqhFUdXiJimTCAgEAAwIAA3kABx4E"

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    try:
        # Check membership
        await client.get_chat_member(CHANNEL_USERNAME, message.from_user.id)
        # Fast sending: send_cached_media use karne se photo/doc error nahi aayega
        await client.send_cached_media(chat_id=message.from_user.id, file_id=FILE_ID, caption="✅ Verification Successful!")
    except UserNotParticipant:
        buttons = [
            [InlineKeyboardButton("📺 YouTube Page", url=YT_LINK)],
            [InlineKeyboardButton("📢 Join Telegram", url=f"https://t.me/{CHANNEL_USERNAME}")],
            [InlineKeyboardButton("✅ VERIFY", callback_data="check_sub")]
        ]
        await message.reply_text("⚠️ **Access Denied!**\n\nBot use karne ke liye join karein.", reply_markup=InlineKeyboardMarkup(buttons))
    except Exception as e:
        print(f"Error: {e}")

@app.on_callback_query(filters.regex("check_sub"))
async def verify(client, callback_query):
    try:
        await client.get_chat_member(CHANNEL_USERNAME, callback_query.from_user.id)
        await callback_query.message.delete()
        await client.send_cached_media(chat_id=callback_query.from_user.id, file_id=FILE_ID, caption="✅ Verified!")
    except UserNotParticipant:
        await callback_query.answer("❌ Pehle join karein!", show_alert=True)

app.run()
