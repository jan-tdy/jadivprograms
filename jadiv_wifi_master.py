import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QComboBox, QLabel

class WifiManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Wi-Fi Správca")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.network_label = QLabel("Vyberte Wi-Fi sieť:")
        layout.addWidget(self.network_label)

        self.network_combo = QComboBox()
        layout.addWidget(self.network_combo)

        # Získanie dostupných Wi-Fi sietí
        self.scan_wifi_button = QPushButton("Prehľadať siete")
        self.scan_wifi_button.clicked.connect(self.scan_wifi)
        layout.addWidget(self.scan_wifi_button)

        self.connect_button = QPushButton("Pripojiť sa")
        self.connect_button.clicked.connect(self.connect_wifi)
        layout.addWidget(self.connect_button)

        self.status_label = QLabel("")
        layout.addWidget(self.status_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.scan_wifi()

    def scan_wifi(self):
        self.network_combo.clear()
        self.status_label.setText("Prehľadávam dostupné siete...")

        # Spustenie príkazu na získanie dostupných Wi-Fi sietí
        result = subprocess.run(["nmcli", "-t", "-f", "SSID", "dev", "wifi"], capture_output=True, text=True)

        networks = result.stdout.splitlines()
        for network in networks:
            self.network_combo.addItem(network)

        self.status_label.setText("Siete načítané.")

    def connect_wifi(self):
        selected_network = self.network_combo.currentText()
        if selected_network:
            self.status_label.setText(f"Pripojujem sa k: {selected_network}")
            # Pripojenie k vybranej sieti (tu môže byť potrebné zadať heslo)
            result = subprocess.run(["nmcli", "dev", "wifi", "connect", selected_network], capture_output=True, text=True)

            if result.returncode == 0:
                self.status_label.setText(f"Úspešne pripojené k {selected_network}.")
            else:
                self.status_label.setText(f"Chyba pri pripojení k {selected_network}.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WifiManager()
    window.show()
    sys.exit(app.exec_())
