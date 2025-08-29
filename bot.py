import os
import logging
import subprocess
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")  # Lấy token từ Railway Variables

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ================== HÀM GỌI TOOL GỐC ==================
def run_tool(username: str, password: str):
    """
    Gọi tool gốc lbdxaov.py bằng subprocess
    """
    try:
        process = subprocess.Popen(
            ["python3", "lbdxaov.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        # Tool thường yêu cầu nhập user & pass
        out, err = process.communicate(f"{username}\n{password}\n", timeout=120)

        # Kiểm tra log
        logger.info("Tool output: %s", out)
        if err:
            logger.error("Tool error: %s", err)

        return True
    except Exception as e:
        logger.error("Tool execution failed: %s", str(e))
        return False

# ================== COMMAND HANDLERS ==================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["/login"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("🤖 Bot sẵn sàng!\nNhấn /login để bắt đầu.", reply_markup=reply_markup)

async def login(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔑 Vui lòng nhập tài khoản và mật khẩu theo dạng:\n\n`user|pass`", parse_mode="Markdown")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if "|" in text:  # user nhập tài khoản|mật khẩu
        username, password = text.split("|", 1)
        await update.message.reply_text("⚙️ Đang chạy tool, vui lòng chờ...")

        success = run_tool(username.strip(), password.strip())
        if success:
            # Tool chạy xong -> gửi file kết quả
            output_file = "output/result.txt"  # thay tên file tool xuất ra
            if os.path.exists(output_file):
                await update.message.reply_document(document=open(output_file, "rb"))
            else:
                await update.message.reply_text("❌ Không tìm thấy file output.")
        else:
            await update.message.reply_text("❌ Tool lỗi, vui lòng thử lại.")

# ================== MAIN ==================
def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("login", login))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == "__main__":
    main()
