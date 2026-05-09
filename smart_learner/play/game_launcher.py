"""玩板块 - 游戏启动器"""

import os
import subprocess
from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from smart_learner.config.config_manager import ConfigManager


class GameLauncher(QWidget):
    """游戏启动器组件"""

    def __init__(self, config: ConfigManager) -> None:
        super().__init__()
        self.config = config
        self._init_ui()
        self._load_games()

    def _init_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(12)

        header = QLabel("🎮 游戏中心")
        header.setFont(QFont("Noto Sans CJK SC", 18, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)

        subtitle = QLabel("劳逸结合，适度游戏有助于放松大脑")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #888; margin-bottom: 8px;")
        layout.addWidget(subtitle)

        # 游戏列表
        games_group = QGroupBox("已添加的游戏")
        games_layout = QVBoxLayout(games_group)

        self._game_list = QListWidget()
        self._game_list.setFont(QFont("Noto Sans CJK SC", 13))
        self._game_list.setMinimumHeight(300)
        self._game_list.itemDoubleClicked.connect(self._launch_selected)
        games_layout.addWidget(self._game_list)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(8)

        launch_btn = QPushButton("▶ 启动游戏")
        launch_btn.setFont(QFont("Noto Sans CJK SC", 13))
        launch_btn.clicked.connect(self._launch_selected)
        btn_layout.addWidget(launch_btn)

        remove_btn = QPushButton("🗑 移除")
        remove_btn.setFont(QFont("Noto Sans CJK SC", 13))
        remove_btn.setStyleSheet(
            "background-color: #e74c3c; color: white;"
            "border: none; border-radius: 6px; padding: 8px 18px;"
        )
        remove_btn.clicked.connect(self._remove_game)
        btn_layout.addWidget(remove_btn)

        games_layout.addLayout(btn_layout)
        layout.addWidget(games_group, 1)

        # 添加游戏
        add_group = QGroupBox("添加新游戏")
        add_layout = QVBoxLayout(add_group)

        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("游戏名称:"))
        self._name_input = QLineEdit()
        self._name_input.setPlaceholderText("输入游戏名称")
        name_layout.addWidget(self._name_input, 1)
        add_layout.addLayout(name_layout)

        path_layout = QHBoxLayout()
        path_layout.addWidget(QLabel("程序路径:"))
        self._path_input = QLineEdit()
        self._path_input.setPlaceholderText("选择游戏程序路径")
        path_layout.addWidget(self._path_input, 1)

        browse_btn = QPushButton("浏览...")
        browse_btn.clicked.connect(self._browse_executable)
        path_layout.addWidget(browse_btn)
        add_layout.addLayout(path_layout)

        add_btn = QPushButton("➕ 添加游戏")
        add_btn.setFont(QFont("Noto Sans CJK SC", 13))
        add_btn.clicked.connect(self._add_game)
        add_layout.addWidget(add_btn)

        layout.addWidget(add_group)

    def _load_games(self) -> None:
        self._game_list.clear()
        games = self.config.get("games", "custom_games", [])
        for game in games:
            name = game.get("name", "未命名")
            path = game.get("path", "")
            item = QListWidgetItem(f"🎯 {name}")
            item.setData(Qt.UserRole, path)
            item.setToolTip(f"路径: {path}")
            self._game_list.addItem(item)

    def _add_game(self) -> None:
        name = self._name_input.text().strip()
        path = self._path_input.text().strip()

        if not name or not path:
            QMessageBox.warning(self, "提示", "请填写游戏名称和程序路径")
            return

        if not os.path.isfile(path):
            QMessageBox.warning(self, "提示", f"文件不存在: {path}")
            return

        games = self.config.get("games", "custom_games", [])
        games.append({"name": name, "path": path})
        self.config.set("games", "custom_games", games)
        self.config.save()

        self._name_input.clear()
        self._path_input.clear()
        self._load_games()

    def _remove_game(self) -> None:
        current = self._game_list.currentItem()
        if not current:
            QMessageBox.information(self, "提示", "请先选择要移除的游戏")
            return

        row = self._game_list.row(current)
        games = self.config.get("games", "custom_games", [])
        if 0 <= row < len(games):
            reply = QMessageBox.question(
                self,
                "确认",
                f"确定要移除「{games[row]['name']}」吗？",
                QMessageBox.Yes | QMessageBox.No,
            )
            if reply == QMessageBox.Yes:
                games.pop(row)
                self.config.set("games", "custom_games", games)
                self.config.save()
                self._load_games()

    def _launch_selected(self) -> None:
        current = self._game_list.currentItem()
        if not current:
            QMessageBox.information(self, "提示", "请先选择要启动的游戏")
            return

        path = current.data(Qt.UserRole)
        if not path or not os.path.isfile(path):
            QMessageBox.warning(self, "错误", f"游戏程序不存在: {path}")
            return

        try:
            working_dir = str(Path(path).parent)
            subprocess.Popen(
                [path],
                cwd=working_dir,
                start_new_session=True,
            )
        except PermissionError:
            QMessageBox.warning(
                self,
                "权限不足",
                f"无法启动程序，请确保文件有可执行权限:\n{path}\n\n"
                f"尝试运行: chmod +x {path}",
            )
        except OSError as e:
            QMessageBox.critical(self, "启动失败", f"无法启动游戏:\n{e}")

    def _browse_executable(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self, "选择游戏程序", str(Path.home()), "所有文件 (*)"
        )
        if path:
            self._path_input.setText(path)
            if not self._name_input.text():
                self._name_input.setText(Path(path).stem)

    def reload_config(self) -> None:
        self._load_games()
