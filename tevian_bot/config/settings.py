import os
from dotenv import load_dotenv

load_dotenv()

# Tevian API configuration
TEVIAN_USERNAME = os.getenv('TEVIAN_USERNAME')
TEVIAN_PASSWORD = os.getenv('TEVIAN_PASSWORD')
TEVIAN_BASE_URL = os.getenv('TEVIAN_BASE_URL', 'https://presaletest.tevian.ai')
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Bot settings
DEFAULT_THRESHOLD = 0.9
DEFAULT_LIMIT = 10
REQUEST_TIMEOUT = 30

def validate_config():
    """Проверка обязательных переменных окружения"""
    required_vars = {
        'TEVIAN_USERNAME': TEVIAN_USERNAME,
        'TEVIAN_PASSWORD': TEVIAN_PASSWORD,
        'BOT_TOKEN': BOT_TOKEN
    }
    
    missing_vars = [var for var, value in required_vars.items() if not value]
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    return True