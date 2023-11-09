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

today = date.today()

# apt install -y python3-libtorrent tesseract-ocr

connection = connect(
    host='localhost',
    database='rarbg',
    user='postgres',
    password=config('PASSWORD_DB')
)
cursor = connection.cursor()


snd = config('FROM_MAIL')
rcv = config('TO_MAIL')
sbj = f'Movies Added in RARbg ({today.strftime("%d/%m/%Y")})'
passwd = config('PASSWORD')

# https://stackoverflow.com/questions/64717302/deprecationwarning-executable-path-has-been-deprecated-selenium-python
chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument('--start-maximized')

driver = webdriver.Chrome(
    options=chrome_options,
    service=Service(ChromeDriverManager().install())
)
driver.get('https://rarbgproxied.org/torrents.php')

wait = WebDriverWait(driver, 10)

try:
    # wait = WebDriverWait(driver, 10)
    element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'lista')))
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

html = driver.page_source
soup = beauty(html, 'html.parser')

# from pdb import set_trace; set_trace()

attachment = {}
for iterate in range(0, 8):
    title = soup.find_all("td", {
        "class": "lista",
        "align": "left",
        "valign": "top"
    })[iterate].a['title']

    url = soup.find_all("td", {
        "class": "lista",
        "align": "left",
        "valign": "top"
    })[iterate].a['href']

    clear_title = title[0:title.find(
        search('20[0-9][0-9]', title)[0]) - 1].replace('.', ' ')

    release = title[title.find(search('20[0-9][0-9]', title)[0]):title.find(
        search('20[0-9][0-9]', title)[0]) + 4]
    release_date = int(release)

    cursor.execute(
        'SELECT EXISTS ( SELECT 1 FROM torrent WHERE title = %s )',
        (f'{clear_title}',))

    if cursor.fetchone()[0] is False:
        cursor.execute("INSERT INTO torrent (title, url, release_date) VALUES "
                       f"('{clear_title}', '{url}', '{release_date}') "
                       "RETURNING id")
        data = cursor.fetchone()
        attachment[data[0]] = f'{clear_title}'
        connection.commit()

# from pdb import set_trace; set_trace()

# attachment.append(clear_title)
# print(data[0])

cursor.close()
connection.close()
driver.close()

if attachment:
    with open('/tmp/list_movies.txt', 'w') as writer:
        writer.write('''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
    <head>
        <meta charset="utf-8">
    </head>
    <body>
''')
        for key, value in attachment.items():
            writer.write(f'        <h1>{key}. {value}</h1>\n')
        writer.write('''    </body>
</html>''')

    file = open('/tmp/list_movies.txt')
    # from pdb import set_trace; set_trace()
    msg = file.read()

    head = f'Subject: {sbj}\nFrom: {snd}\nTo: {rcv}\nContent-Type: text/html\n{msg}'

    try:
        server = SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(snd, passwd)
        server.sendmail(snd, rcv, head)
        server.close()
    except Exception as e:
        print("Failed to send the mail..", e)
