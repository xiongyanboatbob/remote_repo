"""设置板块 - 配置管理界面"""

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QComboBox,
    QDoubleSpinBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSpinBox,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from smart_learner.config.config_manager import ConfigManager


class SettingsWidget(QWidget):
    """设置界面组件"""

    settings_saved = pyqtSignal()

    def __init__(self, config: ConfigManager) -> None:
        super().__init__()
        self.config = config
        self._init_ui()
        self._load_values()

    def _init_ui(self) -> None:
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(20, 16, 20, 16)

        header = QLabel("⚙ 设置")
        header.setFont(QFont("Noto Sans CJK SC", 18, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        outer_layout.addWidget(header)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)

        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setSpacing(16)

        # --- AI 设置 ---
        ai_group = QGroupBox("AI 对话设置")
        ai_form = QFormLayout(ai_group)
        ai_form.setSpacing(10)
        ai_form.setContentsMargins(16, 24, 16, 16)

        self._api_url_input = QLineEdit()
        self._api_url_input.setPlaceholderText("https://api.openai.com/v1/chat/completions")
        ai_form.addRow("API 地址:", self._api_url_input)

        self._api_key_input = QLineEdit()
        self._api_key_input.setEchoMode(QLineEdit.Password)
        self._api_key_input.setPlaceholderText("输入 API 密钥")
        ai_form.addRow("API 密钥:", self._api_key_input)

        self._model_input = QLineEdit()
        self._model_input.setPlaceholderText("gpt-3.5-turbo")
        ai_form.addRow("模型名称:", self._model_input)

        self._max_tokens_input = QSpinBox()
        self._max_tokens_input.setRange(64, 16384)
        self._max_tokens_input.setSingleStep(256)
        ai_form.addRow("最大 Token:", self._max_tokens_input)

        self._temperature_input = QDoubleSpinBox()
        self._temperature_input.setRange(0.0, 2.0)
        self._temperature_input.setSingleStep(0.1)
        self._temperature_input.setDecimals(1)
        ai_form.addRow("温度 (Temperature):", self._temperature_input)

        self._system_prompt_input = QTextEdit()
        self._system_prompt_input.setMaximumHeight(100)
        self._system_prompt_input.setPlaceholderText("设定 AI 助手的系统提示词...")
        ai_form.addRow("系统提示词:", self._system_prompt_input)

        layout.addWidget(ai_group)

        # --- 外观设置 ---
        appearance_group = QGroupBox("外观设置")
        appearance_form = QFormLayout(appearance_group)
        appearance_form.setSpacing(10)
        appearance_form.setContentsMargins(16, 24, 16, 16)

        self._theme_combo = QComboBox()
        self._theme_combo.addItems(["浅色 (Light)", "深色 (Dark)"])
        appearance_form.addRow("主题:", self._theme_combo)

        self._font_size_input = QSpinBox()
        self._font_size_input.setRange(10, 24)
        self._font_size_input.setSuffix(" px")
        appearance_form.addRow("字体大小:", self._font_size_input)

        layout.addWidget(appearance_group)

        # --- 通用设置 ---
        general_group = QGroupBox("通用设置")
        general_form = QFormLayout(general_group)
        general_form.setSpacing(10)
        general_form.setContentsMargins(16, 24, 16, 16)

        self._start_tab_combo = QComboBox()
        self._start_tab_combo.addItems(["学习", "玩", "设置"])
        general_form.addRow("启动时默认页面:", self._start_tab_combo)

        self._history_limit_input = QSpinBox()
        self._history_limit_input.setRange(10, 1000)
        self._history_limit_input.setSingleStep(10)
        general_form.addRow("聊天记录上限:", self._history_limit_input)

        layout.addWidget(general_group)

        # --- 按钮 ---
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        save_btn = QPushButton("💾 保存设置")
        save_btn.setFont(QFont("Noto Sans CJK SC", 14, QFont.Bold))
        save_btn.setMinimumHeight(48)
        save_btn.setMinimumWidth(160)
        save_btn.clicked.connect(self._save_settings)
        btn_layout.addWidget(save_btn)

        reset_btn = QPushButton("重置为默认")
        reset_btn.setFont(QFont("Noto Sans CJK SC", 13))
        reset_btn.setMinimumHeight(48)
        reset_btn.setStyleSheet(
            "background-color: #f39c12; color: white;"
            "border: none; border-radius: 6px; padding: 8px 18px;"
        )
        reset_btn.clicked.connect(self._reset_defaults)
        btn_layout.addWidget(reset_btn)

        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        layout.addStretch()

        scroll.setWidget(content)
        outer_layout.addWidget(scroll, 1)

    def _load_values(self) -> None:
        self._api_url_input.setText(
            self.config.get("ai", "api_url", "https://api.openai.com/v1/chat/completions")
        )
        self._api_key_input.setText(self.config.get("ai", "api_key", ""))
        self._model_input.setText(self.config.get("ai", "model", "gpt-3.5-turbo"))
        self._max_tokens_input.setValue(self.config.get("ai", "max_tokens", 2048))
        self._temperature_input.setValue(self.config.get("ai", "temperature", 0.7))
        self._system_prompt_input.setPlainText(self.config.get("ai", "system_prompt", ""))

        theme = self.config.get("appearance", "theme", "light")
        self._theme_combo.setCurrentIndex(0 if theme == "light" else 1)
        self._font_size_input.setValue(self.config.get("appearance", "font_size", 14))

        self._start_tab_combo.setCurrentIndex(self.config.get("general", "start_tab", 0))
        self._history_limit_input.setValue(
            self.config.get("general", "chat_history_limit", 100)
        )

    def _save_settings(self) -> None:
        self.config.set("ai", "api_url", self._api_url_input.text().strip())
        self.config.set("ai", "api_key", self._api_key_input.text().strip())
        self.config.set("ai", "model", self._model_input.text().strip())
        self.config.set("ai", "max_tokens", self._max_tokens_input.value())
        self.config.set("ai", "temperature", self._temperature_input.value())
        self.config.set("ai", "system_prompt", self._system_prompt_input.toPlainText().strip())

        self.config.set(
            "appearance",
            "theme",
            "light" if self._theme_combo.currentIndex() == 0 else "dark",
        )
        self.config.set("appearance", "font_size", self._font_size_input.value())

        self.config.set("general", "start_tab", self._start_tab_combo.currentIndex())
        self.config.set("general", "chat_history_limit", self._history_limit_input.value())

        self.config.save()
        self.settings_saved.emit()
        QMessageBox.information(self, "设置", "设置已保存！")

    def _reset_defaults(self) -> None:
        reply = QMessageBox.question(
            self,
            "确认",
            "确定要将所有设置重置为默认值吗？",
            QMessageBox.Yes | QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            from smart_learner.config.config_manager import DEFAULT_CONFIG

            for section, values in DEFAULT_CONFIG.items():
                for key, value in values.items():
                    self.config.set(section, key, value)
            self.config.save()
            self._load_values()
            self.settings_saved.emit()
            QMessageBox.information(self, "设置", "已重置为默认设置")
