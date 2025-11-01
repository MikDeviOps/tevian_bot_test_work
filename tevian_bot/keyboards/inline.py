from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from services.tevian_api import TevianAPI

api = TevianAPI()

def create_bucket_button(bucket, action_type):
    """Создание кнопки для картотеки"""
    bucket_name = bucket['bucket_name']
    num_records = bucket.get('num_records', 0)
    button_text = f"{bucket_name} ({num_records} лиц)"
    callback_data = f"{action_type}:{bucket_name}"
    return InlineKeyboardButton(text=button_text, callback_data=callback_data)

def create_face_button(face, bucket_name, action_type):
    """Создание кнопки для лица"""
    face_id = face['face_id']
    identity = face.get('identity', 'Без имени')
    button_text = f"{identity} (ID: {face_id})"
    callback_data = f"{action_type}|{bucket_name}|{face_id}"
    return InlineKeyboardButton(text=button_text, callback_data=callback_data)

def get_buckets_inline_keyboard(action_type: str):
    response = api.get_buckets()
    if response.status_code != 200:
        return None
        
    buckets = response.json().get('data', [])
    if not buckets:
        return None
    
    keyboard = [
        [create_bucket_button(bucket, action_type)]
        for bucket in buckets
    ]
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_faces_inline_keyboard(bucket_name: str, action_type: str):
    faces = api.get_all_faces_from_bucket(bucket_name)
    if faces:
        keyboard = [
            [create_face_button(face, bucket_name, action_type)]
            for face in faces
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)
    else:
        keyboard = [[InlineKeyboardButton(text="В картотеке нет лиц", callback_data="no_faces")]]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_confirmation_keyboard(bucket_name: str, face_id: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Да, удалить", callback_data=f"execute_delete_face|{bucket_name}|{face_id}"),
            InlineKeyboardButton(text="Отмена", callback_data="cancel_delete")
        ]
    ])