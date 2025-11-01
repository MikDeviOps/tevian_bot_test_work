import logging
from aiogram import Router, types
from services.tevian_api import TevianAPI
from keyboards.main import get_main_keyboard
from keyboards.inline import get_buckets_inline_keyboard

router = Router()
api = TevianAPI()
logger = logging.getLogger(__name__)

@router.message(lambda message: message.text == "Добавить лицо в картотеку")
async def add_face_handler(message: types.Message):
    keyboard = get_buckets_inline_keyboard("add_face")
    if keyboard:
        await message.answer(
            "Выберите картотеку для добавления лица:",
            reply_markup=keyboard
        )
    else:
        await message.answer("Нет доступных картотек. Сначала создайте картотеку.", reply_markup=get_main_keyboard())

@router.message(lambda message: message.text == "Удалить лицо из картотеки")
async def delete_face_handler(message: types.Message):
    keyboard = get_buckets_inline_keyboard("delete_face")
    if keyboard:
        await message.answer(
            "Выберите картотеку для удаления лица:",
            reply_markup=keyboard
        )
    else:
        await message.answer("Нет доступных картотек.", reply_markup=get_main_keyboard())