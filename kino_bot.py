import json
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "9019552343:AAEvvOIrAin6y-Xl_jf4FKHU-xa9TnTJBgU"
ADMIN_ID = 8418889117
FAYL = "kinolar.json"


def yuklash():
    if os.path.exists(FAYL):
        with open(FAYL, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def saqlash(data):
    with open(FAYL, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salom! Kino kodini yozing.")


async def video_qabul(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    msg = update.message
    if msg.video:
        fayl_id, turi = msg.video.file_id, "video"
    else:
        fayl_id, turi = msg.document.file_id, "document"
    kinolar = yuklash()
    kod = str(len(kinolar) + 1)
    kinolar[kod] = {"file_id": fayl_id, "turi": turi, "nom": msg.caption or "Kino"}
    saqlash(kinolar)
    await msg.reply_text(f"Saqlandi! Kod: {kod}")


async def kod_qabul(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kod = update.message.text.strip()
    kinolar = yuklash()
    if kod not in kinolar:
        await update.message.reply_text("Bunday kod topilmadi.")
        return
    k = kinolar[kod]
    if k["turi"] == "video":
        await update.message.reply_video(k["file_id"], caption=k["nom"])
    else:
        await update.message.reply_document(k["file_id"], caption=k["nom"])


app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.VIDEO | filters.Document.ALL, video_qabul))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, kod_qabul))
app.run_polling()
