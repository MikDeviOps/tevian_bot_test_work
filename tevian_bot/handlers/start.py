from aiogram import Router, types
from aiogram.filters import Command
from keyboards.main import get_main_keyboard

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    caption_text = (
        "В рамках тестового задания в данном боте обрабатываются следующие методы для web-интерфейса Tevian - https://presaletest.tevian.ai\n\n"
        "Реализованные методы - согласно ТЗ:\n"
        "- Создание картотеки и добавления в нее нескольких лиц\n"
        "- Поиск похожих лиц в картотеках\n"
        "- Удаление лица из картотеки\n"
        "- Удаление самой картотеки\n\n"
        "Выберите действие:"
    )
    
    await message.answer_photo(
        photo="https://cdn.dprofile.ru/public/1871/107122/e93997217063299.678a3ed69756c.png",
        caption=caption_text,
        reply_markup=get_main_keyboard()
    )