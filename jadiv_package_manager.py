import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLineEdit, QLabel

class PackageManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Správca balíčkov")
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        # Vyhľadávanie balíčkov
        self.package_input = QLineEdit()
        self.package_input.setPlaceholderText("Zadajte názov balíčka...")
        layout.addWidget(self.package_input)

        # Vyhľadanie balíčka
        self.search_button = QPushButton("Vyhľadať balíček")
        self.search_button.clicked.connect(self.search_package)
        layout.addWidget(self.search_button)

        # Inštalovanie balíčka
        self.install_button = QPushButton("Inštalovať balíček")
        self.install_button.clicked.connect(self.install_package)
        layout.addWidget(self.install_button)

        # Status
        self.status_label = QLabel("")
        layout.addWidget(self.status_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def search_package(self):
        package = self.package_input.text()
        if package:
            self.status_label.setText(f"Hľadám balíček: {package}")
            result = subprocess.run(["apt-cache", "search", package], capture_output=True, text=True)
            self.status_label.setText(f"Výsledky: {result.stdout}")
        else:
            self.status_label.setText("Zadajte názov balíčka!")

    def install_package(self):
        package = self.package_input.text()
        if package:
            self.status_label.setText(f"Inštalujem: {package}")
            result = subprocess.run(["sudo", "apt", "install", "-y", package], capture_output=True, text=True)
            self.status_label.setText(f"Inštalácia úspešná!\n{result.stdout}")
        else:
            self.status_label.setText("Zadajte názov balíčka na inštaláciu!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PackageManager()
    window.show()
    sys.exit(app.exec_())
