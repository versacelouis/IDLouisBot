import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- BOT TOKEN ---
TOKEN = os.environ.get("BOT_TOKEN")
if not TOKEN:
    raise SystemExit("Error: BOT_TOKEN environment variable not set.")

# --- PORTFOLIO LINKS ---
PORTFOLIO_LINKS = {
    "Potong Pasir": "https://tinyurl.com/LYPotongPasir",
    "Water Gardens": "https://tinyurl.com/LYWaterGardens",
    "Keat Hong Pride": "https://tinyurl.com/LYKeatHongPride",
    "Keat Hong Axis": "https://tinyurl.com/LY808CCK",
    "182 Edgefield Plains": "https://tinyurl.com/LY182EdgefieldPlains",
    "23 Bedok": "https://tinyurl.com/LY23Bedok",
    "Birghminham Mansions": "https://tinyurl.com/LY130Thomson",
    "Fernval EC": "https://tinyurl.com/LYFernvaleEC",
    "Tampines Treasures": "https://tinyurl.com/LYTampTreasures",
    "Sumang Walk": "https://tinyurl.com/LY322Sumang",
    "Keat Hong Mirage": "https://tinyurl.com/LYKeatHongMirage",
    "Jurong East EA": "https://tinyurl.com/LYJurongEastEA",
    "Punggol Northshore": "https://tinyurl.com/LYPunggolNorthShore",
    "Clementi West Coast": "https://tinyurl.com/LYClementiWestCoast",
    "Clementi 3GEN": "https://tinyurl.com/LYClementi3gen",
    "Fernvale": "https://tinyurl.com/LYFernvale",
    "Bedok North": "https://tinyurl.com/LYBedokNorth",
}

# --- FILES ---
MOODBOARD_FILE = "DnI-MoodBoard.pdf"
NAMECARD_FILE = "Louis.Yeo.pdf"
ABOUT_ME_IMAGE = "https://i.imgur.com/mCJbLqz.jpg"  # About Me image

# --- MAIN MENU KEYBOARD ---
def main_menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("About Me", callback_data="about")],
        [InlineKeyboardButton("Name Card", callback_data="namecard")],
        [InlineKeyboardButton("MoodBoard", callback_data="moodboard")],
        [InlineKeyboardButton("Portfolio", callback_data="portfolio")],
        [InlineKeyboardButton("Contact Me", callback_data="contact")]
    ])

# --- START COMMAND ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_first_name = update.effective_user.first_name
    welcome_text = (
        f"🌟 Welcome {user_first_name}! 🌟\n\n"
        "I'm Louis, your interior designer with over 5 years of experience.\n\n"
        "Use the buttons below to explore About Me, view my Name Card, check MoodBoard & Portfolio, or get in touch!"
    )
    await update.message.reply_text(welcome_text, reply_markup=main_menu_keyboard())

# --- CALLBACK HANDLER ---
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat.id

    # --- ABOUT ME ---
    if query.data == "about":
        about_text = (
            "👋 Hi! I'm Louis, an interior designer with over 5 years of experience.\n\n"
            "I specialize in modern residential and commercial interiors that reflect my clients’ personalities and needs.\n\n"
            "Every space tells a story, and I love turning ideas into inspiring realities.\n"
            "Collaboration is key, and I work closely with clients to ensure each project is stylish and practical."
        )
        keyboard = [[InlineKeyboardButton("Back to menu", callback_data="menu")]]
        await context.bot.send_photo(chat_id=chat_id, photo=ABOUT_ME_IMAGE, caption=about_text,
                                     reply_markup=InlineKeyboardMarkup(keyboard))

    # --- NAME CARD (send PDF) ---
    elif query.data == "namecard":
        keyboard = [[InlineKeyboardButton("Back to menu", callback_data="menu")]]
        if os.path.exists(NAMECARD_FILE):
            with open(NAMECARD_FILE, "rb") as f:
                await context.bot.send_document(chat_id=chat_id, document=f,
                                                caption="📇 Here’s my Name Card (PDF). Save my contact for future projects.",
                                                reply_markup=InlineKeyboardMarkup(keyboard))
        else:
            await context.bot.send_message(chat_id=chat_id,
                                           text="❌ Name Card PDF not found. Please upload 'Louis.Yeo.pdf' to the bot folder.",
                                           reply_markup=InlineKeyboardMarkup(keyboard))

    # --- MOODBOARD ---
    elif query.data == "moodboard":
        keyboard = [[InlineKeyboardButton("Back to menu", callback_data="menu")]]
        if os.path.exists(MOODBOARD_FILE):
            with open(MOODBOARD_FILE, "rb") as f:
                await context.bot.send_document(chat_id=chat_id, document=f,
                                                caption="🎨 Check out my MoodBoard for design inspirations!",
                                                reply_markup=InlineKeyboardMarkup(keyboard))
        else:
            await context.bot.send_message(chat_id=chat_id,
                                           text="❌ MoodBoard PDF not found. Please upload 'DnI-MoodBoard.pdf' to the bot folder.",
                                           reply_markup=InlineKeyboardMarkup(keyboard))

    # --- PORTFOLIO ---
    elif query.data == "portfolio":
        keyboard = [[InlineKeyboardButton(name, url=link)] for name, link in PORTFOLIO_LINKS.items()]
        keyboard.append([InlineKeyboardButton("Back to menu", callback_data="menu")])
        portfolio_text = "✨ My Portfolio ✨\n\nClick a project to view it:"
        await context.bot.send_message(chat_id=chat_id, text=portfolio_text,
                                       reply_markup=InlineKeyboardMarkup(keyboard))

    # --- CONTACT ---
    elif query.data == "contact":
        contact_text = (
            "📞 Let's get in touch!\n\n"
            "Call/Text: +65 8719 1818\n\n"
            "Or reach out via the buttons below:"
        )
        keyboard = [
            [InlineKeyboardButton("Back to menu", callback_data="menu")],
            [InlineKeyboardButton("Chat on WhatsApp", url="https://wa.me/6587191818")],
            [InlineKeyboardButton("Chat on Telegram", url="https://t.me/idlouisyeo")],
            [InlineKeyboardButton("Instagram", url="https://www.instagram.com/idlouisyeo")]
        ]
        await context.bot.send_message(chat_id=chat_id, text=contact_text,
                                       reply_markup=InlineKeyboardMarkup(keyboard))

    # --- BACK TO MENU ---
    elif query.data == "menu":
        menu_text = "🌟 Welcome! Choose an option:"
        await context.bot.send_message(chat_id=chat_id, text=menu_text, reply_markup=main_menu_keyboard())

# --- MAIN ---
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
