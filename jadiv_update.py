import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel
from PyQt5.QtCore import QTimer

class AutoUpdater(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Automatický aktualizačný nástroj")
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        self.status_label = QLabel("Kontrolujem aktualizácie...")
        layout.addWidget(self.status_label)

        self.update_button = QPushButton("Aktualizovať teraz")
        self.update_button.clicked.connect(self.update_system)
        layout.addWidget(self.update_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.check_for_updates()

    def check_for_updates(self):
        # Kontroluje aktualizácie každých 30 minút
        QTimer.singleShot(1800000, self.check_for_updates)
        self.status_label.setText("Kontrolujem dostupné aktualizácie...")
        subprocess.run(["sudo", "apt", "update"])

    def update_system(self):
        self.status_label.setText("Aktualizujem systém...")
        result = subprocess.run(["sudo", "apt", "upgrade", "-y"], capture_output=True, text=True)
        self.status_label.setText(f"Aktualizácia dokončená!\n{result.stdout}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AutoUpdater()
    window.show()
    sys.exit(app.exec_())
