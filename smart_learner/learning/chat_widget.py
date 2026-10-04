"""学习板块 - AI 对话界面"""

import json
import threading
from datetime import datetime

import requests
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QTextCursor
from PyQt5.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from smart_learner.config.config_manager import ConfigManager


class ChatWidget(QWidget):
    """AI 对话界面组件"""

    response_received = pyqtSignal(str)
    error_received = pyqtSignal(str)

    def __init__(self, config: ConfigManager) -> None:
        super().__init__()
        self.config = config
        self._messages: list[dict[str, str]] = []
        self._init_system_prompt()
        self._init_ui()
        self.response_received.connect(self._display_response)
        self.error_received.connect(self._display_error)

    def _init_system_prompt(self) -> None:
        prompt = self.config.get("ai", "system_prompt", "")
        if prompt:
            self._messages = [{"role": "system", "content": prompt}]

    def _init_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(12)

        # 标题
        header = QLabel("🤖 AI 学习助手")
        header.setFont(QFont("Noto Sans CJK SC", 18, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)

        subtitle = QLabel("向 AI 提问，获取知识解答、学习建议和难题分析")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #888; margin-bottom: 8px;")
        layout.addWidget(subtitle)

        # 聊天展示区域
        self._chat_display = QTextEdit()
        self._chat_display.setReadOnly(True)
        self._chat_display.setFont(QFont("Noto Sans CJK SC", 13))
        self._chat_display.setPlaceholderText("对话内容将显示在这里...")
        layout.addWidget(self._chat_display, 1)

        # 输入区域
        input_layout = QHBoxLayout()
        input_layout.setSpacing(8)

        self._input_field = QLineEdit()
        self._input_field.setFont(QFont("Noto Sans CJK SC", 13))
        self._input_field.setPlaceholderText("输入你的问题，按 Enter 发送...")
        self._input_field.setMinimumHeight(42)
        self._input_field.returnPressed.connect(self._send_message)
        input_layout.addWidget(self._input_field, 1)

        self._send_btn = QPushButton("发送")
        self._send_btn.setFont(QFont("Noto Sans CJK SC", 13))
        self._send_btn.setMinimumHeight(42)
        self._send_btn.setMinimumWidth(80)
        self._send_btn.clicked.connect(self._send_message)
        input_layout.addWidget(self._send_btn)

        self._clear_btn = QPushButton("清空")
        self._clear_btn.setFont(QFont("Noto Sans CJK SC", 13))
        self._clear_btn.setMinimumHeight(42)
        self._clear_btn.setMinimumWidth(80)
        self._clear_btn.setStyleSheet(
            "background-color: #e74c3c; color: white;"
            "border: none; border-radius: 6px; padding: 8px 18px;"
        )
        self._clear_btn.clicked.connect(self._clear_chat)
        input_layout.addWidget(self._clear_btn)

        layout.addLayout(input_layout)

    def _send_message(self) -> None:
        text = self._input_field.text().strip()
        if not text:
            return

        self._input_field.clear()
        self._append_message("你", text, "#1a73e8")

        self._messages.append({"role": "user", "content": text})

        self._send_btn.setEnabled(False)
        self._send_btn.setText("思考中...")

        thread = threading.Thread(target=self._call_api, daemon=True)
        thread.start()

    def _call_api(self) -> None:
        api_url = self.config.get("ai", "api_url", "")
        api_key = self.config.get("ai", "api_key", "")
        model = self.config.get("ai", "model", "gpt-3.5-turbo")
        max_tokens = self.config.get("ai", "max_tokens", 2048)
        temperature = self.config.get("ai", "temperature", 0.7)

        if not api_key:
            self.error_received.emit("请先在「设置」中配置 API 密钥")
            return

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }
        payload = {
            "model": model,
            "messages": self._messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }

        try:
            resp = requests.post(
                api_url, headers=headers, json=payload, timeout=60
            )
            resp.raise_for_status()
            data = resp.json()
            content = data["choices"][0]["message"]["content"]
            self._messages.append({"role": "assistant", "content": content})
            self._trim_history()
            self.response_received.emit(content)
        except requests.exceptions.Timeout:
            self.error_received.emit("请求超时，请检查网络连接后重试")
        except requests.exceptions.ConnectionError:
            self.error_received.emit("无法连接到 API 服务器，请检查网络和 API 地址")
        except requests.exceptions.HTTPError as e:
            status = e.response.status_code if e.response is not None else "未知"
            self.error_received.emit(f"API 返回错误 (HTTP {status})，请检查 API 密钥和配置")
        except (KeyError, IndexError, json.JSONDecodeError):
            self.error_received.emit("API 响应格式异常，请检查 API 地址是否正确")
        except Exception as e:
            self.error_received.emit(f"未知错误: {e}")

    def _trim_history(self) -> None:
        limit = self.config.get("general", "chat_history_limit", 100)
        # keep system prompt + last N exchanges
        if len(self._messages) > limit * 2 + 1:
            system = [m for m in self._messages if m["role"] == "system"]
            self._messages = system + self._messages[-(limit * 2) :]

    def _display_response(self, text: str) -> None:
        self._append_message("AI 助手", text, "#2ecc71")
        self._send_btn.setEnabled(True)
        self._send_btn.setText("发送")

    def _display_error(self, text: str) -> None:
        self._append_message("系统提示", text, "#e74c3c")
        self._send_btn.setEnabled(True)
        self._send_btn.setText("发送")

    def _append_message(self, sender: str, text: str, color: str) -> None:
        timestamp = datetime.now().strftime("%H:%M:%S")
        html = (
            f'<div style="margin: 8px 0;">'
            f'<b style="color: {color};">[{sender}]</b> '
            f'<span style="color: #999; font-size: 11px;">{timestamp}</span>'
            f"<br/>{text.replace(chr(10), '<br/>')}"
            f"</div>"
        )
        self._chat_display.append(html)
        cursor = self._chat_display.textCursor()
        cursor.movePosition(QTextCursor.End)
        self._chat_display.setTextCursor(cursor)

    def _clear_chat(self) -> None:
        self._chat_display.clear()
        self._messages.clear()
        self._init_system_prompt()

    def reload_config(self) -> None:
        """当设置变更后重新加载配置"""
        pass
