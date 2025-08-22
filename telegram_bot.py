#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram群组欢迎机器人
当新用户加入群组时，自动发送包含图片集和欢迎文字的消息
"""

import os
import glob
import random
import logging
from typing import List
from telegram import Update, InputMediaPhoto
from telegram.ext import Application, ChatMemberHandler, CommandHandler, ContextTypes
from telegram.constants import ChatMemberStatus
from config import BOT_TOKEN, ALLOWED_CHAT_IDS, WELCOME_MESSAGE, IMAGES_FOLDER, MAX_IMAGES

# 设置日志
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class TelegramWelcomeBot:
    def __init__(self):
        if not BOT_TOKEN:
            raise ValueError("请在环境变量中设置 TELEGRAM_BOT_TOKEN")
        
        self.application = Application.builder().token(BOT_TOKEN).build()
        self._setup_handlers()

    def _setup_handlers(self):
        """设置消息处理器"""
        # 添加成员变化处理器
        self.application.add_handler(ChatMemberHandler(
            self.handle_chat_member_update,
            ChatMemberHandler.CHAT_MEMBER
        ))
        
        # 添加命令处理器
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("test_welcome", self.test_welcome_command))

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """处理 /start 命令"""
        await update.message.reply_text(
            "欢迎使用Telegram群组欢迎机器人！\n\n"
            "功能：\n"
            "• 自动检测新用户加入群组\n"
            "• 发送包含图片集的欢迎消息\n\n"
            "命令：\n"
            "/help - 显示帮助信息\n"
            "/test_welcome - 测试欢迎消息"
        )

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """处理 /help 命令"""
        help_text = """
🤖 Telegram群组欢迎机器人

📋 功能说明：
• 当新用户加入群组时，自动发送欢迎消息
• 消息包含随机选择的图片集和自定义文字

🎯 使用方法：
1. 将机器人添加到群组
2. 给机器人管理员权限
3. 新用户加入时会自动触发欢迎消息

⚙️ 命令列表：
/start - 开始使用机器人
/help - 显示此帮助信息
/test_welcome - 测试欢迎消息（仅群组管理员可用）

📁 图片管理：
• 将欢迎图片放入 images/ 文件夹
• 支持 jpg, jpeg, png, gif 格式
• 每次最多发送 {max_images} 张图片
        """.format(max_images=MAX_IMAGES)
        
        await update.message.reply_text(help_text)

    async def test_welcome_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """测试欢迎消息功能"""
        if update.effective_chat.type == 'private':
            await update.message.reply_text("此命令只能在群组中使用！")
            return

        # 检查用户是否是群组管理员
        chat_member = await context.bot.get_chat_member(
            update.effective_chat.id, 
            update.effective_user.id
        )
        
        if chat_member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            await update.message.reply_text("只有群组管理员可以使用此命令！")
            return

        # 发送测试欢迎消息
        await self.send_welcome_message(update.effective_chat.id, context)

    async def handle_chat_member_update(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """处理群组成员变化"""
        try:
            # 检查是否是新用户加入
            chat_member_update = update.chat_member
            old_status = chat_member_update.old_chat_member.status
            new_status = chat_member_update.new_chat_member.status
            
            # 如果用户从非成员状态变为成员状态，则认为是新用户加入
            if (old_status in [ChatMemberStatus.LEFT, ChatMemberStatus.KICKED] and 
                new_status == ChatMemberStatus.MEMBER):
                
                chat_id = chat_member_update.chat.id
                user = chat_member_update.new_chat_member.user
                
                # 检查是否在允许的群组列表中（如果设置了的话）
                if ALLOWED_CHAT_IDS and chat_id not in ALLOWED_CHAT_IDS:
                    logger.info(f"群组 {chat_id} 不在允许列表中，跳过欢迎消息")
                    return
                
                # 忽略机器人加入
                if user.is_bot:
                    logger.info(f"机器人 {user.username} 加入群组，跳过欢迎消息")
                    return
                
                logger.info(f"新用户 {user.full_name} ({user.id}) 加入群组 {chat_id}")
                
                # 发送欢迎消息
                await self.send_welcome_message(chat_id, context)
                
        except Exception as e:
            logger.error(f"处理群组成员变化时出错: {e}")

    def get_random_images(self) -> List[str]:
        """获取随机图片列表"""
        if not os.path.exists(IMAGES_FOLDER):
            logger.warning(f"图片文件夹 {IMAGES_FOLDER} 不存在")
            return []
        
        # 支持的图片格式
        image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.JPG', '*.JPEG', '*.PNG', '*.GIF']
        image_files = []
        
        for extension in image_extensions:
            image_files.extend(glob.glob(os.path.join(IMAGES_FOLDER, extension)))
        
        if not image_files:
            logger.warning(f"在 {IMAGES_FOLDER} 文件夹中未找到图片文件")
            return []
        
        # 随机选择图片，最多MAX_IMAGES张
        selected_images = random.sample(
            image_files, 
            min(len(image_files), MAX_IMAGES)
        )
        
        logger.info(f"选择了 {len(selected_images)} 张图片发送")
        return selected_images

    async def send_welcome_message(self, chat_id: int, context: ContextTypes.DEFAULT_TYPE):
        """发送欢迎消息"""
        try:
            # 获取随机图片
            image_files = self.get_random_images()
            
            if image_files:
                # 创建媒体组
                media_group = []
                for i, image_file in enumerate(image_files):
                    with open(image_file, 'rb') as photo:
                        # 第一张图片添加说明文字
                        caption = WELCOME_MESSAGE if i == 0 else None
                        media_group.append(InputMediaPhoto(media=photo.read(), caption=caption))
                
                # 发送媒体组
                await context.bot.send_media_group(chat_id=chat_id, media=media_group)
                logger.info(f"成功发送包含 {len(image_files)} 张图片的欢迎消息到群组 {chat_id}")
            else:
                # 如果没有图片，只发送文字消息
                await context.bot.send_message(chat_id=chat_id, text=WELCOME_MESSAGE)
                logger.info(f"成功发送文字欢迎消息到群组 {chat_id}")
                
        except Exception as e:
            logger.error(f"发送欢迎消息时出错: {e}")

    def run(self):
        """启动机器人"""
        logger.info("启动Telegram欢迎机器人...")
        
        # 创建images文件夹（如果不存在）
        if not os.path.exists(IMAGES_FOLDER):
            os.makedirs(IMAGES_FOLDER)
            logger.info(f"创建了图片文件夹: {IMAGES_FOLDER}")
        
        # 启动机器人
        self.application.run_polling(drop_pending_updates=True)


def main():
    """主函数"""
    try:
        bot = TelegramWelcomeBot()
        bot.run()
    except KeyboardInterrupt:
        logger.info("机器人已停止")
    except Exception as e:
        logger.error(f"启动机器人时出错: {e}")


if __name__ == '__main__':
    main()
