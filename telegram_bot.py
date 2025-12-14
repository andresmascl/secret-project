from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Función que responde al comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hola! Soy tu bot HeyRobot_andresmascl_bot.")

# Crear la aplicación del bot
app = ApplicationBuilder().token("8268160120:AAEYBp6AeJDvpuv-pJQwVhajnLuPigdOKTg").build()

# Agregar el handler para /start
app.add_handler(CommandHandler("start", start))

# Ejecutar el bot
app.run_polling()