from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import os
import subprocess
from dotenv import load_dotenv

load_dotenv()  # Carga las variables del .env

BOT_TOKEN = os.getenv("TOKEN")
PRINTER_NAME = os.getenv("PRINTER_NAME")  # Nombre de la impresora configurada en mi PC

print(f"📄 Usando impresora: '{PRINTER_NAME}'")


# Carpeta donde guardar los archivos recibidos
SAVE_PATH = "archivos_recibidos"
os.makedirs(SAVE_PATH, exist_ok=True)

# Variable para saber si el usuario está en modo "enviar archivo para imprimir"
user_waiting_file = set()

# Commando /hello para iniciar la conversación
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋Hola, soy tu bot impresor.\nEnvíame un archivo PDF con /printfile y lo imprimiré automáticamente.")

# Commando /print para indicar que se quiere enviar un archivo para imprimir
async def printFile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_waiting_file.add(update.effective_user.id)
    await update.message.reply_text("Por favor envíame el archivo que quieres imprimir.")

async def handleDocument(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in user_waiting_file:
        await update.message.reply_text("Si quieres imprimir, usa el comando /printfile primero.")
        return
    
    document = update.message.document

    # Descargar el archivo
    file_name = document.file_name
    file_path = os.path.join(SAVE_PATH, file_name)

    file = await context.bot.getFile(document.file_id)
    await file.download_to_drive(file_path)

    # Eliminar de la lista de espera
    user_waiting_file.remove(user_id)

    # Enviar a imprimir usando lp y la impresora compartida
    try:
        if PRINTER_NAME:
            subprocess.run(["lp", "-d", PRINTER_NAME, file_path], check=True)
        else:
            subprocess.run(["lp", file_path], check=True)

        await update.message.reply_text(f"✅ '{file_name}' enviado a la impresora.")
    except subprocess.CalledProcessError as e:
        await update.message.reply_text(f"❌ No se pudo imprimir '{file_name}'. Error: {e}")
        return

    #Borrar el archivo después de imprimir
    try:
        os.remove(file_path)
    except OSError:
        pass



if __name__ == "__main__":
    if not BOT_TOKEN:
        raise ValueError("No se encontró TOKEN en el archivo .env")
    
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    #Comandos
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("printfile", printFile))

    #Archivos
    app.add_handler(MessageHandler(filters.Document.ALL, handleDocument))

    print("🤖 Bot iniciado y escuchando...")
    app.run_polling()

    



