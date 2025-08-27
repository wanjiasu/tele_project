#!/bin/bash

# Telegram Bot FastAPI 部署脚本

set -e

echo "🚀 开始部署 Telegram Welcome Bot..."

# 检查环境变量文件
if [ ! -f .env ]; then
    echo "⚠️  未找到 .env 文件，正在从模板创建..."
    if [ -f env.example ]; then
        cp env.example .env
        echo "📝 请编辑 .env 文件，设置正确的 TELEGRAM_BOT_TOKEN"
        echo "按回车键继续..."
        read
    else
        echo "❌ 未找到 env.example 文件"
        exit 1
    fi
fi

# 构建并启动服务
echo "🔨 构建并启动服务..."
docker-compose up -d --build

# 等待服务启动
echo "⏳ 等待服务启动..."
sleep 10

# 检查服务状态
echo "🔍 检查服务状态..."
docker-compose ps

# 检查健康状态
echo "🏥 检查健康状态..."
if curl -f http://localhost:8000/health &> /dev/null; then
    echo "✅ 服务运行正常！"
    echo "🌐 API 地址: http://localhost:8000"
    echo "📚 API 文档: http://localhost:8000/docs"
else
    echo "❌ 服务启动失败，请检查日志："
    docker-compose logs telegram-bot
fi

echo ""
echo "📋 部署完成！"
