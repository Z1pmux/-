import os
import asyncio
import random
from PIL import Image, ImageDraw, ImageFont
from telethon import TelegramClient
from telethon.tl.functions.photos import UploadProfilePhotoRequest

# script by @x0603 tg 
def add_watermark(image_path, text="script by @x0603"):
    try:
        with Image.open(image_path).convert("RGBA") as img:
            txt = Image.new('RGBA', img.size, (255, 255, 255, 0))
            draw = ImageDraw.Draw(txt)

            # script by @x0603 tg
            font = ImageFont.load_default()

            # script by @x0603 tg
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]

            # script by @x0603 tg
            position = (10, img.height - text_height - 10)

            # script by @x0603 tg
            draw.text(position, text, font=font, fill=(255, 255, 255))  # script by @x0603 tg

            watermarked = Image.alpha_composite(img, txt)
            watermarked = watermarked.convert("RGB")  # script by @x0603 tg
            watermarked.save(image_path)
            print(f"Текст '{text}' добавлен на изображение.")
    except Exception as e:
        print(f"Ошибка при добавлении текста: {e}")

async def set_profile_picture(client, image_path):
    # script by @x0603 tg
    if not os.path.exists(image_path):
        print(f"Файл {image_path} не найден.")
        return

    # script by @x0603 tg
    if not image_path.lower().endswith(('.jpg', '.png')):
        print(f"Неподдерживаемый формат изображения: {image_path}")
        return

    # script by @x0603 tg
    add_watermark(image_path)

    # script by @x0603 tg
    try:
        with Image.open(image_path) as img:
            print(f"Открыто изображение: {image_path}")
            print(f"Исходное разрешение: {img.size}")
            img = img.resize((512, 512))  # script by @x0603 tg
            img.save(image_path)  # script by @x0603 tg
            print(f"Размер изображения изменен на: {img.size}")
    except Exception as e:
        print(f"Ошибка при изменении размера изображения: {e}")
        return

    async def upload_profile():
        try:
            file = await client.upload_file(image_path)
            await client(UploadProfilePhotoRequest(file=file))
            print(f'Установлено новое изображение профиля script by @x0603')
        except Exception as e:
            print(f'Ошибка при установке изображения: {e}')

    # script by @x0603 tg
    i = 0
    while True:
        await upload_profile()
        i += 1
        print(f'Установлено {i}-е изображение script by @x0603')

        # script by @x0603 tg
        delay = random.randint(5, 15)  # script by @x0603 tg
        print(f'Ожидание {delay} секунд перед следующей установкой... script by @x0603')
        await asyncio.sleep(delay)

async def main(api_id, api_hash, phone_number, folder_path):
    # script by @x0603 tg
    client = TelegramClient('session_name', api_id, api_hash)
    await client.start(phone=phone_number)

    # script by @x0603 tg
    image_path = os.path.join(folder_path, 'test.jpg')  # script by @x0603 tg

    # script by @x0603 tgо
    await set_profile_picture(client, image_path)

if __name__ == "__main__":
    # script by @x0603 tg
    api_id = int(input("Введите API ID: "))
    api_hash = input("Введите API Hash: ")
    phone_number = input("Введите номер телефона: ")
    folder_path = input("Введите путь к папке с изображением: ")

    # script by @x0603 tg
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(api_id, api_hash, phone_number, folder_path))