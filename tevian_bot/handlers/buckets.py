import logging
from aiogram import Router, types
from services.tevian_api import TevianAPI
from keyboards.main import get_main_keyboard
from keyboards.inline import get_buckets_inline_keyboard
from states.user_states import user_state_manager

router = Router()
api = TevianAPI()
logger = logging.getLogger(__name__)

@router.message(lambda message: message.text == "Создать картотеку")
async def create_bucket_handler(message: types.Message):
    user_state_manager.set_state(message.from_user.id, 'awaiting_bucket_name')
    await message.answer(
        "Введите название картотеки (только имя, без presale02:):",
        reply_markup=types.ReplyKeyboardRemove()
    )

@router.message(lambda message: message.text == "Проверить картотеки")
async def check_buckets_handler(message: types.Message):
    response = api.get_buckets()
    if response.status_code == 200:
        data = response.json()
        buckets = data.get('data', [])
        if buckets:
            bucket_list = "\n".join([f"- {b['bucket_name']} ({b.get('num_records', 0)} лиц)" for b in buckets])
            await message.answer(f"Картотеки:\n{bucket_list}")
        else:
            await message.answer("Картотек нет")
    else:
        await message.answer(f"Ошибка: {response.text}")

@router.message(lambda message: message.text == "Удалить картотеку")
async def delete_bucket_handler(message: types.Message):
    keyboard = get_buckets_inline_keyboard("delete_bucket")
    if keyboard:
        await message.answer(
            "Выберите картотеку для удаления:",
            reply_markup=keyboard
        )
    else:
        await message.answer("Нет картотек для удаления")