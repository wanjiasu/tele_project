# Telegram群组欢迎机器人

一个自动为新加入群组的用户发送包含图片集和欢迎文字的Telegram机器人。

## 功能特点

- 🎯 **自动检测新用户加入群组**
- 📸 **发送随机图片集**（支持多张图片组合发送）
- 💬 **自定义欢迎文字**
- 🛡️ **群组权限控制**（可指定特定群组）
- 🤖 **忽略机器人加入**
- 📝 **完整日志记录**

## 安装步骤

### 1. 克隆项目
```bash
git clone <repository-url>
cd facebook_api
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 创建Telegram机器人
1. 在Telegram中找到 [@BotFather](https://t.me/BotFather)
2. 发送 `/newbot` 创建新机器人
3. 按提示设置机器人名称和用户名
4. 获取机器人Token

### 4. 配置环境变量
创建 `.env` 文件：
```bash
cp .env.example .env
```

编辑 `.env` 文件，填入你的机器人Token：
```
TELEGRAM_BOT_TOKEN=your_bot_token_here
# 可选：指定特定群组ID
# ALLOWED_CHAT_IDS=chat_id1,chat_id2
```

### 5. 添加欢迎图片
将你想要发送的图片放入 `images/` 文件夹中。支持的格式：
- JPG/JPEG
- PNG
- GIF

**注意**：机器人会随机选择最多10张图片发送。

### 6. 自定义欢迎消息
编辑 `config.py` 文件中的 `WELCOME_MESSAGE` 变量来自定义欢迎文字。

## 使用方法

### 启动机器人
```bash
python telegram_bot.py
```

### 将机器人添加到群组
1. 将机器人添加到你的Telegram群组
2. 给机器人管理员权限（必须）
3. 当新用户加入群组时，机器人会自动发送欢迎消息

### 可用命令
- `/start` - 开始使用机器人
- `/help` - 显示帮助信息  
- `/test_welcome` - 测试欢迎消息（仅群组管理员可用）

## 配置选项

### config.py 配置说明

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `BOT_TOKEN` | Telegram机器人Token | 从环境变量获取 |
| `ALLOWED_CHAT_IDS` | 允许的群组ID列表（可选） | 空列表（所有群组） |
| `WELCOME_MESSAGE` | 欢迎消息文字 | 可自定义 |
| `IMAGES_FOLDER` | 图片文件夹路径 | "images" |
| `MAX_IMAGES` | 最大图片数量 | 10 |

### 获取群组ID
如果想限制机器人只在特定群组工作：
1. 将机器人添加到群组
2. 发送消息到群组
3. 查看机器人日志，会显示群组ID
4. 将群组ID添加到 `ALLOWED_CHAT_IDS` 环境变量中

## 项目结构

```
facebook_api/
├── telegram_bot.py      # 主程序文件
├── config.py           # 配置文件
├── requirements.txt    # Python依赖
├── .env               # 环境变量（需自创建）
├── images/            # 欢迎图片文件夹
└── README.md          # 说明文档
```

## 故障排除

### 常见问题

1. **机器人没有响应新用户加入**
   - 确保机器人有管理员权限
   - 检查机器人Token是否正确
   - 查看控制台日志是否有错误信息

2. **图片发送失败**
   - 检查 `images/` 文件夹是否存在
   - 确保图片文件格式正确
   - 检查图片文件大小（Telegram限制单个文件最大50MB）

3. **权限错误**
   - 确保机器人在群组中有管理员权限
   - 检查群组设置是否允许机器人发送消息

### 日志查看
程序运行时会在控制台显示详细日志，包括：
- 新用户加入事件
- 图片选择和发送状态
- 错误信息和调试信息

## 技术说明

- 使用 `python-telegram-bot` 库
- 支持异步处理
- 自动处理Telegram API限制
- 完整的错误处理和日志记录

## 许可证

本项目采用MIT许可证。

## 贡献

欢迎提交Issue和Pull Request来改进这个项目！
