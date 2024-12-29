import sys
import psutil
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel

class SystemMonitor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Monitorovanie systémových zdrojov")
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        self.cpu_label = QLabel("CPU: Loading...")
        self.ram_label = QLabel("RAM: Loading...")
        self.disk_label = QLabel("Disk: Loading...")

        layout.addWidget(self.cpu_label)
        layout.addWidget(self.ram_label)
        layout.addWidget(self.disk_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.update_system_stats()

    def update_system_stats(self):
        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent

        self.cpu_label.setText(f"CPU: {cpu}%")
        self.ram_label.setText(f"RAM: {ram}%")
        self.disk_label.setText(f"Disk: {disk}%")

        # Update every 2 seconds
        QTimer.singleShot(2000, self.update_system_stats)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SystemMonitor()
    window.show()
    sys.exit(app.exec_())
