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
WELCOME_MESSAGE = """杭州高端SPA会所欢迎您！优质服务等您体验🌸

地址： #西湖区 #滨江区 #拱墅区

🔥 服务特色：
• 专业技师团队，手法娴熟
• 环境优雅舒适，私密性强
• 正规经营，诚信服务

💆‍♀️ 多种项目可选，欢迎咨询了解！
无套路消费，明码标价，让您放心享受！"""

# 图片文件夹路径
IMAGES_FOLDER = "images"

# 最大图片数量
MAX_IMAGES = 10
