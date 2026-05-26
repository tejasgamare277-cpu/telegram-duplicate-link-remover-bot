import re
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")

sent_links = set()

async def remove_duplicate_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    text = update.message.text

    links = re.findall(r'(https?://\S+|t\.me/\S+)', text)

    for link in links:
        if link in sent_links:
            try:
                await update.message.delete()
                await update.message.reply_text("⚠️ Duplicate link removed!")
            except Exception as e:
                print(e)
            return
        else:
            sent_links.add(link)

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, remove_duplicate_links)
)

print("Bot Started...")
app.run_polling()
