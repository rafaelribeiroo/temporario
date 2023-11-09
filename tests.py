# from webdriver_manager.core.os_manager import ChromeType
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from bs4 import BeautifulSoup as beauty
# from selenium import webdriver
# from os import system
# from re import sub


# chrome_options = Options()

# chrome_options.binary_location = str(system('which brave-browser'))
# chrome_options.add_argument('binary_location')
# driver = webdriver.Chrome(
#     options=chrome_options
#     # service=Service(ChromeDriverManager().install())
# )

# # from pdb import set_trace; set_trace()
# driver.get('https://www.facebook.com/marketplace/item/669670138622856/?ref=search&referral_code=null&referral_story_type=post&tracking=browse_serp%3A0afc0ed3-9f61-411d-b18f-0ff4bdd7aca0')
# html = driver.page_source
# soup = beauty(html, 'html.parser')
# link = soup.find_all('img', class_='xz74otr')[0].get('src')
# article = sub(r'&amp;', '&', link)







'''Após os imports e config'''
# print('[+] Starting the telegram client...')
# bot = Bot(config['TELEGRAM']['token'])
# print('[+] Telegram client started...')


# async def send_ad_telegram(filename, title, price, url):
#     await bot.send_photo(
#         chat_id=config['TELEGRAM']['chat_id'],
#         photo=open(
#             f'./tmp/{filename}', 'rb'
#         ),
#         parse_mode='HTML',
#         caption=f'🆕 <span class="tg-spoiler"><a href="{url}">{title}</a> <i>R$ {price}</i></span> 🆕'
#     )
#     remove(f'./tmp/{filename}')

# connection = connect(
#     host='localhost',
#     database=config['DATABASE']['DB_NAME'],
#     user='postgres',
#     password=config['DATABASE']['DB_PASS']
# )
# cursor = connection.cursor()




'''Após o processo ser startado'''
# data = []
# with open('items.json', 'r+') as file:
#     data = load(file)
#     for ad in data:
#         cursor.execute(
#             f"SELECT title FROM ad WHERE title = '{ad['title']}'"
#             f" AND url = '{ad['link']}'"
#         )
#         exist = cursor.fetchone()
#         if exist:
#             continue
#         else:
#             cursor.execute(
#                 f"INSERT INTO ad (title, price, url) VALUES "
#                 f"('{ad['title']}', '{ad['price']}', "
#                 f"'{ad['link']}')"
#             )
#             connection.commit()

#             img_data = get(ad['image_url']).content
#             filename = search(
#                 r'\/\d+.*\.(png|jpg)',
#                 ad['image_url']
#             )[0][1:]
#             with open(f'./tmp/{filename}', 'wb') as handler:
#                 handler.write(img_data)

#             global loop
#             loop = get_event_loop()
#             if not ad['old_price']:
#                 loop.run_until_complete(
#                     send_ad_telegram(
#                         filename,
#                         ad['title'],
#                         ad['price'],
#                         ad['link']
#                     )
#                 )
#                 loop.close()
#     file.truncate(0)
