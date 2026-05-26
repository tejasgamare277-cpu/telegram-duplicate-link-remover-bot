import re
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

BOT_TOKEN = 8992802234:AAE_89qVGU9KIc13a-GX8WLNRvTYPhEUMJ4

sent_links = set()

async def remove_duplicate_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    text = update.message.text

    links = re.findall(r'(https?://\S+|t\.me/\S+)', text)

    duplicate_found = False

    for link in links:
        if link in sent_links:
            duplicate_found = True
            try:
                await update.message.delete()
                await update.message.reply_text(
                    "⚠️ Duplicate link removed!"
                )
            except:
                pass
            return
        else:
            sent_links.add(link)

    if not duplicate_found:
        print("New link allowed")

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, remove_duplicate_links)
)

print("Bot Started...")
app.run_polling()
