"""主窗口 - 包含三个板块的切换界面"""

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from smart_learner.config.config_manager import ConfigManager
from smart_learner.learning.chat_widget import ChatWidget
from smart_learner.play.game_launcher import GameLauncher
from smart_learner.settings.settings_widget import SettingsWidget


class MainWindow(QMainWindow):
    """应用主窗口"""

    def __init__(self) -> None:
        super().__init__()
        self.config = ConfigManager()
        self._init_ui()
        self._apply_theme()

    def _init_ui(self) -> None:
        self.setWindowTitle("智能学习机")
        self.setMinimumSize(1024, 680)
        self.resize(1200, 800)

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 顶部导航栏
        nav_bar = QWidget()
        nav_bar.setObjectName("navBar")
        nav_layout = QHBoxLayout(nav_bar)
        nav_layout.setContentsMargins(20, 8, 20, 8)

        title_label = QLabel("智能学习机")
        title_label.setObjectName("titleLabel")
        title_label.setFont(QFont("Noto Sans CJK SC", 16, QFont.Bold))
        nav_layout.addWidget(title_label)
        nav_layout.addStretch()

        self._nav_buttons: list[QPushButton] = []
        tabs = [("📖 学习", 0), ("🎮 玩", 1), ("⚙ 设置", 2)]
        for text, index in tabs:
            btn = QPushButton(text)
            btn.setObjectName("navButton")
            btn.setFont(QFont("Noto Sans CJK SC", 13))
            btn.setCheckable(True)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setMinimumWidth(100)
            btn.setMinimumHeight(40)
            btn.clicked.connect(lambda checked, i=index: self._switch_tab(i))
            nav_layout.addWidget(btn)
            self._nav_buttons.append(btn)

        main_layout.addWidget(nav_bar)

        # 页面堆栈
        self._stack = QStackedWidget()
        self._chat_widget = ChatWidget(self.config)
        self._game_launcher = GameLauncher(self.config)
        self._settings_widget = SettingsWidget(self.config)
        self._settings_widget.settings_saved.connect(self._on_settings_saved)

        self._stack.addWidget(self._chat_widget)
        self._stack.addWidget(self._game_launcher)
        self._stack.addWidget(self._settings_widget)

        main_layout.addWidget(self._stack, 1)

        start_tab = self.config.get("general", "start_tab", 0)
        self._switch_tab(start_tab)

    def _switch_tab(self, index: int) -> None:
        self._stack.setCurrentIndex(index)
        for i, btn in enumerate(self._nav_buttons):
            btn.setChecked(i == index)

    def _on_settings_saved(self) -> None:
        self._apply_theme()
        self._chat_widget.reload_config()
        self._game_launcher.reload_config()

    def _apply_theme(self) -> None:
        theme = self.config.get("appearance", "theme", "light")
        font_size = self.config.get("appearance", "font_size", 14)

        if theme == "dark":
            self.setStyleSheet(self._dark_style(font_size))
        else:
            self.setStyleSheet(self._light_style(font_size))

    @staticmethod
    def _light_style(font_size: int) -> str:
        return f"""
            QWidget {{
                font-size: {font_size}px;
                color: #333;
                background-color: #f5f5f5;
            }}
            #navBar {{
                background-color: #ffffff;
                border-bottom: 2px solid #e0e0e0;
            }}
            #titleLabel {{
                color: #1a73e8;
            }}
            #navButton {{
                border: none;
                border-radius: 8px;
                padding: 8px 16px;
                margin: 2px 4px;
                background-color: transparent;
                color: #555;
            }}
            #navButton:checked {{
                background-color: #1a73e8;
                color: white;
            }}
            #navButton:hover:!checked {{
                background-color: #e8f0fe;
            }}
            QTextEdit, QLineEdit, QListWidget, QComboBox, QSpinBox {{
                background-color: #ffffff;
                border: 1px solid #ddd;
                border-radius: 6px;
                padding: 6px;
            }}
            QPushButton {{
                background-color: #1a73e8;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 18px;
            }}
            QPushButton:hover {{
                background-color: #1557b0;
            }}
            QPushButton:disabled {{
                background-color: #ccc;
            }}
            QGroupBox {{
                font-weight: bold;
                border: 1px solid #ddd;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 20px;
                background-color: #ffffff;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 16px;
                padding: 0 6px;
            }}
        """

    @staticmethod
    def _dark_style(font_size: int) -> str:
        return f"""
            QWidget {{
                font-size: {font_size}px;
                color: #e0e0e0;
                background-color: #1e1e1e;
            }}
            #navBar {{
                background-color: #2d2d2d;
                border-bottom: 2px solid #444;
            }}
            #titleLabel {{
                color: #8ab4f8;
            }}
            #navButton {{
                border: none;
                border-radius: 8px;
                padding: 8px 16px;
                margin: 2px 4px;
                background-color: transparent;
                color: #aaa;
            }}
            #navButton:checked {{
                background-color: #8ab4f8;
                color: #1e1e1e;
            }}
            #navButton:hover:!checked {{
                background-color: #3d3d3d;
            }}
            QTextEdit, QLineEdit, QListWidget, QComboBox, QSpinBox {{
                background-color: #2d2d2d;
                border: 1px solid #555;
                border-radius: 6px;
                padding: 6px;
                color: #e0e0e0;
            }}
            QPushButton {{
                background-color: #8ab4f8;
                color: #1e1e1e;
                border: none;
                border-radius: 6px;
                padding: 8px 18px;
            }}
            QPushButton:hover {{
                background-color: #aecbfa;
            }}
            QPushButton:disabled {{
                background-color: #555;
                color: #888;
            }}
            QGroupBox {{
                font-weight: bold;
                border: 1px solid #555;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 20px;
                background-color: #2d2d2d;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 16px;
                padding: 0 6px;
            }}
        """
