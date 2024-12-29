import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel

class AppManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("JADIV Aplikácie")
        self.setGeometry(100, 100, 400, 300)

        # Vytvorenie hlavného layoutu
        layout = QVBoxLayout()

        # Pridanie názvu aplikácie
        self.title_label = QLabel("Vyberte aplikáciu na spustenie:")
        layout.addWidget(self.title_label)

        # Tlačidlá pre spustenie jednotlivých aplikácií
        self.package_manager_button = QPushButton("Správca balíčkov")
        self.package_manager_button.clicked.connect(self.launch_package_manager)
        layout.addWidget(self.package_manager_button)

        self.system_monitor_button = QPushButton("Monitorovanie systémových zdrojov")
        self.system_monitor_button.clicked.connect(self.launch_system_monitor)
        layout.addWidget(self.system_monitor_button)

        self.wifi_manager_button = QPushButton("Wi-Fi Správca")
        self.wifi_manager_button.clicked.connect(self.launch_wifi_manager)
        layout.addWidget(self.wifi_manager_button)

        self.time_manager_button = QPushButton("Nastavenie dátumu a času")
        self.time_manager_button.clicked.connect(self.launch_time_manager)
        layout.addWidget(self.time_manager_button)

        self.status_label = QLabel("")
        layout.addWidget(self.status_label)

        # Nastavenie layoutu na hlavnú obrazovku
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    # Funkcie pre spustenie jednotlivých aplikácií
    def launch_package_manager(self):
        self.status_label.setText("Spúšťam Správcu balíčkov...")
        subprocess.run(["python3", "package_manager.py"])

    def launch_system_monitor(self):
        self.status_label.setText("Spúšťam Monitorovanie systémových zdrojov...")
        subprocess.run(["python3", "system_monitor.py"])

    def launch_wifi_manager(self):
        self.status_label.setText("Spúšťam Wi-Fi Správcu...")
        subprocess.run(["python3", "wifi_manager.py"])

    def launch_time_manager(self):
        self.status_label.setText("Spúšťam Nastavenie dátumu a času...")
        subprocess.run(["python3", "time_manager.py"])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AppManager()
    window.show()
    sys.exit(app.exec_())
