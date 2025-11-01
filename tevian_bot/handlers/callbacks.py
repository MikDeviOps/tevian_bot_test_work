import logging
from aiogram import Router, types
from services.tevian_api import TevianAPI
from keyboards.main import get_main_keyboard
from keyboards.inline import get_faces_inline_keyboard, get_confirmation_keyboard
from states.user_states import user_state_manager
from utils.helpers import display_search_results, display_photo_search_results

router = Router()
api = TevianAPI()
logger = logging.getLogger(__name__)

@router.callback_query()
async def handle_inline_buttons(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    data = callback.data
    
    logger.info(f"Inline button pressed: {data} by user {user_id}")
    
    if data.startswith("add_face:"):
        bucket_name = data.replace("add_face:", "")
        user_state_manager.set_state(user_id, 'awaiting_face_name', bucket_name)
        
        await callback.message.edit_text(
            f"Выбрана картотека: {bucket_name}\n\n"
            "Введите имя для лица (ФИО или описание):"
        )
        await callback.answer()
    
    elif data.startswith("find_similar:"):
        bucket_name = data.replace("find_similar:", "")
        keyboard = get_faces_inline_keyboard(bucket_name, "search_face")
        
        if keyboard:
            await callback.message.edit_text(
                f"Выберите лицо для поиска похожих в картотеке {bucket_name}:",
                reply_markup=keyboard
            )
        else:
            await callback.message.edit_text(f"В картотеке {bucket_name} нет лиц для поиска.")
        await callback.answer()
    
    elif data.startswith("search_face|"):
        parts = data.split("|")
        if len(parts) >= 3:
            bucket_name = parts[1]
            face_id = parts[2]
            
            await callback.message.edit_text("Ищу похожие лица...")
            
            response = api.search_similar_faces(bucket_name, face_id)
            
            if response.status_code == 200:
                result = response.json()
                
                if not result.get('history_matches') and not result.get('bucket_matches'):
                    await callback.message.edit_text("Похожих лиц не найдено.")
                else:
                    await display_search_results(callback.message, result, "похожих лиц")
            else:
                error_msg = f"Ошибка поиска: {response.status_code}"
                if response.text:
                    error_msg += f"\n{response.text}"
                await callback.message.edit_text(error_msg)
        else:
            await callback.message.edit_text("Ошибка: неверный формат данных")
        
        await callback.answer()
    
    elif data.startswith("delete_face:"):
        bucket_name = data.replace("delete_face:", "")
        keyboard = get_faces_inline_keyboard(bucket_name, "confirm_delete_face")
        
        if keyboard:
            await callback.message.edit_text(
                f"Выберите лицо для удаления из картотеки {bucket_name}:",
                reply_markup=keyboard
            )
        else:
            await callback.message.edit_text(f"В картотеке {bucket_name} нет лиц для удаления.")
        await callback.answer()
    
    elif data.startswith("confirm_delete_face|"):
        parts = data.split("|")
        if len(parts) >= 3:
            bucket_name = parts[1]
            face_id = parts[2]
            
            keyboard = get_confirmation_keyboard(bucket_name, face_id)
            
            await callback.message.edit_text(
                f"Вы уверены, что хотите удалить лицо ID {face_id} из картотеки {bucket_name}?",
                reply_markup=keyboard
            )
        await callback.answer()
    
    elif data.startswith("execute_delete_face|"):
        parts = data.split("|")
        if len(parts) >= 3:
            bucket_name = parts[1]
            face_id = parts[2]
            
            logger.info(f"Attempting to delete face: bucket={bucket_name}, face_id={face_id}")
            
            response = api.delete_face_from_bucket(bucket_name, face_id)
            
            if response.status_code == 200:
                await callback.message.edit_text(f"Лицо ID {face_id} удалено из картотеки {bucket_name}")
            else:
                error_msg = f"Ошибка удаления: {response.status_code}"
                if response.text:
                    error_msg += f"\n{response.text}"
                await callback.message.edit_text(error_msg)
        else:
            await callback.message.edit_text("Ошибка: неверный формат данных для удаления")
        await callback.answer()
    
    elif data == "cancel_delete":
        await callback.message.edit_text("Удаление отменено.")
        await callback.answer()
    
    elif data.startswith("delete_bucket:"):
        bucket_name = data.replace("delete_bucket:", "")
        
        response = api.delete_bucket(bucket_name)
        
        if response.status_code == 200:
            await callback.message.edit_text(f"Картотека удалена: {bucket_name}")
        else:
            await callback.message.edit_text(f"Ошибка удаления: {response.text}")
        
        await callback.answer()
    
    elif data == "no_faces":
        await callback.answer("В картотеке нет лиц", show_alert=True)