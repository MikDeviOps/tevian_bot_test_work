
![Logo](https://radika1.link/2025/11/01/1231231a6caa54f854a787.png)


<p align="center">
  # Tevian Face Recognition Telegram Bot
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12+-blue?style=for-the-badge&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Aiogram-3.x-green?style=for-the-badge" alt="Aiogram">
</p>

Удобный Telegram-бот для взаимодействия с системой распознавания лиц **Tevian AI**. Позволяет управлять картотеками, добавлять и удалять лица, а также выполнять поиск похожих лиц или загружать фото для мгновенного анализа — всё прямо из чата.


<details>

<summary>Структура проекта</summary>

```
tevian-bot/
├── 📂 config/                    # Конфигурация приложения
│   ├── __init__.py
│   └── settings.py               # Настройки, переменные окружения, валидация
│
├── 📂 handlers/                  # Обработчики Telegram сообщений
│   ├── __init__.py
│   ├── start.py                  # Обработчик команды /start
│   ├── buckets.py                # Управление картотеками (создание, просмотр, удаление)
│   ├── faces.py                  # Управление лицами (добавление, удаление)
│   ├── search.py                 # Поисковые функции (похожие лица, поиск по фото)
│   ├── messages.py               # Обработка текстовых сообщений и состояний
│   └── callbacks.py              # Обработка инлайн-кнопок (все callback_query)
│
├── 📂 services/                  # Бизнес-логика и внешние API
│   ├── __init__.py
│   └── tevian_api.py             # Клиент для Tevian API (8 основных методов)
│       ├── create_bucket()       # POST /api/bucket/{name}
│       ├── get_buckets()         # GET /api/v1/buckets
│       ├── delete_bucket()       # DELETE /api/bucket/{name}
│       ├── add_face_to_bucket()  # POST /api/bucket_all_faces
│       ├── get_all_faces_from_bucket()  # GET /api/v1/buckets/face/list
│       ├── delete_face_from_bucket()    # DELETE /api/bucket/{name}/{face_id}
│       ├── search_by_photo()     # POST /api/photo/matches
│       └── search_similar_faces() # GET /api/bucket/{name}/{face_id}/matches
│
├── 📂 keyboards/                 # Клавиатуры и интерфейс бота
│   ├── __init__.py
│   ├── main.py                   # Главное меню бота (ReplyKeyboardMarkup)
│   └── inline.py                 # Инлайн-клавиатуры (кнопки картотек, лиц, подтверждения)
│       ├── get_buckets_inline_keyboard()
│       ├── get_faces_inline_keyboard()
│       └── get_confirmation_keyboard()
│
├── 📂 states/                    # Управление состояниями пользователей
│   ├── __init__.py
│   └── user_states.py            # Менеджер состояний с TTL
│       ├── UserState dataclass
│       └── UserStateManager
│
├── 📂 utils/                     # Вспомогательные функции
│   ├── __init__.py
│   └── helpers.py                # Утилиты для обработки медиа и отображения результатов
│       ├── process_photo_message()
│       ├── process_document_message()
│       ├── process_search_photo_message()
│       ├── process_search_document_message()
│       ├── process_tevian_response()
│       ├── display_search_results()
│       ├── display_photo_search_results()
│       └── download_media_content()
│
├── 📄 .env                       # Переменные окружения (не в git)
│   ├── TEVIAN_USERNAME
│   ├── TEVIAN_PASSWORD
│   ├── TEVIAN_BASE_URL
│   └── BOT_TOKEN
│
├── 📄 .env.example               # Шаблон .env файла
├── 📄 .dockerignore              # Исключения для Docker
├── 📄 .gitignore                 # Исключения для Git
├── 📄 Dockerfile                 # Конфигурация Docker
├── 📄 docker-compose.yml         # Docker Compose конфигурация
├── 📄 requirements.txt           # Зависимости Python
├── 📄 main.py                    # Точка входа приложения
└── 📄 README.md                  # Документация проекта
```

</details>

## Описание

### Для пользователей:
<details>
<summary>Информация</summary><br>
  
> Управление базами лиц через Telegram

> Мгновенный поиск по фото в картотеках

> Быстрое добавление новых лиц в систему

> Поиск похожих лиц в архиве камер
</details>

### Для бизнеса:
<details>
<summary>Информация</summary><br>

> Автоматизация безопасности - вместо ручного просмотра

> Мобильный доступ к системе распознавания

> Оперативное реагирование - поиск за секунды

> Цифровизация процессов идентификации
</details>

### Технические:
<details>
<summary>Информация</summary><br>

> Демо-стенд Tevian API

> Образец архитектуры Telegram бота

> Готовое решение для интеграции распознавания лиц
</details>


## Установка

### Предварительные требования

* Python 3.11+

* Docker и Docker Compose

* Аккаунт в Tevian AI

* Telegram Bot Token от @BotFather

* To deploy this project run

#### Клонирование репозитория:
```bash
git clone https://github.com/your-username/tevian_bot_test_work.git
cd tevian-face-bot
```

#### Настройка окружения:

Создайте файл .env на основе примера:
```bash
cp .env.example .env
```

#### Заполните .env файл:
```bash
# Tevian API credentials
TEVIAN_USERNAME=your_username
TEVIAN_PASSWORD=your_password
TEVIAN_BASE_URL=https://presaletest.tevian.ai

# Telegram Bot
BOT_TOKEN=your_telegram_bot_token
```

#### Запуск Docker:
```bash
# Сборка и запуск
docker-compose up -d --build

# Просмотр логов
docker-compose logs -f

# Остановка
docker-compose down
```

## Использование

* Начните с команды /start

* Используйте кнопки меню для навигации

* Создайте картотеку для организации лиц

* Добавляйте лица с фото и описанием

* Используйте поиск для нахождения совпадений


## Методы API

| Метод  | Endpoint | HTTP Method | Назначение  |
| ------------- | ------------- | ------------- | ------------- |
| create_bucket()  | /api/bucket/{name}  |  POST| Создание картотеки
| get_buckets()  | 	/api/v1/buckets  |  GET| Получение списка картотек
| delete_bucket() | /api/bucket/{name}  |  DELETE| Удаление картотеки
| add_face_to_bucket()  | /api/bucket_all_faces  |  POST| Добавление лица
| get_all_faces_from_bucket() | 	/api/v1/buckets/face/list  |  GET| Получение лиц из картотеки
| delete_face_from_bucket()  | /api/bucket/{name}/{face_id}  |  DELETE| Удаление лица
| search_by_photo()  | /api/photo/matches  |  POST| Поиск по фото
| search_similar_faces()  | /api/bucket/{name}/{face_id}/matches  |  GET| Поиск похожих лиц

## Demo

[Призентация работы приложения](https://disk.yandex.ru/client/disk?idApp=client&dialog=slider&idDialog=%2Fdisk%2Fvideo_2025-11-01_13-21-21.mp4)
