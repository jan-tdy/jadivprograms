import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTreeView, QFileSystemModel, QVBoxLayout,
    QWidget, QLabel, QTabWidget, QPushButton, QHBoxLayout, QTextEdit, QComboBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import psutil
import RPi.GPIO as GPIO

class FileExplorer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Jadiv File & System Explorer")
        self.setGeometry(100, 100, 900, 700)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.init_file_explorer()
        self.init_system_info()
        self.init_gpio_control()
        self.init_file_editor()

    # 1. Prehliadač súborov
    def init_file_explorer(self):
        file_tab = QWidget()
        layout = QVBoxLayout()

        self.file_model = QFileSystemModel()
        self.file_model.setRootPath(os.path.expanduser("~"))

        self.tree_view = QTreeView()
        self.tree_view.setModel(self.file_model)
        self.tree_view.setRootIndex(self.file_model.index(os.path.expanduser("~")))
        self.tree_view.setColumnWidth(0, 250)

        layout.addWidget(self.tree_view)
        file_tab.setLayout(layout)
        self.tabs.addTab(file_tab, "Súbory")

    # 2. Systémové informácie
    def init_system_info(self):
        system_tab = QWidget()
        layout = QVBoxLayout()

        self.system_info_label = QLabel()
        self.update_system_info()
        layout.addWidget(self.system_info_label)

        refresh_button = QPushButton("Aktualizovať")
        refresh_button.clicked.connect(self.update_system_info)
        layout.addWidget(refresh_button)

        system_tab.setLayout(layout)
        self.tabs.addTab(system_tab, "Systém")

    def update_system_info(self):
        cpu_usage = psutil.cpu_percent()
        memory = psutil.virtual_memory()
        memory_usage = f"{memory.used // (1024 ** 2)} MB / {memory.total // (1024 ** 2)} MB"

        info = f"""
        **CPU využitie:** {cpu_usage}%
        **Pamäť:** {memory_usage}
        **Disk:** {psutil.disk_usage('/').percent}% využité
        """
        self.system_info_label.setText(info)

    # 3. GPIO ovládanie
    def init_gpio_control(self):
        gpio_tab = QWidget()
        layout = QVBoxLayout()

        self.gpio_label = QLabel("GPIO Pin:")
        layout.addWidget(self.gpio_label)

        self.gpio_select = QComboBox()
        self.gpio_select.addItems([str(i) for i in range(2, 28)])
        layout.addWidget(self.gpio_select)

        self.gpio_button = QPushButton("Zapnúť/Vypnúť")
        self.gpio_button.clicked.connect(self.toggle_gpio)
        layout.addWidget(self.gpio_button)

        gpio_tab.setLayout(layout)
        self.tabs.addTab(gpio_tab, "GPIO")

        # Inicializácia GPIO
        GPIO.setmode(GPIO.BCM)

    def toggle_gpio(self):
        pin = int(self.gpio_select.currentText())
        GPIO.setup(pin, GPIO.OUT)
        current_state = GPIO.input(pin)
        GPIO.output(pin, not current_state)

    # 4. Editor súborov
    def init_file_editor(self):
        editor_tab = QWidget()
        layout = QVBoxLayout()

        self.text_edit = QTextEdit()
        self.text_edit.setFont(QFont("Courier", 12))
        layout.addWidget(self.text_edit)

        self.save_button = QPushButton("Uložiť súbor")
        self.save_button.clicked.connect(self.save_file)
        layout.addWidget(self.save_button)

        editor_tab.setLayout(layout)
        self.tabs.addTab(editor_tab, "Editor")

    def save_file(self):
        file_path = os.path.expanduser("~/edited_file.txt")
        with open(file_path, "w") as file:
            file.write(self.text_edit.toPlainText())
        self.statusBar().showMessage(f"Súbor uložený: {file_path}", 3000)

    def closeEvent(self, event):
        GPIO.cleanup()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Nastavenie moderného vzhľadu
    try:
        import qdarkstyle
        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    except ImportError:
        pass  # Štýl nie je povinný

    window = FileExplorer()
    window.show()
    sys.exit(app.exec_())
