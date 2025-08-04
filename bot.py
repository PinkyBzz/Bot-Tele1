import io
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ContextTypes, CallbackQueryHandler, filters
)
from PIL import Image, ImageDraw, ImageFont
import textwrap

TOKEN = "8292715371:AAHvPN0QUpyJDwUnS4dZbkqNeF4N2tzu-tI"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("Generate", callback_data="generate")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Klik tombol Generate untuk membuat stiker brat.",
        reply_markup=reply_markup
    )

# Handler untuk /generate command
async def generate_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Silakan masukkan teks yang ingin dijadikan stiker brat:")
    context.user_data["expecting_text"] = True

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("Silakan masukkan teks yang ingin dijadikan stiker brat:")
    context.user_data["expecting_text"] = True

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("expecting_text"):
        context.user_data["expecting_text"] = False
        text = update.message.text
        img = generate_brat_image(text)
        bio = io.BytesIO()
        bio.name = "brat.png"
        img.save(bio, "PNG")
        bio.seek(0)
        await update.message.reply_photo(photo=bio, caption="Ini brat kamu!")

def generate_brat_image(text):
    img = Image.new("RGBA", (512, 512), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", 36)
    except:
        font = ImageFont.load_default()
    wrapped = textwrap.wrap(text, width=15)
    line_height = font.getbbox('hg')[3] - font.getbbox('hg')[1]
    total_height = len(wrapped) * line_height
    y = (512 - total_height) // 2
    for line in wrapped:
        line_width = draw.textlength(line, font=font)
        x = (512 - line_width) // 2
        draw.text((x, y), line, font=font, fill="black")
        y += line_height
    return img

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("generate", generate_command))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.run_polling()
