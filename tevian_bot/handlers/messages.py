import logging
from aiogram import Router, types
from services.tevian_api import TevianAPI
from keyboards.main import get_main_keyboard
from states.user_states import user_state_manager
from utils.helpers import (
    process_tevian_response,
    process_photo_message,
    process_document_message,
    process_search_photo_message,
    process_search_document_message
)

router = Router()
api = TevianAPI()
logger = logging.getLogger(__name__)

@router.message()
async def handle_all_messages(message: types.Message):
    user_id = message.from_user.id
    state = user_state_manager.get_state(user_id)
    
    if state and state.state == 'awaiting_bucket_name':
        bucket_name = f"presale02:{message.text}"
        response = api.create_bucket(bucket_name)
        
        if response.status_code == 200:
            await message.answer(f"Картотека создана: {bucket_name}", reply_markup=get_main_keyboard())
        else:
            await message.answer(f"Ошибка создания: {response.text}", reply_markup=get_main_keyboard())
        
        user_state_manager.clear_state(user_id)
    
    elif state and state.state == 'awaiting_face_name':
        face_name = message.text
        user_state_manager.set_state(
            user_id, 
            'awaiting_face_photo', 
            state.bucket_name, 
            face_name
        )
        await message.answer(
            f"Имя лица: {face_name}\n"
            f"Картотека: {state.bucket_name}\n\n"
            "Отправьте фото лица:"
        )
    
    elif state and state.state == 'awaiting_face_photo':
        if message.photo:
            await process_photo_message(message, state, message.bot)
        elif message.document and message.document.mime_type and message.document.mime_type.startswith('image/'):
            await process_document_message(message, state, message.bot)
        else:
            await message.answer("Пожалуйста, отправьте изображение с лицом.", reply_markup=get_main_keyboard())
            user_state_manager.clear_state(user_id)
    
    elif state and state.state == 'awaiting_search_photo':
        if message.photo:
            await process_search_photo_message(message, message.bot)
        elif message.document and message.document.mime_type and message.document.mime_type.startswith('image/'):
            await process_search_document_message(message, message.bot)
        else:
            await message.answer("Пожалуйста, отправьте изображение для поиска.", reply_markup=get_main_keyboard())
            user_state_manager.clear_state(user_id)