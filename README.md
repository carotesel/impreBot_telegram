# 🖨️ Telegram Printer Bot

Un bot de Telegram en **Python** que recibe archivos PDF y los imprime automáticamente en una impresora compartida en red.  
Pensado para **impresoras antiguas USB** conectadas a una **Mac** usando **Printer Sharing**.


## 🚀 Características

- Recibe archivos PDF enviados a través de Telegram.
- Guarda los archivos localmente en tu computadora.
- Envía automáticamente el PDF a una impresora en red usando `lp`.
- Configurable mediante variables de entorno.
- Funciona en **Linux** y **macOS** (Windows requiere pequeño ajuste).


## 🖨️ ¿Qué es Printer Sharing en macOS?

En **macOS**, **Printer Sharing** (*Compartir impresora*) es una función que permite que una impresora conectada **por USB** a tu Mac pueda ser usada por **otros dispositivos en la misma red** como si fuera una impresora de red.

Cuando activas esta opción:
- macOS expone la impresora mediante el protocolo **IPP (Internet Printing Protocol)**.
- Cualquier computadora o dispositivo en la red local (WiFi o cableada) puede enviar trabajos de impresión hacia esa impresora **a través de la Mac**.
- Ideal para impresoras antiguas que **no tienen WiFi** (como la mía).



### 🔹 Cómo activar Printer Sharing en macOS

1. **Conectá la impresora a tu Mac** y verificá que imprime correctamente.
2. Andá a ** Menú → Preferencias del Sistema → Impresoras y Escáneres**.
3. Seleccioná tu impresora en la lista.
4. Marcá la opción **Compartir esta impresora en la red**.
5. Andá a ** Menú → Preferencias del Sistema → Compartir**.
6. Activá **Compartir impresoras** (*Printer Sharing*).
7. Anotate:
   - El **nombre de la impresora** que aparece en la configuración.
   - La **dirección IP** de la Mac (*Preferencias de Red*).


### 🔹 Cómo conectarse a la impresora compartida
- **En macOS**:  
  1. Abrí **Preferencias de Impresoras y Escáneres**.
  2. Pulsá **+** para agregar impresora.
  3. Buscá en **Red** la impresora compartida.

- **En Linux (CUPS)**:  
  1. Abrí en el navegador: `http://localhost:631`.
  2. Agregá impresora → **IPP**.
  3. URL:
     ```
     ipp://IP_DE_LA_MAC/printers/NOMBRE_DE_IMPRESORA
     ```

- **En Windows**:  
  1. Andá a **Panel de control → Dispositivos e impresoras → Agregar impresora**.
  2. Seleccioná **Agregar impresora de red**.
  3. Dirección:
     ```
     http://IP_DE_LA_MAC:631/printers/NOMBRE_DE_IMPRESORA
     ```



## 💡 Equivalentes en otros sistemas

- **Windows** → *Printer Sharing* está en:  
  `Panel de control → Dispositivos e impresoras → Clic derecho en impresora → Propiedades → Compartir`.
  
- **Linux (CUPS)** → Se habilita desde:  
  `http://localhost:631 → Administración → Compartir esta impresora`.



## 📦 Requisitos
- Python 3.10+
- Una impresora compartida en red (**Printer Sharing** en macOS o equivalente en tu SO).
- Acceso a la API de Telegram (token desde [BotFather](https://t.me/BotFather)).
- Tener configurado el comando `lp` en tu sistema para imprimir.



## ⚙️ Instalación
```bash
git clone https://github.com/TU_USUARIO/telegram-printer-bot.git
cd telegram-printer-bot
pip install -r requirements.txt
```


## 🔑 Configuración

1. Renombrá el archivo **.env.example** a **.env**:
2. Editalo:
   ```bash
   TOKEN=TU_TOKEN_DE_BOTFATHER
   PRINTER_NAME=Nombre_de_tu_impresora
   ```



## ▶️ Ejecución
```bash
python3 bot.py
```