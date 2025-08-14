from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import os
import subprocess
import time
from dotenv import load_dotenv
from telegram.error import NetworkError, TelegramError
from apscheduler.schedulers.background import BackgroundScheduler

# Cargar variables de entorno
load_dotenv()

BOT_TOKEN = os.getenv("TOKEN")
PRINTER_NAME = os.getenv("PRINTER_NAME")  # Nombre exacto de la impresora en CUPS

print(f"📄 Usando impresora: '{PRINTER_NAME}'")

# Carpeta donde se guardan los archivos recibidos temporalmente
SAVE_PATH = "archivos_recibidos"
os.makedirs(SAVE_PATH, exist_ok=True)

# Usuarios esperando enviar archivo
user_waiting_file = set()

# --- Comandos ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hola, soy tu bot impresor.\n"
        "Usá /printfile y enviame un PDF para imprimir."
    )

async def printFile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_waiting_file.add(update.effective_user.id)
    await update.message.reply_text("📂 Enviame el archivo que querés imprimir.")

# --- Manejo de documentos ---
async def handleDocument(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in user_waiting_file:
        await update.message.reply_text("Usá /printfile antes de enviarme un archivo.")
        return

    document = update.message.document
    file_name = document.file_name
    file_path = os.path.join(SAVE_PATH, file_name)

    # Descargar archivo
    file = await context.bot.getFile(document.file_id)
    await file.download_to_drive(file_path)

    user_waiting_file.remove(user_id)

    # Imprimir archivo
    try:
        if PRINTER_NAME:
            subprocess.run(["lp", "-d", PRINTER_NAME, file_path], check=True)
        else:
            subprocess.run(["lp", file_path], check=True)

        await update.message.reply_text(f"✅ '{file_name}' enviado a la impresora.")
        print(f"🖨️ Archivo '{file_name}' enviado a imprimir.")
    except subprocess.CalledProcessError as e:
        await update.message.reply_text(f"❌ No se pudo imprimir '{file_name}'. Error: {e}")
        print(f"⚠️ Error al imprimir: {e}")

    # Borrar archivo temporal
    try:
        os.remove(file_path)
        print(f"🗑️ Archivo temporal '{file_name}' eliminado.")
    except OSError:
        pass

# --- Ping para mantener conexión ---
def keep_alive():
    print("🔄 Ping al bot para mantener conexión activa.")

# --- Función para correr el bot con reconexión ---
def run_bot():
    while True:
        try:
            app = ApplicationBuilder().token(BOT_TOKEN).build()

            # Comandos
            app.add_handler(CommandHandler("start", start))
            app.add_handler(CommandHandler("printfile", printFile))

            # Archivos
            app.add_handler(MessageHandler(filters.Document.ALL, handleDocument))

            # Scheduler para mantener vivo el bot
            scheduler = BackgroundScheduler()
            scheduler.add_job(keep_alive, "interval", minutes=5)
            scheduler.start()

            print("🤖 Bot iniciado y escuchando...")
            app.run_polling(drop_pending_updates=True)

        except (NetworkError, TelegramError) as e:
            print(f"⚠️ Error de red o Telegram: {e}. Reintentando en 5 segundos...")
            time.sleep(5)
        except Exception as e:
            print(f"❌ Error inesperado: {e}. Reiniciando en 10 segundos...")
            time.sleep(10)

if __name__ == "__main__":
    if not BOT_TOKEN:
        raise ValueError("No se encontró TOKEN en el archivo .env")

    run_bot()