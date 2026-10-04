# 智能学习机

通过 AI 让人更高效地学习的 Ubuntu 桌面应用程序。

## 功能

应用分为三个板块：

### 📖 学习
- AI 对话界面，支持与大语言模型实时对话
- 可配置 API 地址、模型、密钥等参数
- 支持 OpenAI 兼容的 API 接口
- 对话历史管理

### 🎮 玩
- 游戏启动器，可添加和管理本地游戏程序
- 双击或点击按钮启动游戏
- 支持浏览文件系统选择游戏程序

### ⚙ 设置
- AI 对话参数配置（API 地址、密钥、模型、温度等）
- 外观设置（浅色/深色主题、字体大小）
- 通用设置（默认启动页面、聊天记录上限）
- 一键重置为默认设置

## 硬件要求

- 内存：4GB 及以上
- 硬盘：256GB 及以上
- 输入设备：键盘 + 鼠标
- 网络：需要网卡连接互联网（AI 对话功能需要网络）

## 安装

### 系统依赖

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv python3-pyqt5
```

### 安装应用

```bash
# 克隆仓库
git clone https://github.com/xiongyanboatbob/remote_repo.git
cd remote_repo

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 或使用 pip 直接安装
pip install -e .
```

## 运行

```bash
# 方式一：使用模块运行
python3 -m smart_learner.main

# 方式二：安装后使用命令行
smart-learner
```

## 配置 AI 对话

1. 启动应用后，点击「设置」标签页
2. 在「AI 对话设置」中填入：
   - **API 地址**：兼容 OpenAI 格式的 API 端点
   - **API 密钥**：对应服务的 API Key
   - **模型名称**：如 `gpt-3.5-turbo`、`gpt-4` 等
3. 点击「保存设置」

支持任何兼容 OpenAI Chat Completions API 格式的服务。

## 项目结构

```
smart_learner/
├── __init__.py              # 包初始化
├── main.py                  # 应用入口
├── main_window.py           # 主窗口（板块切换）
├── config/
│   └── config_manager.py    # 配置管理器
├── learning/
│   └── chat_widget.py       # AI 对话界面
├── play/
│   └── game_launcher.py     # 游戏启动器
├── settings/
│   └── settings_widget.py   # 设置界面
└── resources/
    └── icons/               # 图标资源
```

## 开发

```bash
# 安装开发依赖
pip install -e ".[dev]"

# 运行代码检查
ruff check smart_learner/

# 运行测试
pytest tests/
```

## 技术栈

- **Python 3.9+**
- **PyQt5** - GUI 框架
- **requests** - HTTP 网络请求
- **OpenAI Chat API** - AI 对话内核

## 许可证

MIT License
