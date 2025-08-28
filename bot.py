from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes
import os

# Lấy token từ biến môi trường Heroku
TOKEN = os.environ.get("BOT_TOKEN")

# Hàm /start hiển thị menu
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    menu = [
        ["Lấy ID telegram", "Chọn skin Cần Mod"],
        ["pack mod skin", "Tiến Hành Auto ModSkin"],
        ["test file mod"],
        ["Chức Năng:Cam Xa, HD Skill, PersonalButton"],
        ["Kiểm Tra Vip", "Tìm Skin Nhanh", "Xoá Skin Nhanh"]
    ]
    reply_markup = ReplyKeyboardMarkup(menu, resize_keyboard=True)
    await update.message.reply_text("Bot bắt đầu + InfoAdmin!!", reply_markup=reply_markup)

# Ví dụ: lấy ID Telegram
async def get_user_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    await update.message.reply_text(f"ID Telegram của bạn là: {user_id}")

# Ví dụ: placeholder cho lệnh khác
async def chay_mod(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Đang chạy Auto ModSkin... (bạn gắn tool Python vào đây)")

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("userid", get_user_id))
    app.add_handler(CommandHandler("chaymod", chay_mod))

    print("Bot đang chạy trên Heroku...")
    app.run_polling()

if __name__ == "__main__":
    main()