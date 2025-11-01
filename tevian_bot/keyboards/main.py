from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Создать картотеку")],
            [KeyboardButton(text="Добавить лицо в картотеку")],
            [KeyboardButton(text="Найти похожие лица")],
            [KeyboardButton(text="Поиск по фото")],
            [KeyboardButton(text="Удалить лицо из картотеки")],
            [KeyboardButton(text="Проверить картотеки")],
            [KeyboardButton(text="Удалить картотеку")]
        ],
        resize_keyboard=True
    )
    return keyboard