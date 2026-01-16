"""
Configuration loader for the spam removal bot
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot configuration
BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN muhit o'zgaruvchisi .env faylda belgilanmagan!")

# Spam detection settings
MAX_EMOJIS = int(os.getenv('MAX_EMOJIS', '5'))
MAX_MESSAGE_LENGTH = int(os.getenv('MAX_MESSAGE_LENGTH', '4096'))

# Spam detection patterns
SPAM_KEYWORDS = [
    # Uzbek promotional keywords
    'chegirma', 'aksiya', 'tekin', 'bepul', 'narxi', 'sotiladi',
    'buyurtma', 'zakaz', 'reklama', 'kanal', 'guruh', 'obuna',
    'murojaat', 'aloqa', 'bog\'lanish', 'xizmat', 'ishga', 'vakansiya',
    
    # Russian promotional keywords
    'скидка', 'акция', 'бесплатно', 'заказ', 'реклама', 'канал',
    'группа', 'подписка', 'цена', 'продается', 'работа', 'вакансия',
    
    # Common promotional phrases
    'join', 'subscribe', 'follow', 'click here', 'buy now',
    'limited offer', 'special price', 'discount', 'manager',
    'admin', 'contact', 'earn', 'money', 'crypto',
]

# URL patterns to detect
URL_PATTERNS = [
    'http://',
    'https://',
    't.me/',
    'telegram.me/',
    'www.',
    '.com',
    '.net',
    '.org',
    '.ru',
    '.uz',
]

# Phone number patterns (simple detection)
PHONE_PATTERNS = [
    '+998',  # Uzbekistan
    '+7',    # Russia/Kazakhstan
]
