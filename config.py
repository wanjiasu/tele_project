import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# Telegram Bot Token
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# 允许的群组ID列表（可选）
ALLOWED_CHAT_IDS = []
if os.getenv('ALLOWED_CHAT_IDS'):
    ALLOWED_CHAT_IDS = [int(chat_id.strip()) for chat_id in os.getenv('ALLOWED_CHAT_IDS').split(',')]

# 欢迎消息配置
WELCOME_MESSAGE = """长沙摸摸看高质量在发一组照片！

地址： #五一广场 #解放西 #芙蓉广场

无任何套路、无隐形消费、无强制消费、靠谱诚信经营

不要问这个在不在、那个在不在！直接过来海选！海选！海选‼️"""

# 图片文件夹路径
IMAGES_FOLDER = "images"

# 最大图片数量
MAX_IMAGES = 10
