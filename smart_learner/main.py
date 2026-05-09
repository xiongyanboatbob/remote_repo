"""智能学习机 - 应用入口"""

import sys

from PyQt5.QtWidgets import QApplication

from smart_learner.main_window import MainWindow


def main() -> None:
    app = QApplication(sys.argv)
    app.setApplicationName("智能学习机")
    app.setApplicationVersion("1.0.0")

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
