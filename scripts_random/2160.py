from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from pytesseract.pytesseract import image_to_string
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as beauty
from selenium import webdriver
from psycopg2 import connect
from decouple import config
from datetime import date
from smtplib import SMTP
from io import BytesIO
from PIL import Image
from re import search


chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument('--start-maximized')

driver = webdriver.Chrome(
    options=chrome_options,
    service=Service(ChromeDriverManager().install())
)
driver.get('https://rarbgproxied.org/torrents.php?category=movies')

wait = WebDriverWait(driver, 10)

data = ['The Black Demon', '2023']

try:
    # wait = WebDriverWait(driver, 10)
    element = wait.until(EC.element_to_be_clickable((By.ID, 'searchinput')))

    driver.find_element(By.ID, 'searchinput').send_keys(f'{data[0]} {data[1]}')
    driver.find_element(By.TAG_NAME, 'button').submit()

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'black'))
    )

    html = driver.page_source
    soup = beauty(html, 'html.parser')

    from pdb import set_trace; set_trace()

    # for iterate in range(0, 8):
    #     title = soup.find_all("td", {
    #         "class": "lista2",
    #         "align": "left",
    #         "valign": "top"
    #     })[iterate].a['title']


except TimeoutException:
    # print("Loading took too much time!")
    # wait = WebDriverWait(driver, 10)
    element = wait.until(EC.element_to_be_clickable((By.NAME, 'solve_string')))
    # Saves in memory picture of html element containing code to be transcript
    img_bytes = driver.find_element(
        By.XPATH,
        "//img[contains(@src, 'cid')]"
    ).screenshot_as_png
    # img_dwnl = Image.open(BytesIO(img_bytes)).save('example.png')
    txt = image_to_string(Image.open(BytesIO(img_bytes)))

    driver.find_element(By.NAME, 'solve_string').send_keys(txt[:5])
    driver.find_element(By.CLASS_NAME, 'button').submit()

    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'lista')))
