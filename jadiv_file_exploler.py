import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTreeView, QFileSystemModel, QVBoxLayout,
    QWidget, QLabel, QTabWidget, QPushButton, QHBoxLayout
)
from PyQt5.QtCore import Qt
import psutil

class FileExplorer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Jadiv File & System Explorer")
        self.setGeometry(100, 100, 800, 600)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.init_file_explorer()
        self.init_system_info()

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

    def init_system_info(self):
        system_tab = QWidget()
        layout = QVBoxLayout()

        # Zobrazenie informácií o systéme
        self.system_info_label = QLabel()
        self.update_system_info()
        layout.addWidget(self.system_info_label)

        # Aktualizačné tlačidlo
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileExplorer()
    window.show()
    sys.exit(app.exec_())
