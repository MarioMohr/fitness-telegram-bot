import os
import sqlite3
from datetime import datetime
import zoneinfo
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

DB_PATH = os.environ.get("DB_PATH", "/data/fitness.db")
MY_TZ = zoneinfo.ZoneInfo("Asia/Kuala_Lumpur")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pool_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            wochentag TEXT,
            uhrzeit TEXT,
            status TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_log (
            datum TEXT PRIMARY KEY,
            proteine INTEGER DEFAULT 0,
            magnesium INTEGER DEFAULT 0,
            elektrolyte INTEGER DEFAULT 0,
            cashews INTEGER DEFAULT 0,
            schwimmen INTEGER DEFAULT 0,
            bahnen INTEGER DEFAULT 0,
            dpc_walk INTEGER DEFAULT 0,
            ddp_yoga INTEGER DEFAULT 0,
            saft TEXT DEFAULT '',
            gewicht REAL DEFAULT 0.0,
            yoga_video TEXT DEFAULT ''
        )
    ''')
    try:
        cursor.execute("ALTER TABLE daily_log ADD COLUMN yoga_video TEXT DEFAULT ''")
    except sqlite3.OperationalError:
        pass
    conn.commit()
    conn.close()

def get_main_keyboard():
    keyboard = [
        ['🏊 Pool Status', '🥩 Nutrition & Sport'],
        ['📊 Statistics', '⚖️ Log Weight']
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_cancel_keyboard():
    return ReplyKeyboardMarkup([['⬅️ Cancel']], resize_keyboard=True)

def get_yoga_keyboard():
    keyboard = [
        ['⚡ Energy', '🔥 Red Hot Core'],
        ['🏃 Fat Burner', '🌱 Beginner Beginner'],
        ['📐 Diamond Dozen', '💎 Diamond Cutter'],
        ['💪 Strength Builder', '🧱 Below The Belt'],
        ['🐦 The Black Crow', '🌋 Terrible 10s'],
        ['👴 Kickin Old School', '💥 100 Push Up Challenge'],
        ['🚨 Living In The Red Zone', '✈️ Harrier Jet'],
        ['⬅️ Cancel']
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Your Fitness Trainer is ready. Choose an option:",
        reply_markup=get_main_keyboard()
    )

def get_status_msg(text: str) -> str:
    if "Proteins" in text: return "Meat proteins logged!"
    if "Magnesium" in text: return "100% Cacao logged!"
    if "Electrolytes" in text: return "100 Plus Zero logged!"
    if "Cashews" in text: return "Cashews logged!"
    if "DPC Walk" in text: return "Walk in DPC recorded! Hope you got your juice at Waterfront."
    if "Breathing" in text: return "Breathing exercises completed!"
    return "Logged!"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    jetzt = datetime.now(MY_TZ)
    heute = jetzt.strftime("%Y-%m-%d")
    user_data = context.user_data

    if text == '⬅️ Cancel':
        user_data['state'] = None
        await update.message.reply_text("Action canceled. Back to main menu.", reply_markup=get_main_keyboard())
        return

    # --- WEIGHT INPUT ---
    if user_data.get('state') == 'waiting_for_weight':
        try:
            val = float(text.replace(',', '.'))
            if 50.0 < val < 200.0:
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                cursor.execute("INSERT OR IGNORE INTO daily_log (datum) VALUES (?)", (heute,))
                cursor.execute("UPDATE daily_log SET gewicht = ? WHERE datum = ?", (val, heute))
                conn.commit()
                conn.close()
                user_data['state'] = None
                await update.message.reply_text(f"Weight of {val} kg saved!", reply_markup=get_main_keyboard())
                return
        except ValueError:
            await update.message.reply_text("Please send a valid number or press Cancel.", reply_markup=get_cancel_keyboard())
            return

    # --- LAPS INPUT ---
    if user_data.get('state') == 'waiting_for_laps':
        try:
            anzahl = int(text)
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("INSERT OR IGNORE INTO daily_log (datum) VALUES (?)", (heute,))
            cursor.execute("UPDATE daily_log SET schwimmen = 1, bahnen = bahnen + ? WHERE datum = ?", (anzahl, heute))
            conn.commit()
            conn.close()
            user_data['state'] = None
            await update.message.reply_text("Laps tracking updated successfully!", reply_markup=get_main_keyboard())
            return
        except ValueError:
            await update.message.reply_text("Please send a whole number for the laps or press Cancel.", reply_markup=get_cancel_keyboard())
            return

    # --- YOGA SELECTION HANDLING ---
    if user_data.get('state') == 'waiting_for_yoga_selection':
        cleaned_video = text.strip().replace('⚡ ', '').replace('🔥 ', '').replace('🏃 ', '').replace('🌱 ', '').replace('📐 ', '').replace('💎 ', '').replace('💪 ', '').replace('🧱 ', '').replace('🐦 ', '').replace('🌋 ', '').replace('👴 ', '').replace('💥 ', '').replace('🚨 ', '').replace('✈️ ', '')
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO daily_log (datum) VALUES (?)", (heute,))
        cursor.execute("UPDATE daily_log SET ddp_yoga = 1, yoga_video = ? WHERE datum = ?", (cleaned_video, heute))
        conn.commit()
        conn.close()
        user_data['state'] = None
        await update.message.reply_text(f"Awesome! Logged entry for DDP Yoga: {cleaned_video}", reply_markup=get_main_keyboard())
        return

    # POOL MENU
    if text == '🏊 Pool Status':
        keyboard = [
            ['🟢 Pool is EMPTY', '🔴 Pool is FULL'],
            ['🌧️ Raining (Empty)', '🎉 Public Holiday'],
            ['⬅️ Back']
        ]
        await update.message.reply_text("What is the situation at the pool right now?", reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
    
    elif text in ['🟢 Pool is EMPTY', '🔴 Pool is FULL', '🌧️ Raining (Empty)', '🎉 Public Holiday']:
        status_map = {
            '🟢 Pool is EMPTY': 'FREI',
            '🔴 Pool is FULL': 'VOLL',
            '🌧️ Raining (Empty)': 'REGEN_LEER',
            '🎉 Public Holiday': 'FEIERTAG'
        }
        status = status_map[text]
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO pool_log (timestamp, wochentag, uhrzeit, status) VALUES (?, ?, ?, ?)", (jetzt.isoformat(), jetzt.strftime("%A"), jetzt.strftime("%H:%M"), status))
        conn.commit()
        conn.close()
        await update.message.reply_text(f"Pool status updated to {status}.", reply_markup=get_main_keyboard())

    # NUTRITION & SPORT MENU
    elif text == '🥩 Nutrition & Sport':
        keyboard = [
            ['✅ Proteins (Meat)', '✅ Magnesium (Cacao)'],
            ['✅ Electrolytes (100+)', '✅ Cashews'],
            ['🏊 Log Swim Laps', '🚶 DPC Walk'],
            ['✅ DDP Yoga', '✅ Breathing Exercises'],
            ['⬅️ Back']
        ]
        await update.message.reply_text("Select an activity or meal item:", reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
    
    elif text == '🏊 Log Swim Laps':
        user_data['state'] = 'waiting_for_laps'
        await update.message.reply_text("How many laps did you swim today?", reply_markup=get_cancel_keyboard())
    
    elif text == '✅ DDP Yoga':
        user_data['state'] = 'waiting_for_yoga_selection'
        await update.message.reply_text("Which video did you do today?", reply_markup=get_yoga_keyboard())

    elif text.startswith('✅') or text == '🚶 DPC Walk':
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO daily_log (datum) VALUES (?)", (heute,))
        
        spalte = ""
        if "Proteins" in text: spalte = "proteine"
        elif "Magnesium" in text: spalte = "magnesium"
        elif "Electrolytes" in text: spalte = "elektrolyte"
        elif "Cashews" in text: spalte = "cashews"
        elif "DPC Walk" in text: spalte = "dpc_walk"
        elif "Breathing" in text: spalte = "ddp_yoga"

        cursor.execute(f"UPDATE daily_log SET {spalte} = 1 WHERE datum = ?", (heute,))
        conn.commit()
        conn.close()
        await update.message.reply_text(get_status_msg(text), reply_markup=get_main_keyboard())

    elif text == '⚖️ Log Weight':
        user_data['state'] = 'waiting_for_weight'
        await update.message.reply_text("Send me your estimated weight as a number:", reply_markup=get_cancel_keyboard())

    elif text == '⬅️ Back':
        await update.message.reply_text("Main Menu", reply_markup=get_main_keyboard())
    
    else:
        if any(x in text.lower() for x in ["saft", "wasser", "dragon", "juice", "melon"]):
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("INSERT OR IGNORE INTO daily_log (datum) VALUES (?)", (heute,))
            cursor.execute("UPDATE daily_log SET saft = ? WHERE datum = ?", (text, heute))
            conn.commit()
            conn.close()
            await update.message.reply_text(f"Juice break documented: {text}", reply_markup=get_main_keyboard())
        else:
            await update.message.reply_text("Command not recognized.", reply_markup=get_main_keyboard())

def main():
    init_db()
import os

    token = os.getenv("TELEGRAM_BOT_TOKEN")
    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == '__main__':
    main()

