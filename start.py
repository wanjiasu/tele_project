#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
启动脚本 - 简化的启动方式
"""

import os
import sys

def main():
    """主函数"""
    print("🤖 Telegram群组欢迎机器人")
    print("=" * 40)
    
    # 检查环境变量
    if not os.getenv('TELEGRAM_BOT_TOKEN'):
        print("❌ 错误：未找到 TELEGRAM_BOT_TOKEN 环境变量")
        print("请创建 .env 文件并设置你的机器人Token")
        print("\n示例 .env 文件内容：")
        print("TELEGRAM_BOT_TOKEN=your_bot_token_here")
        return
    
    # 检查图片文件夹
    images_folder = "images"
    if not os.path.exists(images_folder):
        os.makedirs(images_folder)
        print(f"📁 已创建图片文件夹: {images_folder}")
    
    image_count = len([f for f in os.listdir(images_folder) 
                      if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))])
    print(f"📸 找到 {image_count} 张图片")
    
    if image_count == 0:
        print("⚠️  警告：images/ 文件夹中没有图片，将只发送文字消息")
    
    print("\n🚀 启动机器人...")
    
    # 导入并启动机器人
    try:
        from telegram_bot import main as bot_main
        bot_main()
    except KeyboardInterrupt:
        print("\n👋 机器人已停止")
    except Exception as e:
        print(f"\n❌ 启动失败: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
