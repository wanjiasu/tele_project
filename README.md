# Telegram群组欢迎机器人 - FastAPI版本

基于FastAPI的Telegram群组欢迎机器人，当新用户加入群组时，自动发送包含图片集和欢迎文字的消息。

## 🚀 功能特性

- **FastAPI框架**: 现代化的异步Python Web框架
- **Docker支持**: 完整的容器化部署方案
- **健康检查**: 内置健康检查端点
- **API文档**: 自动生成的Swagger/OpenAPI文档
- **自动欢迎**: 检测新用户加入并发送欢迎消息
- **图片支持**: 随机发送欢迎图片集

## 📁 项目结构

```
tele_project/
├── backend/              # FastAPI应用
│   ├── main.py          # FastAPI主应用
│   ├── config.py        # 配置文件
│   ├── requirements.txt # Python依赖
│   ├── Dockerfile       # Docker镜像构建文件
│   └── .dockerignore    # Docker忽略文件
├── images/              # 欢迎图片文件夹
├── docker-compose.yml   # Docker Compose配置
├── env.example         # 环境变量示例
└── README.md           # 项目文档
```

## 🛠️ 快速开始

### 1. 配置环境变量

复制环境变量模板：
```bash
cp env.example .env
```

编辑`.env`文件，设置必要配置：
```bash
TELEGRAM_BOT_TOKEN=your_bot_token_here
ALLOWED_CHAT_IDS=  # 可选，用逗号分隔
MAX_IMAGES=10
```

### 2. 准备图片

将欢迎图片放入`images/`文件夹，支持格式：
- JPG/JPEG
- PNG  
- GIF

### 3. 使用Docker Compose部署

```bash
# 构建并启动服务
docker-compose up -d --build

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f telegram-bot
```

## 🌐 API端点

- `GET /` - 根路径健康检查
- `GET /health` - 健康检查端点
- `GET /docs` - API文档 (Swagger UI)
- `GET /bot/status` - 获取机器人状态
- `POST /bot/test-welcome` - 测试欢迎消息
- `GET /bot/images` - 获取可用图片列表

## 🔧 配置选项

| 环境变量 | 说明 | 默认值 |
|---------|------|--------|
| `TELEGRAM_BOT_TOKEN` | Telegram Bot Token | 必须设置 |
| `ALLOWED_CHAT_IDS` | 允许的群组ID列表 | 空（允许所有） |
| `MAX_IMAGES` | 最大图片数量 | 10 |

## 🐳 Docker命令

```bash
# 启动服务
docker-compose up -d

# 停止服务  
docker-compose down

# 重启服务
docker-compose restart

# 查看日志
docker-compose logs -f

# 重新构建
docker-compose up -d --build
```

## 📋 使用方法

1. 将机器人添加到Telegram群组
2. 给机器人管理员权限
3. 新用户加入时会自动触发欢迎消息
4. 群组管理员可使用`/test_welcome`命令测试功能

## 🚨 注意事项

- 确保机器人有发送消息的权限
- 图片文件大小不要超过Telegram限制
- 建议定期检查机器人运行状态
- 服务运行在8000端口

## 🔍 故障排除

### 常见问题

1. **机器人无法启动**
   - 检查`TELEGRAM_BOT_TOKEN`是否正确
   - 查看容器日志：`docker-compose logs telegram-bot`

2. **图片无法发送**
   - 确保`images/`文件夹存在且包含图片
   - 检查图片格式是否支持

3. **服务无法访问**
   - 检查端口是否被占用：`netstat -tulpn | grep 8000`
   - 确认防火墙设置

### 健康检查

```bash
curl http://localhost:8000/health
```

## 📄 许可证

本项目采用MIT许可证。