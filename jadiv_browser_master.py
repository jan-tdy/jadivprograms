import sys
import os
import subprocess
import RPi.GPIO as GPIO
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout,
    QPushButton, QFileDialog, QLineEdit, QTextEdit, QLabel, QComboBox
)
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile
from PyQt5.QtCore import Qt

class FileAndWebBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Jadiv Browser and File Explorer")
        self.setGeometry(100, 100, 900, 700)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.init_file_browser()
        self.init_web_browser()
        self.init_gpio_control()

    # 1. Prehliadač súborov
    def init_file_browser(self):
        file_tab = QWidget()
        layout = QVBoxLayout()

        self.file_explorer = QTextEdit()
        self.file_explorer.setPlaceholderText("Vyberte adresár na prehliadanie súborov.")
        layout.addWidget(self.file_explorer)

        self.browse_button = QPushButton("Vybrať adresár")
        self.browse_button.clicked.connect(self.open_file_browser)
        layout.addWidget(self.browse_button)

        file_tab.setLayout(layout)
        self.tabs.addTab(file_tab, "Prehliadač súborov")

    def open_file_browser(self):
        directory = QFileDialog.getExistingDirectory(self, "Vyberte adresár")
        if directory:
            self.show_files_in_directory(directory)

    def show_files_in_directory(self, directory):
        files = "\n".join(os.listdir(directory))
        self.file_explorer.setText(files)

    # 2. Prehliadač webových stránok
    def init_web_browser(self):
        web_tab = QWidget()
        layout = QVBoxLayout()

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Zadajte URL a stlačte Enter...")
        self.url_input.returnPressed.connect(self.load_web_page)
        layout.addWidget(self.url_input)

        self.web_view = QWebEngineView()
        layout.addWidget(self.web_view)

        web_tab.setLayout(layout)
        self.tabs.addTab(web_tab, "Webový prehliadač")

    def load_web_page(self):
        url = self.url_input.text()
        if url:
            self.web_view.setUrl(url)

    # 3. Ovládanie GPIO
    def init_gpio_control(self):
        gpio_tab = QWidget()
        layout = QVBoxLayout()

        self.pin_selector = QComboBox()
        self.pin_selector.addItem("GPIO Pin 17")
        self.pin_selector.addItem("GPIO Pin 27")
        self.pin_selector.addItem("GPIO Pin 22")
        layout.addWidget(self.pin_selector)

        self.control_button = QPushButton("Zapnúť/Odpojiť LED")
        self.control_button.clicked.connect(self.toggle_gpio_pin)
        layout.addWidget(self.control_button)

        self.gpio_status = QLabel("Stav GPIO: ")
        layout.addWidget(self.gpio_status)

        gpio_tab.setLayout(layout)
        self.tabs.addTab(gpio_tab, "Ovládanie GPIO")

        # Inicializácia GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(17, GPIO.OUT)
        GPIO.setup(27, GPIO.OUT)
        GPIO.setup(22, GPIO.OUT)

    def toggle_gpio_pin(self):
        selected_pin = self.pin_selector.currentText()
        pin_mapping = {
            "GPIO Pin 17": 17,
            "GPIO Pin 27": 27,
            "GPIO Pin 22": 22
        }
        pin = pin_mapping.get(selected_pin)

        if GPIO.input(pin) == GPIO.LOW:
            GPIO.output(pin, GPIO.HIGH)
            self.gpio_status.setText(f"GPIO {pin} zapnuté")
        else:
            GPIO.output(pin, GPIO.LOW)
            self.gpio_status.setText(f"GPIO {pin} vypnuté")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileAndWebBrowser()
    window.show()
    sys.exit(app.exec_())
