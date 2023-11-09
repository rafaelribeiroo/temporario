from telegram import Bot, InputMediaPhoto
from decouple import config as decouple
from asyncio import get_event_loop
from instagrapi import Client
from os import remove, mkdir
from psycopg2 import connect
from re import sub, search
from os.path import isdir
from time import sleep
from instagrapi.exceptions import (
    BadCredentials,
    ProxyAddressIsBlocked,
    BadPassword
)

# ### Instagram API setup ###
ACCOUNT_USERNAME = decouple('username')
ACCOUNT_PASSWORD = decouple('password')
ACCOUNT_SESSIONID = decouple('session_id')
feed_wait_time = int(decouple('feed_wait_time'))
amount = int(decouple('amount'))

print('[+] Starting the instagram API...')
api = Client()
try:
    api.login(ACCOUNT_USERNAME, ACCOUNT_PASSWORD, relogin=True)
except (ProxyAddressIsBlocked, BadPassword, BadCredentials):
    api.login_by_sessionid(ACCOUNT_SESSIONID)
print('[+] API started...')

# ### Telegram Client Setup ###
BOT_TOKEN = decouple('token')
target_group = decouple('telegram_destination_group_id')

print('[+] Starting the telegram client...')
bot = Bot(BOT_TOKEN)
print('[+] Telegram client started...')

# ### Database Setup ###
DB_NAME = decouple('db_name')
DB_PASS = decouple('db_pass')

connection = connect(
    host='localhost',
    database=DB_NAME,
    user='postgres',
    password=DB_PASS
)
cursor = connection.cursor()


async def send_photo_telegram(filename, clean_caption):
    await bot.send_photo(
        chat_id='-1001746032698',
        photo=open(f'./tmp/{filename}', 'rb'),
        caption=f'{clean_caption}'
    )
    remove(f'./tmp/{filename}')


async def send_video_telegram(filename, clean_caption):
    await bot.send_video(
        chat_id='-1001746032698',
        video=open(f'./tmp/{filename}', 'rb'),
        caption=f'{clean_caption}',
        has_spoiler=True
    )
    remove(f'./tmp/{filename}')


async def send_multiple_telegram(filenames, clean_caption):
    await bot.send_media_group(
        chat_id='-1001746032698',
        media=[
            InputMediaPhoto(open(f'./tmp/{file}', 'rb')) for file in filenames
        ],
        caption=f'{clean_caption}'
    )
    [remove(f'./tmp/{file}') for file in filenames]


def main(requests={}):

    for username, amount in requests.items():

        user_id = api.user_id_from_username(username)
        pinned_medias = api.user_pinned_medias(user_id)
        if pinned_medias:
            amount += len(pinned_medias)
        # from pdb import set_trace; set_trace()
        feed = api.user_medias(user_id, amount)

        for post in feed:

            if pinned_medias:
                for item in pinned_medias:
                    if post.code == item.code:
                        continue
                    else:
                        pass

            cursor.execute(
                f"SELECT codigo FROM post WHERE codigo = '{post.code}' AND "
                f"user_insta = '{username}'"
            )
            data = cursor.fetchone()
            # from pdb import set_trace; set_trace()
            if data:
                continue
            else:
                cursor.execute(
                    f"INSERT INTO post (codigo, user_insta) "
                    f"VALUES ('{post.code}', '{username}')"
                )
                connection.commit()

            # full filename
            # search(r'\/\d+.*\.(png|jpg)', post.thumbnail_url[0:])[0][1:]

            # caroussel/multiple files
            if post.media_type == 8:
                filenames = []
                for item in post.resources:
                    extension = search(r'(png|jpg|gif)', item.thumbnail_url)[0]
                    # Get user post due to collab posts
                    # import pdb; pdb.set_trace()
                    # if item.user:
                    try:
                        filenames.append(
                            f"{item.user.username}_{item.pk}.{extension}"
                        )
                    except AttributeError:
                        filenames.append(
                            f"{username}_{item.pk}.{extension}"
                        )
            else:
                extension = search(r'(png|jpg|gif)', post.thumbnail_url)[0]
                # filename = f'./tmp/{username}_{post.pk}.{extension}'
                # from pdb import set_trace; set_trace()
                # if post.user:
                try:
                    filename = f'{post.user.username}_{post.pk}.{extension}'
                except AttributeError:
                    filename = f'{username}_{post.pk}.{extension}'

            clean_caption = sub(
                "(\n[T-t]hanks.*|\n#.*)",
                '',
                post.caption_text
            )

            loop = get_event_loop()
            if post.media_type == 1:
                # Photo
                api.photo_download(post.pk, './tmp/')
                loop.run_until_complete(
                    send_photo_telegram(filename, clean_caption)
                )
            elif post.media_type == 2 and post.product_type == "feed":
                # Video
                api.video_download(post.pk, './tmp/')
                loop.run_until_complete(
                    send_video_telegram(filename, clean_caption)
                )
            elif post.media_type == 2 and post.product_type == "igtv":
                # IGTV
                api.video_download(post.pk, './tmp/')
                loop.run_until_complete(
                    send_video_telegram(filename, clean_caption)
                )
            elif post.media_type == 2 and post.product_type == "clips":
                # Reels
                api.video_download(post.pk, './tmp/')
                loop.run_until_complete(
                    send_video_telegram(filename, clean_caption)
                )
            elif post.media_type == 8:
                # Album
                api.album_download(post.pk, './tmp/')
                loop.run_until_complete(
                    send_multiple_telegram(filenames, clean_caption)
                )
    # loop.close()
    return


if __name__ == "__main__":
    # username = input("Enter username: ")
    # while True:
    #     amount = input("How many posts to process (default: 5)? ").strip()
    #     if amount == "":
    #         amount = "5"
    #     if amount.isdigit():
    #         break
    if not isdir('./tmp'):
        mkdir('./tmp')

    # print("(+) Checking internet speed")
    # if internet():
    while True:
        main({'popnewws_': amount})
        # 'thescarletjoker': amount
        sleep(feed_wait_time)
    cursor.close()
    connection.close()
