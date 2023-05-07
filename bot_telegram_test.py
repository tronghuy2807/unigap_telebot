import requests
import telegram
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import datetime
import time
import os
# import pyautogui
# Code tren server
# Xóa tất cả các tệp tin trong thư mục 'photos'
folder_path = '/home/huyanh/working/unigap/sources/automation/coach/image'
for file_name in os.listdir(folder_path):
    file_path = os.path.join(folder_path, file_name)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
    except Exception as e:
        print(f"Failed to delete {file_path}. Reason: {e}")

# Setup Chrome driver
# options = ChromeOptions()
# options.add_argument("--headless")
# driver = webdriver.Chrome(
#     executable_path='/home/huyanh/working/unigap/sources/telegram/new/chromedriver.exe')  # path to driver file
# driver.set_window_size(1920, 1080)
# Here Firefox  will be used
options = FirefoxOptions()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options,
                           executable_path=r'/home/huyanh/Downloads/geckodriver-v0.33.0-linux64/geckodriver')
driver.set_window_size(1570, 1000)
# pyautogui.press('f11')

# Setup Telegram bots
# '5707243837:AAGSdNhMdzr7Cqodq4AT1Y2pCp1AUIriHC8'
# '6096572878:AAGZZuQwkB5ngjXr4lxZI4E5ykmu29APpGM'
TELEGRAM_BOT_TOKENS = '5707243837:AAGSdNhMdzr7Cqodq4AT1Y2pCp1AUIriHC8'
TELEGRAM_CHAT_IDS = [
    # '-965197811', '-965197811', '-965197811', '-965197811', '-965197811'
    '-732144767', # DAC Coach - Unigap
    '-879763889', # Application Improvement
    '-1001878000161', # UniGap_MKT Team
    '-813447774',  # UniGap Leader
    '-689915316' #DEC
]

# URL list to capture screenshots
DRIVE_URLS = [
    # Stage 1. DA fundamental
    'https://docs.google.com/spreadsheets/d/1QlqbhWlmb1cbcEfmG6cxoY7_0vMdp-rJSa_oNGG1g9M/edit#gid=1493654716',
    # Stage 2 - Application
    'https://docs.google.com/spreadsheets/d/1QlqbhWlmb1cbcEfmG6cxoY7_0vMdp-rJSa_oNGG1g9M/edit#gid=1689071588',
    'https://docs.google.com/spreadsheets/d/1QlqbhWlmb1cbcEfmG6cxoY7_0vMdp-rJSa_oNGG1g9M/edit#gid=1797942273',  # Channel
    'https://docs.google.com/spreadsheets/d/1QlqbhWlmb1cbcEfmG6cxoY7_0vMdp-rJSa_oNGG1g9M/edit#gid=1323487540',  # PDP Dashboard
    'https://docs.google.com/spreadsheets/d/1tpB8SkNK3Jai9Sha2wiZyFNlKuT5FVpfw1qp0ZceMAI/edit#gid=1029441081']  # DEC Performance Dashboard'
MESSAGE = ['Stage 1. DA fundamental', 'Stage 2 - Application',
           'Channel Dashboard', 'PDP Dashboard', 'DEC Performance Dashboard']
PHOTO_PATHS = [
    f'/home/huyanh/working/unigap/sources/automation/coach/image/{url.split("=")[-1]}_{datetime.datetime.now().strftime("%y-%m-%d_%H-%M-%S")}.png' for url in DRIVE_URLS]


def capture_url(url, photo_path):
    # Open Google Drive URL
    driver.get(url)
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(8)  # wait for 3 seconds
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    # Take screenshot and save to local path
    driver.save_screenshot(photo_path)


def main():
    # Capture screenshots of all Google Drive URLs
    for url, photo_path in zip(DRIVE_URLS, PHOTO_PATHS):
        capture_url(url, photo_path)

    # Send captured screenshots to Telegram groups
    for chat_id, message, photo_path in zip(TELEGRAM_CHAT_IDS, MESSAGE, PHOTO_PATHS):
        with open(photo_path, 'rb') as f:
            # bot = telegram.Bot(token=TELEGRAM_BOT_TOKENS)
            # bot.send_message(chat_id=chat_id, text="Daily Good Rate")
            # bot.send_photo(chat_id=chat_id, photo=open(photo_path, 'rb'))
            bot = telegram.Bot(token=TELEGRAM_BOT_TOKENS)
            bot.send_photo(chat_id=chat_id, photo=f, caption=message)
            send = requests.post('https://api.telegram.org/bot' + TELEGRAM_BOT_TOKENS +
                                 '/sendPhoto?chat_id=' + chat_id + '&caption=' + message, files={'photo': f})
    # pyautogui.press('f11')
    driver.quit()


if __name__ == '__main__':
    main()
