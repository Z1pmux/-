Зашифруй этот скрипт и отправь мне его файлом 

import os
import asyncio
import random
from PIL import Image, ImageDraw, ImageFont
from telethon import TelegramClient
from telethon.tl.functions.photos import UploadProfilePhotoRequest

# Функция для добавления текста на изображение
def add_watermark(image_path, text="script by @x0603"):
    """Добавляет непрозрачный текст на изображение."""
    try:
        with Image.open(image_path).convert("RGBA") as img:
            txt = Image.new('RGBA', img.size, (255, 255, 255, 0))
            draw = ImageDraw.Draw(txt)

            # Настройка шрифта и размера
            font = ImageFont.load_default()

            # Получение размеров текста с помощью textbbox
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]

            # Позиция текста в левом нижнем углу
            position = (10, img.height - text_height - 10)

            # Добавление непрозрачного белого текста
            draw.text(position, text, font=font, fill=(255, 255, 255))  # Белый текст без прозрачности

            watermarked = Image.alpha_composite(img, txt)
            watermarked = watermarked.convert("RGB")  # Преобразование обратно в RGB
            watermarked.save(image_path)
            print(f"Текст '{text}' добавлен на изображение.")
    except Exception as e:
        print(f"Ошибка при добавлении текста: {e}")

async def set_profile_picture(client, image_path):
    # Проверка на существование файла
    if not os.path.exists(image_path):
        print(f"Файл {image_path} не найден.")
        return

    # Проверка формата изображения
    if not image_path.lower().endswith(('.jpg', '.png')):
        print(f"Неподдерживаемый формат изображения: {image_path}")
        return

    # Добавляем водяной знак на изображение
    add_watermark(image_path)

    # Изменяем размер изображения до 512x512
    try:
        with Image.open(image_path) as img:
            print(f"Открыто изображение: {image_path}")
            print(f"Исходное разрешение: {img.size}")
            img = img.resize((512, 512))  # Изменяем размер изображения
            img.save(image_path)  # Сохраняем измененное изображение
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

    # Устанавливаем изображение бесконечное количество раз
    i = 0
    while True:
        await upload_profile()
        i += 1
        print(f'Установлено {i}-е изображение script by @x0603')

        # Динамическая задержка с увеличением времени и рандомизацией
        delay = random.randint(5, 15)  # Рандомная задержка между 5 и 15 секундами
        print(f'Ожидание {delay} секунд перед следующей установкой... script by @x0603')
        await asyncio.sleep(delay)

async def main(api_id, api_hash, phone_number, folder_path):
    # Стартуем клиента и авторизуемся
    client = TelegramClient('session_name', api_id, api_hash)
    await client.start(phone=phone_number)

    # Путь к изображению
    image_path = os.path.join(folder_path, 'test.jpg')  # Путь к вашему изображению в указанной папке

    # Устанавливаем изображение как аватарку бесконечно
    await set_profile_picture(client, image_path)

if __name__ == "__main__":
    # Ввод данных
    api_id = int(input("Введите API ID: "))
    api_hash = input("Введите API Hash: ")
    phone_number = input("Введите номер телефона: ")
    folder_path = input("Введите путь к папке с изображением: ")

    # Запуск клиента
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(api_id, api_hash, phone_number, folder_path))