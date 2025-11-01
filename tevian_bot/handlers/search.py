import logging
from aiogram import Router, types
from services.tevian_api import TevianAPI
from keyboards.main import get_main_keyboard
from keyboards.inline import get_buckets_inline_keyboard
from states.user_states import user_state_manager

router = Router()
api = TevianAPI()
logger = logging.getLogger(__name__)

@router.message(lambda message: message.text == "Найти похожие лица")
async def find_similar_faces_handler(message: types.Message):
    keyboard = get_buckets_inline_keyboard("find_similar")
    if keyboard:
        await message.answer(
            "Выберите картотеку для поиска похожих лиц:",
            reply_markup=keyboard
        )
    else:
        await message.answer("Нет доступных картотек.", reply_markup=get_main_keyboard())

@router.message(lambda message: message.text == "Поиск по фото")
async def search_by_photo_handler(message: types.Message):
    user_state_manager.set_state(message.from_user.id, 'awaiting_search_photo')
    await message.answer(
        "Отправьте фото для поиска в базе:\n\n"
        "Бот найдет похожие лица в картотеках.",
        reply_markup=types.ReplyKeyboardRemove()
    )