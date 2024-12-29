import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QDateEdit, QPushButton, QLabel

class TimeManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nastavenie dátumu a času")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.date_label = QLabel("Vyberte dátum a čas:")
        layout.addWidget(self.date_label)

        self.date_edit = QDateEdit()
        layout.addWidget(self.date_edit)

        self.set_button = QPushButton("Nastaviť dátum a čas")
        self.set_button.clicked.connect(self.set_date_time)
        layout.addWidget(self.set_button)

        self.status_label = QLabel("")
        layout.addWidget(self.status_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def set_date_time(self):
        date_time = self.date_edit.date().toString("yyyy-MM-dd HH:mm:ss")
        self.status_label.setText(f"Nastavujem: {date_time}")
        result = subprocess.run(["sudo", "date", date_time], capture_output=True, text=True)

        if result.returncode == 0:
            self.status_label.setText(f"Úspešne nastavený dátum a čas: {date_time}.")
        else:
            self.status_label.setText("Chyba pri nastavovaní dátumu a času.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TimeManager()
    window.show()
    sys.exit(app.exec_())
