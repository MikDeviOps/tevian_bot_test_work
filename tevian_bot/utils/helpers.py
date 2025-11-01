import logging
from aiogram import types
from services.tevian_api import TevianAPI
from keyboards.main import get_main_keyboard
from states.user_states import user_state_manager

logger = logging.getLogger(__name__)
api = TevianAPI()

async def download_media_content(message, bot):
    """Универсальная загрузка медиа-контента"""
    try:
        if message.photo:
            file = await bot.get_file(message.photo[-1].file_id)
        elif message.document:
            file = await bot.get_file(message.document.file_id)
        else:
            return None
            
        file_bytes = await bot.download_file(file.file_path)
        return file_bytes.read()
        
    except Exception as e:
        logger.error(f"Error downloading media: {e}")
        raise

async def process_media_message(message: types.Message, state, bot, operation_type: str):
    """Обработка медиа-сообщений для добавления лица"""
    user_id = message.from_user.id
    processing_text = "Обрабатываю фото..." if operation_type == "photo" else "Обрабатываю файл..."
    
    await message.answer(processing_text)
    
    try:
        image_data = await download_media_content(message, bot)
        if not image_data:
            raise ValueError("Не удалось загрузить изображение")
        
        bucket_name = state.bucket_name
        face_name = state.face_name
        
        response = api.add_face_to_bucket(bucket_name, face_name, image_data)
        await process_tevian_response(message, response, bucket_name, face_name)
    
    except Exception as e:
        logger.error(f"Error processing {operation_type}: {e}", exc_info=True)
        await message.answer(f"Произошла ошибка: {str(e)}", reply_markup=get_main_keyboard())
    
    finally:
        user_state_manager.clear_state(user_id)

async def process_photo_message(message: types.Message, state, bot):
    """Обработка фото для добавления лица"""
    await process_media_message(message, state, bot, "photo")

async def process_document_message(message: types.Message, state, bot):
    """Обработка документа для добавления лица"""
    await process_media_message(message, state, bot, "document")

async def process_search_media(message: types.Message, bot, media_type: str):
    """Обработка медиа для поиска"""
    user_id = message.from_user.id
    
    try:
        image_data = await download_media_content(message, bot)
        if not image_data:
            raise ValueError("Не удалось загрузить изображение")
        
        response = api.search_by_photo(image_data)
        
        if response.status_code == 200:
            result = response.json()
            await display_photo_search_results(message, result)
        else:
            error_msg = f"Ошибка поиска: {response.status_code}"
            if response.text:
                error_msg += f"\n{response.text}"
            await message.answer(error_msg, reply_markup=get_main_keyboard())
    
    except Exception as e:
        logger.error(f"Error processing search {media_type}: {e}", exc_info=True)
        await message.answer(f"Произошла ошибка: {str(e)}", reply_markup=get_main_keyboard())
    
    finally:
        user_state_manager.clear_state(user_id)

async def process_search_photo_message(message: types.Message, bot):
    """Обработка фото для поиска"""
    await process_search_media(message, bot, "photo")

async def process_search_document_message(message: types.Message, bot):
    """Обработка документа для поиска"""
    await process_search_media(message, bot, "document")

async def process_tevian_response(message: types.Message, response, bucket_name: str, face_name: str):
    """Обработка ответа от Tevian API"""
    if response.status_code == 200:
        result = response.json()
        num_faces = result.get('num_faces', 0)
        faces = result.get('faces', [])
        
        if num_faces > 0 and faces:
            face_info = faces[0]
            face_id = face_info.get('face_id')
            
            await message.answer(
                f"Лицо успешно добавлено!\n"
                f"Картотека: {bucket_name}\n"
                f"Имя: {face_name}\n"
                f"ID лица: {face_id}\n"
                f"Обнаружено лиц: {num_faces}",
                reply_markup=get_main_keyboard()
            )
        else:
            await message.answer(
                "Лицо не обнаружено на изображении.",
                reply_markup=get_main_keyboard()
            )
    else:
        await message.answer(
            f"Ошибка при добавлении лица: {response.text}",
            reply_markup=get_main_keyboard()
        )

async def display_search_results(message: types.Message, result, search_type: str):
    """Отображение результатов поиска похожих лиц"""
    history_matches = result.get('history_matches', [])
    bucket_matches = result.get('bucket_matches', [])
    
    response_text = f"Результаты поиска {search_type}:\n\n"
    
    if history_matches:
        response_text += "Совпадения в истории:\n"
        for i, match in enumerate(history_matches[:5]):
            camera_name = match.get('camera_name', 'Неизвестная камера')
            similarity = match.get('similarity', 0)
            timestamp = match.get('timestamp', '')
            response_text += f"{i+1}. Камера: {camera_name}\n"
            response_text += f"   Сходство: {similarity:.2%}\n"
            if timestamp:
                response_text += f"   Время: {timestamp}\n"
            response_text += "\n"
    else:
        response_text += "Совпадений в истории не найдено\n\n"
    
    if bucket_matches:
        response_text += "Совпадения в картотеках:\n"
        for i, match in enumerate(bucket_matches[:5]):
            bucket_name = match.get('bucket_name', '')
            identity = match.get('identity', 'Без имени')
            similarity = match.get('similarity', 0)
            response_text += f"{i+1}. {identity}\n"
            response_text += f"   Картотека: {bucket_name}\n"
            response_text += f"   Сходство: {similarity:.2%}\n\n"
    else:
        response_text += "Совпадений в картотеках не найдено\n"
    
    total_history = result.get('num_history_matches', 0)
    total_bucket = result.get('num_bucket_matches', 0)
    response_text += f"\nВсего найдено: {total_history} в истории, {total_bucket} в картотеках"
    
    await message.answer(response_text, reply_markup=get_main_keyboard())

async def display_photo_search_results(message: types.Message, result):
    """Отображение результатов поиска по фото"""
    faces = result.get('faces', [])
    
    if not faces:
        await message.answer("На фото не обнаружено лиц или не найдено совпадений.", reply_markup=get_main_keyboard())
        return
    
    response_text = "Результаты поиска по фото:\n\n"
    
    for i, face in enumerate(faces[:3]):
        features = face.get('features', {})
        age = features.get('age', 'не определен')
        gender = features.get('gender', 'не определен')
        glasses = features.get('glasses', 'нет')
        facial_hair = features.get('facial_hair', 'нет')
        
        response_text += f"Лицо {i+1}:\n"
        response_text += f"   Возраст: {age}\n"
        response_text += f"   Пол: {gender}\n"
        response_text += f"   Очки: {glasses}\n"
        response_text += f"   Борода/усы: {facial_hair}\n\n"
        
        history_matches = face.get('history_matches', [])
        if history_matches:
            response_text += f"   Совпадения в истории: {len(history_matches)}\n"
            for match in history_matches[:2]:
                camera_name = match.get('camera_name', 'Неизвестная камера')
                similarity = match.get('similarity', 0)
                response_text += f"      • {camera_name} ({similarity:.2%})\n"
        
        bucket_matches = face.get('bucket_matches', [])
        if bucket_matches:
            response_text += f"   Совпадения в картотеках: {len(bucket_matches)}\n"
            for match in bucket_matches[:2]:
                identity = match.get('identity', 'Без имени')
                similarity = match.get('similarity', 0)
                response_text += f"      • {identity} ({similarity:.2%})\n"
        
        response_text += "\n"
    
    total_faces = result.get('num_faces', 0)
    response_text += f"Всего обнаружено лиц на фото: {total_faces}"
    
    await message.answer(response_text, reply_markup=get_main_keyboard())